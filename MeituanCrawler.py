# -*- coding:utf-8 -*-
import sys
import requests
import random
import ip_pool


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
    web_content = requests.get("http://waimai.meituan.com/restaurant/144813147278623122",headers=headers,  timeout=4)

    print(web_content.text)

def html_parser(html):

    # 设置提取的正则表达式
    path_pharm_name =

    tree = etree.HTML(html)
    pharm_name = "data-poiname=\".+\""

if __name__ == '__main__':
    main()

