#!/usr/bin/env python
# coding=utf-8
'''
@Author: wang wen jie
@Date: 2020-07-27 21:58:15
@LastEditTime: 2020-07-28 22:10:17
@LastEditors: wjiewang@mail.ustc.edu.cn
@Description: 
@FilePath: /book-crawler/code/test.py
@
'''
import requests
import time
import os

start_index = 1
cur_index = 1
end_index = 945
page_type = "PA"

# 最大错误次数
max_err_time = 10
# 当前错误次数
cur_err_time = 0

# 下载的页面
download_page_arr = []
# 出错的页面
error_page_arr = []

header = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    , 'referer': 'https://books.google.com.au/books?id=7_QCqQeIPL4C&printsec=frontcover&dq=TemperatureElectronics+Physics&hl=zh-CN&sa=X&ved=2ahUKEwjKl_S07O_qAhVgzDgGHZDvAdYQ6AEwAHoECAAQAg'
    , 'cookie': '_ga=GA1.4.46321440.1595935894; _gid=GA1.4.1961983430.1595935894; NID=204=vR3rt-duDnd9mkxU2r5vLwb5t3cr3RrYgl7RPmFMBHECSfokUgUQD57YUQ6Irveo3Sk1csDEtxpKhvzwPiufsrWsAm0CKSV-0XkUSZdxuQpk0ejYjeIIRuzQRgoXoiPXeS_126Lau-bkHtPHlchkk1eA1_HOZS9ZVHtrjbzMK_g; 1P_JAR=2020-7-28-12'
}

def download_pic(index, pic_url, type):
    global cur_err_time

    try:
        response = requests.get(url=pic_url, headers=header)
        if(response.status_code==200):
            # 当前次数置为0
            cur_err_time = 0

            file_path = "../image/%s%d.png" % (type, index)
            with open(file_path, "wb") as fout:
                fout.write(response.content)
        else:
            print("error when download %s%d" % (type, index))
            raise Exception("error when download %s%d" % (type, index))
    except Exception as e:
        raise e

def get_label(json_content, key="page", idx=0, label="src"):
    if(not json_content.has_key(key)):
        return None
    if(not isinstance(json_content[key], list)):
        return None
    if(len(json_content[key]) <= idx):
        return None
    if(not json_content[key][idx].has_key(label)):
        return None
    return json_content[key][idx][label]
        
def redownload(json_content):
    try:
        for error_page in reversed(error_page_arr):
            for idx in range(0, 10):
                label = get_label(json_content=json_content, idx=idx, label="pid")
                pic_url = get_label(json_content=json_content, idx=idx, label="src")
                if(label and pic_url and label=="%s%d"%(page_type, error_page)):
                    download_pic(index=error_page, pic_url=pic_url, type=page_type)

    except Exception as e:
        raise e

def get_content(start_page, page_num, type):
    global cur_index
    global download_page_arr

    params = {
        "id": "7_QCqQeIPL4C",
        "lpg": "PP1",
        "dq": "TemperatureElectronics Physics",
        "vq": "TemperatureElectronics Physics",
        "hl": "zh-CN",
        "pg": "PA1",
        "jscmd": "click3"
    }
    url = "https://books.google.com.au/books"

    try:
        for index in range(start_page, page_num+start_page):
            #  延迟0.5秒
            time.sleep(0.05)
            # params["pg"] = "PR%d" % index
            params["pg"] = "%s%d" % (type, index)
            # print(params)

            response = requests.get(url=url, params=params, headers=header)
            if(response.status_code == 200):
                cur_index = index
                # print(response.content.decode("utf-8"))
                with open("../response/%s%d.json"%(type,index), "w") as fout:
                    # fout.write(response.content.decode("utf-8"))
                    fout.write(response.text)

                pic_url = get_label(response.json())
                print("page%d: %s" % (index, pic_url))
                if(pic_url):
                    #  延迟0.5秒
                    time.sleep(0.05)
                    #  下载
                    download_pic(index=index, pic_url=pic_url, type=type)
                    print("success download page: %d" % index)
                    download_page_arr.append(index)
                else:
                    # print("can not parse url of page: %d" % index)
                    raise Exception("can not parse url of page: %d" % index)
                    # print("exit")
                    # break
            else:
                # print("can not get content of page: %d" % index)
                raise Exception("can not get content of page: %d" % index)
    except Exception as e:
        raise e
    else:
        print("success for all")

def download():
    global cur_index
    global cur_err_time
    global error_page_arr

    while(True):
        if(cur_index < end_index):
            # 如果出错次数超过最大允许出错次数，则跳过该页面的下载
            if(cur_err_time >= max_err_time):
                print("exceed max error time when download *%s%d*, so pass this page" % (page_type, cur_index))
                error_page_arr.append(cur_index)
                cur_index += 1
                cur_err_time = 0
            # 继续下载其他页面
            try:
                get_content(cur_index, end_index-cur_index+1, "PA")
            except Exception as e:
                print("error time %d" % cur_err_time)
                print(e)
                cur_err_time += 1
        else:
            break

def mkdir(dir_path):
    folder = os.path.exists(dir_path)
    if(not folder):
        os.makedirs(dir_path)

def save_log():
    global download_page_arr
    global error_page_arr

    mkdir("../logs")    
    with open("../logs/success-page.log", "w") as fout:
        fout.write(str(download_page_arr))
    with open("../logs/error-page.log", "w") as fout:
        fout.write(str(error_page_arr))

if __name__ == "__main__":
    download()
    save_log()