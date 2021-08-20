#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import setuptools
import EpubCrawler

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="EpubCrawler",
    version=EpubCrawler.__version__,
    url="https://github.com/apachecn/epub-crawler",
    author=EpubCrawler.__author__,
    author_email=EpubCrawler.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
    ],
    description="EpubCrawler，用于抓取网页内容并制作 EPUB 的小工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "ebook",
        "epub",
        "crawler",
        "爬虫",
        "电子书",
    ],
    install_requires=install_requires,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "crawl-epub=EpubCrawler.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
)
