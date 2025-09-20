from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Query
from openai import OpenAI
from loguru import logger
from classes import *
from models import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Soflo Atlas Backend Server",
    description="Backend server for Soflo Tech Hub Hackathon 2025 Project - Soflo Atlas",
    version="0.1.0"
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
attom = AttomManager()

@app.get("/heatmap-data")
async def get_heatmap_data(
    zip_code: str = Query(..., description="5-digit ZIP (e.g., 33068)"),
    section: str = Query(..., description="Top-level section, e.g. 'naturalDisasters'"),
    field: str = Query(..., description="Field name, e.g. 'hurricane_Index'")
):
    # Returns: [{lat: number, lng: number, val: number}, ...]

    try:
        value_path = f"{section}.{field}"
        heatmap = attom.get_heat_map_json(zip_code, value_path)
        return JSONResponse(content=heatmap)
    except KeyError as e:
        # The section/field doesn't exist in the 'community' payload
        raise HTTPException(status_code=400, detail=f"Unknown path: {value_path} (missing key {e!s})")
    except ValueError as e:
        # Unsupported geometry type, non-numeric value, etc.
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Network/auth errors from ATTOM, etc.
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/insights")  
async def get_ai_insights(body: InsightsRequest) -> InsightsResponse:
    logger.info(f"Sending prompt request for '{body.category}' in zipcode '{body.zipcode}'")
    response = client.responses.create(
        model="gpt-4o",
        instructions="You are an insightful guru providing knowledge about various factors across South Florida to locals and prospective home owners",
        input=f"Give me a 2 sentence summary about insights on {body.category} in the city belonging to zipcode {body.zipcode}. Do not mention the zipcode in your response. You don't need to mention that the city is located in South Florida. Refer to the city by name only.",
    )
    logger.info("Successfully received prompt response")
    
    return {"content": response.output_text}
