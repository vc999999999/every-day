import requests
import te_pb2
from google.protobuf import json_format
import xlwt
import random


# 视频弹幕
def get_danmu(aid, cid):
    url = "https://api.bilibili.com/x/v2/dm/web/seg.so"
    params = {
        'type': '1',
        'oid': cid,
        'pid': aid,
        'segment_index': '1'
    }
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, params=params, timeout=8)
    content = resp.content

    # 调用方法解析弹幕编码
    danmaku_seg = te_pb2.DmSegMobileReply()
    danmaku_seg.ParseFromString(content)

    # 解析后写入
    line = 0
    for i in danmaku_seg.elems:
        data = json_format.MessageToDict(i)
        print(data)
        d_id = data["id"]
        try:
            progress = data["progress"]
        except KeyError:
            progress = "-"
        mode = data["mode"]
        fontsize = data["fontsize"]
        color = data["color"]
        midHash = data["midHash"]
        content = data["content"]
        ctime = data["ctime"]
        idStr = data["idStr"]

        line += 1
        she_name.write(line, 0, d_id)
        she_name.write(line, 1, progress)
        she_name.write(line, 2, mode)
        she_name.write(line, 3, fontsize)
        she_name.write(line, 4, color)
        she_name.write(line, 5, midHash)
        she_name.write(line, 6, content)
        she_name.write(line, 7, ctime)
        she_name.write(line, 8, idStr)
    workbookr.save("bilibili展示.xls")


# 获取历史弹幕
def get_history(date, oid, line):
    # 需要登录才能 获取历史弹幕 这俩参数到视频录里的cookie取
    cookies = {
        'buvid3': '8F153023-86CE-4C8B-9790-6E3366AB8957167618infoc',
        'SESSDATA': 'c3ef5f54,1663066919,1d532*31',
    }

    headers = {
        'authority': 'api.bilibili.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.bilibili.com',
        'pragma': 'no-cache',
        'referer': 'https://www.bilibili.com/video/BV1WF411h7WT?spm_id_from=333.337.search-card.all.click',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    }
    # 写入 视频的oid 和日期
    print(date)
    params = {
        'type': '1',
        'oid': oid,
        'date': date,
    }
    ress = requests.get("http://proxy.httpdaili.com/apinew.asp?ddbh=2535043392946477733").text
    xxx = random.randint(0, 15)

    ipp = ress.split("\r\n")[xxx]
    ip = ipp.split(":")[0]
    port = ipp.split(":")[1]
    proxies = {"http": "http://{}:{}".format(ip, port), "https": "http://{}:{}".format(ip, port)}

    resp = requests.get('https://api.bilibili.com/x/v2/dm/web/history/seg.so', headers=headers, params=params, cookies=cookies, proxies=proxies)
    content = resp.content

    danmaku_seg = te_pb2.DmSegMobileReply()
    danmaku_seg.ParseFromString(content)
    for i in danmaku_seg.elems:
        data = json_format.MessageToDict(i)
        print(data)
        d_id = data["id"]
        try:
            progress = data["progress"]
        except KeyError:
            progress = "-"
        mode = data["mode"]
        fontsize = data["fontsize"]
        color = data["color"]
        midHash = data["midHash"]
        content = data["content"]
        ctime = data["ctime"]
        idStr = data["idStr"]

        line += 1
        she_name.write(line, 0, d_id)
        she_name.write(line, 1, progress)
        she_name.write(line, 2, mode)
        she_name.write(line, 3, fontsize)
        she_name.write(line, 4, color)
        she_name.write(line, 5, midHash)
        she_name.write(line, 6, content)
        she_name.write(line, 7, ctime)
        she_name.write(line, 8, idStr)
        she_name.write(line, 9, oid)
    return line


if __name__ == "__main__":

    workbookr = xlwt.Workbook(encoding='ascii')
    she_name = workbookr.add_sheet("弹幕数据")
    she_name.write(0, 0, "id")
    she_name.write(0, 1, "progress")
    she_name.write(0, 2, "mode")
    she_name.write(0, 3, "fontsize")
    she_name.write(0, 4, "color")
    she_name.write(0, 5, "midHash")
    she_name.write(0, 6, "content")
    she_name.write(0, 7, "ctime")
    she_name.write(0, 8, "idStr")
    she_name.write(0, 9, "oid")
    line = 0

    # 视频首页展示弹幕
    # pid = "423439717"
    #oid = "490578166"
    # get_danmu(pid, oid)

    da_cf = ""
    # oid 视频这个弹幕的id  data 你要查询的历史弹幕日期 会爬取到视频发布到输入日期的弹幕
    oid = "583826951"

    date = "2022-04-28"
    line = get_history(date, oid, line)

    workbookr.save("bilibili{}.xls".format(oid))
