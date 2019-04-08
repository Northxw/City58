# -*- coding: utf-8 -*-

from scrapy import Item, Field

class City58XiaoQuInfo(Item):
    table = 'xiaoqu'
    id = Field()
    name = Field()
    location = Field()
    price = Field()
    business_area = Field()
    address = Field()
    building_age = Field()
    property = Field()
    households = Field()
    present_sale_rooms = Field()
    present_zu_rooms = Field()

class City58ErShouFang(Item):
    table = 'ershoufang'
    id = Field()        # 二手房详情页URL
    title = Field()
    decoration_type = Field()
    room_type = Field()
    property = Field()
    floor = Field()
    house_type = Field()
    total_price = Field()
    price_per_square_meter = Field()
    square_meter = Field()

class City58ChuZuFang(Item):
    table = 'chuzufang'
    id = Field()
    house_title = Field()
    monthly_rent = Field()
    rental_method = Field()
    house_type = Field()
    area_attribution = Field()
    address = Field()