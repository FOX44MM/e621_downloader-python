try:
    import requests
    import time
    import json
    import os
    from bs4 import BeautifulSoup
    from DownloadKit import DownloadKit
    from e621.configer import configer

# 模块没有找到或不存在
except ModuleNotFoundError:
    print(
        "该脚本依赖 beautifulsoup4 DownloadKit requests"
    )
    print("未找到库")
# ---------------------------------------------

headers = {
    'User-Agent': 'MyProject/1.0 (fox44mm)'
}

posts_api = "https://e621.net/posts.json?"  # posts_api
pools_api = "https://e621.net/pools/"  # pools_api

e621_data = {  # 记录各个标签信息
    "pools": {},
    "artists": {},
    "general": {},
    "sets": {},
    "single-post": {}
}
config = {
    "downloadsDirectory": "",
    "R18": True
}

wait_time = 0.6
tags_file = {}  # 标签文件
data_json = {}


# -------------------------------------------------------------------------------------
def message(info):
    url = f"https://api.day.app/77dX6F4i4XK7GBd88iTsc/e621_downloader/{info}?group=e621_downloader&icon=https://img.picui.cn/free/2024/06/18/6671823ebba81.jpg&sound=birdsong"
    response = requests.get(url)
    if response.status_code == 200:
        print(f" - 已向iphone发送信息!")

    def __getitem__(self, key):
        return self.tags_file[key]


def get_response(URL):
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Get failure!\terror code:{response.status_code} ")

    return response


# todo 搜索下载
def general_search():
    for general in tags_file['general']:  # 处理url
        print(f"解析 general {general}")
        e621_data['general'][general] = {}
        url = posts_api + "limit=320" + "&tags=" + general.replace(' ', '+')

        # 处理url
        while True:
            json_data = get_response(url).json()
            Len = len(json_data['posts'])
            for index in range(0, Len):
                file_url = json_data['posts'][index]['file']['url']
                ext = json_data['posts'][index]['file']['ext']
                id = json_data['posts'][index]['id']
                # todo 判断获取到空值
                if file_url is None:
                    continue
                e621_data['general'][general][f"{id}.{ext}"] = file_url

            print(f"{general} 获取到的数量{Len}")
            time.sleep(wait_time)

            if Len == 320:  # todo 当数量大于320时，及结果有分页时
                url += f"&page=b{json_data['posts'][319]['id']}"
            else:
                break


# https://e621.net/pools/37864

# todo 艺术家作品下载
def artist():
    for artist in tags_file['artists']:  # 处理url
        e621_data['artists'][artist] = {}
        url = posts_api + "limit=320" + "&tags=" + artist

        # 处理url
        while True:
            json_data = get_response(url).json()
            Len = len(json_data['posts'])

            print(f"{artist} 获取到的数量{Len}")
            for index in range(0, Len):
                # todo 判断获取到空值
                file_url = json_data['posts'][index]['file']['url']
                ext = json_data['posts'][index]['file']['ext']
                id = json_data['posts'][index]['id']
                if file_url is None:
                    print(f"{file_url} is None")
                    continue
                e621_data['artists'][artist][f"{id}.{ext}"] = file_url
            time.sleep(wait_time)

            if Len == 320:  # todo 当数量大于320时，及结果有分页时
                url += f"&page=b{json_data['posts'][319]['id']}"
            else:
                break


# todo 泳池下载
def pool():
    for pool_id in tags_file['pools']:
        print(f"pool_id:{pool_id}")  # 正在获取的pool_id
        url = pools_api + pool_id  # 合并url
        content = get_response(url).content  # 获取内容
        soup = BeautifulSoup(content, 'lxml')  # 使用soup对内容进行解析
        time.sleep(wait_time)

        # 泳池名称
        # todo 修改此处分析代码
        # 泳池 37864 无法正常解析
        pool_name = soup.find(class_='pool-category-series').string.replace(' ', '_')
        tags = soup.find_all(name='article')

        e621_data['pools'][pool_name] = {}
        for num, tag in enumerate(tags):
            file_url = tags[num].attrs['data-file-url']
            ext = file_url.split('.')[-1]
            name = pool_name + "_%05d" % (num + 1) + f".{ext}"
            e621_data['pools'][pool_name][name] = file_url
            # print(f"{name} : {file_url}")


# todo 用户收藏下载

def start_download():
    path = data_json['downloadDirectory']
    D = DownloadKit()
    D.set.if_file_exists.skip()
    start_time = time.time()

    for option in e621_data.keys():  # general pools artist
        if len(e621_data[option]) == 0:  # 判断是否有数据
            continue
        for tag in e621_data[option].keys():  # size_difference growth muscle giantess
            if len(e621_data[option][tag]) == 0:  # 判断是否有数据
                continue
            print(f"Downloading {option} -> {tag}: ")
            D.set.goal_path(path + "/" + option + "/" + tag)
            # ./download / artists / growth
            length = len(e621_data[option][tag])  # 遍历链接
            for index in e621_data[option][tag].keys():
                D.add(e621_data[option][tag][index], rename=index, file_exists='skip')  # 添加名称
            D.wait(show=True)
    count_second = time.time() - start_time
    print(f"下载耗时 %d:%02d" % (int(count_second / 60), int(count_second % 60)))

    # todo 可下载 post_set 集
    # todo 添加命令行参数，以实现某些功能
    # todo 使用flet UI库制作界面


def initer():  # 初始化函数
    if not os.path.exists("./config.json"):
        print("生成配置文件")
        with open("./config.json", 'w') as f:
            temp = "{\n\t\"downloadDirectory\": \"./downloads/\",\n\t\"R18\": true\n}"

            f.write(temp)

    if not os.path.exists("./tags.txt"):
        print("不存在标签文件")
        with open("./tags.txt", 'w', encoding="UTF-8") as f:
            temp = "# This is the tag file that you will use so the program can know what tags to search.\n# If you wish to comment in this file, simply put `#` at the beginning or end of line.\n# Insert tags you wish to download in the appropriate group (remove all example tags and IDs with what you wish to download):\n[artists]\n[pools]\n[artists]\n[general]\n"
            f.write(temp)
            f.flush()
            f.close()
            exit()

    global tags_file
    tags_file = configer("./tags.txt")
    file = open("config.json", "r")
    global data_json
    data_json = json.load(file)


# todo 添加是否启用清水图
# todo 将pool中的内容压缩为zip文档
# todo 抛出各种异常
# todo ip池功能
# todo 图形界面？


if __name__ == '__main__':
    initer()  # 调用初始化函数

    if not data_json['R18']:
        print("Close R18")
        pools_api = pools_api.replace("621", "926")
        posts_api = posts_api.replace("621", "926")

    pool()  # 解析泳池内的信息
    general_search()  # 解析全局搜索
    artist()  # 解析艺术家

    start_download()  # 开始下载
