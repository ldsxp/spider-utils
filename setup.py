﻿import os
import sys

from pypandoc import convert
from setuptools import setup, find_packages

version = '0.0.7'

"""
pip install -U spider-utils
pip --no-cache-dir install -U spider-utils

# 检查错误
# twine check dist/*

echo 使用 twine 上传到官方的pip服务器:
echo 在系统添加 TWINE_USERNAME 和 TWINE_PASSWORD 变量，不用输入用户名和密码
rmdir /S/Q build
rmdir /S/Q dist
python setup.py sdist bdist_wheel
echo 上传到PyPI:
twine upload dist/*

"""

# twine upload dist/* 使用 twine 上传
# 添加上传到 PyPI 的命令
if sys.argv[-1] == 'up':
    # os.system('rm -rf dist')
    # os.system('rm -rf build')
    os.system('rmdir /S/Q build')
    os.system('rmdir /S/Q dist')
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine check dist/*')
    os.system('twine upload dist/*')
    sys.exit()

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    # 名称
    name="spider-utils",
    # 版本
    version=version,
    # version=".".join(map(str, __import__('html2text').__version__)),
    # 关键字列表
    keywords=("spider", "utils"),
    # 简单描述
    description="常用爬虫模块的集合，为了多平台，多电脑调用方便!",
    # 详细描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    # 授权信息
    license="GNU GPL 3",

    # 官网地址
    url="https://github.com/ldsxp/spider-utils",
    # 程序的下载地址
    download_url="https://pypi.org/project/spider-utils",
    # 作者
    author="lds",
    # 作者的邮箱地址
    author_email="85176878@qq.com",

    # 需要处理的包目录（包含__init__.py的文件夹）
    packages=find_packages('.', exclude=['tests', 'tests.*']),
    # 软件平台列表
    platforms="any",
    # 所属分类列表
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    # 需要安装的依赖包
    install_requires=[
        'requests',
        'fake_useragent',
        'tqdm',
    ],
    # data_files=[('', ['spider_utils/data/fake_useragent_0.1.11.json', 'spider_utils/data/mobile_user_agents.txt', ])],
    include_package_data=True,
    extras_require={'dev': ['wheel', 'twine', ]},
    python_requires='>=3.6',

    zip_safe=False
)
