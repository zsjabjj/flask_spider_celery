# -*- coding: utf-8 -*-
import datetime
import calendar
import os
import re

# 正则转换器
from functools import wraps
from threading import Thread

from flask import session, g, jsonify, redirect, url_for
from werkzeug.routing import BaseConverter

from inchange_net import constants
from inchange_net.utils.response_code import RET


# 自定义正则转换器
class RegexConverter(BaseConverter):
    # 重新init方法, 增加参数
    # regex: 就是在使用时, 传入的正则表达式
    def __init__(self, url_map, regex):
        # 调用父类方法
        super(RegexConverter, self).__init__(url_map)
        self.regex = regex

# 自定义检测用户是否登录的装饰器
# 去session中获取数据 id
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # 获取已登录用户的id保存到g变量中, 以便之后使用
        user_id = session.get('user_id')
        if user_id is not None:
            # 表示用户已经登录
            # 使用g对象保存user_id，在视图函数中可以直接使用
            # 比如后面设置头像的时候, 仍然需要获取session的数据.
            # 为了避免多次访问redis服务器. 可以使用g变量
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            # 用户未登录
            resp = {
                "errno": RET.SESSIONERR,
                "errmsg": "用户未登录"
            }
            return jsonify(resp)
            # return redirect(url_for('/sessions'))
    return wrapper

# def async(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         thr = Thread(target=f, args=args, kwargs=kwargs)
#         thr.start()
#     return wrapper

# 获取download和upload文件夹中的文件
def get_files():
    if os.path.exists(constants.UPLOAD_DIR):
        pass
    else:
        os.mkdir(constants.UPLOAD_DIR)
    dirpath_up, dirnames_up, filenames_up = list(os.walk(constants.UPLOAD_DIR))[0]
    dirpath_down, dirnames_down, filenames_down = list(os.walk(constants.DOWNLOAD_DIR))[0]
    filenames = filenames_up + filenames_down
    return filenames

# 文件下载处理
def generate(filename):
    file_name = filename.encode('latin-1').decode()
    try:
        with open(constants.DOWNLOAD_DIR+file_name, "rb+") as r:
            while True:
                chunk_data = r.read()
                if not chunk_data:
                    break
                yield chunk_data
    except:
        with open(constants.UPLOAD_DIR+file_name, "rb+") as r:
            while True:
                chunk_data = r.read()
                if not chunk_data:
                    break
                yield chunk_data

# 爬虫抓取后的存数据的目录树
def getFiles(dir):
    '''目录树'''
    # print(dir)
    dir_tree = dict()
    for dirpath, dirnames, filenames in os.walk(dir):
        # print(dirpath)
        dir_tree[dirpath.split('/')[-1]] = dirnames + filenames
        # print(dir_tree)
    dir_tree['dir_path'] = constants.BASE_DIR
    return dir_tree

# 日期格式判断
def date_judge(date_time):
    '''日期格式判断'''
    __cur = datetime.datetime.now()

    if len(date_time) != 10:
        msg = '日期格式输入有误，请重新输入！'
        # print('日期格式输入有误，请重新输入！')
        return False, msg
    elif '-' not in date_time:
        msg = '日期格式输入有误，请重新输入！'
        # print('格式输入有误，请重新输入！')
        return False, msg
    elif len(date_time.split('-')) != 3:
        msg = '日期格式输入有误，请重新输入！'
        # print('格式输入有误，请重新输入！')
        return False, msg
    else:
        # 判断日期是否超出当前时间
        # cur = datetime.datetime.now()
        # calendar.monthrange(2013, 6)
        # 获取年，月，日
        try:
            Year, Month, Day = re.findall(r'(\d+)-(\d+)-(\d+)', date_time)[0]
        except Exception as e:
            msg = '您输入的日期超出范围或日期有问题，请重新输入！'
            print('您输入的日期超出范围或日期有问题，请重新输入！')
            return False, msg
        # 将年，月，日转成整型，提供后续使用
        try:
            Year = int(Year)
            Month = int(Month)
            Day = int(Day)
        except:
            msg = '日期格式输入有误，请重新输入！'
            # print('格式输入有误，请重新输入！')
            return False, msg
        # 判断输入的年，月，日是否为0
        if not Year * Month * Day:
            msg = '日期输入有误，请重新输入！'
            print('日期输入有误，请重新输入！')
            return False, msg
        else:
            # 某年某月天数，返回是星期（0-6）和天数
            _, days = calendar.monthrange(Year, Month)

            if Year > __cur.year:
                msg = '输入"年"超出范围，请重新输入！'
                print('输入"年"超出范围，请重新输入！')
                return False, msg
            # 当前年，月份超出范围
            elif Year == __cur.year and Month > __cur.month:
                msg = '输入"月"超出范围，请重新输入！'
                print('输入"月"超出范围，请重新输入！')
                return False, msg
            # 过去年，月份超出12
            elif Year < __cur.year and Month > 12:
                msg = '输入"月"超出范围，请重新输入！'
                print('输入"月"超出范围，请重新输入！')
                return False, msg
            # 当前月，天超出范围
            elif Month == __cur.month and Day >= __cur.day:
                msg = '输入"日"超出范围，请重新输入！'
                print('输入"日"超出范围，请重新输入！')
                return False, msg
            # 过去月，天超过天数
            elif Month < __cur.month and Day > days:
                msg = '输入"日"超出范围，请重新输入！'
                print('输入"日"超出范围，请重新输入！')
                return False, msg
            else:
                msg = 'ok'
                print(Year, Month, Day)
                return True, msg

