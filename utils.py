import json
import socket
import os
import requests
# from sqlalchemy.orm import Session
from pydantic import ValidationError, model_validator
from models import IPGeolocation
# from celery_worker import add_record_to_db


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
        
    # for debug only 
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
        data = response.json()
        if data.get("success") == False:
            raise Exception(f"{data.get('error').get('info')}")
        try:
            result = IPGeolocation.model_validate(data)
        except ValidationError as e:
            print(e)
            return {"message": "Invalid data", "data": data}
    return result
    

