from fastapi import FastAPI
from openai import OpenAI
from loguru import logger
from classes import *
from models import *


# TODO - add logging 

app = FastAPI(
    title="Soflo Atlas Backend Server",
    description="Backend server for Soflo Tech Hub Hackathon 2025 Project - Soflo Atlas",
    version="0.1.0"
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.get("/community-data")
async def get_data(criteria: str) -> DataResponse:
    # TODO - call the Attom client/manager to get processed community criteria data
    return None


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
