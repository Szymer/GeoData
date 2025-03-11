import json
from sqlalchemy.orm import Session
from db_models import Location, TimeZone, Currency, Connection, IPData
from models import IPGeolocation
from utils import get_ip


"""
functions to read, insert and update data in database

"""





def read_ip_data(db: Session, ip: str):
    "Read data from database"
    #
    if  ip.split(".")[-1].isdigit() == False:
        ip = get_ip(ip)
    x =  db.query(IPData).filter(IPData.ip == ip).first()
    if x:
        IPGeolocation.model_validate(x)
        return x
    else:
        return 



def insert_ip_data(db: Session, ip_data: IPGeolocation):
    """
    insert data to database
    
    """
    # check if record already exists to avoid duplicates
    if x := read_ip_data(db=db, ip=ip_data.ip): 
        return {"message": "Record already exists" , "data": x}
    try:
        #check if location already exists
        if ip_data.location:
            existing_location = db.query(Location).filter_by(geoname_id=ip_data.location.geoname_id).first()
            if existing_location:
                location = existing_location
            else:  
                location = Location(
                geoname_id=ip_data.location.geoname_id,
                capital=ip_data.location.capital,
                languages=json.dumps([lang.model_dump() for lang in ip_data.location.languages]),
                country_flag=ip_data.location.country_flag,
                country_flag_emoji=ip_data.location.country_flag_emoji,
                country_flag_emoji_unicode=ip_data.location.country_flag_emoji_unicode,
                calling_code=ip_data.location.calling_code,
                is_eu=ip_data.location.is_eu
                    )
                db.add(location)
                db.commit()
                db.refresh(location)
            #check if time_zone already exists 
        if ip_data.time_zone:
            existing_time_zone = db.query(TimeZone).filter_by(tz_id=ip_data.time_zone.id).first()
            if existing_time_zone:
                time_zone = existing_time_zone
            else:
                time_zone = TimeZone(
                    tz_id=ip_data.time_zone.id,
                    current_time=ip_data.time_zone.current_time,
                    gmt_offset=ip_data.time_zone.gmt_offset,
                    code=ip_data.time_zone.code,
                    is_daylight_saving=ip_data.time_zone.is_daylight_saving
                )
                db.add(time_zone)
                db.commit()
                db.refresh(time_zone)
        #check if currency already exists
        if ip_data.currency:
            existing_currency = db.query(Currency).filter_by(code=ip_data.currency.code).first()
            if existing_currency:
                currency = existing_currency
            else:
                currency = Currency(
                    code=ip_data.currency.code,
                    name=ip_data.currency.name,
                    plural=ip_data.currency.plural,
                    symbol=ip_data.currency.symbol,
                    symbol_native=ip_data.currency.symbol_native
                )
                db.add(currency)
                db.commit()
                db.refresh(currency)
        #check if connection already exists
        if ip_data.connection:
            existing_connection = db.query(Connection).filter_by(asn=ip_data.connection.asn).first()
            if existing_connection:
                connection = existing_connection
            else:   
                connection = Connection(
                    asn=ip_data.connection.asn,
                    isp=ip_data.connection.isp,
                    sld=ip_data.connection.sld,
                    tld=ip_data.connection.tld,
                    carrier=ip_data.connection.carrier,
                    home=ip_data.connection.home,
                    organization_type=ip_data.connection.organization_type,
                    isic_code=ip_data.connection.isic_code,
                    naics_code=ip_data.connection.naics_code
                )
                db.add(connection)
                db.commit()
                db.refresh(connection)

        ip_record = IPData(
            ip=ip_data.ip,
            type=ip_data.type,
            continent_code=ip_data.continent_code,
            continent_name=ip_data.continent_name,
            country_code=ip_data.country_code,
            country_name=ip_data.country_name,
            region_code=ip_data.region_code,
            region_name=ip_data.region_name,
            city=ip_data.city,
            zip=ip_data.zip,
            latitude=ip_data.latitude,
            longitude=ip_data.longitude,
            msa=ip_data.msa,
            dma=ip_data.dma,
            radius=ip_data.radius,
            ip_routing_type=ip_data.ip_routing_type,
            connection_type=ip_data.connection_type,
            location_id=location.id if ip_data.location else None,
            time_zone_id=time_zone.id if ip_data.time_zone else None,
            currency_id=currency.id if ip_data.currency else None,
            connection_id=connection.id if ip_data.connection else None
        )
        db.add(ip_record)
        db.commit()
        db.refresh(ip_record)

        return {"message": "Success" , "data": IPGeolocation.model_validate(ip_record)}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def update_ip_data( db: Session, ip: str, payload : dict):
  
    if "ip" in payload:
      return {"message": "You can't change IP address", "data": None}
    
    ip_record = read_ip_data(db=db, ip=ip)
    if not ip_record:
        return {"error": "Record not found"}
    update_data = payload
    # update relation in IPData
    for key, value in update_data.items():
        if hasattr(ip_record, key) and key not in ["location", "time_zone", "currency", "connection"]:
            setattr(ip_record, key, value)

    # update relation : Location
    if "location" in update_data and ip_record.location:
        loc_data = update_data["location"]
        for key, value in loc_data.items():
            if hasattr(ip_record.location, key):
                setattr(ip_record.location, key, value)

    # update relation: TimeZone
    if "time_zone" in update_data and ip_record.time_zone:
        tz_data = update_data["time_zone"]
        for key, value in tz_data.items():
            if hasattr(ip_record.time_zone, key):
                setattr(ip_record.time_zone, key, value)

    # update relation: Currency
    if "currency" in update_data and ip_record.currency:
        cur_data = update_data["currency"]
        for key, value in cur_data.items():
            if hasattr(ip_record.currency, key):
                setattr(ip_record.currency, key, value)

    # update relation: Connection
    if "connection" in update_data and ip_record.connection:
        conn_data = update_data["connection"]
        for key, value in conn_data.items():
            if hasattr(ip_record.connection, key):
                setattr(ip_record.connection, key, value)

    db.commit()
    return {"message": "Record updated", "data": IPGeolocation.model_validate(ip_record)}