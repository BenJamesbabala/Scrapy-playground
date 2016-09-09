# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class PythonjobsPipeline(object):
    def __init__(self):
        self.handler = open("Debug-items.text","w")

    def process_item(self, item, spider):
        self.handler.write(str(item))
        self.handler.write("-"*100)
        if 'python' not in item['title'].lower():
            raise DropItem("title not including 'python' key word")

    def __del__(self):
        self.handler.close()