import requests
import execjs
from lxml import etree
import xlwt

# 安装node.js 网上查找
# npm install -g jsdom 安装所需包
# npm install -g canvas 安装所需包
# pip install requests 安装所需包
# pip install lxml 安装所需包
# pip install PyExecJS 安装所需包
# pip install xlwt 安装所需包


all_data_type = [
    # 预估
    "yjyg",
    # 快报
    "yjkb",
    # 公告
    "yjgg",

]

all_date = [
    # 2022 第一季度
    "2022-03-31",

    # 2021 年报
    "2021-12-31",
    # 2021 第三季度
    "2021-09-30",
    # 2021 中报
    "2021-06-30",
    # 2021 第一季度
    "2021-03-31",

    # 2020 年报
    "2020-12-31",
    # 2020 第三季度
    "2020-09-30",
    # 2020 中报
    "2020-06-30",
    # 2020 第一季度
    "2020-03-31",

    # 2019 年报
    "2019-12-31",


]
yg_data_type = [
    "序号",
    "股票代码",
    "股票简称",
    "业绩预告类型",
    "业绩预告摘要",
    "净利润变动幅度(%)",
    "上年同期净利润(元)",
    "公告日期",
]


gg_data_type = [
    "序号",
    "股票代码",
    "股票简称",
    "公告日期",
    "营业收入（元）",
    "营业收入同比增长（%）",
    "营业收入季度环比增长（%）",
    "净利润（元）",
    "净利润同比增长（%）",
    "净利润季度环比增长（%）",
    "每股收益（元）",
    "每股净资产（元）",
    "净资产收益率（%）",
    "每股经营现金流量（元）",
    "销售毛利率（%）",
]


kb_data_type = [
    "序号",
    "股票代码",
    "股票简称",
    "公告日期",
    "营业收入（元）",
    "去年同期（元）",
    "同比增长（%）",
    "季度环比增长（%）",
    "净利润（元）",
    "去年同期（元）",
    "同比增长（%）",
    "季度环比增长（%）",
    "每股收益（元）",
    "每股净资产（元）",
    "净资产收益率（%）",
]


def write_yjyg(data,n, line):
    code = {}
    if n == 8:
        print(data)
        n = 0
        line += 1
        print(line)
        all_sheet.write(line, 0, data["序号"])
        all_sheet.write(line, 1, data["股票代码"])
        all_sheet.write(line, 2, data["股票简称"])
        all_sheet.write(line, 3, data["业绩预告类型"])
        all_sheet.write(line, 4, data["业绩预告摘要"])
        all_sheet.write(line, 5, data["净利润变动幅度(%)"])
        all_sheet.write(line, 6, data["上年同期净利润(元)"])
        all_sheet.write(line, 7, data["公告日期"])
        code['n'] = n
        code['line'] = line
        code['code'] = 2
        return code
    else:
        code['n'] = n
        code['line'] = line
        code['code'] = 1
        return code


def write_yjgg(data, n, line):
    code = {}

    if n == 15:
        print(data)
        n = 0
        line += 1
        print(line)
        reduction_sheet.write(line, 0, data["序号"])
        reduction_sheet.write(line, 1, data["股票代码"])
        reduction_sheet.write(line, 2, data["股票简称"])
        reduction_sheet.write(line, 3, data["公告日期"])
        reduction_sheet.write(line, 4, data["营业收入（元）"])
        reduction_sheet.write(line, 5, data["营业收入同比增长（%）"])
        reduction_sheet.write(line, 6, data["营业收入季度环比增长（%）"])
        reduction_sheet.write(line, 7, data["净利润（元）"])
        reduction_sheet.write(line, 8, data["净利润同比增长（%）"])
        reduction_sheet.write(line, 9, data["净利润季度环比增长（%）"])
        reduction_sheet.write(line, 10, data["每股收益（元）"])
        reduction_sheet.write(line, 11, data["每股净资产（元）"])
        reduction_sheet.write(line, 12, data["净资产收益率（%）"])
        reduction_sheet.write(line, 13, data["每股经营现金流量（元）"])
        reduction_sheet.write(line, 14, data["销售毛利率（%）"])
        code['n'] = n
        code['line'] = line
        code['code'] = 2
        return code
    else:
        code['n'] = n
        code['line'] = line
        code['code'] = 1
        return code


def write_yjkb(data, n, line):
    code = {}
    if n == 15:
        print(data)
        n = 0
        line += 1
        print(line)
        increase_sheet.write(line, 0, data["序号"])
        increase_sheet.write(line, 1, data["股票代码"])
        increase_sheet.write(line, 2, data["股票简称"])
        increase_sheet.write(line, 3, data["公告日期"])
        increase_sheet.write(line, 4, data["营业收入（元）"])
        increase_sheet.write(line, 5, data["去年同期（元）"])
        increase_sheet.write(line, 6, data["同比增长（%）"])
        increase_sheet.write(line, 7, data["季度环比增长（%）"])
        increase_sheet.write(line, 8, data["净利润（元）"])
        increase_sheet.write(line, 9, data["去年同期（元）"])
        increase_sheet.write(line, 10, data["同比增长（%）"])
        increase_sheet.write(line, 11, data["季度环比增长（%）"])
        increase_sheet.write(line, 12, data["每股收益（元）"])
        increase_sheet.write(line, 13, data["每股净资产（元）"])
        increase_sheet.write(line, 14, data["净资产收益率（%）"])
        code['n'] = n
        code['line'] = line
        code['code'] = 2
        return code
    else:
        code['n'] = n
        code['line'] = line
        code['code'] = 1
        return code


# 获取财报数据并写入
def get_data(v, url, data_type, line):
    g_code = {}
    data = {}
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'hexin-v': v,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'http://data.10jqka.com.cn/financial/{}/'.format(data_type),
    }
    response = requests.get(url, headers=headers, verify=False)
    text = response.text
    stock_info = etree.HTML(text)
    try:
        stock_data = stock_info.xpath('//table/tbody/tr')
    except AttributeError:
        g_code['stock'] = -1
        return g_code
    if text.find("今日无数据") > -1:
        g_code['stock'] = -1
        return g_code
    if stock_data == []:
        g_code['stock'] = -1
        return g_code

    n = 0
    for td_data in stock_data:
        td_all_data = td_data.xpath("./td")
        if data_type == "yjkb":
            file_data_type = kb_data_type

        elif data_type == "yjgg":
            file_data_type = gg_data_type

        elif data_type == "yjyg":
            file_data_type = yg_data_type
        else:
            g_code['stock'] = -1
            return g_code

        for grid, s_type in zip(td_all_data, file_data_type):
            n += 1

            try:
                grid = grid.xpath('string(.)').replace("\r", "").replace("\n", "").replace("	", "").replace(" ", "")
            except AttributeError:
                pass

            data[s_type] = grid

            if data_type == "yjkb":
                code = write_yjkb(data, n, line)
                n = code["n"]
                line = code["line"]

            elif data_type == "yjgg":
                code = write_yjgg(data, n, line)
                n = code["n"]
                line = code["line"]

            elif data_type == "yjyg":
                code = write_yjyg(data, n, line)
                n = code["n"]
                line = code["line"]
            else:
                g_code['stock'] = -1
                return g_code

    g_code['line'] = line
    g_code['stock'] = 0

    return g_code


# 运行js文件获取cookies
def get_cookie():
    with open("get_cookie.js", "r", encoding="utf-8") as f:
        js = f.read()
    # npm root -g 查看路径放入
    v = execjs.compile(js, cwd="C:\\Users\\VC\\AppData\\Roaming\\npm\\node_modules").call("getCookie")
    # print(v)
    return v


if __name__ == '__main__':

    date = input("输入对应日期:")
    data_type = input("输入下载类型:")
    line = 0

    workbook = xlwt.Workbook(encoding='ascii')

    # 创建新的sheet表
    all_sheet = workbook.add_sheet("预告")
    increase_sheet = workbook.add_sheet("快报")
    reduction_sheet = workbook.add_sheet("公告")

    # 往表格写入内容
    all_sheet.write(0, 0, "序号")
    all_sheet.write(0, 1, "股票代码")
    all_sheet.write(0, 2, "股票简称")
    all_sheet.write(0, 3, "业绩预告类型")
    all_sheet.write(0, 4, "业绩预告摘要")
    all_sheet.write(0, 5, "净利润变动幅度(%)")
    all_sheet.write(0, 6, "上年同期净利润(元)")
    all_sheet.write(0, 7, "公告日期")

    increase_sheet.write(0, 0, "序号")
    increase_sheet.write(0, 1, "股票代码")
    increase_sheet.write(0, 2, "股票简称")
    increase_sheet.write(0, 3, "公告日期")
    increase_sheet.write(0, 4, "营业收入（元）")
    increase_sheet.write(0, 5, "去年同期（元）")
    increase_sheet.write(0, 6, "同比增长（%）")
    increase_sheet.write(0, 7, "季度环比增长（%）")
    increase_sheet.write(0, 8, "净利润（元）")
    increase_sheet.write(0, 9, "去年同期（元）")
    increase_sheet.write(0, 10, "同比增长（%）")
    increase_sheet.write(0, 11, "季度环比增长（%）")
    increase_sheet.write(0, 12, "每股收益（元）")
    increase_sheet.write(0, 13, "每股净资产（元）")
    increase_sheet.write(0, 14, "净资产收益率（%）")

    reduction_sheet.write(0, 0, "序号")
    reduction_sheet.write(0, 1, "股票代码")
    reduction_sheet.write(0, 2, "股票简称")
    reduction_sheet.write(0, 3, "公告日期")
    reduction_sheet.write(0, 4, "营业收入（元）")
    reduction_sheet.write(0, 5, "营业收入同比增长（%）")
    reduction_sheet.write(0, 6, "营业收入季度环比增长（%）")
    reduction_sheet.write(0, 7, "净利润（元）")
    reduction_sheet.write(0, 8, "净利润同比增长（%）")
    reduction_sheet.write(0, 9, "净利润季度环比增长（%）")
    reduction_sheet.write(0, 10, "每股收益（元）")
    reduction_sheet.write(0, 11, "每股净资产（元）")
    reduction_sheet.write(0, 12, "净资产收益率（%）")
    reduction_sheet.write(0, 13, "每股经营现金流量（元）")
    reduction_sheet.write(0, 14, "销售毛利率（%）")

    for i in range(1, 100):
        # print(data_type)
        url = "http://data.10jqka.com.cn/ajax/{}/date/{}/board/ALL/field/stockcode/order/desc/page/{}/ajax/1/free/1/".format(data_type, date, i)
        hexin_v = get_cookie()
        g_code = get_data(hexin_v, url, data_type, line)
        if g_code['stock'] == -1:
            break
        line = g_code['line']
        # time.sleep(10)
    # 保存
    workbook.save("{}{}.xls".format(data_type, date))


