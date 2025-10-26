from pydantic import BaseModel, Field
from typing import Optional

class DocIn(BaseModel):
    title: str = Field(..., example="My title")
    body: str = Field(..., example="Body text here")

class DocOut(DocIn):
    id: str