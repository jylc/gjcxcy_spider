# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from loguru import logger
import os
import gjcxcy_spider.items
import gjcxcy_spider.excelutils as eu
import gjcxcy_spider.redisutils as ru


class GjcxcySpiderPipeline:
    frame_file_name = './gjcxcy_spider/output/frame.xlsx'
    output_file_name = './gjcxcy_spider/output/statistics.xlsx'
    excel_file = None

    def open_spider(self, spider):
        print(os.getcwd())
        self.excel_file = eu.open_excel(self.frame_file_name)

    def close_spider(self, spider):
        pass

    def write_to_excel(self, data):
        if self.excel_file is None:
            self.excel_file = eu.open_excel(self.frame_file_name)
        else:
            eu.write_to_excel(self.excel_file, data, output=self.output_file_name)

    def process_item(self, item, spider):
        logger.info('start process item')
        if type(item) == gjcxcy_spider.items.ProjectItem:
            self.write_to_excel(item)
        return item


class RedisPipeline:
    def __init__(self):
        self.redis_pool = None

    def open_spider(self, spider):
        self.redis_pool = ru.connect_redis_pool()
        pass

    def close_spider(self, spider):
        self.redis_pool.close()

    def process_item(self, item, spider):
        logger.info('start store item into redis')
        if type(item) == gjcxcy_spider.items.ProjectItem:
            Id = str(item['id'])
            item_dict = str(item)
            self.redis_pool.set(Id, item_dict, nx=True)
        return item

    pass
