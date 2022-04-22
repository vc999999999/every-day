import requests
from lxml import etree

# 网页数据对应的类型
data_type = [
    "招生单位",
    "所在地",
    "研究生院",
    "自划线院校",
    "博士点",
]


# 硕士 专业学位 招生数据查询 https://yz.chsi.com.cn/zsml/queryAction.do
def master():
    # 先通过接口获取 专业学位里 所有学位的编号
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://yz.chsi.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://yz.chsi.com.cn/zsml/queryAction.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'mldm': 'zyxw',
    }

    p_res = requests.post('https://yz.chsi.com.cn/zsml/pages/getZy.jsp', headers=headers, data=data)
    profession_data = p_res.json()
    # 循环所有的 专业名称和专业ID
    query_data = {}

    for dm in profession_data:
        # mldm 是查询的专业学位 yjxkdm 是这个专业领域的编号
        data = {
            'ssdm': '',
            'dwmc': '',
            'mldm': 'zyxw',
            'mlmc': '',
            'yjxkdm': dm['dm'],
            'zymc': '',
            'xxfs': '',
            'pageno': 2,
        }

        res = requests.post('https://yz.chsi.com.cn/zsml/queryAction.do', headers=headers,data=data)
        # 接口查询出数据后使用 xpath 解析
        res_info = etree.HTML(res.text)
        table_info = res_info.xpath('//table[@class="ch-table"]/tbody/tr')
        for td_data in table_info:
            td_all_data = td_data.xpath("./td")
            # 循环td 里的每一格数据 和 数据的对应类型一起循环方便处理
            for grid, d_type in zip(td_all_data, data_type):
                grid = grid.xpath('string(.)').replace("\r", "").replace("\n", "").replace("	", "").replace(" ", "")
                # 处理页面是上 是否
                if grid == " ":
                    grid = "NO"
                if grid == "":
                    grid = "YES"
                # 把查询出来的数据 赋值到query_data字典方便处理
                query_data[d_type] = grid
                print(query_data)


# 学术学位查询
def academic():
    # 先通过接口获取 学术学位里 所有专业的编号
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://yz.chsi.com.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://yz.chsi.com.cn/zsml/queryAction.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    # 比如 哲学 01
    data = {
        'mldm': '01',
    }

    p_res = requests.post('https://yz.chsi.com.cn/zsml/pages/getZy.jsp', headers=headers, data=data)
    profession_data = p_res.json()
    # 循环所有的 专业名称和专业ID
    query_data = {}

    for dm in profession_data:
        # mldm 要写学术的编号  比如哲学 01 yjxkdm 是学科类别的编号
        data = {
            'ssdm': '',
            'dwmc': '',
            'mldm': '01',
            'mlmc': '',
            'yjxkdm': dm['dm'],
            'zymc': '',
            'xxfs': '',
            'pageno': 1,
        }

        res = requests.post('https://yz.chsi.com.cn/zsml/queryAction.do', headers=headers,data=data)
        # 接口查询出数据后使用 xpath 解析
        res_info = etree.HTML(res.text)
        table_info = res_info.xpath('//table[@class="ch-table"]/tbody/tr')
        for td_data in table_info:
            td_all_data = td_data.xpath("./td")
            # 循环td 里的每一格数据 和 数据的对应类型一起循环方便处理
            for grid, d_type in zip(td_all_data, data_type):
                grid = grid.xpath('string(.)').replace("\r", "").replace("\n", "").replace("	", "").replace(" ", "")
                # 处理页面是上 是否
                if grid == " ":
                    grid = "NO"
                if grid == "":
                    grid = "YES"
                # 把查询出来的数据 赋值到query_data字典方便处理
                query_data[d_type] = grid
                print(query_data)


# 运行函数
if __name__ == '__main__':
    academic()