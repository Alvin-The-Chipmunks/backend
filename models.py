from pydantic import BaseModel
from typing import List


class InsightsRequest(BaseModel):
    category: str
    zipcode: str
    
class InsightsResponse(BaseModel):
    content: str
