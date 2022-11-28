# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import logging
import pymongo

class MongodbPipeline:
    collection_name = 'best_movies'

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        # logging.warning('SPIDER OPENED FROM PIPELINE')
        self.client = pymongo.MongoClient('mongodb+srv://rrenans:<Aurum@123>@cluster0.sebzwig.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        # logging.warning('SPIDER CLOSED FROM PIPELINE')
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
