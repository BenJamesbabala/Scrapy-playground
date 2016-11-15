# -*- encoding: utf-8 -*-
from __future__ import division
from selenium import webdriver
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlite3 import dbapi2 as sqlite
import datetime

def get_url(num_page):
    for i in xrange(1,num_page+1):
        yield "http://www.xicidaili.com/nn/{0}".format(i)

class IP(object):
    pass

try:
    n = int(raw_input("Number of pages to crawl:"))
    engine = create_engine("sqlite:///ips.db")   # refer to http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#module-sqlalchemy.dialects.sqlite.pysqlite

    try:
        iptable=Table('ips',MetaData(engine),autoload=True)
    except Exception:
        iptable = Table('ips',MetaData(engine),
                    Column('ip',VARCHAR(16),primary_key=True),
                    Column('port',Integer,nullable=False),
                    Column('address',VARCHAR(20)),
                    Column('proxy_type',VARCHAR(5)),
                    Column('speed',Integer),
                    Column('connection',Integer),
                    Column('dur', TEXT),
                    Column('check',DateTime(timezone="Asia/Shanghai"))
                    )
        iptable.create()

    mapper(IP,iptable)
    Session = sessionmaker(bind=engine)
    session = Session()

    f = webdriver.Firefox()
    count = 0
    for url in get_url(n):
        count = count+1
        f.get(url)
        trs = f.find_elements_by_xpath('//table[@id="ip_list"]/tbody/tr[position()>1]')
        count2 = 0
        num_records = len(trs)
        for row in trs:
            count2 = count2+1
            print "*" * int(count2/num_records *50)
            tds = row.find_elements_by_tag_name("td")
            ip_record = IP()
            ip_record.ip = tds[1].text
            ip_record.port = tds[2].text
            ip_record.address = tds[3].text
            ip_record.proxy_type = tds[5].text
            ip_record.speed = tds[6].find_element_by_xpath("//div[@title]").get_attribute("title")[:-1]
            ip_record.connection = tds[7].find_element_by_xpath("//div[@title]").get_attribute("title")[:-1]
            ip_record.dur = tds[8].text
            ip_record.check=datetime.datetime.strptime(tds[9].text, "%y-%m-%d %H:%M")
            if not session.query(IP).filter(IP.ip==ip_record.ip).filter(IP.port==ip_record.port).all():
                session.add(ip_record)
        session.commit()
        print "{0} pages sucessfully crawled!".format(count).center(50,'-')
    session.close()
    print "Finish!".center(50,'-')
except KeyboardInterrupt:
    session.close()
    print "Interruptted in {0}th page.".format(count)
