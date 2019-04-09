# City58
&emsp; 58同城全国城市房屋信息爬虫，爬取内容包括：各行政区内小区的详情页数据、各小区内出租房和二手房的详情页数据。

## 抓取流程
1. 进入XA小区列表页面, 抓取各行政区编号，并初始化各行政区首页URL

2. 遍历抓取各行政区所有页面的小区详情页URL

3. 进入小区详情页，抓取小区名称、房价、地址等数据

4. 进入小区二手房列表页面, 翻页抓取所有二手房名称、房价、户型等数据

5. 进入小区出租房列表页面, 翻页抓取所有出租房详情页URL

6. 进入出租房详情页，抓取名称、房价、户型、地址、房屋类型等数据

## 第三方依赖
库 | 描述
:---:|:---:
Twisted | （最新）18.9.0
Pywin32 | [pywin32 官网](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/)

&emsp; 注意：
- Twisted 18.9.0 以下版本可能需要安装 微软 Visual C++ Build Tools

- Pywin32不可pip安装，必须去官网下载对应版本的.exe程序手动安装。

## 解释
&emsp; 为方便调试程序，Spider 中设置仅抓取一个行政区内的第一个小区内的二手房和出租房列表首页中的所有房屋信息，可根据需要去掉注释或修改代码完成某个城市的房屋信息抓取。例如：
```Python
# 根据小区编号构造所有小区URL
for area_url in area_url_list:
    yield Request(url=area_url,
                  callback=self.parse_xiaoqu_url_list,
                  errback=self.error_back,
                  priority=10)
    # 测试仅抓取一个行政区
    break
```
&emsp; 为清晰展示 Spider 中的抓取结构，已将主要的解析代码块移入到了 utils.parse 模块中，结构如下：
```Python
def parse_xiaoqu_detail_page(response):
  pass
  
def parse_ershoufang_list_page(response):
  pass
  
def parse_chuzufang_detail_page(response):
  pass
```
&emsp; 58同城房屋信息的字体反爬主要存在于：小区列表页、二手房和出租房详情页。本次代码中涉及的字体反爬页面仅为 "出租房详情页"，已处理。处理字体反爬的部分代码（utils.common）如下：
```Python
def handlefont(page_source, prase_string):
    base64_str = re.findall("charset=utf-8;base64,(.*?)'\)", page_source)[0]
    font = TTFont(BytesIO(base64.decodebytes(base64_str.encode())))
    cmap_ = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
    handled_string = []
    try:
        for char_ in prase_string:
            ......
        return ''.join(handled_string)
    except Exception as e:
        _ = e
``` 
&emsp; 若要抓取全国各大城市的房屋信息，需修改 settings.py 中 HOST 参数为列表类型，并添加城市名称英文小写，例如：北京 - bj。最后遍历该HOST列表即可。

&emsp; 已实现的中间件：UA、Proxy、Retry。 已实现的管道：MysqlTwisted、Json。其他功能详见代码。

## 反反爬
- 挂代理。58同城的反爬措施主要为 IP 反爬，真机访问次数稍多就会被 ban 掉一段时间，所以代理是必不可少的，但同样会被 ban 掉不少。

- 随机UA。设置随机 User-Agent 可在一定程序上减轻58反爬。

- 下载延时。在已经实现上述两种反反爬措施的前提下，设置下载延时为0-1秒之间的随机数（最大可能保证抓取效率），可有效解决反爬。

## 部署
&emsp; 代码已部署到本地 Scrapyd 服务器。若 Window 执行命令报错 "scrapyd-deploy 不是内部或外部命令，也不是可运行的程序"，请移步：[解决方案](https://www.jianshu.com/p/457003a8dbc4)

## 运行
&emsp; 除直接 run main.py 外，可切换至项目根目录下执行 Scrapyd API启动爬虫：
```
curl http://localhost:6800/schedule.json -d project=City58 -d spider=58
```

## Bug
&emsp; 由于某种原因，添加 Scrapy 内置邮件发送模块后，总会报错。但不影响正常的抓取流程。欢迎提交 issue。报错部分代码如下：
```
......
File "C:\Users\xxxxxx\AppData\Local\Programs\Python\Python36\lib\site-packages\twisted\protocols\tls.py", line 252, in _flushSendBIO
    bytes = self._tlsConnection.bio_read(2 ** 15)
builtins.AttributeError: 'NoneType' object has no attribute 'bio_read'
```

## 待实现功能
- 全国主要城市房屋信息可视化
- ...

## 更新列表
&emsp; 2019/4/8 已更新。

## 公告
&emsp; 本代码仅作学习交流，若涉及58同城侵权，请邮箱联系，将在第一时间处理。
