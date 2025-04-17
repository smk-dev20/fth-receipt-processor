import uvicorn
from fastapi import FastAPI, Request, status, Depends, HTTPException
from fastapi.responses import JSONResponse 
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
import models, schemas
from models import Receipt, Point
from database import engine, get_db
import math

# Initialize FastAPI app
app = FastAPI()

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Calculate points for receipt based on rules
def calculatePoints(receipt: schemas.ReceiptBase):
    points_total = 0

    #Rule 1: One point for every alphanumeric character in the retailer name.
    points_rule1 = sum(c.isalnum() for c in receipt.retailer)
    print("Rule-1 points: ", points_rule1)
    points_total += points_rule1
    print("points_total after Rule-1: ", points_total)

    #Rule 2: 50 points if the total is a round dollar amount with no cents.
    if receipt.total % 1 == 0:
            points_rule2 = 50
            print("Rule-2 points: ", points_rule2)
            points_total += points_rule2
    print("points_total after Rule-2: ", points_total)


    # Rule 3: 25 points if the total is a multiple of 0.25
    if receipt.total % 0.25 == 0:
        points_rule3 = 25
        print("Rule-3 points: ", points_rule3)
        points_total += points_rule3
    print("points_total after Rule-3: ", points_total)


    # Rule 4: 5 points for every two items on the receipt
    item_count = len(receipt.items)
    points_rule4 = (item_count // 2) * 5
    print("Rule-4 points: ", points_rule4)
    points_total += points_rule4
    print("points_total after Rule-4: ", points_total)

    # Rule 5: If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points_rule5 = math.ceil(item.price * 0.2)
            print("Rule-5 points: ", points_rule5)
            points_total += points_rule5
    print("points_total after Rule-5: ", points_total)

    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = receipt.purchaseDate
    if purchase_date.day % 2 != 0:
            points_rule6 = 6
            print("Rule-6 points: ", points_rule6)
            points_total += points_rule6
    print("points_total after Rule-6: ", points_total)

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = receipt.purchaseTime
    if 14 <= purchase_time.hour < 16:
            points_rule7 = 10
            print("Rule-7 points: ", points_rule7)
            points_total += points_rule7
    print("points_total after Rule-7: ", points_total)

    return points_total


# API endpoint to process a receipt
@app.post("/receipts/process")
def process_receipt(receipt: schemas.ReceiptBase, db: Session = Depends(get_db)): 
    try:
        json_receipt = jsonable_encoder(receipt)
        receipt_obj = Receipt(input_receipt=json_receipt)
        db.add(receipt_obj)
        db.commit()
        db.refresh(receipt_obj)

        points = calculatePoints(receipt)

        # Store Calculated Points
        point_obj = Point(receipt_id=receipt_obj.id, awarded_points=points)
        db.add(point_obj)
        db.commit()

        return { "id": receipt_obj.id }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/receipts/{id}/points")
def get_receipt_points(id: str, db: Session = Depends(get_db)):
    point_record = db.query(models.Point).filter(models.Point.receipt_id == id).first()
    if not point_record:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    
    return { "points": point_record.awarded_points }
     


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    #override pydantic 422 error
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": "The receipt is invalid."}),
    )    

@app.get("/")
def start():
    return {"message": "Receipt Processor"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)