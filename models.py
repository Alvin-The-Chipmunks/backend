from pydantic import BaseModel

class InsightsRequest(BaseModel):
    category: str
    zipcode: str
    
class InsightsResponse(BaseModel):
    content: str
