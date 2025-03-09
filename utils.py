import json
import socket
import os
import requests
from sqlalchemy.orm import Session
from pydantic import ValidationError
from models import IPGeolocation
from celery_worker import add_record_to_db


IPSTACK_URL='http://api.ipstack.com/'



def get_ip(url: str) -> str:
    try:
        ip = socket.gethostbyname(url)
    except:
        raise Exception(f" {url}  - > can't translate to IP")
    return ip


def geodata_api_call(ip: str) -> IPGeolocation:
    """
    104	usage_limit_reached	The maximum allowed amount of monthly API requests has been reached.

    """
    if  ip.split(".")[-1].isdigit() == False:
        ip = get_ip(ip)
    if os.getenv("TEST") == "true":
        with open("test.json") as f:
            data = json.load(f)
        result = IPGeolocation(**data)
        return result
    else:
        try:
            response = requests.get(IPSTACK_URL+ ip + "?access_key=" + os.getenv("IPSTACK_API_KEY"))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        if response.status_code == 104:
            raise Exception("Usage limit reached")
        data = response.json()
        try:
            val = IPGeolocation.model_validation(data)
        except ValidationError as e:
            print(e)
            return
        result = IPGeolocation(**data)
    return result
    
    
def get_geo_data(item: str) -> dict:
    geo_data = geodata_api_call(item)
    return geo_data
    
    
def add_data(db:Session, item: str) -> None:
    data =get_geo_data(item)
    task = add_record_to_db(db, data)
    return  {"status": task.get('status'), "Record": task.get('record'), }


def get_data(db:Session, item:str) -> dict:
    return


def update_data(item:str):
    pass
    return
