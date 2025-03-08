from celery import Celery
from models import IPGeolocation

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def add_record_to_db(db, ip_data: IPGeolocation):
    from curd import insert_ip_data
    insert_ip_data(db=db, ip_data = ip_data)
    return {"status": "success", "ip": ip_data.ip}