import re

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException


def get_response(url, params=None, **kwargs):
    """
    请求获取网页内容，为了防止程序中断，捕捉错误，返回 None。
    :param url:
    :param params:
    :param kwargs:
    :return:
    """
    try:
        response = requests.get(url, params=params, **kwargs)
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        return None


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None, ):
    """
    长链接会话，支持重试

    例子：
    from requests.exceptions import ConnectTimeout, ConnectionError, ProxyError

    TIMEOUT = 5
    DEFAULT_RETRIES = 3
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }
    proxies = None
    session = requests_retry_session()
    url = 'https://www.baidu.com'
    for i in range(DEFAULT_RETRIES):
        try:
            r = session.get(url,
                            proxies=proxies, timeout=TIMEOUT,
                            headers=HEADERS)
        except ProxyError:
            print(f'Proxy {proxies} is dead!')
        except (ConnectTimeout, ConnectionError):
            pass
        else:
            break
    print(r.text)
    :param retries:
    :param backoff_factor:
    :param status_forcelist:
    :param session:
    :return:
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,  # 允许的重试总次数，优先于其他计数
        read=retries,  # 重试读取错误的次数
        connect=retries,
        backoff_factor=backoff_factor,  # 休眠时间： {backoff_factor} * (2 ** ({重试总次数} - 1))
        status_forcelist=status_forcelist,  # 强制重试的状态码
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_response_to_file(url, file_name=None, params=None, **kwargs):
    """
    请求获取网页内容，并保存到文件。
    :param url:
    :param file_name:
    :param params:
    :param kwargs:
    :return:
    """

    if file_name is None:
        file_name = url.split('/')[-1]
        file_name = re.sub('[\/:*?"<>|]', '-', file_name)

    ret = get_response(url, params=params, **kwargs)
    if ret:
        with open(file_name, 'w', encoding='utf-8') as fout:
            fout.write(ret.text)
        return file_name
    else:
        return None
