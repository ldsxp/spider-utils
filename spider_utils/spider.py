import re
from pathlib import Path
from datetime import datetime
from collections import namedtuple

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException
import html2text
from bs4 import BeautifulSoup

from .client import BaseSpiderClient  # , logger

PageContext = namedtuple('PageContext', ['name', 'page', 'url', ])


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


class BaseSpider(BaseSpiderClient):

    def __init__(self, base_url, start_page=1, page_max=100, name='', save_dir=Path('cache'), is_update=False,
                 log_function=print, wx_thread=None, debug=False,
                 retry=None,
                 retries=None):
        super().__init__(retry, retries)
        self.name = name
        self.base_url = base_url
        self.page_url = '{base_url}/page/{page}/'
        self.start_url = '{base_url}/'
        self.save_dir = save_dir
        self.start_page = start_page
        self.page_max = page_max
        self.is_update = is_update

        self.log_function = log_function
        self.wx_thread = wx_thread
        self.debug = debug
        self.infos = []
        self.errors = []

        text_maker = html2text.HTML2Text()
        text_maker.body_width = 0
        # text_maker.ignore_links = True # 忽略链接
        # text_maker.kypass_tables = False # 循环表
        text_maker.kypass_tables = True
        self.text_maker = text_maker

        if not self.save_dir.exists():
            self.save_dir.mkdir()

    def get_urls(self):
        """
        获取需要爬取的 url
        """
        if self.start_page == 1 and self.start_url:
            self.start_page += 1
            yield PageContext(name=self.name, page=1, url=self.start_url.format(base_url=self.base_url))
        for i in range(self.start_page, self.page_max + 1):
            # print('next_page', i)
            yield PageContext(name=self.name, page=i, url=self.page_url.format(base_url=self.base_url, page=i))

    def parse_list(self, content):
        """
        解析网页内容
        """
        soup = BeautifulSoup(content, 'lxml')
        article_list = soup.find_all('article', class_='post')
        data_list = []

        for article in article_list:
            # print(article)
            title = article.h2.text
            url = article.h2.a.get('href')

            data = {
                'title': title,
                'url': url,
            }
            # print(data)
            data_list.append(data)

        return data_list

    def parse_detail(self, content):
        """
        解析网页内容
        """
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find('div', class_='entry-content')
        data = {}
        # html = soup.prettify("utf-8")
        # print(type(html), html)
        # print(article)
        # print(article.p)

        md_content = self.text_maker.handle(article.prettify("utf-8").decode(encoding="utf-8"))

        data['content'] = md_content

        return data

    def update_detail(self, objs, update_associated_data=False, ):
        """
        更新详情，一般是用用更新导入以后的内容

        :param objs:
        :param update_associated_data: 更新关联数据
        :return:
        """
        infos = []

        return infos

    def process_list_page(self, content):
        """
        采集详情页
        """
        data_list = self.parse_list(content)
        for data in data_list:
            yield data

    def crawl(self, overlay_file=False, max_exist=3):
        """
        爬取内容

        1. 爬取列表内容
        2. 解析列表内容中的详情内容
        3. 添加内容到数据库
        :param overlay_file: 如果文件已经存在是否重新下载
        :param max_exist: 超过最大数量就退出爬取
        :return:
        """

        exist_count = 0

        i = 1
        for page in self.get_urls():
            file = self.save_dir / f'{datetime.now().strftime("%Y-%m-%d %H.%M.%S")} {page.page:05}.html'
            self.log_function(page.url, file)
            if file.exists() and not overlay_file:
                continue
            with open(file, 'wb') as f:
                try:
                    r = self.get(page.url)
                    f.write(r.content)
                    for data in self.process_list_page(r.content):
                        yield data
                except Exception as e:
                    self.log_function(f'错误:{e}')
                    self.errors.append(f'错误:{e}')
            i += 1
            # random_sleep()
            if exist_count >= max_exist:
                break
