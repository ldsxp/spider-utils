import re

import requests


def download_file(url, file_name=None):
    """
    下载文件

    :param url:
    :param file_name:
    :return:
    """

    r = requests.get(url, stream=True)
    # print(type(r.headers.get('Content-Disposition')))
    content_disposition = r.headers.get('Content-Disposition')

    if file_name is None:
        if content_disposition and 'attachment; filename="' in content_disposition:
            file_name = content_disposition[22:-1]
        else:
            file_name = url.split('/')[-1]
            file_name = re.sub('[\/:*?"<>|]', '-', file_name)

    file_size = r.headers.get('Content-Length')
    if file_size is None:
        # pprint(r.headers)
        print('文件大小获取失败，%s 不是合法文件......' % file_name)
        return None

    print("开始下载：%s \n文件大小：%s" % (file_name, file_size))

    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    print("%s 下载完成!\n" % file_name)
    return file_name
