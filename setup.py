# -*- coding:utf-8 -*-

# Name: setup
# Product_name: PyCharm
# Description:
# Author : 'zhangjiawen'
# Data : 2021/6/9 17:35

from setuptools import setup, find_packages


# python3 setup.py bdist_wheel
setup(
    name='wenyu-common',
    version='1.0.0.dev',
    description='Those common packages used in my python projects',
    url='https://github.com/Wen2yu/python-common',
    author='zhangjiawen',
    author_email='939529834@qq.com',
    packages=find_packages(),
    install_requires=['numpy', 'redis', 'requests', 'SQLAlchemy', 'urllib3']
)
