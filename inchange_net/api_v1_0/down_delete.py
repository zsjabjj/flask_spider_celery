# -*- coding: utf-8 -*-
import os

from flask import Response, stream_with_context, redirect, url_for

from inchange_net import constants
from inchange_net.api_v1_0 import api
from inchange_net.utils.common import login_required, generate


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

