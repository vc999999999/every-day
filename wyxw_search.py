import requests, csv
from lxml import etree
import time

# 获取视频id 方法
def get_id(keyword):
    headers = {
        'authority': 'www.163.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.163.com/search?keyword=%E5%88%A9%E7%89%A9%E6%B5%A6',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }
    # 想搜索的关键词
    params = {
        'keyword': keyword,
    }
    # 请求页面获取搜索出来的所有文章 url
    res = requests.get('https://www.163.com/search', params=params, headers=headers)
    resp = etree.HTML(res.text)
    all_div = resp.xpath('//div[@class="keyword_list "]/div')
    all_url = []
    for i in all_div:
        href = i.xpath('./h3/a/@href')
        all_url.append(href[0])
    return all_url


# 获取详情页数据 写入csv文件
def get_data(all_url, keyword):
    all_date = []
    # 循环 输入关键词的所有url
    for url in all_url:
        date_title = {}

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        # 请求详情页
        res = requests.get(url, headers=headers)
        resp = etree.HTML(res.text)
        body_text = ""
        # 获取标题  跳过搜索出的视频只拿文章
        try:
            title = resp.xpath('//h1[@class="post_title"]/text()')[0]
        except IndexError:
            continue
        # 获取时间并处理
        post_info = resp.xpath('//div[@class="post_info"]/text()')[0]
        release_date = post_info.split("\u3000")[0].replace("\n", "").replace(" ", "")
        m = release_date[:-8]
        d = release_date[10:]
        dt = m + " " + d
        # 转换成时间戳 方便以时间排序
        time_stamp = date_time(dt)
        # 作者
        author = post_info.split("\u3000")[1].replace(" ", "").replace("\n", "")
        # 时间戳存入
        # date_title[title] = dt
        # 获取文章主体
        all_text = resp.xpath('//div[@class="post_body"]/p')
        for i in all_text:
            p_text = i.xpath("string(.)")
            body_text += p_text
        # 复制到 date_title 然后传入 all_date
        date_title["title"] = title
        date_title["dt"] = time_stamp
        date_title["author"] = author
        date_title["body_text"] = body_text
        date_title["date"] = dt
        all_date.append(date_title)
        print(title)
    # 传入 all_date 进行排序
    data = choose_sort(all_date)
    # 把排序完的数据写入
    for y in data:
        with open('{}.csv'.format(keyword), 'a+', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerows([[y['title'], y['author'], y['body_text'], y['date']]])


# 转换时间格式方法
def date_time(dt):
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp


# 使用插入排序 让数据按照转换完的时间戳排序
def choose_sort(ls):
    for i in range(len(ls)):
        tmp = ls[i]["dt"]
        pos = i
        for j in range(i+1, len(ls)):
            if ls[j]["dt"] < tmp:
                pos = j
                tmp = ls[j]["dt"]
        if i != pos:
            ls[i], ls[pos] = ls[pos], ls[i]
    return ls


if __name__ == '__main__':
    # 输入想搜索的关键词
    keyword = input("关键词:")
    # 获取搜索结果的详情页
    all_url = get_id(keyword)
    # 创建csv文件
    with open('{}.csv'.format(keyword), 'a+', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['标题', '作者', '内容', '发布时间']
        writer_ = csv.DictWriter(f, fieldnames=fieldnames)  # DictWriter以字典形式写入
        writer_.writeheader()
    # 获取详情页数据并写入
    get_data(all_url, keyword)
