#!/usr/bin/env python
# coding=utf-8
'''
@Author: wang wen jie
@Date: 2020-07-27 21:58:15
@LastEditTime: 2020-07-28 17:38:47
@LastEditors: wjiewang@mail.ustc.edu.cn
@Description: 
@FilePath: /spider/code/test.py
@
'''
import requests
import time


def download_pic(index, pic_url):
    response = requests.get(url=pic_url)
    if(response.status_code==200):
        file_path = "PR%d.png" % index
        with open(file_path, "wb") as fout:
            fout.write(response.content)

def get_url(json_content):
    if(not json_content.has_key("page")):
        return None
    if(not isinstance(json_content["page"], list)):
        return None
    if(not json_content["page"][0].has_key("src")):
        return None
    return json_content["page"][0]["src"]
        
def get_content(page_num):
    params = {
        "id": "7_QCqQeIPL4C",
        "lpg": "PP1",
        "dq": "TemperatureElectronics Physics",
        "hl": "zh-CN",
        "pg": "PP1",
        "jscmd": "click3"
    }
    url = "https://books.google.nl/books"
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }

    for index in range(1, page_num+1):
        #  延迟0.5秒
        time.sleep(0.5)
        response = requests.get(url=url, params=params, headers=header)
        if(response.status_code == 200):
            # print(response.content.decode("utf-8"))
            pic_url = get_url(response.json())
            if(pic_url):
                #  延迟0.5秒
                time.sleep(0.5)
                #  下载
                download_pic(index=index, pic_url=pic_url)
                print("success download page: %d" % index)
            else:
                print("can not download page: %d" % index)
                print("exit")
                break
        else:
            print("can get content of page: %d" % index)

def download():
    get_content(10)

if __name__ == "__main__":
    download()