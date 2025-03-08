from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class IPRecord(Base):
    __tablename__ = "ip_records"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, nullable=False)
    country_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    raw_data = Column(JSON)  # Pełne dane JSON


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    geoname_id = Column(Integer, unique=True)
    capital = Column(String)
    languages = Column(JSON)  # Przechowujemy listę słowników
    country_flag = Column(String)
    country_flag_emoji = Column(String)
    country_flag_emoji_unicode = Column(String)
    calling_code = Column(String)
    is_eu = Column(Boolean)


class TimeZone(Base):
    __tablename__ = 'time_zone'
    id = Column(Integer, primary_key=True)
    tz_id = Column(String, unique=True)
    current_time = Column(String)
    gmt_offset = Column(Integer)
    code = Column(String, unique=True)
    is_daylight_saving = Column(Boolean)


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    plural = Column(String)
    symbol = Column(String)
    symbol_native = Column(String)


class Connection(Base):
    __tablename__ = 'connection'
    id = Column(Integer, primary_key=True)
    asn = Column(Integer)
    isp = Column(String)
    sld = Column(String)
    tld = Column(String)
    carrier = Column(String)
    home = Column(Boolean, nullable=True)  # Poprawiony typ
    organization_type = Column(String, nullable=True)
    isic_code = Column(String, nullable=True)
    naics_code = Column(String, nullable=True)


class IPData(Base):
    __tablename__ = 'ip_data'
    id = Column(Integer, primary_key=True)
    ip = Column(String, unique=True, nullable=False)
    type = Column(String)
    continent_code = Column(String)
    continent_name = Column(String)
    country_code = Column(String)
    country_name = Column(String)
    region_code = Column(String)
    region_name = Column(String)
    city = Column(String)
    zip = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    msa = Column(String)
    dma = Column(String)
    radius = Column(Integer, nullable=True)
    ip_routing_type = Column(String, nullable=True)
    connection_type = Column(String, nullable=True)

    location_id = Column(Integer, ForeignKey('location.id', ondelete="CASCADE"))
    time_zone_id = Column(Integer, ForeignKey('time_zone.id', ondelete="CASCADE"))
    currency_id = Column(Integer, ForeignKey('currency.id', ondelete="CASCADE"))
    connection_id = Column(Integer, ForeignKey('connection.id', ondelete="CASCADE"))

    location = relationship("Location")
    time_zone = relationship("TimeZone")
    currency = relationship("Currency")
    connection = relationship("Connection")
