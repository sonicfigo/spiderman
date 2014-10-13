======
spiderman
======

This is a python project to scrape websites from public web directories such as http://www.cnbeta.com
这是一个python项目，用于抓取web页面。

安装
======
Python 版本2.7.6
Pip https://pypi.python.org/pypi/pip

Python包 Scrapy(使用pip安装):
	
	pip install scrapy

Spiders
=======
目前该项目包含一个spider ``cb_realtime``，可以通过以下命令查看所有的spider
Fow now,this project contains one spider called ``cb_realtime`` that you can see by running::

    scrapy list

Spider: cb_realtime
------------
``cb_realtime`` spider 抓取www.CnBeta.com 的 '实时更新' 栏目.

运行蜘蛛使用以下命令
	
	python main.py crawl cb_realtime

如果需要保存页面用于查看
	
	python main.py crawl cb_realtime -a SAVE_HTMLFILE=1

抓取结果Items
=====

The items scraped by this project are websites, and the item is defined in the
抓取的结果在以下类进行定义。

    core.items.RealTimeMainItem
    core.items.RealTimeDetailItem
    
抓取结果目录
=========
在目录crawl_data/cb_realtime 查看
配置于 settings.py的

    FEED_URI = 'file:./crawl_data/%(name)s/item%(time)s.json'

Pipelines
=========

This project uses a pipeline to filter out websites containing certain
forbidden words in their description. This pipeline is defined in the class::

    dirbot.pipelines.FilterWordsPipeline
