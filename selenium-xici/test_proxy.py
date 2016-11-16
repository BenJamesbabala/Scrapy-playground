# -*- encoding: utf-8 -*-
import sys
sys.path.append('../PythonJobs')
from pythonJobs.middlewares import httpProxyDownloaderMiddleware, IP
import urllib
from bs4 import BeautifulSoup
from sqlalchemy import or_
import socket
printf = sys.stdout.write

socket.setdefaulttimeout(20)
my_db = httpProxyDownloaderMiddleware()
fail = 0
success = 0
try:
    for i in xrange(my_db.count_ips):
        ip,port = my_db.get_proxy()
        proxies = {
            'http': 'http://{0}:{1}'.format(ip,port)
        }
        try:
            printf("{0}th crawling".format(i))
            handler = urllib.urlopen("http://www.baidu.com",proxies = proxies)
            html = handler.read()
        except Exception,e:
            printf(str(e))
            fail+=1
            my_db.session.query(IP).filter(IP.ip == ip).filter(IP.port == port).delete()
            my_db.session.commit()
            printf("fail")
            printf('-'*30)
            continue

        soup=BeautifulSoup(html,'lxml')
        if len(soup('title'))<1 or u'百度' not in soup('title')[0].text:
            my_db.session.query(IP).filter(IP.ip==ip).filter(IP.port==port).delete()
            my_db.session.commit()
            fail+=1
            printf("fail")
            printf('-' * 30)
        else:
            success +=1
            printf("success")
            printf('-'*30)
        printf("%d of %d" % (i,my_db.count_ips))
except KeyboardInterrupt,e:
    printf(str(e))
finally:
    my_db.session.close()
printf("{0} of {1} proxies success, {2} proxies fail!".format(success,my_db.count_ips,fail))
