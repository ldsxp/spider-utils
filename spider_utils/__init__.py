"""
路径和网址 url 互相转换

from urllib.request import pathname2url
from urllib.request import url2pathname
str2 = parse.quote(str1)  # url 编码
str3 = parse.unquote(str2)  # url 解码
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from .utils import (  # noqa
    random_sleep,
    url_to_dict,
    get_cookie_dict,
)

from .download import (  # noqa
    download,
    download_progress,
)

from .spider import (  # noqa
    get_response,
    requests_retry_session,
    get_response_to_file,
)

from .useragent import get_user_agent  # noqa
