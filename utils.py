import json
import socket
import os
import sys
import requests
from pydantic import ValidationError
from models import IPGeolocation


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
    try:
        response = requests.get(IPSTACK_URL+ ip + "?access_key=" + os.getenv("IPSTACK_API_KEY"))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    if response.status_code == 104:
        raise Exception("Usage limit reached")
    data = response.json()
    try:
        val = data.model_validation(data)
    except ValidationError as e:
        print(e)
        return
    result = IPGeolocation(**data)
    return result
    
def send_to_queue(data: IPGeolocation) -> None:
    
    return
    
def get_geo_data(item: str) -> dict:
    geo_data = geodata_api_call(item)
    send_to_queue(geo_data)
    
    
def add_data(item: str) -> None:
    get_geo_data(item)
    return


def get_data(item:str):
    pass
    return


def update_item(item:str):
    pass
    return
