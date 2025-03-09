import json
from sqlalchemy.orm import Session
from db_models import Location, TimeZone, Currency, Connection, IPData
from models import IPGeolocation
from utils import get_ip

def read_ip_data(db: Session, ip: str):
    if  ip.split(".")[-1].isdigit() == False:
        ip = get_ip(ip)
    x =  db.query(IPData).filter(IPData.ip == ip).first()
    if x:
        IPGeolocation.model_validate(x)
        return x
    else:
        return 



def insert_ip_data(db: Session, ip_data: IPGeolocation):
    
    if x := read_ip_data(db=db, ip=ip_data.ip): 
        return {"message": "Record already exists" , "data": x}
    try:
        
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
            location_id=location.id,
            time_zone_id=time_zone.id,
            currency_id=currency.id,
            connection_id=connection.id
        )
        db.add(ip_record)
        db.commit()
        db.refresh(ip_record)

        return {"message": "Succes" , "data": IPGeolocation.model_validate(ip_record)}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


    