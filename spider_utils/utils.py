import time
import random

from urllib import parse


def random_sleep(start=1, end=3, debug=True):
    """
    随机延迟，因为如果你访问了很多页面，你的 ip 可能会被封。
    """
    sleep_time = random.randint(start, end)
    if debug:
        print('随机延迟：%s 秒......' % sleep_time)
    time.sleep(sleep_time)


def url_to_dict(url):
    """
    把 url 转换为 dict 字典
    """
    params = {}
    url = parse.unquote(url)
    for param in url.split('&'):
        # print(param)
        k, v = param.split('=')
        params[k] = v
        # print("'{}': '{}',".format(k, v),)
    return params


def get_cookie_dict(cookie):
    """
    转换 Raw 格式的 Cookie 为字典格式
    """
    params = {}
    cookie = cookie.strip()
    if cookie.startswith('Cookie:'):
        cookie = cookie[7:].strip()
    for param in cookie.split(';'):
        k, v = param.split('=')
        params[k.strip()] = v.strip()
        # print("'{}': '{}',".format(k, v), )
    return params
