# -*- coding: utf-8 -*-
import scrapy

# -*- coding: utf-8 -*-
import scrapy
from collectip.items import XiciItem


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com',
    )

    def start_requests(self):  # 作用：生成初始的request
        reqs = []  # 定义reqs(空集)

        for i in range(1, 3):  # 设置变量：页码1到206
            req = scrapy.Request("http://www.xicidaili.com/nn/%s" % i)
            yield req

    def parse(self, response):
        # 提取每一行的xpath位置
        ip_list = response.xpath('//table[@id="ip_list"]')  # ip_list=xpath提取（table标签下的"ip_list"属性）

        trs = ip_list[0].xpath('tr')  # 变量trs=ip_list加入tr标签

        items = []  # 定义items空集

        for ip in trs[1:]:  # ip的tr从[1以后开始]
            pre_item = XiciItem()  # pre_item=加载XiCiItem()

            pre_item['IP'] = ip.xpath('td[3]/text()')[0].extract()  # 取文字

            pre_item['PORT'] = ip.xpath('td[4]/text()')[0].extract()  # 取文字

            pre_item['POSITION'] = ip.xpath('string(td[5])')[0].extract().strip()

            pre_item['TYPE'] = ip.xpath('td[7]/text()')[0].extract()
            # speed取到td的title属性，再用正则（匹配到数字）
            pre_item['SPEED'] = ip.xpath(
                'td[8]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]

            pre_item['LAST_CHECK_TIME'] = ip.xpath('td[10]/text()')[0].extract()

            items.append(pre_item)  # 把pre_item添加到项目

        return items  # 返回项目
