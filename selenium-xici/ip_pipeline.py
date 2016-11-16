#! -*- encoding:utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlite3 import dbapi2 as sqlite
import sys
printf = sys.stdout.write


class IP(object):
    pass

class Ip_pipeline(object):
    '''
    session
    current       current row(read)
    offset        for next iteration
    count_ips     total record retried in __init__
    get_proxy     get one ip record and move offset for next iter
    '''


    def __init__(self):
        self.engine = create_engine("sqlite:///ips.db")
        self.changed = 0 # To calculate when to commit
        try:
            self.iptable = Table('ips', MetaData(self.engine), autoload=True)
        except Exception:
            self.iptable = Table('ips', MetaData(self.engine),
                            Column('ip', VARCHAR(16), primary_key=True),
                            Column('port', Integer, nullable=False),
                            Column('address', VARCHAR(20)),
                            Column('proxy_type', VARCHAR(5)),
                            Column('speed', Integer),
                            Column('connection', Integer),
                            Column('dur', TEXT),
                            Column('check', DateTime(timezone="Asia/Shanghai"))
                            )
            self.iptable.create()

        self.Session=sessionmaker(bind=self.engine)
        self.session = Session()
        mapper(IP,self.iptable)
        self.offset = 0
        self.current = 0
        self.count_ips = self.session.query(IP).count()

    def get_proxy(self, proxy_type): # proxy_type = 'HTTP' or 'HTTPS'
        try:
            ip = self.session.query(IP.ip,IP.port).filter(IP.proxy_type==proxy_type).limit(1).offset(self.offset).one()
        except Exception,e:
            self.offset=0
            ip = self.session.query(IP.ip, IP.port).filter(IP.proxy_type == proxy_type).limit(1).offset(self.offset).one()
        self.current = self.offset + 1 # Current row = current offset + 1, Bug: current could be larger than cout_ips, but it's not used elsewhere anyway.
        self.offset = (self.offset + 1) % self.count_ips  # prepare offset for next iteration
        return ip

    def save_proxy(self, proxy_item):  # proxy_item 为IP 对象
        if self.session.query(IP).filter(IP.ip == proxy_item.ip).count() == 0:  # 去重
            printf("Already in db.\n")
            return None
        try:
            self.session.add(proxy_item)
        except:
            return None
        self.changed += 1
        if self.changed%5 == 0:
            self.session.commit()

    def delete_proxy(self, ip):
        try:
            ip = self.session.query(IP).filter(IP.ip==ip).delete()
            self.changed += 1
            if self.changed%5 == 0:
                self.session.commit()
                printf("Commit".center(30,'-'))
            printf("Deleted.")
        except Exception, e:
            printf("Proxy not in db.")

    def __del__(self):
        self.session.commit()
        self.session.close()