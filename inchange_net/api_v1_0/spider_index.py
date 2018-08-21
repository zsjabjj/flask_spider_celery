# -*- coding: utf-8 -*-
import logging

from flask import render_template, request, jsonify

from inchange_net import constants, redis_store
from inchange_net.api_v1_0 import api
from inchange_net.utils.common import getFiles, date_judge

# cookie值保存
from inchange_net.utils.response_code import RET
# from manager import panduan
from celery_tasks.tasks import sanyo_spider, midea_spider, tmall_spider

COOKIE = ''
date_type = ''
partnerName = ''
date_time = ''

# @celery.task
# def panduan():
#     BrandRatio(COOKIE).run()

# 猫超进度条页面
@api.route('/partners/tmall', methods=['GET',])
def tmall():
    '''异步spider'''
    tmall_spider.delay(COOKIE, date_time, date_type)
    if redis_store.exists('tmall'):
        return jsonify(status=RET.OK, partner='猫超')
    else:
        return jsonify(status=RET.NODATA)

# 三洋进度条页面
@api.route('/partners/sanyo', methods=['GET',])
def sanyo():
    '''异步spider'''
    sanyo_spider.delay(COOKIE, date_time, date_type)
    if redis_store.exists('sanyo'):
        return jsonify(status=RET.OK, partner='三洋')
    else:
        return jsonify(status=RET.NODATA)


# 美的进度条页面
@api.route('/partners/midea', methods=['GET',])
def midea():
    '''异步spider'''
    midea_spider.delay(COOKIE, date_time, date_type)
    if redis_store.exists('midea'):
        return jsonify(status=RET.OK, partner='美的')
    else:
        return jsonify(status=RET.NODATA)


@api.route('/spiders', methods=['GET', 'POST'])
def spider_index():
    '''首页'''
    global COOKIE
    global date_type
    global date_time
    # 1. 判断请求方式是post
    if request.method == 'POST':
        # 接收ajax发送的数据
        data_dict = request.get_json()
        # 提取数据
        # 合作商名
        partner_name = data_dict.get('partner_name')
        # cookie
        cookie = data_dict.get('cookie')
        # 时间类型
        dateType = data_dict.get('dateType')
        # 日期
        dateTime = data_dict.get('dateTime')

        # 判断手动输入的时间格式
        if 'day' == dateType:
            if not dateTime:

                return jsonify(status=RET.DATAERR, msg='日期不能为空，请输入日期')
            else:
                status, msg = date_judge(dateTime)

                if not status:

                    return jsonify(status=RET.DATAERR, msg=msg)
        
        # 判断合作商和cookie是否都有
        if not partner_name and not cookie:

            return jsonify(status=RET.DATAERR, msg='请选择合作商，并且输入cookie')
		
        # 判断合作商是否有
        elif not partner_name:

            return jsonify(status=RET.DATAERR, msg='请选择合作商')
			

        # 判断cookie是否有
        elif not cookie:
            
            return jsonify(status=RET.DATAERR, msg='请输入cookie')

        # 没有问题就返回'success'，跳转对应进度条页面
        else:
            COOKIE = cookie
            date_type = dateType
            date_time = dateTime
            logging.info(COOKIE)
            return jsonify(status=RET.OK, msg=partner_name)
	
    # get请求返回首页
    # return render_template('spider_index.html')

# 爬取的数据下载页
@api.route('/downpages', methods=['POST',])
def down_page():
    '''显示文件下载页'''
    global partnerName
    if request.method == 'POST':
        data_dict = request.get_json()
        # print(data_dict)
        partnerName = data_dict.get('partner')
        # if '三洋' == partnerName:
        #     pass
        # elif '美的' == partnerName:
        #     pass
        # elif '猫超' == partnerName:
        #     pass
        # print('-----------', partner_name)
        return jsonify(msg=1)

# 文件列表获取
@api.route('/getFiles', methods=['POST',])
def get_file():
    '''获取文件列表'''
    global partnerName
    if request.method == 'POST':
        # print('==========', partner_name)
        return jsonify(part=partnerName, fileList=getFiles(constants.BASE_DIR + "/datas/Data"))



