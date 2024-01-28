from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response, status
from database import  engine, SessionLocal
import models
from pydantic import BaseModel
from sqlalchemy.orm import Session
from calculator import calculate_npi
from sqlalchemy import inspect

app = FastAPI()

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

@app.get('/')
def home():
    return {'message': 'Hello World'}

@app.post('/calculations/{expression}', status_code=status.HTTP_201_CREATED)
async def create_calculation(expression: str, db: Session = Depends(get_db)):
    result = calculate_npi(expression)
    
    db_calculation = models.Calculation(expression=expression, result=result)
    db.add(db_calculation)
    db.commit()
    
    return {"expression": expression, "result": result}

@app.get('/calculations/', response_model=List[CalculationBase])
def get_all_calculations(db: Session = Depends(get_db)):
    calculations = db.query(models.Calculation).all()
    return [{"expression": calc.expression, "result": calc.result} for calc in calculations]