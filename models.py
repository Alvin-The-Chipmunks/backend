from pydantic import BaseModel
from typing import List


class PromptRequest(BaseModel):
    critiera: List[str]

class DataResponse(BaseModel):
    # TODO - need to update this after confirming the schema needed on the frontend
    name: str
    description: str | None = None
    price: float
    tax: float | None = None