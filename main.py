from fastapi import FastAPI
from database import  engine, SessionLocal
import models
from pydantic import BaseModel

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_calculation_table():
    models.Base.metadata.create_all(bind=engine)

class CalculationBase(BaseModel):
    expression: str
    result: str

class CalculationCreate(CalculationBase):
    result: str

@app.get('/')
def home():
    return {'message': 'Hello World'}