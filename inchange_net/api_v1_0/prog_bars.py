import logging

from flask import render_template, jsonify

# from config import SESSION_REDIS
from inchange_net import redis_store
from inchange_net.api_v1_0 import api
from inchange_net.utils.common import login_required
from inchange_net.utils.response_code import RET
from inchange_net.api_v1_0.spider_index import panduan

mideaList = list()
tamllList = list()


@api.route('/tmalls', methods=['GET',])
def tmalls():
    '''猫超进度条'''
    
    global tamllList

    for i in range(len(tamllList), 150):
        tamllList.append(i)

        i = len(tamllList)* 100 // 150

        return jsonify(time=i)
    tamllList = list()

@api.route('/sanyos', methods=['GET',])
def sanyos():
    '''三洋进度条'''
    logging.info('in sanyos')
    logging.info(redis_store.llen('sanyo'))
    logging.info(redis_store.lindex("sanyo", -1))
    i = 100 if 'ratio采集完成请导出' == redis_store.lindex("sanyo", -1).decode('utf-8') else redis_store.llen('sanyo') * 100 // 40
    logging.info(i)
    if i <= 100:
        return jsonify(time=i)
    elif i > 100:
        return jsonify(time=RET.DATAERR)
    # sanyoList = list()

@api.route('/mideas', methods=['GET',])
def mideas():
    '''美的进度条'''
    
    global mideaList

    for i in range(len(mideaList), 30):
        mideaList.append(i)

        i = len(mideaList)* 100 // 30

        return jsonify(time=i)
    mideaList = list()