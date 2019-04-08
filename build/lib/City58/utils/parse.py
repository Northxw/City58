# -*- coding:utf-8 -*-

from City58.utils.common import get_md5, handlefont
import requests
import re

def parse_xiaoqu_detail_page(response):
    """
    解析小区详情页
    """
    result = dict()
    try:
        result['id'] = get_md5(response.url)
        result['name'] = response.css('.title-bar > span.title::text').extract_first()
        result['location'] = response.css('.title-bar > span.addr::text').extract_first()
        result['price'] = response.css('.price-container > span.price::text').extract_first('2000')
        result['business_area'] = response.xpath('//table[@class="info-tb"]/tr[1]/td[2]/@title').extract_first()
        result['address'] = response.xpath('//table[@class="info-tb"]/tr[1]/td[4]/@title').extract_first()
        result['building_age'] = response.xpath('//table[@class="info-tb"]/tr[5]/td[2]/@title').re_first('\d+')
        result['property'] = response.xpath('//table[@class="info-tb"]/tr[4]/td[2]/@title').re_first('\d+')
        result['households'] = response.xpath('//table[@class="info-tb"]/tr[2]/td[4]/@title').re_first('\d+')
        result['present_sale_rooms'] = response.css('tr[class="tb-btm"]').css('td:nth-child(2) > a > span::text').re_first('\d+')
        result['present_zu_rooms'] = response.css('tr[class="tb-btm"]').css('td:nth-child(4) > a > span::text').re_first('\d+')
        return result
    except Exception as e:
        _ = e

def parse_ershoufang_list_page(response):
    """
    解析二手房列表页信息
    """
    ershoufang_results = []
    # 二手房信息列表
    ershoufang_list = response.css('#infolist > div.listwrap > table > tr')
    for ershoufang in ershoufang_list:
        result = dict()
        # 二手房详情页URL作ID
        result['id'] = get_md5(ershoufang.css('td.t > a.t::attr(href)').extract_first())
        result['title'] = ershoufang.css('td.t > a.t::text').extract_first()
        # 处理有效信息
        elements = re.sub('\s+', '', '/'.join(ershoufang.css('td::text').extract()).strip()).replace('/', ' ').strip().split()
        result['decoration_type'] = elements[1]
        result['room_type'] = elements[2]
        # 部分城市的"房屋朝向"和"产权年限"位置相反,正则匹配更佳
        result['property'] = re.search('(\d+)', ''.join(elements[3:5])).group(1)
        result['floor'] = '|'.join(elements[5:7])
        # 户型
        try:
            result['house_type'] = elements[7]
        except IndexError as e:
            _ = e
            result['house_type'] = '暂无数据'
        # 房屋总价
        result['total_price'] = '{}'.format(str(ershoufang.css('.tc .pri::text').extract_first('暂无数据')))
        # 每平米房价
        result['price_per_square_meter'] = ershoufang.css('td.tc > span:nth-child(3)::text').re_first('\d+')
        result['square_meter'] = ershoufang.css('td.tc > span:nth-child(5)::text').extract_first('暂无数据')
        ershoufang_results.append(result)
    return ershoufang_results

def parse_chuzufang_detail_page(response):
    """
    解析小区出租房详情页
    """
    # 网页源码 - 获取base64字符串处理字体反爬
    page_sourse = response.text
    # 初始化处理函数
    result = dict()
    result['id'] = get_md5(response.url)
    result['house_title'] = handlefont(page_sourse, response.css('.main-wrap > div.house-title > h1::text').extract_first())
    result['monthly_rent'] = handlefont(page_sourse, response.css('.house-pay-way span b::text').extract_first())
    result['rental_method'] = response.css('.house-desc-item ul li:first-child span:last-child::text').extract_first('暂无数据').strip()
    house_type = handlefont(
        page_sourse, response.css('.house-desc-item > ul > li:nth-child(2) > span:last-child::text').extract_first())
    result['house_type'] = house_type.replace(' ','').replace(u'\xa0',u' ')
    area_b = response.css('.house-desc-item ul li:nth-child(5) span:nth-child(2) a:nth-child(1)::text').extract_first()
    area_a = response.css('.house-desc-item ul li:nth-child(5) span:nth-child(2) a:nth-child(2)::text').extract_first()
    result['area_attribution'] = area_b + area_a
    result['address'] = response.css('.house-desc-item > ul > li:last-child > span:nth-child(2)::text').extract_first('暂无数据').strip()
    return result

if __name__ == '__main__':
    pass
    # 测试链接
    # url = 'https://cd.58.com/xiaoqu/21611/'                           # 小区列表页
    # url = 'https://cd.58.com/xiaoqu/nanhuguojishequ/'                 # 小区详情页
    # url = 'https://cd.58.com/xiaoqu/nanhuguojishequ/ershoufang/'      # 二手房页面
    # url = 'https://cd.58.com/xiaoqu/nanhuguojishequ/chuzu/'           # 出租房页面
    # url = 'https://cd.58.com/pinpaigongyu/36183067306911x.shtml'      # 出租房详情页信息