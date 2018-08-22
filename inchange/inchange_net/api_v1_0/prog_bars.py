import logging

from flask import render_template, jsonify

# from config import SESSION_REDIS
from inchange_net import redis_store
from inchange_net.api_v1_0 import api
from inchange_net.utils.common import login_required
from inchange_net.utils.response_code import RET


mideaList = list()
tamllList = list()


@api.route('/tmalls', methods=['GET',])
def tmalls():
    '''猫超进度条'''

    i = 100 if 'tmall采集完成请导出' == redis_store.lindex("tmall", -1).decode('utf-8') else redis_store.llen('tmall') * 100 // 1600
    # logging.info(i)
    if i <= 100:
        return jsonify(time=i)
    elif i > 100:
        return jsonify(time=RET.DATAERR)

@api.route('/sanyos', methods=['GET',])
def sanyos():
    '''三洋进度条'''
    # logging.info('in sanyos')
    # logging.info(redis_store.llen('sanyo'))
    # logging.info(redis_store.lindex("sanyo", -1))
    i = 100 if 'ratio采集完成请导出' == redis_store.lindex("sanyo", -1).decode('utf-8') else redis_store.llen('sanyo') * 100 // 40
    # logging.info(i)
    if i <= 100:
        return jsonify(time=i)
    elif i > 100:
        return jsonify(time=RET.DATAERR)
    # sanyoList = list()

@api.route('/mideas', methods=['GET',])
def mideas():
    '''美的进度条'''

    # logging.info('in mideas')
    # logging.info(redis_store.llen('midea'))
    # logging.info(redis_store.lindex("midea", -1))
    i = 100 if 'midea采集完成请导出' == redis_store.lindex("midea", -1).decode('utf-8') else redis_store.llen(
        'midea') * 100 // 13
    # logging.info(i)
    if i <= 100:
        return jsonify(time=i)
    elif i > 100:
        return jsonify(time=RET.DATAERR)

