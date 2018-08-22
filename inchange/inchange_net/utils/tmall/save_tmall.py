# -*- coding: utf-8 -*-
import datetime
import logging
import os

import xlsxwriter

from inchange_net import redis_store, constants
from inchange_net.utils.DateRangeAndTimeStamp import dir_time
from inchange_net.utils.format_style import xlsx_style


class SaveTmall(object):
    '''数据处理：曲线走势和流量数据'''
    trend_colname = [
        '品类',
        '品牌/型号',
        '日期',
        '支付转化率',
        '支付子订单数',
        '支付件数',
    ]

    trend_col = [
        'device_category',
        'bm',
        'date_time',
        'payByrRateIndex',
        'payOrdCnt',
        'payItemQty',
    ]

    srcflow_col = [
        '品类',
        '品牌',
        '型号',
        '商品ID',
        '天猫搜索',
        '淘宝搜索',
        '直接访问',
        '淘宝站内其他',
        '购物车',
        '淘宝客',
        '聚划算',
        '淘宝其他店铺',
        '淘宝首页',
        '已买到商品',
        '其他',
        '淘宝类目',
        '淘外流量其他',
        '天猫首页',
        '我的淘宝首页',
        '淘内免费其他',
        '手淘首页',
        '手淘搜索',
        '淘宝客',
        '手淘品牌街',
        '购物车',
        '我的淘宝',
        '手淘问大家',
        '猫客搜索',
        '猫客首页',
        '手淘其他店铺商品详情',
        'WAP天猫',
        '手淘找相似',
        '猫客天猫超市',
        '聚划算',
        '手淘消息中心',
        '手淘拍立淘',
        '直接访问',
        '手淘其他店铺',
        '手淘扫一扫',
        '手淘我的评价',
        '手淘微淘',
        '直通车',
        '手淘淘抢购',
    ]

    srcflow_colname = [
        'device_category',
        'brandName',
        'modelName',
        'itemId',
        'pc',
        'pc_uv',
        'wifi',
        'wifi_uv',
    ]

    def __init__(self, date_time):
        '''初始化文件'''

        # 获取到指定日期
        self.date_time = date_time
        # 判断指定日期是否是手动输入
        if self.date_time:
            pass
        else:
            self.date_time = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%m月%d日')
        # 获取所需的年月日
        Year, Month, Day, year_t, month_t, day_t = dir_time()
        # 设置存储目录
        # 前一天
        # tmallDir_y = '{tmall_dir}tmall_{year}/tmall_{month}/tmall_{day}/'.format(tmall_dir=constants.TMALL_DIR, year=Year, month=Year + Month, day=Year + Month + Day)
        # 今天
        tmallDir_t = '{tmall_dir}tmall_{year}/tmall_{month}/tmall_{day}/'.format(tmall_dir=constants.TMALL_DIR, year=year_t, month=year_t + month_t, day=year_t + month_t + day_t)
        # 判断文件夹是否存在
        # if os.path.exists(tmallDir_y):
        #     pass
        # else:
        #     # os.mkdir(sanyoDir_y)
        #     os.makedirs(tmallDir_y)

        if os.path.exists(tmallDir_t):
            pass
        else:
            # os.mkdir(sanyoDir_t)
            os.makedirs(tmallDir_t)

        # folder = './ctmall/ctmall_%s/' % datetime.datetime.now().strftime("%Y%m%d")
        # if os.path.exists(folder):
        #     print('exists')
        # else:
        #     os.mkdir(folder)
        #
        # logging.info('start write Trend')
        # filename_trend = folder + 'Trend_%s.xlsx' % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_trend = tmallDir_t + 'Trend_%s.xlsx' % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if os.path.exists(filename_trend):
            logging.info('remove xlsx start')
            os.remove(filename_trend)
            logging.info('remove xlsx end')
        # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
        logging.info('create xlsx')

        logging.info('start write SrcFlow')
        # filename_srcflow = folder + 'SrcFlow_%s.xlsx' % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_srcflow = tmallDir_t + 'SrcFlow_%s.xlsx' % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if os.path.exists(filename_srcflow):
            logging.info('remove xlsx start')
            os.remove(filename_srcflow)
            logging.info('remove xlsx end')
        # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
        logging.info('create xlsx')

        # 创建一个新的excel文件并添加一个工作表
        self.wb_trend = xlsxwriter.Workbook(filename_trend)

        # 创建一个新的excel文件并添加一个工作表
        self.wb_srcflow = xlsxwriter.Workbook(filename_srcflow)

        # 创建工作簿
        self.ws_trend = self.wb_trend.add_worksheet('曲线走势图数据')
        logging.info('chuang jian trend')

        # 创建工作簿
        self.ws_srcflow = self.wb_srcflow.add_worksheet('流量数据改版')
        logging.info('chuang jian srcflow')

        # 创建工作簿
        self.ws_srcflow1 = self.wb_srcflow.add_worksheet('流量数据原版')
        logging.info('chuang jian srcflow')

        # 行，列初始值
        self.row_trend = 0
        self.col_trend = 0

        # 设置表头
        for coln in self.trend_colname:
            self.ws_trend.write(self.row_trend, self.col_trend, coln)
            self.col_trend += 1

        # 行，列初始值
        self.row_srcflow1 = 0
        self.col_srcflow1 = 0

        # 设置表头
        for coln in self.srcflow_colname:
            self.ws_srcflow1.write(self.row_srcflow1, self.col_srcflow1, coln)
            self.col_srcflow1 += 1

        # 行，列初始值
        self.row_srcflow = 1
        self.col_srcflow = 0
        # 居中格式
        center_style_pc = self.wb_srcflow.add_format(xlsx_style(bg_color='#FFFF00'))
        center_style_wifi = self.wb_srcflow.add_format(xlsx_style(bg_color='#FFCC00'))
        # 合并单元格
        self.ws_srcflow.merge_range(0, 4, 0, 18, 'pc')
        self.ws_srcflow.merge_range(0, 19, 0, 42, '无线')
        self.ws_srcflow.write(0, 4, 'pc', center_style_pc)
        self.ws_srcflow.write(0, 19, '无线', center_style_wifi)

        # 设置表头
        for coln in self.srcflow_col:
            self.ws_srcflow.write(self.row_srcflow, self.col_srcflow, coln)
            self.col_srcflow += 1

    def save_tmall_data(self):
        '''数据处理'''

        # 从redis中获取数据
        for i in range(1, redis_store.llen('tmall') - 1):
            item = redis_store.lindex('tmall', i)
            logging.info(item)
            # string to dict
            item = eval(item)
            if 'trend' == item['mark']:

                # 筛选
                # 整理出item字典中的所有key
                item_keys = list(item.keys())
                # 根据表头字段筛选出需要的key
                itemkey_list = [item_key for item_key in item_keys if item_key in self.trend_col]

                # 建立一个新的字典
                item_dict = dict()
                last_dict = dict()
                # 将数据存入新的字典
                for _, itemkey in enumerate(itemkey_list):
                    item_dict[itemkey] = item[itemkey]
                # 根据表格样式拼接字段数据，因为一个品牌型号下，有多条数据
                if item['num'] == item['total'] - 1:
                    item_dict['bm'] = item['brandName'] + ' ' + item['modelName']
                    item_dict['device_category'] = item['device_category']

                else:
                    item_dict['bm'] = ''
                    item_dict['device_category'] = ''
                # 将数据存入表格中文字段字典中
                last_dict['品类'] = item_dict['device_category']
                last_dict['品牌/型号'] = item_dict['bm']
                last_dict['日期'] = item_dict['date_time']
                last_dict['支付转化率'] = item_dict['payByrRateIndex']
                last_dict['支付子订单数'] = item_dict['payOrdCnt']
                last_dict['支付件数'] = item_dict['payItemQty']

                # 行的移动
                self.row_trend += 1
                # 写入时间数据
                # self.ws.write(self.row, 0, item_dict['date_time'])
                # 写入主要数据
                for key, value in last_dict.items():
                    for index, col in enumerate(self.trend_colname):
                        if key == col:
                            self.ws_trend.write(self.row_trend, index, value)


            elif 'srcflow' in item['mark']:
                # 获取数据中pc和wifi数据的字典
                pc_dict = item['pc']
                wifi_dict = item['wifi']

                # 选择数量最多的，来完成表格字段排布
                max_num = max(len(pc_dict), len(wifi_dict))

                # extend合并列表
                pc_keys = list(pc_dict.keys())
                wifi_keys = list(wifi_dict.keys())

                # 筛选
                # item_keys = list(item.keys())
                # itemkey_list = [item_key for item_key in item_keys if item_key in self.colname]

                # 建立一个新的字典
                item_dict = dict()

                item_dict['品类'] = item['device_category']
                item_dict['品牌'] = item['brandName']
                item_dict['型号'] = item['modelName']
                item_dict['商品ID'] = item['itemId']

                for i in range(max_num):
                    item_dict1 = dict()
                    if i == 0:
                        item_dict1['device_category'] = item['device_category']
                        item_dict1['brandName'] = item['brandName']
                        item_dict1['modelName'] = item['modelName']
                        item_dict1['itemId'] = item['itemId']
                    else:
                        item_dict1['device_category'] = ''
                        item_dict1['brandName'] = ''
                        item_dict1['modelName'] = ''
                        item_dict1['itemId'] = ''
                    try:
                        item_dict1['pc'] = pc_keys[i]
                        item_dict1['pc_uv'] = pc_dict[pc_keys[i]]
                    except:
                        item_dict1['pc'] = ''
                        item_dict1['pc_uv'] = ''
                    try:
                        item_dict1['wifi'] = wifi_keys[i]
                        item_dict1['wifi_uv'] = wifi_dict[wifi_keys[i]]
                    except:
                        item_dict1['wifi'] = ''
                        item_dict1['wifi_uv'] = ''

                    # 行的移动
                    self.row_srcflow1 += 1

                    # 写入主要数据
                    for key, value in item_dict1.items():
                        for index, col in enumerate(self.srcflow_colname):
                            if key == col:
                                self.ws_srcflow1.write(self.row_srcflow1, index, value)

                # 行的移动
                self.row_srcflow += 1

                # 写入主要数据
                for key, value in item_dict.items():
                    for index, col in enumerate(self.srcflow_col):
                        if key == col:
                            self.ws_srcflow.write(self.row_srcflow, index, value)
                # 写入主要数据
                for key, value in pc_dict.items():
                    for index, col in enumerate(self.srcflow_col):
                        if key == col and index < 19:
                            self.ws_srcflow.write(self.row_srcflow, index, value)
                # 写入主要数据
                for key, value in wifi_dict.items():
                    for index, col in enumerate(self.srcflow_col):
                        if key == col and index > 18:
                            self.ws_srcflow.write(self.row_srcflow, index, value)


    def __del__(self):
        '''关闭文件'''

        # 在爬虫结束时，关闭文件节省资源
        logging.info('Trend finished')

        # 表格存储结束
        self.wb_trend.close()

        # 在爬虫结束时，关闭文件节省资源
        logging.info('SrcFlow finished')

        # 表格存储结束
        self.wb_srcflow.close()


