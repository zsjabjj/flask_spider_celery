# -*- coding: utf-8 -*-
import logging
import os

from flask import Response, stream_with_context, redirect, url_for, send_from_directory, make_response

from inchange_net import constants
from inchange_net.api_v1_0 import api
from inchange_net.utils.common import login_required, generate, generates


@api.route('/download/<string:filename>', methods=['GET',])
def download(filename):  # 所有分片均上传完后被调用
    # print(filename)
    file_name = filename.encode().decode('latin-1')
    response = Response(stream_with_context(generate(file_name)))
    response.headers['Content-Disposition'] = "attachment; filename={0}".format(file_name)
    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Length'] = 20 * 1024 * 1024
    return response

@api.route('/delete/<string:filename>', methods=['GET',])
def delete(filename):  # 所有分片均上传完后被调用
    try:
        os.remove(constants.DOWNLOAD_DIR + filename)
    except:
        os.remove(constants.UPLOAD_DIR + filename)
    return redirect('hello.html')

@api.route('/downloads/<path:dir_path>/<string:filename>')
def downloads(dir_path, filename):
    dir_path = os.sep + dir_path + os.sep
    logging.info(dir_path)
    logging.info(filename)
    logging.info(os.getcwd())
    # return send_from_directory(dir_path, filename, as_attachment=True)
    # response = make_response(send_from_directory(dir_path, filename, as_attachment=True, mimetype='application/octet-stream'))
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    # logging.info('1')
    # return response

    file_name = filename.encode().decode('latin-1')
    logging.info(file_name)
    response = Response(stream_with_context(generates(dir_path, file_name)))
    response.headers['Content-Disposition'] = "attachment; filename={0}".format(file_name)
    response.headers['Content-Type'] = "application/octet-stream"
    response.headers['Content-Length'] = 20 * 1024 * 1024
    return response

