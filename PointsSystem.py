from fastapi import FastAPI,HTTPException

from PointsManagerHelper import PointManager, InsufficientBalance
from Models.Request import Transaction, Redeem

app = FastAPI()
PointsTracker = PointManager()

@app.post("/points/add-points")
async def transaction(body: Transaction):
    PointsTracker.add_points(body.payer,body.amount, body.timestamp)
    return dict(PointsTracker.get_balance_detailed())

@app.post("/points/redeem")
async def redeem(body: Redeem):
    try:
        transactions = PointsTracker.redeem_points(body.points)
    except InsufficientBalance as e:
        raise HTTPException(status_code=400, detail=e.message)
    else:
        return transactions

@app.get("/points/balance")
async def balance():
    return PointsTracker.get_balance_detailed()

@app.get("/points/transactions-history")
async def balance():
    return PointsTracker.TRANSACTIONS_HISTORY
