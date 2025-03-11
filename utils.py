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
        if response.status_code == 104:
            raise Exception("Usage limit reached")
        if response.status_code == 101:
            raise Exception("invalid_access_key")
        if response.status_code == 103:
            raise Exception("invalid_api_function")
        if response.status_code == 104:
            raise Exception("Usage limit reached")
        if response.status_code == 301:
            raise Exception("nvalid_fields	One or more invalid fields were specified using the fields parameter.")
        if response.status_code == 302:
            raise Exception("too_many_ips	Too many IPs have been specified for the Bulk Lookup Endpoint. (max. 50)")
        if response.status_code == 303:
            raise Exception("atch_not_supported_on_plan	The Bulk Lookup Endpoint is not supported on the current subscription plan")
        data = response.json()
        try:
            result = IPGeolocation.model_validate(data)
        except ValidationError as e:
            print(e)
            return {"message": "Invalid data", "data": data}
    return result
    

