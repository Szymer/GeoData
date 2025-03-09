from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import IPGeolocation
from utils import  add_data
from curd import read_ip_data
from celery_worker import add_record_to_db, update_record_in_db

router = APIRouter()


db = Session = Depends(get_db)
@router.get("/")
def read_root():
    return {"Welcome in GeoAPI"}


@router.get("/item/get/{item_id}")
def read_item(item_id: str, db: Session = Depends(get_db)):
    data = read_ip_data(db, item_id) 
    result = data if data else {"message": "Record not found"}
    return result


@router.post("/item/add/{item_id}")
def add_item(item_id: str, db: Session = Depends(get_db)):
    i = add_data(db=db , item = item_id)
    return i


@router.put("/item/update/{item_id}")
def update_item(item_id: str, db: Session = Depends(get_db), payload: dict=None):
    if not payload:
        return {"message": "Payload is empty"}
    i = update_record_in_db(db, item_id, payload=payload)
    return i
  
