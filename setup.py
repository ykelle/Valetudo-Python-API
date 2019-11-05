#!/usr/bin/env python3
from setuptools import setup

setup(
    name='valetudo',
    version='1.0',
    description='Python lib to control Mi vacuum robot with valetudo installed',
    author='Yannick Keller',
    url='https://github.com/ykelle/Valetudo-Python-API',
    py_modules=['valetudo'],
    license='MIT',
    zip_safe=False,
    install_requires=['requests'],
)