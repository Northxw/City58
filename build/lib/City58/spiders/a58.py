# -*- coding: utf-8 -*-

import scrapy
import requests
import time
from scrapy.mail import MailSender
from scrapy.selector import Selector
from scrapy.http import Request
from City58.items import City58XiaoQuInfo, City58ErShouFang, City58ChuZuFang
from City58.utils.parse import parse_xiaoqu_detail_page, parse_ershoufang_list_page,\
                                parse_chuzufang_detail_page

class A58Spider(scrapy.Spider):
    # 爬虫启动时间
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = '58'
    allowed_domains = ['58.com']
    xiaoqu_url = 'https://{}/xiaoqu/{}'
    cnt_page = 1

    def start_requests(self):
        """
        构造当前城市各行政区URL
        """
        # 获取当前城市个行政区编号
        area_url_list = []
        response = Selector(requests.get(url='https://{}/xiaoqu/'.format(self.settings.get('HOST'))))
        area_code_list = response.css('.filter-wrap dl:nth-child(1) dd > a::attr(value)').extract()
        if area_code_list:
            for code in area_code_list:
                if code:
                    area_url_list.append(self.xiaoqu_url.format(self.settings.get('HOST'), str(code)))
        # self.logger.debug("XiaoquCodes: %s" % str(area_url_list))

        # 根据小区编号构造所有小区URL
        for area_url in area_url_list:
            yield Request(url=area_url,
                          callback=self.parse_xiaoqu_url_list,
                          errback=self.error_back,
                          priority=10)
            # 测试仅抓取一个行政区
            break

    def parse_xiaoqu_url_list(self, response):
        """
        获取小区详情页URL
        """
        # 记录请求成功的数量
        self.crawler.stats.inc_value("Success_Reqeust")
        xiaoqu_url_list = response.css('.content-wrap .content-side-left ul > li .list-info > h2 > a::attr(href)').extract()
        # self.logger.debug(xiaoqu_url_list)
        if xiaoqu_url_list:
            for xiaoqu_url in xiaoqu_url_list:
                if xiaoqu_url:
                    yield Request(url=xiaoqu_url,
                                  callback=self.xiaoqu_detail_page,
                                  errback=self.error_back,
                                  priority=9)
                # 测试仅抓取一个小区
                break

        # 测试仅抓取小区列表页首页
        """
        # 获取下一页小区列表
        next = response.css('a[class="nextPage"]')
        if next:
            self.cnt_page += 1
            yield Request(url=response.url[0:-5] + '/pn_{}'.format(self.cnt_page) ,
                          callback=self.parse_xiaoqu_url_list,
                          errback=self.error_back,
                          priority=9)
        """

    def xiaoqu_detail_page(self, response):
        """
        解析小区详情页
        """
        # 记录请求成功的数量
        self.crawler.stats.inc_value("Success_Reqeust")
        xiaoqu_detail_data = parse_xiaoqu_detail_page(response)
        item = City58XiaoQuInfo()
        item.update(xiaoqu_detail_data)
        self.logger.debug(item)
        yield item


        # 二手房列表页首页
        ershoufang_url = response.url + 'ershoufang'
        yield Request(url=ershoufang_url,
                      callback=self.ershoufang_list_page,
                      errback=self.error_back,
                      priority=8)


        # 出租房列表页首页
        chuzufang_url = response.url + 'chuzu'
        yield Request(url=chuzufang_url,
                      callback=self.chuzufang_list_page,
                      errback=self.error_back,
                      priority=7)

    def ershoufang_list_page(self, response):
        """
        解析二手房列表页信息 (从列表页直接获取有效信息,不再递归向下处理)
        """
        # 获取当前小区二手房的数量
        ersohufang_nums = eval(response.css("div.fl.filterCheckbox > span > b::text").extract_first())
        if ersohufang_nums:
            # 记录请求成功的数量
            self.crawler.stats.inc_value("Success_Reqeust")
            ershoufang_list_page_data = parse_ershoufang_list_page(response)
            self.logger.debug(ershoufang_list_page_data)
            for ershoufang_data in ershoufang_list_page_data:
                item = City58ErShouFang()
                item.update(ershoufang_data)
                yield item

            # 测试仅抓取二手房列表的第一页数据
            """
            # 获取二手房列表下一页数据
            next_page_url = response.css('.listwrap .pagerNumber  a:last-child::attr(href)').extract_first()
            if next_page_url:
                yield Request(url=next_page_url,
                              callback=self.ershoufang_list_page,
                              errback=self.error_back)
            """

    def chuzufang_list_page(self, response):
        """
        获取小区出租房详情页URL
        """
        chuzufang_detail_url_list = response.css('.listwrap > table > tr > td.t > a.t::attr(href)').extract()
        if chuzufang_detail_url_list:
            # 记录请求成功的数量
            self.crawler.stats.inc_value("Success_Reqeust")
            for chuzufang_detail_url in chuzufang_detail_url_list:
                yield Request(url=chuzufang_detail_url,
                              callback=self.chuzufang_detail_url,
                              errback=self.error_back)

        # 测试仅抓取出租房列表页第一页
        """
        # 获取小区出租房列表下一页
        next_page_url = response.css('.listwrap .pagerNumber a:last-child::attr(href)').extract_first()
        if next_page_url:
            yield Request(url=next_page_url,
                          callback=self.chuzufang_list_page,
                          errback=self.error_back,
                          priority=5)
        """

    def chuzufang_detail_url(self, response):
        """
        解析小区出租房详情页数据
        """
        # 记录请求成功的数量
        self.crawler.stats.inc_value("Success_Reqeust")
        chuzufang_detail_data = parse_chuzufang_detail_page(response)
        item = City58ChuZuFang()
        item.update(chuzufang_detail_data)
        self.logger.debug(item)
        yield item

    def error_back(self, e):
        """
        数据收集器记录失败请求
        """
        _ = self
        self.logger.debug('Error: %s' % (e.reason))
        self.crawler.stats.inc_value("Failed_Reqeust")

    def close(self, reason):
        """
        爬虫邮件报告状态
        """
        # 结束时间
        fnished = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 创建邮件发送对象
        mail = MailSender.from_settings(self.settings)
        # 邮件内容
        spider_name = self.settings.get('BOT_NAME')
        start_time = self.start
        success_request = self.crawler.stats.get_value("Success_Reqeust")
        failed_request = self.crawler.stats.get_value("Failed_Reqeust")
        # 若请求成功, 则默认为0
        if failed_request == None:
            failed_request = 0
        insert_into_success = self.crawler.stats.get_value("Success_Inserted_DB")
        failed_db = self.crawler.stats.get_value("Failed_Insert_DB")
        # 若插入成功, 则默认为0
        if failed_db == None:
            failed_db = 0
        fnished_time = fnished
        body = "爬虫名称: {}\n\n 开始时间: {}\n\n 请求成功总量：{}\n 请求失败总量：{} \n\n 数据库存储总量：{}\n 数据库存储失败总量：{}\n\n 结束时间  : {}\n".format(
            spider_name,
            start_time,
            success_request,
            failed_request,
            insert_into_success,
            failed_db,
            fnished_time)
        try:
            # 发送邮件
            mail.send(to=self.settings.get('RECEIVE_LIST'), subject=self.settings.get('SUBJECT'), body=body)
        except Exception as e:
            self.logger.error("Send Email Existing Error, Reason: {}".format(e.args))