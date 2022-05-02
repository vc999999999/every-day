import re
import time
import requests
import json
from lxml import etree
import xlwt
from fontTools.ttLib import TTFont
import xlrd
import random


# 字体识别工具获取的文字
texts = [
        '1','2','3','4','5','6','7','8',
        '9','0','店','中','美','家','馆','小','车','大',
        '市','公','酒','行','国','品','发','电','金','心',
        '业','商','司','超','生','装','园','场','食','有',
        '新','限','天','面','工','服','海','华','水','房',
        '饰','城','乐','汽','香','部','利','子','老','艺',
        '花','专','东','肉','菜','学','福','饭','人','百',
        '餐','茶','务','通','味','所','山','区','门','药',
        '银','农','龙','停','尚','安','广','鑫','一','容',
        '动','南','具','源','兴','鲜','记','时','机','烤',
        '文','康','信','果','阳','理','锅','宝','达','地',
        '儿','衣','特','产','西','批','坊','州','牛','佳',
        '化','五','米','修','爱','北','养','卖','建','材',
        '三','会','鸡','室','红','站','德','王','光','名',
        '丽','油','院','堂','烧','江','社','合','星','货',
        '型','村','自','科','快','便','日','民','营','和',
        '活','童','明','器','烟','育','宾','精','屋','经',
        '居','庄','石','顺','林','尔','县','手','厅','销',
        '用','好','客','火','雅','盛','体','旅','之','鞋',
        '辣','作','粉','包','楼','校','鱼','平','彩','上',
        '吧','保','永','万','物','教','吃','设','医','正',
        '造','丰','健','点','汤','网','庆','技','斯','洗',
        '料','配','汇','木','缘','加','麻','联','卫','川',
        '泰','色','世','方','寓','风','幼','羊','烫','来',
        '高','厂','兰','阿','贝','皮','全','女','拉','成',
        '云','维','贸','道','术','运','都','口','博','河',
        '瑞','宏','京','际','路','祥','青','镇','厨','培',
        '力','惠','连','马','鸿','钢','训','影','甲','助',
        '窗','布','富','牌','头','四','多','妆','吉','苑',
        '沙','恒','隆','春','干','饼','氏','里','二','管',
        '诚','制','售','嘉','长','轩','杂','副','清','计',
        '黄','讯','太','鸭','号','街','交','与','叉','附',
        '近','层','旁','对','巷','栋','环','省','桥','湖',
        '段','乡','厦','府','铺','内','侧','元','购','前',
        '幢','滨','处','向','座','下','県','凤','港','开',
        '关','景','泉','塘','放','昌','线','湾','政','步',
        '宁','解','白','田','町','溪','十','八','古','双',
        '胜','本','单','同','九','迎','第','台','玉','锦',
        '底','后','七','斜','期','武','岭','松','角','纪',
        '朝','峰','六','振','珠','局','岗','洲','横','边',
        '济','井','办','汉','代','临','弄','团','外','塔',
        '杨','铁','浦','字','年','岛','陵','原','梅','进',
        '荣','友','虹','央','桂','沿','事','津','凯','莲',
        '丁','秀','柳','集','紫','旗','张','谷','的','是',
        '不','了','很','还','个','也','这','我','就','在',
        '以','可','到','错','没','去','过','感','次','要',
        '比','觉','看','得','说','常','真','们','但','最',
        '喜','哈','么','别','位','能','较','境','非','为',
        '欢','然','他','挺','着','价','那','意','种','想',
        '出','员','两','推','做','排','实','分','间','甜',
        '度','起','满','给','热','完','格','荐','喝','等',
        '其','再','几','只','现','朋','候','样','直','而',
        '买','于','般','豆','量','选','奶','打','每','评',
        '少','算','又','因','情','找','些','份','置','适',
        '什','蛋','师','气','你','姐','棒','试','总','定',
        '啊','足','级','整','带','虾','如','态','且','尝',
        '主','话','强','当','更','板','知','己','无','酸',
        '让','入','啦','式','笑','赞','片','酱','差','像',
        '提','队','走','嫩','才','刚','午','接','重','串',
        '回','晚','微','周','值','费','性','桌','拍','跟',
        '块','调','糕'
    ]


cookies = {
    's_ViewType': '10',
    'cy': '4',
    'cye': 'guangzhou',
    'fspop': 'test',
    'aburl': '1',
    'm_flash2': '1',

}


dian_ping_headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.dianping.com',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


# 搜索店铺 如果有则获取那个店铺的 星级 评价数 人均
def dian_ping(name):
    dian_ping_data = {}
    # 这里的 4 代表的是广州
    dian_ping_url = "https://www.dianping.com/search/keyword/4/0_" + name
    # 搜索大众点评是否有该店铺

    dian_ping_res = requests.get(dian_ping_url, headers=dian_ping_headers, cookies=cookies, timeout=1)
    res_info = etree.HTML(dian_ping_res.text)
    if dian_ping_res.text.find("很抱歉") > -1:

        print("无结果")
        return -1
    # 搜索页获取店铺详情页url
    for i in range(1, 4):
        if i == 3:
            print("无结果")
            return -1
        try:
            dian_ping_name = res_info.xpath('//div[@id="shop-all-list"]/ul/li[{}]/div[@class="txt"]/div[@class="tit"]/a/h4/text()'.format(i))[0]
        except IndexError:
            continue
        if dian_ping_name == name:
            try:
                dian_ping_data["shop_href"] = res_info.xpath('//div[@id="shop-all-list"]/ul/li[{}]/div[@class="txt"]/div[@class="tit"]/a/@href'.format(i))[0]
                break
            except IndexError:
                continue
    # 访问店铺点评详情页
    dian_ping_shop_res = requests.get(dian_ping_data["shop_href"], headers=dian_ping_headers, timeout=1).content.decode("utf-8")
    # print(dian_ping_data["shop_href"])

    # 正则匹配获取css文件的地址
    ex = '<link rel="stylesheet" type="text/css" href="//s3plus.meituan.net/v1/(.*?).css">'
    pattern = re.compile(ex)
    # 没有加密字体代表店铺无结果
    try:
        css = pattern.findall(dian_ping_shop_res)[0]
        # print(css)
    except IndexError:
        print("无结果")
        return -1

    # 请求css文件的地址获取文件内容

    css_url = f'http://s3plus.meituan.net/v1/{css}.css'
    css_text =  requests.get(css_url).text
    # print(css_text)
    # 在css文件中获取字体文件链接
    woff = css_text.split('");} .num{font-family:')[0].split('"),url("')[-1]
    print(woff)
    woffurl = 'http:' + woff
    wofftxt = requests.get(woffurl).content
    # 请求字体文件 写入到num.woff
    with open('num.woff', 'wb') as f:
        f.write(wofftxt)
    shop_info = etree.HTML(dian_ping_shop_res)
    # xpath 处理页面文本
    v_count = shop_info.xpath('//span[@id="reviewCount"]/text()')[0]
    try:
        v_count2 = shop_info.xpath('//span[@id="reviewCount"]/text()')[-1]
    except:
        v_count2 = ""
    r_count = ''.join(shop_info.xpath('//span[@id="reviewCount"]/d/text()'))
    avg_body = shop_info.xpath('//span[@id="avgPriceTitle"]/text()')[0]
    avg = shop_info.xpath('//span[@id="avgPriceTitle"]/d/text()')

    # getGlyphOrder()方法返回所有字符编码名称，按表格顺序提取，类型为列表
    font = TTFont('num.woff')
    lis = font.getGlyphOrder()[2:]
    dic = {}

    # 将 字体名字 和 我们查看到的值 组成一个字典 如：'unif2ab': '副'
    for index, value in enumerate(texts):
        string = lis[index].replace("uni", '\\u')
        dic[json.loads(f'"{string}"')] = value
    # print(dic)

    # 匿名函数
    clear = lambda n: dic[n] if n in dic else n
    # 正常写法
    # def clear(n):
    #     if n in dic:
    #         n = dic[n]
    #     else:
    #         n = n
    #     return n
    numres = ''.join([clear(n) for n in r_count])
    avg_res = ''.join([clear(n) for n in avg])

    # 正常写法
    # numres = ''
    # for n in score:
    #     n = clear(n)
    #     numres += n

    # 拼接数据
    numres = v_count+numres+v_count2
    avg = avg_body+avg_res
    dian_ping_data["reviewCount"] = numres
    dian_ping_data["avgPriceTitle"] = avg
    shop_add = dian_ping_data["shop_href"].split("/")[-1]
    score_url = "http://m.dianping.com/shop/{}".format(shop_add)

    # 获取星级
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'http://www.dianping.com/guangzhou/ch10/g116',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    }

    params = {
        'source': 'pc_jump',
    }
    score_json = requests.get(score_url, params=params, headers=header, verify=False).text
    # 正则匹配获取css文件的地址
    exx = 'score="(.*?)"'
    pattern = re.compile(exx)
    score = pattern.findall(score_json)[0]

    dian_ping_data["score"] = score

    print(dian_ping_data)
    return 0


if __name__ == '__main__':

    name = input("数据要查询的店铺名:")
    shop_href = dian_ping(name)

