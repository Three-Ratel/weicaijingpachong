# -*- coding: utf-8 -*-
import scrapy
from sseiPro.items import SseiproItem


def trans(n):
    m = n.split(',')
    n = ''
    for i in range(0, len(m)):
        n = n + m[i]

    n = float(n)
    return n

class SseiSpider(scrapy.Spider):
    name = 'ssei'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=1991&season=1']
    url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=%d&season=%d'

    # start_urls = [url]
    i = 1991
    j = 1
    pageNum = (i, j,)
    all_data = []
    def parse(self, response):

        # all_data = []
        tr_lists = response.xpath('/html/body/div[2]/div[3]/table//tr')
        tr_list = tr_lists[1:]
        #print(type(tr_list))
        for tr in tr_list[::-1]:
            date = tr.xpath('./td[1]/text()').extract_first()
            opening_price = tr.xpath('./td[2]/text()').extract_first()
            highest_price = tr.xpath('./td[3]/text()').extract_first()
            bottom_price = tr.xpath('./td[4]/text()').extract_first()
            closing_price = tr.xpath('./td[5]/text()').extract_first()
            #in_de_price = tr.xpath('./td[6]/text()').extract_first()
            #in_de_rate = tr.xpath('./td[7]/text()').extract_first()
            turnover = tr.xpath('./td[8]/text()').extract_first()
            #volume = tr.xpath('./td[9]/text()').extract_first()
            # open = opening_price.split(',')
            # for i in range(0,len(open)):
            #
            # opening_price = open[]
            #print(date,opening_price,type(date),type(opening_price))

            date = date[0:4] + '-' + date[4:6] + '-' + date[6:]
            item = SseiproItem()
            item['date'] = date
            item['opening_price'] = trans(opening_price)
            item['highest_price'] = trans(highest_price)
            item['bottom_price'] = trans(bottom_price)
            item['closing_price'] = trans(closing_price)
            item['turnover'] = trans(turnover)

            yield item




        if self.i < 2020:
            #self.i += 1
            if self.j < 4:
                self.j += 1
                #print(self.j)
                self.pageNum = (self.i, self.j,)
                new_url = format(self.url%self.pageNum)
                yield scrapy.Request(new_url, callback=self.parse)
            else:
                #print('###########################################################################')
                self.i += 1
                self.j = 1
                self.pageNum = (self.i, self.j,)
                new_url = format(self.url % self.pageNum)
                yield scrapy.Request(new_url, callback=self.parse)

            #手动请求(get)的发送
            # yield scrapy.Request(new_url,callback=self.parse)
        # print(self.all_data, len(self.all_data))
        # print('###########################################################################')

        #return self.all_data

