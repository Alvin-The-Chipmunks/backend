from dotenv import load_dotenv
from loguru import logger
import os, requests, json
from typing import Optional, Tuple
load_dotenv()


class AttomManager:
    def __init__(self):
        self.url = os.environ['ATTOM_URL']
        self.api_key = os.environ['ATTOM_API_KEY']
        self.headers = {"Accept": "application/json", "apikey": self.api_key}

    def get_geoidv4_by_zip(self, zip_code: str):
        endpoint = f"{self.url}/v4/location/lookup"
        params = {"geographyTypeAbbreviation": "ZI", "name": zip_code}

        logger.info(f"Get GeoIdV4 for zipcode '{zip_code}'")

        r = requests.get(endpoint, headers=self.headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        geos = data.get("geographies", [])
        if not geos:
            raise ValueError(f"No geoIdV4 found for ZIP {zip_code}")
        return geos[0]["geoIdV4"]

    def get_geojson_by_zip(self, zip_code: str) -> dict:
        geoidv4 = self.get_geoidv4_by_zip(zip_code)
        boundary_url = f"{self.url}/v4/area/boundary/detail"

        logger.info(f"Get GeoJSON for zipcode '{zip_code}' and geoidv4 '{geoidv4}'")

        r = requests.get(boundary_url, headers=self.headers, params={"geoIdV4": geoidv4}, timeout=30)
        r.raise_for_status()
        return r.json()  # GeoJSON Feature: {"type":"Feature","geometry":{...},"properties":{...}}

    def get_community_data(self, zip_code: str) -> dict:
        geoidv4 = self.get_geoidv4_by_zip(zip_code)
        endpoint = f"{self.url}/v4/neighborhood/community"

        logger.info(f"Get Community Data for zipcode '{zip_code}'")

        r = requests.get(endpoint, headers=self.headers, params={"geoIdV4": geoidv4}, timeout=30)
        r.raise_for_status()
        return r.json()
    
    def get_heat_map_json(self, zip_code: str, value_path: str):
        """
        Combine ATTOM geojson for a ZIP with a single community value.
        value_path uses exact keys from your fixed schema, e.g.:
          - "demographics.median_Age"
          - "naturalDisasters.hurricane_Index"
        """
        # Get boundary coords
        gj = self.get_geojson_by_zip(zip_code)
        item0 = gj["response"]["result"]["package"]["item"][0]
        boundary = item0["boundary"]  # {'type': 'Polygon'|'MultiPolygon', 'coordinates': ...}
        gtype = boundary["type"]
        coords = boundary["coordinates"]

        # Get community value
        community = self.get_community_data(zip_code)["community"]

        # Get the value using the value_path of the category
        cur = community
        for key in value_path.split("."):
            cur = cur[key]
        val = float(cur)

        logger.info(f"Generate heatmap data for zipcode '{zip_code}' category '{value_path}'")

        # flatten coords -> [{lat,lng,val}]
        out: list[dict] = []

        def push_coord(coord: list[list[float]]):
            for lon, lat in coord:  # NOTE: ATTOM is [lon, lat]
                out.append({"lat": float(lat), "lng": float(lon), "val": val})

        # The boundary type can be either Polygon or MultiPolygon
        if gtype == "Polygon":
            for coord in coords:
                push_coord(coord)
        elif gtype == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    push_coord(ring)
        else:
            raise ValueError(f"Unsupported boundary type: {gtype}")

        return out
