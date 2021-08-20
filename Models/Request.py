from datetime import datetime
from pydantic import BaseModel, PositiveInt


class Transaction(BaseModel):
    payer: str
    amount: PositiveInt
    timestamp: datetime

class Redeem(BaseModel):
    points: PositiveInt
