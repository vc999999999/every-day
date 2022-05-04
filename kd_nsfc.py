import requests
import json
import xlwt

# 国家科学自然基金 数据爬取 信息检索 code申请代码
# 所有的资质类别
zh_type = [
    {"name": "面上项目", "id": "218"},
    {"name": "重点项目", "id": "220"},
    {"name": "重大研究项目", "id": "339"},
    {"name": "联合基金项目", "id": "579"},
    {"name": "青年科学基金项目", "id": "630"},
    {"name": "地区科学基金项目", "id": "631"},
    {"name": "专项基金项目", "id": "649"},
    {"name": "数据天元基金项目", "id": "80"},
]

all_year = [
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
]

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorization': 'Bearer undefined',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://kd.nsfc.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://kd.nsfc.gov.cn/finalSearchList?inputJson=%7B%22code%22%3A%22C15%20%E5%9B%AD%E8%89%BA%E5%AD%A6%E4%B8%8E%E6%A4%8D%E7%89%A9%E8%90%A5%E5%85%BB%E5%AD%A6%22,%22conclusionYear%22%3A%222020%22,%22dependUnit%22%3A%22%22,%22keywords%22%3A%22%22,%22pageNum%22%3A0,%22pageSize%22%3A5,%22personInCharge%22%3A%22%22,%22projectName%22%3A%22%22,%22projectType%22%3A%22218%22,%22subPType%22%3A%22%22,%22psPType%22%3A%22%22,%22ratifyNo%22%3A%22%22,%22ratifyYear%22%3A%22%22%7D',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_data(year, line):
    # 循环查询每个年份的所有类别
    for i in zh_type:
        print(i)

        # 每个类别查询50页
        for page in range(50):

            type_id = i["id"]
            json_data = {
                'code': 'C15',
                'complete': True,
                'conclusionYear': year,
                'dependUnit': '',
                'keywords': '',
                'pageNum': page,
                'pageSize': 10,
                'personInCharge': '',
                'projectName': '',
                'projectType': type_id,
                'subPType': '',
                'psPType': '',
                'ratifyNo': '',
                'ratifyYear': '',
                'order': 'approveYear',
                'ordering': 'desc',
            }

            response = requests.post('https://kd.nsfc.gov.cn/api/baseQuery/completionQueryResultsData', headers=headers, json=json_data)
            json_str = json.loads(response.text)
            results = json_str["data"]["resultsData"]
            # 判断是否数据为空
            if json_str["data"]["resultsData"] is []:
                print(111)
                break
            if json_str["data"]["itotalRecords"] == "0":
                print(222)
                break
            for data in results:
                h_id = data[0]
                # 关键词
                h_keyword = data[8]
                # 类别
                project_Type = i["name"]
                # 年度
                year_data = year
                # 项目成果
                gain = data[10]
                gain = " 期刊论文[{}]; 会议论文[{}]; 著作[{}]; 奖励[{}]; 专利[{}]".format(gain.split(";")[0], gain.split(";")[1], gain.split(";")[2], gain.split(";")[3], gain.split(";")[4])
                res = requests.get('https://kd.nsfc.gov.cn/api/baseQuery/conclusionProjectInfo/{}'.format(h_id), headers=headers)
                json_res = json.loads(res.text)
                if json_res["code"] == 200:
                    # 项目批准号
                    ratify = json_res["data"]["ratifyNo"]
                    # 申请代码
                    code = json_res["data"]["code"]
                    # 项目名称
                    projectName = json_res["data"]["projectName"]
                    # 项目负责人
                    projectAdmin = json_res["data"]["projectAdmin"]
                    # 依托单位
                    dependUnit = json_res["data"]["dependUnit"]
                    # 研究期限
                    researchTimeScope = json_res["data"]["researchTimeScope"]
                    # 资助经费
                    supportNum = json_res["data"]["supportNum"]
                    # 中文摘要
                    projectAbstractC = json_res["data"]["projectAbstractC"]
                    line += 1
                    she_name.write(line, 0, year_data)
                    she_name.write(line, 1, project_Type)
                    she_name.write(line, 2, ratify)
                    she_name.write(line, 3, code)
                    she_name.write(line, 4, projectName)
                    she_name.write(line, 5, projectAdmin)
                    she_name.write(line, 6, dependUnit)
                    she_name.write(line, 7, researchTimeScope)
                    she_name.write(line, 8, supportNum)
                    she_name.write(line, 9, h_keyword)
                    she_name.write(line, 10, gain)
                    she_name.write(line, 11, projectAbstractC)

    return line


if __name__ == '__main__':
    workbookr = xlwt.Workbook(encoding='ascii')
    she_name = workbookr.add_sheet("科研数据")
    she_name.write(0, 0, "年度")
    she_name.write(0, 1, "资助类别")
    she_name.write(0, 2, "项目批准号")
    she_name.write(0, 3, "申请代码")
    she_name.write(0, 4, "项目名称")
    she_name.write(0, 5, "项目负责人")
    she_name.write(0, 6, "依托单位")
    she_name.write(0, 7, "研究期限")
    she_name.write(0, 8, "资助经费")
    she_name.write(0, 9, "关键词")
    she_name.write(0, 10, "项目成果")
    she_name.write(0, 11, "中文摘要")
    line = 0
    for i in all_year:
        print(i)
        line = get_data(i, line)
    workbookr.save("科学基金数据查询.xls")


