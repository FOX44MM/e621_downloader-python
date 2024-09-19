import requests

headers = {  # 头部
    'User-Agent': 'MyProject/1.0 (fox44mm)'
}


def message(info):
    url = f"https://api.day.app/77dX6F4i4XK7GBd88iTsc/e621_downloader/{info}?group=e621_downloader&icon=https://img.picui.cn/free/2024/06/18/6671823ebba81.jpg&sound=birdsong"
    response = requests.get(url)
    if response.status_code == 200:
        print(f" - 已向iphone发送信息!")


def get_response(URL):
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Get failure!\terror code:{response.status_code} ")
    return response

    sorted()
