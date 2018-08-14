# -*- coding: utf-8 -*-
from celery_tasks import make_celery
from inchange_net.utils.brand_ratio import BrandRatio
from manager import app

celery = make_celery(app)
app.extensions['celery'] = celery

@celery.task
def panduan(COOKIE):
    BrandRatio(COOKIE).run()

# if __name__ == '__main__':
#     app.run()


