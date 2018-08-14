# -*- coding: utf-8 -*-
import logging
import time

from inchange_net import celery
from inchange_net.utils.brand_ratio import BrandRatio


# current_time = str(time.strftime('%Y-%m-%d %H:%M:%S'))

@celery.task(name='panduan')
def panduan(Cookie):
    logging.info('spider start %s' % str(time.strftime('%Y-%m-%d %H:%M:%S')))
    BrandRatio(Cookie).run()
    logging.info('spider start %s' % str(time.strftime('%Y-%m-%d %H:%M:%S')))











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


