# -*- encoding: utf-8 -*-
import sys
sys.path.append('../PythonJobs')
from ip_pipeline import Ip_pipeline, IP
import urllib
from bs4 import BeautifulSoup
from sqlalchemy import or_
import socket
printf = sys.stdout.write

socket.setdefaulttimeout(5)
pipeline = Ip_pipeline()
fail = 0
success = 0
try:
    for i in xrange(pipeline.count_ips):
        ip,port = pipeline.get_proxy('HTTP')
        proxies = {
            'http': 'http://{0}:{1}'.format(ip,port)
        }
        try:
            printf("{0}th crawling".format(i + 1) + '\n')
            handler = urllib.urlopen("http://www.baidu.com",proxies = proxies)
            html = handler.read()
        except Exception,e:
            printf(str(e) + '\n')
            fail+=1
            pipeline.session.query(IP).filter(IP.ip == ip).filter(IP.port == port).delete()
            pipeline.session.commit()
            if pipeline.offset >0:
                pipeline.offset -= 1
            printf("fail" + '\n')
            printf("%d of %d" % (i + 1, pipeline.count_ips) + '\n')
            printf('-'*30 + '\n')
            continue

        soup=BeautifulSoup(html,'lxml')
        if len(soup('title'))<1 or u'百度' not in soup('title')[0].text:
            pipeline.session.query(IP).filter(IP.ip==ip).filter(IP.port==port).delete()
            if pipeline.offset>0:
                pipeline.offset -= 1
            pipeline.session.commit()
            fail+=1
            printf("fail" + '\n')
            printf('-' * 30 + '\n')
        else:
            success +=1
            printf("success" + '\n')
        printf("%d of %d" % (i+1,pipeline.count_ips) + '\n')
        printf('-' * 30 + '\n')
except KeyboardInterrupt,e:
    printf(str(e) + '\n')
finally:
    pipeline.session.close()
printf("{0} of {1} proxies success, {2} proxies fail!".format(success,pipeline.count_ips,fail))
