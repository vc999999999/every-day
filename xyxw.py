import requests
from lxml import etree
import csv
import time

# 网易新闻搜索 不登录显示200条数据
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.163.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


# 获取搜索页url
def get_url(keyword):

    params = {
        'keyword': keyword,
    }

    res = requests.get('https://www.163.com/search', params=params, headers=headers)
    search_info = etree.HTML(res.text)
    url_count = search_info.xpath('//div[@class="keyword_list "]/div/h3/a/@href')
    all_url = []
    for i in url_count:
        all_url.append(i)
    return all_url


# 获取新闻具体内容
def get_info(all_url, keyword):
    all_data = []
    # 循环所有新闻的url
    for url in all_url:
        data = {}
        res = requests.get(url, headers=headers)
        html_info = etree.HTML(res.text)
        # 如果是视频换格式处理
        if url.find("video") > -1:
            title = html_info.xpath('//div[@class="title_wrap"]/h1/text()')[0]
            author = html_info.xpath('//div[@class="author"]/a/text()')[0]
            with open('{}视频.csv'.format(keyword), 'a+', encoding='utf-8-sig', newline='') as v:
                w = csv.writer(v)
                w.writerows([[title, author]])
            continue
        # 获取时间 格式处理再转为时间戳
        header_info = html_info.xpath('//div[@class="post_info"]/text()')[0].replace("\n", "").replace(" ", "").replace("\u3000", "")
        try:
            header_date = header_info.replace("　来源:", "")
            d = header_date[:10]
            t = header_date[-8:]
            dt = d+" "+t
            # 转换成时间数组
            time_array = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
            # 转换成时间戳
            time_stamp = time.mktime(time_array)
            author = html_info.xpath('//div[@class="post_info"]/a/text()')[0]
        # 作者和时间一共俩种格式
        except ValueError:
            header_date = header_info.split("来源:")[0].replace(" ", "")
            d = header_date[:10]
            t = header_date[-8:]
            dt = d+" "+t
            # 转换成时间数组
            time_array2 = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
            # 转换成时间戳
            time_stamp = time.mktime(time_array2)
            author = header_info.split("来源:")[1]

        # 获取 作者 标题 内容
        title = html_info.xpath('//h1[@class="post_title"]/text()')[0]
        body_text = ""
        all_p = html_info.xpath('//div[@class="post_body"]/p')
        for p in all_p:
            p_text = p.xpath('string(.)')
            body_text += p_text
        # 赋值传递插入排序方法中
        data['title'] = title
        data['author'] = author
        data['date'] = dt
        data['body_text'] = body_text
        data['dt'] = time_stamp
        all_data.append(data)
    # 排序完数据写入
    sort_data = choose_sort(all_data)
    for i in sort_data:
        title = i["title"]
        author = i["author"]
        date = i["date"]
        body_text = i["body_text"]
        with open('{}文章.csv'.format(keyword), 'a+', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f)
            w.writerows([[title, author, date, body_text]])


# 排序方法
def choose_sort(ls):
    for i in range(len(ls)):
        tmp = ls[i]['dt']
        pos = i
        for j in range(i+1, len(ls)):
            if ls[j]['dt']<tmp:
                pos = j
                tmp = ls[j]['dt']
        if i!=pos:
            ls[i], ls[pos] = ls[pos], ls[i]
    return ls


if __name__ == '__main__':
    keyword = input("输入关键词:")
    # 创建csv文件保存数据
    with open('{}文章.csv'.format(keyword), 'a+', encoding='utf-8-sig', newline='') as f:
        fieldnames = ['标题', '作者', '日期', '内容']
        writer_ = csv.DictWriter(f, fieldnames=fieldnames)  # DictWriter以字典形式写入
        writer_.writeheader()
    with open('{}视频.csv'.format(keyword), 'a+', encoding='utf-8-sig', newline='') as v:
        fieldnames = ['标题', '作者']
        writer_v = csv.DictWriter(v, fieldnames=fieldnames)  # DictWriter以字典形式写入
        writer_v.writeheader()
    all_url = get_url(keyword)
    get_info(all_url, keyword)