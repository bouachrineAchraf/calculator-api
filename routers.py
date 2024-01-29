from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from calculator import calculate_npi
from sqlalchemy import inspect
from fastapi.responses import StreamingResponse
from datetime import datetime
from database import SessionLocal, engine 
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CalculationBase(BaseModel):
    expression: str
    result: str

class CalculationCreate(CalculationBase):
    result: str

    
inspector = inspect(engine)
if 'calculation' not in inspector.get_table_names():
    models.Base.metadata.create_all(bind=engine)

@router.get('/')
def home():
    return {'message': 'Hello World'}

@router.post('/calculations/{expression}', status_code=status.HTTP_201_CREATED)
async def create_calculation(expression: str, db: Session = Depends(get_db)):
    result = str(calculate_npi(expression))

    db_calculation = models.Calculation(expression=expression, result=result)
    db.add(db_calculation)
    db.commit()

    return {"expression": expression, "result": result}

@router.get('/calculations/', response_model=List[CalculationBase])
def get_all_calculations(db: Session = Depends(get_db)):
    calculations = db.query(models.Calculation).all()
    return [{"expression": calc.expression, "result": calc.result} for calc in calculations]

@router.get("/export-csv/")
async def export_csv(db: Session = Depends(get_db)):
    calculations = db.query(models.Calculation).all()

    if not calculations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data to export")
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"exported_data_{now}.csv"
    csv_content = "id,expression,result\n" 
    for calc in calculations:
        csv_content += f"{calc.id},{calc.expression},{calc.result}\n"

    response = StreamingResponse(iter([csv_content]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response
