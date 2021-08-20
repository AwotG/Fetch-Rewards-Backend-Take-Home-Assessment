from pydantic import BaseModel

class Balance(BaseModel):
    points: int
