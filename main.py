from fastapi import FastAPI
from loguru import logger
from typing import List
from classes import *
from models import *


# TODO - add logging 

app = FastAPI(
    title="Backend Server",  # TODO - maybe we can give a cooler name
    description="Backend server for Soflo Tech Hub Hackathon 2025 Project - OneMap",
    version="0.1.0"
)


@app.get("/community-data")
async def get_data(criteria: str) -> DataResponse:
    # TODO - call the Attom client/manager to get processed community criteria data
    return None


@app.get("/insights")  
async def get_ai_insights(criteria: str, latitude: float, longitude: float) -> str:
    # TODO - call Open AI API based on a 'formulaic' prompt like below:
    #   "Give me a 2 sentence insights summary about {criteria} in 
    #   the city belonging to the following location {latitude} {longitude}"
    return None


@app.post("/prompt")  
async def get_ai_suggestion(body: PromptRequest) -> str:
    # TODO - ⚠️ still need to confirm if we'll add this feature
    # Give the user's criteria of interest and provide an AI suggestion
    # for a Soflo location that is ideal for them
    return None
