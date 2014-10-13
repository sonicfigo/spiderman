======
spiderman
======

This is a python project to scrape websites from public web directories such as http://www.cnbeta.com
这是一个python项目，用于抓取web页面。

Items
=====

The items scraped by this project are websites, and the item is defined in the
抓取的结果在以下类进行定义。
class::

    core.items.RealTimeMainItem
    core.items.RealTimeDetailItem

See the source code for more details.

Spiders
=======
目前该项目包含一个spider ``cb_realtime``，可以通过以下命令查看所有的spider
Fow now,this project contains one spider called ``cb_realtime`` that you can see by running::

    scrapy list

Spider: cb_realtime
------------
``cb_realtime`` spider 抓取www.CnBeta.com 的 '实时更新' 栏目.

运行蜘蛛使用以下命令::
python main.py crawl cb_realtime

Pipelines
=========

This project uses a pipeline to filter out websites containing certain
forbidden words in their description. This pipeline is defined in the class::

    dirbot.pipelines.FilterWordsPipeline
