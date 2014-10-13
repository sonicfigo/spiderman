#coding=utf-8
import sys
reload(sys)

#解决str(unicode文本)异常问题
#http://blog.csdn.net/sky_qing/article/details/9251735
sys.setdefaultencoding('utf8')