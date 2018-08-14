# -*- coding: utf-8 -*-
from flask import render_template

from inchange_net.api_v1_0 import api


@api.route('/', methods=['GET',])
def zy():
    return render_template('index.html')