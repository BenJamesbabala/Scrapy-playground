# -*- encoding: utf-8
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlite3 import dbapi2 as sqlite
import urllib

class Item(object):
    pass

class City(object):
    pass

class Geo_job(object):
    pass

class ItemDb(object):
    def __init__(self):
        self.current = 0
        engine = create_engine("sqlite:///Items.db")
        itemTable = Table('jobs',MetaData(engine),autoload = True)
        try:
            cityTable = Table('cities',MetaData(engine),autoload=True)
        except:
            cityTable = Table('cities',MetaData(engine),
                              Column('city',VARCHAR(20),primary_key=True),
                              Column('count',Integer,default=0),
                              Column('lan',FLOAT,nullable=True),
                              Column('lon',FLOAT,nullable=True)
                              )
            cityTable.create()
        Session = sessionmaker()
        self.session = Session()
        mapper(Item,itemTable)
        mapper(City,cityTable)

        try:
            geoTable = Table('geo_job',MetaData(engine),autoload=True)
        except Exception:
            geoTable = Table('geo_job',MetaData(engine),
                             Column('url',ForeignKey(Item.url),primary_key=True),
                             Column('lat',FLOAT),
                             Column('lng',FLOAT)
                             )
            geoTable.create()
        mapper(Geo_job,geoTable)
        self.count = self.session.query(Item).count()

    def __del__(self):
        self.session.close()

    def next(self):
        if self.current < self.count:
            item = self.session.query(Item).limit(1).offset(self.current).one()
            self.current += 1
            return item

    def __iter__(self):
        return self

def get_geo(location):
    googleapi = "http://maps.googleapis.cn/maps/api/geocode/json?"
    print googleapi + urllib.urlencode({'sensor':'false','address':location})
    fhand = urllib.urlopen( googleapi + urllib.urlencode({'sensor':'false','address':location}) )
    response = fhand.read()
    response = dict(response)
    print response

db = ItemDb()
for item in db:
    city_str = item.city.split('-')[0]
    try:
        cityObj = db.session.query(City).filter(City.city==city_str).one()          # record already exit, lan and lon assumed to set
        cityObj.count += 1
        db.session.commit()
    except Exception:
        cityObj = City()   # record not in db, add a new record, fields: city, count, lan, lon
        cityObj.city = city_str
        cityObj.count = 0
        cityObj.lan, cityObj.lon = get_geo(city_str)

    print count