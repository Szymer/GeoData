import os
from celery import Celery
from utils import  geodata_api_call


"""
This module is used to create a celery app instance and define the tasks that will be executed by the celery worker.
The tasks are defined as functions with the @celery_app.task decorator.
The tasks are used to update and add records to the database.
"""



celery_app = Celery(
    "tasks",
    broker = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend = os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0")
)

@celery_app.task
def update_record_in_db(db, ip: str, payload: dict):
    from curd import update_ip_data
    record = update_ip_data(db=db, ip = ip, payload = payload)
    status =  "success" if record.get("message")== None else record.get("message")
    return {"status": status, "record": record.get("data")}

@celery_app.task
def add_record_to_db(db, item:str):
    from curd import insert_ip_data
    ip_data = geodata_api_call(item)
    record = insert_ip_data(db=db, ip_data = ip_data)
    return {"status": record.get('message'), "record": record.get("data")}