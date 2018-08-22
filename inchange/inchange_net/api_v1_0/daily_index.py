# -*- coding: utf-8 -*-
import os
import logging

from flask import request, render_template, jsonify
from inchange_net.api_v1_0 import api
from inchange_net import constants
from inchange_net.utils.common import login_required, get_files
from inchange_net.utils.gmv import sale_gmv
from inchange_net.utils.response_code import RET
from inchange_net.utils.write_xlsx import save_another


# 暂存文件列表
FILE_SET = set()


@api.route('/dailys', methods=['GET', 'POST'])
def daily_index():  # 一个分片上传后被调用
    '''日报处理首页'''
    # post请求处理
    if request.method == 'POST':
        logging.info(request.form)  
        upload_file = request.files['file']
        task = request.form.get('task_id')  # 获取文件唯一标识符
        chunk = request.form.get('chunk', 0)  # 获取该分片在所有分片中的序号
        # up_filename = request.form.get('name')  # 获取上传文件的名称

        if os.path.exists(constants.TEMP_DIR):
            pass
        else:
            os.mkdir(constants.TEMP_DIR)
        filename = constants.TEMP_DIR + '%s%s' % (task, chunk)  # 构成该分片唯一标识符
        upload_file.save(filename)  # 保存分片到本地

    return jsonify(status=RET.OK, files=get_files())
    # return render_template('hello.html', dir='', files=get_files())


@api.route('/success', methods=['GET'])
def upload_success(chunk=0):  # 所有分片均上传完后被调用
    global FILE_SET
    task = request.args.get('task_id')
    name = request.args.get('name')
    logging.info(name)
    # if 6 == len(FILE_SET):
    #     pass
    # else:
    FILE_SET.add(name)
    upload_filename = constants.UPLOAD_DIR + name
    logging.info(request.form)
    with open(constants.UPLOAD_DIR + '%s' % name, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = constants.TEMP_DIR + '%s%d' % (task, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
                chunk += 1
                os.remove(filename)  # 删除该分片，节约空间
            except IOError:
                break

    if '荣事达官旗2.csv' == name:
        pass
    else:
        save_another(upload_filename, constants.DOWNLOAD_DIR)
    if 6 == len(FILE_SET):
        logging.info('-' * 30)
        logging.info(len(FILE_SET))
        logging.info(FILE_SET)
        sale_gmv(FILE_SET, constants.UPLOAD_DIR, constants.DOWNLOAD_DIR)
        FILE_SET = set()
        logging.info('=' * 30)
    return jsonify(errno=0, files=get_files())
    # return render_template('hello.html', dir=constants.UPLOAD_DIR, files=get_files())


# if __name__ == '__main__':
#     app.secret_key = "packet"
#     app.run(debug=True, host='0.0.0.0', port=9001)
