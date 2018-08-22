# -*- coding: utf-8 -*-
# 创建APP用的
import logging
from logging.handlers import RotatingFileHandler

import redis
from celery import Celery

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_dict, Config
# from flask_wtf.csrf import CSRFProtect
# from flask_session import Session
from inchange_net.utils.common import RegexConverter

# 将参数延后传入的技巧
# 问题抛出: 有些对象, 外界需要应用. 但是这个对象又必须在app创建之后
# 解决方案: 可以先创建该对象, 在app创建之后, 再设置app


app = Flask(__name__)

db = SQLAlchemy()

# csrf = CSRFProtect()

# redis_store = None

pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, decode_responses=True)
redis_store = redis.Redis(connection_pool=pool)


celery_task = Celery('celery_tasks.tasks', broker=Config.CELERY_BROKER_URL,backend=Config.CELERY_RESULT_BACKEND)


# 项目日志
'''
日志的级别
ERROR: 错误级别
WARN: 警告级别
INFO: 信息界别
DEBUG: 调试级别

平时开发, 可以使用debug和info替代print, 来查看对象的值
上线时, 不需要删除这个日志, 只需要更改日志的级别为error/warn
'''
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器, 指明日志保存的路径, 每个日志文件的最大大小, 保存的日志文件个数上限
file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名  行数       日志信息
formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象(flask app使用的) 添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 提供一个函数来创建app, 同时提供参数, 让外界传入
def create_app(config_name):

    # 管理app的创建
    app = Flask(__name__)

    # 导入配置参数
    app.config.from_object(config_dict[config_name])

    # Celery configuration
    # app.config['CELERY_BROKER_URL'] = 'redis://{}:{}/{}'.format(Config.REDIS_HOST, Config.REDIS_PORT, Config.REDIS_DB)
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://{}:{}/{}'.format(Config.REDIS_HOST, Config.REDIS_PORT, Config.REDIS_DB)

    # Initialize Celery
    # celery = Celery('manager.celery', broker='redis://{}:{}/{}'.format(Config.REDIS_HOST, Config.REDIS_PORT, Config.REDIS_DB))
    # celery.conf.update(app.config)

    # app.config.update(
    #     CELERY_BROKER_URL='redis://localhost:6379/10',
    #     CELERY_RESULT_BACKEND='redis://localhost:6379/10'
    # )
    # celery = make_celery(app)



    # 创建数据库
    db.init_app(app)

    global redis_store
    # redis, 最优方式是将参数写到配置文件
    # pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, decode_responses=True)
    # redis_store = redis.Redis(connection_pool=pool)
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)

    # 给app的路由转换器字典增加我们自定义的转换器
    app.url_map.converters['re'] = RegexConverter

    # csrf保护
    # 用postman测试时, 需要暂时关闭csrf保护
    # 不然会报错: The CSRF token is missing
    # csrf.init_app(app)

    # Session
    # 创建能够将默认存放在cookie的sesion数据, 转移到redis的对象
    # http://pythonhosted.org/Flask-Session/
    # Session(app)
    # celery.conf.update(app.config)
    celery_task.conf.update(app.config)
    # from flask_bootstrap import Bootstrap
    # Bootstrap(app)

    # 注册蓝图
    # 为了解决循环导入的问题, 需要将蓝图的导入延后导入.
    # url_prefix访问地址前添加的前缀
    from inchange_net.api_v1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1_0')

    from celery_tasks import celery_tasks as celery_task_blueprint
    app.register_blueprint(celery_task_blueprint)

    from inchange_net import web_html
    app.register_blueprint(web_html.static_html)


    return app, db
