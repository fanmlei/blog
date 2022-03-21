import os
import re
import time
import requests

path = "../source/_posts"

def download_img(img_url, image_name):
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        time.sleep(1)
        open(image_name, 'wb').write(r.content) # 将内容写入图片
        print("done")

def read_file(file_name):
    if not os.path.exists(f"{path}/{file_name[:-3]}") and not os.path.isfile(f"{path}/{file_name[:-3]}"):
        os.mkdir(f"{path}/{file_name[:-3]}")
        print(f"创建文件夹{path}/{file_name[:-3]}")
    url_list = []
    with open(f"{path}/{file_name}", "r") as f:
        for line in f.readlines():
            regular = re.compile(r'[a-zA-Z]+://[^\s]*[.com|.cn]')
            url = re.findall(regular, line)
            if url:
                url_list.append(url[0])
    for index, url in enumerate(url_list):
        download_img(url, f"{path}/{file_name[:-3]}/{index+1}.png")
    

def main():
    # file_list = os.listdir(path)
    # for file in file_list:
    #     if os.path.isfile(f"{path}/{file}"):
    #         read_file(file)
    read_file("configparser模块的简单使用.md")


if __name__ == '__main__':
    main()
