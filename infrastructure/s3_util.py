#coding=utf-8
import traceback
from threading import currentThread
import datetime as dtPkg
from datetime import datetime as dtCls
import json
import os

from pytz import timezone
import pytz
import shutil

import s3_global as s3glb


def pickup_numbers(text):
    '''从任意文本中，抽取数字列表'''
    return [int(s) for s in text.split() if s.isdigit()]

def pickup_number(text):
    '''从任意文本中，抽取唯一数字'''
    numbers = [int(s) for s in text.split() if s.isdigit()]
    if len(numbers) == 1:
        return numbers[0]
    else:
        raise ValueError("Not unique number text found in ", text)

#extract 后的文本编码，并去掉前后空格,换行
def clear_text(dirty_unicode):
    return str( dirty_unicode.encode('utf-8') ).strip()

##########################################################################
def utc_now_str():
    return dtCls.utcnow().strftime('%Y-%m-%d %H:%M:%S')

#默认是2014-06-24 13:00格式 每家船公司可能不同,使用date_time_format指定
def parse_time(date_time_text, date_time_format = "%Y-%m-%d %H:%M"):
    if (not date_time_text):
        LogUtil.error("Not date time text can be parse.")
        return None
    else:
        try:
            dt1 = dtCls.strptime(date_time_text, date_time_format)
            return dt1
        except BaseException as ex:
            LogUtil.error('parse_time error,%s' % ex.__str__())
            if date_time_format == "%Y-%m-%d %H:%M":
                return parse_time(date_time_text, date_time_format="%Y-%m-%d")  # 优化逻辑一下,太乱
            raise  # todo 怎样记录完整的trace

def parse_utc_time(date_time_text, date_time_format, from_timezone='UTC'):
    '''解析前台传入的时间字符串,生成UTC时间.
    from_timezone: 时区名，来自抓取的网站(参考pytz.common_timezones).
    默认为'UTC'时（pytz无北京时，使用时用上海时间代替）.

    '''
    if (not date_time_text):
        return None
    else:
        try:
            dtCls_from_parse = dtCls.strptime(date_time_text,
                                              date_time_format)
            if (from_timezone == 'UTC'):
                return dtCls_from_parse

            tz_assigned = timezone(from_timezone)
            time_assigned = tz_assigned.localize(dtCls_from_parse)
            return time_assigned.astimezone(pytz.UTC)
        except BaseException as ex:
            LogUtil.error('parse_utc_time error,%s' % ex.__str__())
            return None


def now_str(dt_format='%Y-%m-%d-%H_%M_%S_%f'):
    dt_str = dtCls.strftime(dtCls.now(), dt_format)
    return dt_str


def add_utcnow_days(days):
    return dtCls.utcnow() + dtPkg.timedelta(days)

##########################################################################
def first_in_list(iterable, length_limit=0, default=None):
    '''获取列表中的第一个元素，
    若列表为空，则通过default参数设置返回值，默认为None
    通过length_limit限制列表长度，默认为0
    若超过长度也认为不符合预期，返回default
    '''
    return iterable[0] if iterable and \
        (len(iterable) > length_limit or length_limit == 0) else default


def search_key_by_value(dict_instance, search_value):
    for (key, value) in dict_instance.items():
        if value == search_value:
            return key
    raise ValueError("Can't find value %s." % search_value)

#def find_key(dic, val):
    #"""return the key of dictionary dic given the value"""
    #return [k for k, v in symbol_dic.iteritems() if v == val][0]

##########################################################################
# File Mode list in s3_util_fileop_test.py

def file_exists(file_path):
    return os.path.exists(file_path)


def open_file(file_path, mode='w'):
    '''Open file, make sure file.close() at the end. '''
    if file_exists(file_path):
        raise IOError(file_path + ' already exist.')
    file1 = open(file_path, mode)
    return file1


def open_file_overwritten(file_path, mode='w'):
    overwrite = False
    if file_exists(file_path):
        overwrite = True

    file1 = open(file_path, mode)

    if overwrite:
        LogUtil.warning(file_path +' exist, but open overwritten.')

    return file1


def create_file(file_path, content, mode='w'):
    '''create file, raise IOError if file exist.'''
    file1 = open_file(file_path, mode)
    file1.write(content)
    file1.close()


def create_file_overwritten(file_path, content, mode='w'):
    '''create file, overwritten original file if exist.'''
    file1 = open_file_overwritten(file_path, mode)
    file1.write(content)
    file1.close()


def insure_dir_exist(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def copy_file_to(source_path, target_path):
    if not file_exists(source_path):
        raise IOError(source_path + ' doesn\'t exist.')
    else:
        shutil.copyfile(source_path, target_path)


def read_file(file_path):
    if not file_exists(file_path):
        raise IOError(file_path + ' doesn\'t exist.')
    try:
        file1 = open(file_path, 'U')  # 只读打开
        content = file1.read()
    finally:
        file1.close()
    return content


def delete_file(file_path):
    if not file_exists(file_path):
        return
    else:
        os.remove(file_path)


def rename_file(old, new):
    os.rename(old, new)

##########################################################################
class S3JsonEncoder(json.JSONEncoder):  # object 序列化成 json串（中间先转为dictionary过渡）

    def default(self, obj):  # convert object to a dict

        dic_var = {}
        dic_var['__class__'] = obj.__class__.__name__
        dic_var['__module__'] = obj.__module__
        dic_var.update(obj.__dict__)
        return dic_var

# decode 后的true 会自动转为 boolean 的True
class S3JsonDecoder(json.JSONDecoder):  # json串反序列化成object (dict的过渡，json框架自动完成)
    def __init__(self):
        try:
            json.JSONDecoder.__init__(self, object_hook=self.dict2object)
        except BaseException as ex:
            LogUtil.error("JsonDecoder initial error: %s" % ex.__str__())

    def dict2object(self, dict_var):  # convert dict to object

        if '__class__' in dict_var:
            class_name = dict_var.pop('__class__')
            module_name = dict_var.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict((key.encode('ascii'), value)
                        for key, value in dict_var.items())  # get args
            inst = class_(**args)  # create new instance
        else:
            inst = dict_var
        return inst

_DECODER = S3JsonDecoder()


def decode(json_str):
    return _DECODER.decode(json_str)


##########################################################################
import logging
import logging.config
import logging.handlers
from logging.handlers import RotatingFileHandler

from scrapy import log

class LogUtil(object):
    system_name = "s3shell"

    @classmethod  #还未找到python的静态构造函数 写法
    #def _initial(cls):
    #def _initial(cls, log_path = os.path.join(os.getcwd(), s3glb.S3LOG_FILE)):
    def _initial(cls):
        logger_name = 's3log'
        if hasattr(cls, 'logger_customer'):
            return
        
        if not file_exists(s3glb.S3LOG_CONFIG):
            msg = ("log config file %s miss!" % s3glb.S3LOG_CONFIG)
            raise IOError(msg)

        logging.config.fileConfig(s3glb.S3LOG_CONFIG)
        cls.logger_customer = logging.getLogger(logger_name)
        
        if cls.logger_customer.handlers.count < 1:
            print 'No any handlers defined, check %s' % \
                  s3glb.S3LOG_CONFIG
        else:
            print 
        
        file_path = cls.logger_customer.handlers[0].baseFilename
        msg = "********************************************\r\n" + \
        "LogUtil.initial() [config]%s, \r\n" + \
        "[file ]%s,\r\n" + \
        "[level] %s, \r\n" + \
        "[scrapyd log] %s, \r\n" + \
        "[maxBytes] %s.\r\n"
        msg = msg % (s3glb.S3LOG_CONFIG,
                     file_path,
                     logging.getLevelName(cls.logger_customer.level),
                     "NA", 
                     cls.logger_customer.handlers[0].maxBytes)
        cls.logger_customer.critical(msg)
        print msg
        
    @classmethod
    def _add_hanlder(cls, log_file_path, max_size_bytes):
        handler = logging.handlers.RotatingFileHandler(
                      log_file_path, maxBytes = max_size_bytes,
                      backupCount=5)
        cls.logger_customer.addHandler(handler)
    @classmethod
    def _now(cls):
        return now_str(dt_format='%Y-%m-%d %H:%M:%S')

    @classmethod
    def debug(cls, msg):
        cls._initial()
        cls.logger_customer.debug(msg)
        print '[S3-DEBUG]', cls._now(), '-', msg

    @classmethod
    def info(cls, msg):
        cls._initial()
        cls.logger_customer.info(msg)
        print '[S3-INFO]', cls._now(), '-', msg

    @classmethod
    def warning(cls, msg):
        cls._initial()
        cls.logger_customer.warning(msg)
        print '[S3-WARN]', cls._now(), '-', msg

    @classmethod
    def error(cls, msg):
        cls._initial()
        cls.logger_customer.error(msg)
        _log_err_scrapyd(msg)
        print '[S3-ERRO]', cls._now(), '-', msg

    @classmethod
    def critical(cls, msg):
        cls._initial()
        cls.logger_customer.critical(msg)
        print '[S3-CRITICAL]', cls._now(), '-', msg

    @classmethod
    def log_ex(cls, msg = ""):
        cls._initial()
        trace_back_info = traceback.format_exc()
        #todo  这不够，无法纪录到外层调用者信息
        LogUtil.error("%s, Error trace info is:%s" % (msg, trace_back_info))

def _log_err_scrapyd(msg):
    '''记录error到scrapyd日志，在http://localhost:6800/jobs可查阅'''
    log.err(_stuff=msg+"[from s3_logutil]", system=LogUtil.system_name)

def assert_eq(obj1, obj2, err_msg='.'):
    '''Assertion util, assert_equal.'''
    if (obj1 != obj2):
        raise AssertionError('S3-AssertionError: %s != %s' % (obj1, obj2),
                             err_msg)


##########################################################################
def hanlde_s3ex(s3error):
    if not hasattr(s3error, 'policy'):
        LogUtil.error(s3error.__str__())
    else:
        if s3error.policy == 'LogAndMail':
            pass


def dom_insure(spider_name):
    '''
    确认某个spider执行时，抓取到正确的dom节点
    监控使用
    '''
    pass



