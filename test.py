try:
    import requests
    import time
    from bs4 import BeautifulSoup
    from DownloadKit import DownloadKit
except ModuleNotFoundError:
    print("未找到库")

headers = {
    'User-Agent': 'MyProject/1.0 (fox44mm)'
}

posts_api = "https://e621.net/posts.json?"  # posts_api
pools_api = "https://e621.net/pools/"  # pools_api

e621_data = {
    "pools": {},
    "artists": {},
    "general": {},
    "sets": {},
    "single-post": {}
}
wait_time = 0.6

class configer:  # 这一个用来读取配置文件的类
    _configure = ''
    config = {}

    def __init__(self, configure_file):  # 初始化方法接受一个配置文件的地址用来打开它
        current = ""
        lines = open(configure_file).readlines()  # 读取所有的行存储到lines变量中

        for line in lines:  # 循环每一行

            if line.startswith('#') or line.startswith('\n'):  # 去除注释
                continue

            if line.find('#') != -1:  # 去除行内注释
                line = line[0:line.find('#') - 1]
            line = line.strip()  # 去除空白字符

            if line.startswith('[') and line.endswith(']'):
                current = line[1:-1]
                self.config[current] = []
                continue
            self.config[current].append(line)

    def __getitem__(self, key):
        return self.config[key]


def get_response(URL):
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Get failure!\terror code:{response.status_code} ")

    return response


# todo 搜索下载
def general_search():
    for general in config['general']:  # 处理url
        print(f"解析 general {general}")
        e621_data['general'][general] = {}
        url = posts_api + "limit=320" + "&tags=" + general.replace(' ', '+')

        # 处理url
        while True:
            json_data = get_response(url).json()
            Len = len(json_data['posts'])
            for index in range(0, Len):
                # todo 判断获取到空值
                file_url = json_data['posts'][index]['file']['url']
                ext = json_data['posts'][index]['file']['ext']
                id = json_data['posts'][index]['id']
                if file_url is None:
                    print(f"{file_url} is None")
                    continue
                e621_data['general'][general][f"{id}.{ext}"] = file_url

            print(f"{general} 获取到的数量{Len}")
            if Len == 320:  # todo 当数量大于320时，及结果有分页时
                url += f"&page=b{json_data['posts'][319]['id']}"
            else:
                break
            time.sleep(wait_time)


# todo 艺术家作品下载
def artist():
    for artist in config['artists']:  # 处理url
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

            if Len == 320:  # todo 当数量大于320时，及结果有分页时
                url += f"&page=b{json_data['posts'][319]['id']}"
            else:
                break
            time.sleep(wait_time)


# todo 泳池下载
def pool():
    for pool_id in config['pools']:
        print(f"pool_id:{pool_id}")  # 正在获取的pool_id
        url = pools_api + pool_id  # 合并url
        content = get_response(url).content  # 获取内容
        soup = BeautifulSoup(content, 'lxml')  # 使用soup对内容进行解析
        time.sleep(wait_time)

        # 泳池名称
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
    path = "./downloads"
    D = DownloadKit()
    D.set.if_file_exists.skip()
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

    # todo 重新设置下载函数，实现保存名称为 id.ext


if __name__ == '__main__':
    config = configer("./tags.txt")  # 标签文件

    pool()
    general_search()
    artist()

    start_time = time.time()
    start_download()
    count_second = time.time() - start_time
    print(f"下载耗时 %d:%02d" % (int(count_second / 60), int(count_second % 60)))
