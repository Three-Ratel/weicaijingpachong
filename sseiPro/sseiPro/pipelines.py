# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class SseiproPipeline(object):
    fp = None

    def open_spider(self, spider):
        print('开始爬虫......')
        #self.fp = open('h.csv', 'a+', encoding='utf-8',newline='')
        #self.writer = csv.writer(self.fp, dialect="excel")
        #self.writer.writerow(['日期', '开盘价', '最高价', '最低价', '收盘价', '成交量'])

    # 使用来接收爬虫文件提交过来的item,然后将其进行任意形式的持久化存储
    # 参数item:就是接收到的item对象
    # 该方法每接收一个item就会调用一次
    def process_item(self, item, spider):
        date = item['date']
        opening_price = item['opening_price']
        highest_price = item['highest_price']
        bottom_price = item['bottom_price']
        closing_price = item['closing_price']
        turnover = item['turnover']

        self.writer.writerow([date,opening_price,highest_price,bottom_price,closing_price,turnover])

        return item  # item是返回给了下一个即将被执行的管道类

    def close_spider(self, spider):
        print('结束爬虫!')
        #self.fp.close()


# import os
# import csv
#
# class MoonBlogPipeline(object):
#
#         def __init__(self):
#             # csv文件的位置,无需事先创建
#             store_file = os.path.dirname(__file__) + '/spiders/articles.csv'
#             print("***************************************************************")
#             # 打开(创建)文件
#
#             self.file = open(store_file, 'a+', encoding="utf-8"，newline='')
#             # csv写法
#             self.writer = csv.writer(self.file, dialect="excel")
#
#         def process_item(self, item, spider):
#             # 判断字段值不为空再写入文件
#             print("正在写入......")
#             if item['article_title']:
#                 # 主要是解决存入csv文件时出现的每一个字以‘，’隔离
#                 self.writer.writerow([item['article_title'],item['article_link'],item['publish_date'],item['scan_num'],item['article_content']])
#             return item
#
#         def close_spider(self, spider):
#             # 关闭爬虫时顺便将文件保存退出
#             self.file.close()