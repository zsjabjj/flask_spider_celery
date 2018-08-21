# -*- coding: utf-8 -*-
import datetime
import json
import logging
import random
import time
import requests
import sys
import threading
from queue import Queue

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from inchange_net import redis_store
from inchange_net import constants
from inchange_net.utils.DateRangeAndTimeStamp import time_stamp, sanyo_time, date_range
from config import Config
from inchange_net.utils.FileToDict import file_dict


class TmallSpider(object):
    '''使用多线程获取数据, 用到队列queue存放需要执行的操作'''

    def __init__(self, cookie_str, date_time, date_type):
        '''初始化'''
        self.date_time = date_time
        self.date_type = date_type

        # 是否指定日期
        if self.date_time:
            # 指定日期
            self.start_time, self.end_time, self.dateType, self.index = self.date_time, self.date_time, 'day', '3'
            self.dateRange = self.start_time + '%7C' + self.end_time
            pass
        else:
            # 最近一天
            # self.date_time = date_time
            # 时间范围
            self.start_time, self.end_time, self.dateType, self.index = date_range('1', self.date_time)
            self.dateRange = self.start_time + '%7C' + self.end_time
            pass

        # 默认时间范围
        # start_time_pre, end_time_pre = date_range_pre()
        start_time_pre, end_time_pre, self.dateTypePre, _ = date_range('1', self.date_time)
        self.dateRangePre = start_time_pre + '%7C' + end_time_pre

        try:
            redis_store.delete('tmall')
        except Exception as err:
            logging.error(err)
        # 构建url
        self.brandListUrl = 'https://sycm.taobao.com/mq/industry/product/product_rank/getRankList.json?brandId={brandId}&cateId=50012082&dateRange={dateRange}&dateType={dateType}&device=0&seller=1&token=f400b7b0f&_={t}'
        self.itemIdUrl = 'https://sycm.taobao.com/mq/rank/listItem.json?brandId={brandId}&cateId=50012082&categoryId=50012082&dateRange={dateRange}&dateRangePre={dateRangePre}&dateType={dateType}&dateTypePre=recent1&device=0&devicePre=0&itemDetailType=5&keyword=&modelId={modelId}&orderDirection=desc&orderField=payOrdCnt&page=1&pageSize=15&rankTabIndex=0&rankType=1&seller=1&spuId={spuId}&token=f400b7b0f&view=rank&_={t}'
        self.itemTrendUrl = 'https://sycm.taobao.com/mq/rank/listItemTrend.json?brandId={brandId}&cateId=50012082&categoryId=50012082&dateRange={dateRange}&dateRangePre={dateRangePre}&dateType={dateType}&dateTypePre=recent1&device=0&devicePre=0&indexes=payOrdCnt,payByrRateIndex,payItemQty&itemDetailType=5&itemId={itemId}&latitude=undefined&modelId={modelId}&rankTabIndex=0&rankType=1&seller=1&spuId={spuId}&token=f400b7b0f&view=detail&_={t}'
        self.itemSrcFlowUrl = 'https://sycm.taobao.com/mq/rank/listItemSrcFlow.json?brandId={brandId}&cateId=50012082&categoryId=50012082&dateRange={dateRange}&dateRangePre={dateRangePre}&dateType={dateType}&dateTypePre={dateTypePre}&device={device}&devicePre=0&itemDetailType=5&itemId={itemId}&modelId={modelId}&rankTabIndex=0&rankType=1&seller=1&spuId={spuId}&token=f400b7b0f&view=detail&_={t}'

        # 建立一个存储列表, 用来存储pc端和无线端的数据
        self.pw_list = list()
        # 构建存储数据列表
        self._list = list()
        self._list.append('tmall开始采集')
        try:
            redis_store.rpush('tmall', 'tmall开始采集')
        except:
            logging.error(dir(redis_store))
        # 构建headers
        self.headers = {
            # 'User-Agent': random.choice(MY_USER_AGENT_PC),
            'Cookie': cookie_str,
        }

        # 创建存放需要执行操作的事件
        self.url_queue = Queue()
        self.resp_queue = Queue()
        self.data_queue = Queue()

    def generate_url_list(self):
        '''构建起始url'''
        # 构建获取品牌型号以及ID的url
        for _, brandId in enumerate(constants.BRANDIDS):
            brand_dict = dict()
            brand_url = self.brandListUrl.format(brandId=brandId, dateRange=self.dateRange, dateType=self.dateType,t=time_stamp())
            brand_dict['url'] = brand_url
            brand_dict['mark'] = 'brandList'

            self.url_queue.put(brand_dict)

    def get_data(self):
        '''获取数据'''
        while self.url_queue.not_empty:
            # resp = requests.get('http://47.100.236.184/zsj/get/')
            resp = requests.get('http://47.100.236.184/proxy/random')
            ip = resp.text
            # request.headers['proxy'] = 'http://{}'.format(ip)
            proxies = {"http": "http://{}".format(ip)}
            data_dict = self.url_queue.get()
            logging.info('__________________________')
            logging.info(data_dict['mark'])
            logging.info('===========================')
            self.headers['User-Agent'] = random.choice(constants.MY_USER_AGENT_PC)
            # 品牌list
            if 'brandList' == data_dict['mark']:
                self.headers[
                    'Referer'] = 'https://sycm.taobao.com/mq/industry/product/rank.htm?spm=a21ag.7782695.LeftMenu.d320.7ee44653mUqxYv'
            # itemid list
            elif 'itemidList' == data_dict['mark']:
                self.headers[
                    'Referer'] = 'https://sycm.taobao.com/mq/industry/rank/spu.htm?spm=a21ag.7782686.0.0.3ffb277512wIuF'
            elif 'trend' == data_dict['mark']:
                self.headers[
                    'Referer'] = 'https://sycm.taobao.com/mq/industry/rank/spu.htm?spm=a21ag.7782686.0.0.3ffb277512wIuF'
            elif 'srcflow' == data_dict['mark']:
                self.headers[
                    'Referer'] = 'https://sycm.taobao.com/mq/industry/rank/spu.htm?spm=a21ag.7782686.0.0.3ffb277512wIuF'

            time.sleep(0.2)
            resp = requests.get(data_dict['url'], headers=self.headers, proxies=proxies)
            jsonp = json.loads(resp.text)

            # 添加json数据
            data_dict['jsonp'] = jsonp
            if 'trend' == data_dict['mark'] or 'srcflow' == data_dict['mark']:
                logging.info('data_queue')
                logging.info(data_dict['mark'])
                self.data_queue.put(data_dict)
            else:
                logging.info('resp_queue')
                logging.info(data_dict['mark'])
                self.resp_queue.put(data_dict)
            self.url_queue.task_done()

    def parse_data_one(self):
        '''第一次解析'''
        while self.resp_queue.not_empty:
            data = self.resp_queue.get()

            if 'hasError' not in data['jsonp']:
                logging.error('brand may be cookie error')

            elif 'brandList' == data['mark']:
                # 品牌型号列表
                bm_list = data['jsonp']['content']['data']

                for bm in bm_list:
                    # 解析得到品牌型号字典
                    bm_dict, _ = file_dict(bm)
                    # 用来存储进行下一步的数据
                    # itemid_dict = dict()

                    if bm_dict:
                        # 构建获取itemid的url
                        itemid_url = self.itemIdUrl.format(
                            brandId=bm_dict['brandId'],
                            dateRange=self.dateRange,
                            dateType=self.dateType,
                            dateRangePre=self.dateRangePre,
                            modelId=bm_dict['modelId'],
                            spuId=bm_dict['spuId'],
                            t=time_stamp()
                        )
                        itemid_dict = bm_dict
                        itemid_dict['url'] = itemid_url
                        itemid_dict['mark'] = 'itemidList'

                        self.url_queue.put(itemid_dict)
                self.resp_queue.task_done()

            elif 'itemidList' == data['mark']:
                itemId_list = data['jsonp']['content']['data']['data']
                # 判断该商品是否能够查到
                if not itemId_list:
                    # 没有查到，直接返回
                    logging.info('商品没有被查到')

                else:
                    # 查到
                    ctmall_list = [itemId for itemId in itemId_list if '天猫超市' == itemId['shopName']]
                    # 判断是否有猫超
                    if not ctmall_list:
                        # 没有猫超
                        logging.info('没有猫超')

                    else:
                        # 有猫超
                        logging.info('有猫超')
                        del data['jsonp']
                        del data['url']
                        del data['mark']
                        logging.info(data)
                        for _, ctmall in enumerate(ctmall_list):
                            trend_dict = dict()
                            srcflow_dict1 = dict()
                            srcflow_dict2 = dict()

                            # 请求曲线数据
                            url_trend = self.itemTrendUrl.format(
                                brandId=data['brandId'],
                                dateRange=self.dateRange,
                                dateType=self.dateType,
                                dateRangePre=self.dateRangePre,
                                modelId=data['modelId'],
                                spuId=data['spuId'],
                                t=time_stamp(),
                                itemId=ctmall['itemId']
                            )
                            trend_dict['modelName'] = data['modelName']
                            trend_dict['brandName'] = data['brandName']
                            trend_dict['brandId'] = data['brandId']
                            trend_dict['spuId'] = data['spuId']
                            trend_dict['modelId'] = data['modelId']
                            trend_dict['device_category'] = data['device_category']
                            trend_dict['url'] = url_trend
                            trend_dict['mark'] = 'trend'
                            logging.info('trend insert')
                            self.url_queue.put(trend_dict)
                            logging.info('-=-==-=-=-=-=-=-=-=-=-')

                            # 请求流量数据

                            i = 1
                            url_srcflow1 = self.itemSrcFlowUrl.format(
                                brandId=data['brandId'],
                                dateRange=self.dateRange,
                                dateType=self.dateType,
                                dateRangePre=self.dateRangePre,
                                modelId=data['modelId'],
                                spuId=data['spuId'],
                                t=time_stamp(),
                                itemId=ctmall['itemId'],
                                device=i,
                                dateTypePre=self.dateTypePre
                            )

                            srcflow_dict1['modelName'] = data['modelName']
                            srcflow_dict1['brandName'] = data['brandName']
                            srcflow_dict1['brandId'] = data['brandId']
                            srcflow_dict1['spuId'] = data['spuId']
                            srcflow_dict1['modelId'] = data['modelId']
                            srcflow_dict1['device_category'] = data['device_category']
                            srcflow_dict1['itemId'] = ctmall['itemId']
                            srcflow_dict1['url'] = url_srcflow1
                            srcflow_dict1['mark'] = 'srcflow'
                            srcflow_dict1['i'] = i
                            self.url_queue.put(srcflow_dict1)

                            i = 2
                            url_srcflow2 = self.itemSrcFlowUrl.format(
                                brandId=data['brandId'],
                                dateRange=self.dateRange,
                                dateType=self.dateType,
                                dateRangePre=self.dateRangePre,
                                modelId=data['modelId'],
                                spuId=data['spuId'],
                                t=time_stamp(),
                                itemId=ctmall['itemId'],
                                device=i,
                                dateTypePre=self.dateTypePre
                            )

                            srcflow_dict2['modelName'] = data['modelName']
                            srcflow_dict2['brandName'] = data['brandName']
                            srcflow_dict2['brandId'] = data['brandId']
                            srcflow_dict2['spuId'] = data['spuId']
                            srcflow_dict2['modelId'] = data['modelId']
                            srcflow_dict2['device_category'] = data['device_category']
                            srcflow_dict2['itemId'] = ctmall['itemId']
                            srcflow_dict2['url'] = url_srcflow2
                            srcflow_dict2['mark'] = 'srcflow'
                            srcflow_dict2['i'] = i
                            self.url_queue.put(srcflow_dict2)

                self.resp_queue.task_done()

    def parse_data_two(self):
        '''第二次解析，流量和趋势数据'''
        while self.data_queue.not_empty:
            data = self.data_queue.get()
            logging.info('------------------')
            # logging.info(data)
            logging.info('+++++++++++++++++++')
            # 判断返回数据是否正确
            if 'hasError' not in data['jsonp']:
                logging.error('may be cookie error')
            # 曲线趋势
            elif 'trend' == data['mark']:
                # 转化率
                logging.info('曲线趋势')
                payByrRateIndexList = data['jsonp']['content']['data']['payByrRateIndexList']
                # 支付订单数
                payOrdCntList = data['jsonp']['content']['data']['payOrdCntList']
                # 支付件数
                payItemQtyList = data['jsonp']['content']['data']['payItemQtyList']

                _1 = len(payByrRateIndexList)
                _2 = len(payOrdCntList)
                _3 = len(payItemQtyList)

                if not all([payByrRateIndexList, payOrdCntList, payItemQtyList]):
                    logging.error('may be cookie error')
                # 三者数量一致
                elif _1 == _2 and _2 == _3:
                    for num in range(_1 - 1, -1, -1):
                        item = data
                        item['payByrRateIndex'] = payByrRateIndexList[num]
                        item['payOrdCnt'] = payOrdCntList[num]
                        item['payItemQty'] = payItemQtyList[num]
                        item['date_time'] = (datetime.date.today() - datetime.timedelta(days=_1 - num)).strftime('%Y-%m-%d')
                        item['total'] = _1
                        item['num'] = num

                        self._list.append(item)
                        logging.info('trend ok')
                        redis_store.rpush('tmall', item)
                    self.data_queue.task_done()

                # 三者数量不一致
                else:
                    for num in range(min(_1, _2, _3) - 1, -1, -1):
                        item = data
                        item['payByrRateIndex'] = payByrRateIndexList[num]
                        item['payOrdCnt'] = payOrdCntList[num]
                        item['payItemQty'] = payItemQtyList[num]
                        item['date_time'] = (datetime.date.today() - datetime.timedelta(days=_1 - num)).strftime('%Y-%m-%d')
                        item['total'] = min(_1, _2, _3)
                        item['num'] = num

                        self._list.append(item)
                        logging.info('trend ok')
                        redis_store.rpush('tmall', item)
                    self.data_queue.task_done()

            # 流量
            elif 'srcflow' == data['mark']:
                logging.info('流量')
                # pc端

                # logging.info(data)
                if 1 == data['i']:
                    pc_list = data['jsonp']['content']['data']
                    pc_dict = dict()
                    for _, pc in enumerate(pc_list):

                        pc_dict[pc['pageName']] = pc['uv']
                    data['pc'] = pc_dict

                    pc_data = data
                    # print(pc_data)
                    self.pw_list.append(pc_data)
                # 无线端
                elif 2 == data['i']:
                    wifi_list = data['jsonp']['content']['data']
                    wifi_dict = dict()
                    for wifi in wifi_list:

                        wifi_dict[wifi['pageName']] = wifi['uv']
                    data['wifi'] = wifi_dict

                    wifi_data = data

                    self.pw_list.append(wifi_data)

                for _, pw in enumerate(self.pw_list):

                    for no in range(self.pw_list.index(pw), len(self.pw_list)):
                        pw_no = self.pw_list[no]
                        if 'pc' in pw and 'wifi' in pw_no and pw['modelName'] == pw_no['modelName']:

                            item = pw
                            item['wifi'] = pw_no['wifi']
                            self.pw_list.pop(self.pw_list.index(pw))
                            self.pw_list.pop(self.pw_list.index(pw_no))

                            self._list.append(item)

                            redis_store.rpush('tmall', item)

                        elif 'wifi' in pw and 'pc' in pw_no and pw['modelName'] == pw_no['modelName']:
                            item = pw
                            item['pc'] = pw_no['pc']
                            self.pw_list.pop(self.pw_list.index(pw))
                            self.pw_list.pop(self.pw_list.index(pw_no))

                            self._list.append(item)

                            redis_store.rpush('tmall', item)
                self.data_queue.task_done()

    def run(self):
        '''程序开始'''

        # 创建存储线程的列表
        thread_list = list()

        # 创建生成url线程
        # print('start create url')
        t_url = threading.Thread(target=self.generate_url_list)
        thread_list.append(t_url)

        # 创建获取数据的线程
        # print('start get data')
        for i in range(3):
            t_data = threading.Thread(target=self.get_data)
            thread_list.append(t_data)

        # 创建解析数据的线程
        # print('start parse data')
        for i in range(3):
            t_parse_one = threading.Thread(target=self.parse_data_one)
            thread_list.append(t_parse_one)

        # 创建解析流量和趋势数据的线程
        for i in range(3):
            t_parse_two = threading.Thread(target=self.parse_data_two)
            thread_list.append(t_parse_two)

        # 开启线程
        # print('start run')
        for t in thread_list:
            # 守护线程的方式
            t.setDaemon(True)
            t.start()


        # 等待子线程结束

        self.url_queue.join()
        logging.info('url queue ok')
        self.resp_queue.join()
        logging.info('resp queue ok')
        self.data_queue.join()
        logging.info('data queue ok')


        self._list.append('tmall采集完成请导出')
        redis_store.rpush('tmall', 'tmall采集完成请导出')

        return self._list


if __name__ == '__main__':
    cookie = sys.argv[1]
    # print(cookie)
    qiushi = TmallSpider(cookie, '', '')
    qiushi.run()
