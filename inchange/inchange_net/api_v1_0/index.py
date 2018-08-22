# -*- coding: utf-8 -*-
from flask import render_template, jsonify

from inchange_net.api_v1_0 import api


@api.route('/index', methods=['GET',])
def zy():
    # return jsonify({"test": "test"})
    return render_template('index.html')
