import requests, re, time, csv
from lxml import etree
import random
import json


# 以宠物用品为关键字 搜索后获取商品的 标题 价格 评论数
# get 方法检测是否到登录界面
def get(url):
    while True:
        try:

            res = requests.get(url, headers=headers, timeout=2)
            if res.status_code == 200:
                if 'https://passport.jd.com/new/login.aspx?' not in res.text and "{'code':200,'limit':1}" not in res.text:
                    return res
        except:
            time.sleep(2)


def search():
    for i in range(1, 200):

        res = get('https://search.jd.com/Search?keyword=%E5%AE%A0%E7%89%A9%E7%94%A8%E5%93%81&enc=utf-8&suggest=1.his.0.0&wq=&pvid=f1b9e05013594ba7a0962c9c5473023b&page={}'.format(i))
        response = etree.HTML(res.text)
        for j in response.xpath('//li[@class="gl-item"]'):
            # 获取价格和url
            price = ''.join(j.xpath('.//div[@class="p-price"]//i/text()'))
            url = ''.join(j.xpath('.//div[@class="p-name p-name-type-2"]/a/@href'))
            title = ''.join(j.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()'))
            # 生产时间戳
            millis = int(round(time.time() * 1000))
            # 匹配视频id
            ex = 'com/(.*).html'
            pattern = re.compile(ex)
            jquery = pattern.findall(url)[0]
            # 提取视频id 请求评价数接口
            count_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={},&callback=jQuery5270209&_={}'.format(str(jquery), millis)
            res = requests.get(count_url, headers=headers)
            exx = 'jQuery[0-9].*({.*})]}'
            pattern_n = re.compile(exx)
            # 提取评价数据
            json_str = pattern_n.findall(res.text)[0]
            json_str = json.loads(json_str)
            count_p = json_str["CommentCountStr"]

            if title == '':
                return
            with open('宠物用品数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
                w = csv.writer(f)
                w.writerows([[title, price, count_p, 'https:'+url]])


if __name__ == '__main__':

    headers = {
        'referer': 'https://item.jd.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    with open('宠物用品数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['名字', '价格', '评价', 'url']
        writer_ = csv.DictWriter(f, fieldnames=fieldnames)  # DictWriter以字典形式写入
        writer_.writeheader()
        search()

