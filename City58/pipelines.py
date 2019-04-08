# -*- coding: utf-8 -*-

from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import logging
import pymysql
import codecs
import json

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls,crawler):
        params = dict(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DB'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **params)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 利用Twisted提供的adbapi实现Mysql的异步插入数据
        query = self.dbpool.runInteraction(self.do_insert, item, spider)
        # 异常处理
        query.addErrback(self.handle_error, spider)

    def handle_error(self, failure, spider):
        # 接收并记录插入失败的数据总量
        spider.crawler.stats.inc_value('Failed_Insert_DB')
        logging.error("Failed Insert DB: %s" % failure)
        _ = failure

    def do_insert(self, cursor, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE".format(
            table=item.table, keys=keys, values=values)
        update = ', '.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        cursor.execute(sql, tuple(data.values())*2)
        # 利用数据收集器记录插入数据库成功的数据总量
        spider.crawler.stats.inc_value('Success_Inserted_DB')

class JsonPipeline(object):
    def open_spider(self, spider):
        self.file = codecs.open('houseinfo.json', 'w', encoding='utf-8')
        self.file.write(b'[\n')

    def process_item(self, item, spider):
        # 序列化数据
        lines = '{}\n'.format(json.dumps(dict(item), indent=2, ensure_ascii=False))
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.write(b']')
        self.file.close()