from celery import Celery
from models import IPGeolocation

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def update_record_in_db(db, ip: str, payload: dict):
    from curd import update_ip_data
    record = update_ip_data(db=db, ip = ip, payload = payload)
    status =  "sucess" if record.get("message")== None else record.get("message")
    return {"status": status, "record": record.get("data")}

@celery_app.task
def add_record_to_db(db, ip_data: IPGeolocation):
    from curd import insert_ip_data
    record = insert_ip_data(db=db, ip_data = ip_data)
    return {"status": record.get('message'), "record": record.get("data")}