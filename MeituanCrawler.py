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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


    # 1、抓取数据内容
    web_content = requests.get("http://waimai.meituan.com/restaurant/144813147279802770",headers=headers,  timeout=4)

    # 2、如果抓取失败就发邮件通知
    if(web_content.status_code == 403 or web_content.status_code == 404):
        sd.sendmail("美团外卖马沧湖店网页抓取失败.报错：" + str(web_content.status_code))
    else:
    #抓取成功就存文件
        print(web_content.text)
        pharm_name = html_parser(web_content.text)
        pharm_name_str = pharm_name[0]
        timestamp = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        if(os.path.exists(config.path + "MeiTuanCrawler") != True):
            # 如果文件夹路径不存在就创建一个
            os.mkdir(config.path + "MeiTuanCrawler")
        os.mknod(pharm_name_str + "&" + timestamp + ".txt")



def html_parser(html):

    # 设置提取的正则表达式

    ret = re.findall(r'data-poiname="(.*)".*?data-poiid=',html)
    return ret

if __name__ == '__main__':
    main()

