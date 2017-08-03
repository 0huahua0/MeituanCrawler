# -*- coding:utf-8 -*-
import json

import requests
import re
import config
import os
import time
import sendmail as sd
import json

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
               'Cookie' : '_lxsdk_cuid=15ccf2d30b9c8-0678fa184b7462-1571466f-13c680-15ccf2d30b9c8; w_uuid=neYqha2pXt9eCyMkIj1DDxF75hdEs4DzTCNbZD66FdE_wMCYuTcCgD84ZyzDr0kf; abt=1501666603.0%7CACE; rvd=28684903; rvct=1%2C57; __mta=251573561.1498124464796.1501666603661.1501666607783.3; __utma=211559370.1310200229.1498124465.1498124465.1501666604.2; __utmz=211559370.1498124465.1.1.utmcsr=baidu|utmccn=baidu|utmcmd=organic|utmcct=homepage; __utmv=211559370.|1=city=bj=1^3=dealtype=263=1; uuid=7f8d8f52c397a93a8c07.1498124463.0.0.0; oc=dXdDOjEvfxUD0738qq8avizSZQpwWehgVm3qx6UgUDIXWnPxIzz5jnbvFlADd2d_pfvhpDj15AeZFZmrNGSyxxIaPsRzb9a4GG2T4MLTcFVB1x7mE2TDndoo9fPd0n4WT1mwSI_FgKb0_gXun4G-C4HyD7Oa1hiDuqGqiFS3Olc; ci=10; _ga=GA1.2.1310200229.1498124465; _gid=GA1.2.475996695.1501635598; w_cid=0; waddrname=; w_geoid=wt3q14r3mby1; w_ah=; _gat=1; JSESSIONID=eiwastx371ak6fszbed443n; _ga=GA1.3.1310200229.1498124465; _gid=GA1.3.475996695.1501635598; __mta=251573561.1498124464796.1501666607783.1501749872722.4; w_utmz="utm_campaign=baidu&utm_source=1522&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; w_visitid=2cb7456d-9ac7-4dad-ab5f-57a3a09b6dbe'
               }


    # 1、抓取数据内容
    # http://waimai.meituan.com/search/wt3jzc9m1gmr/rt?keyword=好药师
    web_content = requests.get("http://waimai.meituan.com/search/wt3jzc9m1gmr/rt?keyword=%E5%A5%BD%E8%8D%AF%E5%B8%88",headers=headers,  timeout=4)

    # 2、如果抓取失败就发邮件通知
    if(web_content.status_code == 403 or web_content.status_code == 404):
        sd.sendmail("美团外卖马沧湖店网页抓取失败.报错：" + str(web_content.status_code))
    else:
        # 先从搜索页面获取详情页的动态url
        getUrl = "http://waimai.meituan.com/restaurant/" + re.findall(r'/restaurant/(\d+)"',web_content.text)[0]
        web_content1 = requests.get(getUrl, headers=headers,timeout = 4 )
        #抓取成功就存文件
        createFile(web_content1.text)


def createFile(text):

    #获取当前时间
    timestamp = str(time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time())))

    print(text)
    #爬取药店名
    pharmNameList = html_parser(text, "pharmName")
    if(len(pharmNameList) != 0):
        pharm_name = pharmNameList[0]
    else:
        sd.sendmail("药店名提取结果为空!")
        exit()

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
    contentList = html_parser(text,"content")
    contentJson = [json.loads(line) for line in contentList]

    content = ''.join(contentJson)
    content1 = content.replace("\n","").replace("\t","").replace("\r","").replace("\"","")
    # 写数据
    if( content1 != ""):
        file.write(content1)
    else:
        sd.sendmail("内容提取结果为空!")
        exit()
    file.close()





def html_parser(text,parameter):

    # 设置提取的正则表达式
    if(parameter == "pharmName"):
        ret = re.findall(r'data-poiname="(.*)".*?data-poiid=',text)
        return ret
    elif(parameter == "content"):
        ret = re.findall(r'<script type="text/template" id="foodcontext-\d+">\r\n\r\n\r\n\r\n\r\n(.*?)</script>',text,re.S)
        return ret
    else:
        sd.sendmail("正则表达式提取失败")
        exit()



if __name__ == '__main__':
    main()

