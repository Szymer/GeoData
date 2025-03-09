import json
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from db_models import Location as Loc, TimeZone as Tz, Currency as Cur, Connection as Con

class Language(BaseModel):
    code: str
    name: str
    native: str

class Location(BaseModel):
    geoname_id: int
    capital: str
    languages: List[Language]
    country_flag: str
    country_flag_emoji: str
    country_flag_emoji_unicode: str
    calling_code: str
    is_eu: bool
    class Config:
      from_attributes=True
          
    @model_validator(mode='before')
    def validate_lang(cls, values):
            try:
                lan = values.languages
            except:
                return values
            if lan  is  not None and not isinstance(lan, list):    
                lan = json.loads(lan)
                values.languages = lan
            return values

class TimeZone(BaseModel):
    id: str | int
    current_time: str
    gmt_offset: int
    code: str
    is_daylight_saving: bool
    class Config:
      from_attributes=True

class Currency(BaseModel):
    code: str
    name: str
    plural: str
    symbol: str
    symbol_native: str
    class Config:
      from_attributes=True

class Connection(BaseModel):
    asn: int
    isp: str
    sld: str
    tld: str
    carrier: str
    home: Optional[bool]
    organization_type: Optional[str]
    isic_code: Optional[str]
    naics_code: Optional[str]
    class Config:
      from_attributes=True

class IPGeolocation(BaseModel):
    ip: str
    type: str
    continent_code: str
    continent_name: str
    country_code: str
    country_name: str
    region_code: str
    region_name: str
    city: str
    zip: str
    latitude: float
    longitude: float
    msa: str = Field(default=None)
    dma: str = Field(default=None)
    radius: Optional[float]
    ip_routing_type: Optional[str]
    connection_type: Optional[str]
    location: Location
    time_zone: TimeZone =  Field(default=None)
    currency: Currency = Field(default=None)
    connection: Connection = Field(default=None)


    class Config:
      from_attributes=True

      
    @model_validator(mode='before')
    def validate_location(cls, values):
        try:
            loc = values.location 
        except:
            return values 
        if isinstance(loc, Loc):
            loc = loc.__dict__
        return values

    @model_validator(mode='before')
    def validate_time_zone(cls, values):
            try:
                tz =  values.time_zone
            except:
                return values
            if isinstance(tz, Tz):
                tz = tz.__dict__
            return values

    @model_validator(mode='before')
    def validate_currency(cls, values):
            try:
                cur  =  values.currency
            except:
                return values
            if isinstance(cur, Cur):
                  cur = cur.__dict__
            return values