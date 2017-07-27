# -*- coding:utf-8 -*-
import requests
import re
import config
import os
import time

def main():
    download_html()


def download_html():
    """
    抓取网页
    """
    # http://waimai.meituan.com/restaurant/144813147278492050


    #请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


    # 抓取数据内容
    web_content = requests.get("http://waimai.meituan.com/restaurant/144813147279212946",headers=headers,  timeout=4)
    print(web_content.text)
    pharm_name = html_parser(web_content.text)
    print(pharm_name)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if(os.path.exists(config.path + "file") == false ):
        print(1)
        os.mkdir(config.path + "file")
    print(pharm_name + "&" + timestamp + ".txt")
    os.mknod(pharm_name + "&" + timestamp + ".txt")



def html_parser(html):

    # 设置提取的正则表达式

    ret = re.findall(r'data-poiname="(.*)".*?data-poiid=',html)
    return ret

if __name__ == '__main__':
    main()

