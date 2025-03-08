from pydantic import BaseModel
from typing import List, Optional

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

class TimeZone(BaseModel):
    id: str
    current_time: str
    gmt_offset: int
    code: str
    is_daylight_saving: bool

class Currency(BaseModel):
    code: str
    name: str
    plural: str
    symbol: str
    symbol_native: str

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
    msa: str
    dma: str
    radius: Optional[float]
    ip_routing_type: Optional[str]
    connection_type: Optional[str]
    location: Location
    time_zone: TimeZone
    currency: Currency
    connection: Connection
