import os
import re
from urllib.request import urlopen

from tqdm import tqdm
import requests


def download(url, dst, resume=True, **kwargs):
    """
    下载文件，支持下载续传（没有进度条）

    :param url: 下载文件的网址
    :param dst: 文件的保存路径
    :param resume: 是否需要下载续传
    :param kwargs:
    :return:
    """

    # 下载续传
    if resume:
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst)
        else:
            first_byte = 0
        file_size = int(urlopen(url).info().get('Content-Length', -1))

        if first_byte >= file_size:
            return file_size

        if 'headers' in kwargs:
            kwargs['headers']['Range'] = 'bytes=%s-%s' % (first_byte, file_size)
        else:
            kwargs['headers'] = {'Range': 'bytes=%s-%s' % (first_byte, file_size)}

    kwargs['stream'] = True

    req = requests.get(url, **kwargs)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return int(req.headers['content-length'])


def download_progress(url, dst, resume=True, **kwargs):
    """
    下载文件，支持下载续传和进度条

    :param url: 下载文件的网址
    :param dst: 文件的保存路径
    :param resume: 是否需要下载续传
    :param kwargs:
    :return:
    """
    first_byte = 0
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    # 下载续传
    if resume:
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst)

        if first_byte >= file_size:
            return file_size

        if 'headers' in kwargs:
            kwargs['headers']['Range'] = 'bytes=%s-%s' % (first_byte, file_size)
        else:
            kwargs['headers'] = {'Range': 'bytes=%s-%s' % (first_byte, file_size)}

    kwargs['stream'] = True

    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1]
    )

    req = requests.get(url, **kwargs)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()

    return file_size
