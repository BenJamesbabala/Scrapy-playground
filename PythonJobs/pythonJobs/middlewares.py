# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlite3 import dbapi2 as sqlite

class IP(object):
    pass

class httpProxyDownloaderMiddle(object):
    def __init__(self):
        engine = create_engine("sqlite:///ips.db")
        iptable = Table('ips',MetaData(engine),autoload = True)
        Session=sessionmaker(bind=engine)
        self.session = Session()
        mapper(IP,iptable)
        self.offset = 0
        self.count_ips = self.session.query(IP).count()

    def get_proxy(self):
        ip = self.session.query(IP.ip,IP.port).filter(IP.proxy_type=='HTTP').limit(1).offset(self.offset).one()

        if not ip:
            self.offset=0
            ip = self.session.query(IP.ip, IP.port).filter(IP.proxy_type == 'HTTP').limit(1).offset(self.offset).one()

        self.offset = (self.offset + 1) % self.count_ips
        return ip

    def process_request(self,request,spider):
        ip,port = self.get_proxy()
        proxy = "http://{0}:{1}".format(ip,port)
        request.meta["proxy"]=proxy
        return None

    def __del__(self):
        self.session.close()