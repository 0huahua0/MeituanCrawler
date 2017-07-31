# -*- coding:utf-8 -*-
import requests
import re
import config
import os
import time
import sendmail as sd

def main():
    download_html()


def download_html():
    """
    抓取网页
    """
    # http://waimai.meituan.com/restaurant/144813147278492050


    #请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
               'Host' : 'waimai.meituan.com',
               'Cookie' : 'td_cookie=18446744069543523117; w_uuid=2zdNjgqzFgyNdpcXBIW-cmk_U9V1aHy1FEk9iG6ixGt3NgWjeli9QOTlEvSqhp-A; td_cookie=18446744069562108394; _ga=GA1.2.696061170.1498180959; _gid=GA1.2.1479918780.1501465377; _gat=1; w_cid=420105; w_cpy_cn="%E6%B1%89%E9%98%B3%E5%8C%BA"; w_cpy=hanyangqu; waddrname="%E9%A9%AC%E6%B2%A7%E6%B9%96"; w_geoid=wt3jzc9m1gmr; w_ah="30.551108848303556,114.24862492829561,%E9%A9%AC%E6%B2%A7%E6%B9%96|30.49746584147215,114.16207272559404,%E5%A5%BD%E8%8D%AF%E5%B8%88%E9%87%91%E8%8D%B7%E8%8A%B1%E5%9B%AD%E5%BA%97%2824%E5%B0%8F%E6%97%B6%E5%8C%85%E9%80%81%29|23.131649997085333,113.32285277545452,%E5%AF%8C%E5%8A%9B%E7%9B%88%E4%B8%B0%E5%A4%A7%E5%8E%A6"; JSESSIONID=ge3u1hk32ehc1a1wif7tnwut4; _ga=GA1.3.696061170.1498180959; _gid=GA1.3.1479918780.1501465377; __mta=143513866.1498180960560.1501489117084.1501489119040.63; w_utmz="utm_campaign=baidu&utm_source=1522&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_visitid=c64d13d6-15f4-49e4-84e4-8494793ce4b8'
               }


    # 1、抓取数据内容
    web_content = requests.get("http://waimai.meituan.com/restaurant/144813147281506706",headers=headers,  timeout=4)

    # 2、如果抓取失败就发邮件通知
    if(web_content.status_code == 403 or web_content.status_code == 404):
        # sd.sendmail("美团外卖马沧湖店网页抓取失败.报错：" + str(web_content.status_code))
        pass
    else:
        #抓取成功就存文件
        createFile(web_content.text)


def createFile(text):

    #获取当前时间
    timestamp = str(time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time())))

    print(text)
    #爬取药店名
    pharm_name = html_parser(text,"pharmName")[0]

    #制定一个文件夹
    isExists = os.path.exists(config.path)

    if not isExists:
        # 如果文件夹路径不存在就创建一个
        os.mkdir(config.path)
    #
    fileUrl = config.path + '\\' + pharm_name + "&" + timestamp + ".txt"

    #创建一个文件夹
    file = open(fileUrl, 'w')
    #提取商品信息
    content = html_parser(text,"content")[0]
    # 写数据
    file.write(content)
    file.close()


def html_parser(text,parameter):

    # 设置提取的正则表达式
    if(parameter == "pharmName"):
        ret = re.findall(r'data-poiname="(.*)".*?data-poiid=',text)
    elif(parameter == "content"):

        ret = re.findall(r'<script type="text/template" id=".*?">(.*?)</script>',text)
    else:
        ret = "正则表达式提取失败"
    return ret


if __name__ == '__main__':
    main()

