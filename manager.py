# -*- coding: utf-8 -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from inchange_net import create_app
# import sys
# print sys.argv[2]
# 根据传递参数决定程序运行环境
app, db = create_app('develop')
# 为了管理程序的启动
manager = Manager(app)
# 对数据库的操作
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    manager.run()
