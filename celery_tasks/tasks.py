# -*- coding: utf-8 -*-

from inchange_net import celery_task
from inchange_net.utils.midea.mideaSpider import MideaSpider
from inchange_net.utils.midea.save_midea import SaveMidea
from inchange_net.utils.sanyo.brand_ratio import BrandRatio
from inchange_net.utils.sanyo.save_ratio import SaveRatio
from inchange_net.utils.tmall.tmallSpider import TmallSpider


@celery_task.task(name='sanyo_spider')
def sanyo_spider(Cookie, date_time, date_type):
    '''三洋数据抓取and存储'''
    file_list = BrandRatio(Cookie, date_time, date_type).run()
    SaveRatio(date_time).save_ratio_data(file_list)

@celery_task.task(name='tmall_spider')
def tmall_spider(Cookie, date_time, date_type):
    '''tmall数据抓取and存储'''
    TmallSpider(Cookie, date_time, date_type).run()
    pass

@celery_task.task(name='midea_spider')
def midea_spider(Cookie, date_time, date_type):
    '''midea数据抓取and存储'''
    file_list = MideaSpider(Cookie, date_time, date_type).run()
    SaveMidea(date_time).save_midea_data(file_list)













# from celery_tasks import make_celery
# from inchange_net.utils.brand_ratio import BrandRatio
# from manager import app

# celery = make_celery(app)
# app.extensions['celery'] = celery

# @celery.task
# def panduan(COOKIE):
#     BrandRatio(COOKIE).run()

# if __name__ == '__main__':
#     app.run()


