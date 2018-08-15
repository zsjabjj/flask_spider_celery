# -*- coding: utf-8 -*-
import json
import logging
import random
import time
import requests
import sys
import threading

from queue import Queue
from inchange_net import redis_store, constants
from inchange_net.utils.DateRangeAndTimeStamp import time_stamp, date_range


class MideaSpider(object):
    '''使用多线程获取数据, 用到队列queue存放需要执行的操作'''

    def __init__(self, cookie_str, date_time, date_type):
        '''初始化'''
        self.date_time = date_time
        self.date_type = date_type
        # 构建时间范围和类型
        if 'recent1' == self.date_type:
            # 时间范围最近一天
            start_time, end_time, dateType, index = date_range('1', self.date_time)
            self.start_time = start_time
            self.dateRange = start_time + '%7C' + end_time
        elif 'day' == self.date_type:
            # 指定日期
            start_time, end_time, dateType, index = date_range('3', self.date_time)
            self.start_time = start_time
            self.dateRange = start_time + '%7C' + end_time
        # 判断redis中是否存在
        try:
            redis_store.delete('midea')
        except Exception as err:
            logging.error(err)

        # 构建url
        # 行业大盘
        self.dapanUrl = 'https://sycm.taobao.com/mq/overview/reportTrend.json?cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&indexCode=uv|searchUvCnt|payPct|payItemQty&seller=-1&token=9a0425930&_={t}'
        # 单品牌
        self.brandUrl = 'https://sycm.taobao.com/mq/brandDetail/listTrendByIndexs.json?brandId=30652,30844,5725958,3222885&cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&index={index}&seller=-1&token=9a0425930&_={t}'
        # 炒锅多两个品
        self.brandcgUrl = 'https://sycm.taobao.com/mq/brandDetail/listTrendByIndexs.json?brandId=30652,30844,5725958,3222885,531544226,1344359932&cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&index={index}&seller=-1&token=9a0425930&_={t}'

        # 构建存储数据列表
        self._list = list()
        self._list.append('midea开始采集')
        # 数据存入redis
        try:
            redis_store.rpush('midea', 'midea开始采集')
        except:
            logging.error(dir(redis_store))

        # 构建headers
        self.headers = {
            'Cookie': cookie_str,
        }

        # 创建存放需要执行操作的事件
        self.url_queue = Queue()
        self.resp_queue = Queue()

    def generate_url_list(self):
        '''构建url'''
        for _, cate in enumerate(constants.MIDEA_CATEID):
            # dapan dict
            dapan_dict = dict()

            # 提取品类和ID  炒锅/50002804
            category, cateId = cate.split('/')

            # 大盘url
            dapan_url = self.dapanUrl.format(cateId=cateId, dateRange=self.dateRange, dateType=self.date_type, t=time_stamp())

            dapan_dict['url'] = dapan_url
            dapan_dict['category'] = category
            dapan_dict['mark'] = 'dapan'

            self.url_queue.put(dapan_dict)

            # 单品牌url
            for _, index in enumerate(constants.MIDEA_INDEXS):
                # danpin dict
                danpin_dict = dict()

                # 炒锅多两个品
                if '炒锅' == category:
                    brand_url = self.brandcgUrl.format(cateId=cateId, dateRange=self.dateRange, dateType=self.date_type, index=index, t=time_stamp())
                else:
                    brand_url = self.brandUrl.format(cateId=cateId, dateRange=self.dateRange, dateType=self.date_type, index=index, t=time_stamp())

                danpin_dict['url'] = brand_url
                danpin_dict['category'] = category
                danpin_dict['mark'] = 'brand'
                danpin_dict['cateId'] = cateId

                self.url_queue.put(danpin_dict)

    def get_data(self):
        '''获取数据'''
        while self.url_queue.not_empty:
            # 获取代理IP
            # resp = requests.get('http://47.100.236.184/zsj/get/')
            resp = requests.get('http://47.100.236.184/proxy/random')
            ip = resp.text
            proxies = {"http": "http://{}".format(ip)}
            # 获取队列URL字典
            data_dict = self.url_queue.get()
            # logging.info(len(data_dict))
            # 添加额外请求头元素
            self.headers['User-Agent'] = random.choice(constants.MY_USER_AGENT_PC)
            # referer区分大盘和单品牌
            self.headers['Referer'] = 'https://sycm.taobao.com/mq/industry/overview/overview.htm?spm=a21ag.7749227.LeftMenu.d293.20b8140dMMIoAZ' if 'dapan' == data_dict['mark'] else 'https://sycm.taobao.com/mq/industry/brand/detail.htm?spm=a21ag.7749233.0.0.52104710Z0OchQ'
            # 延时，手动降低访问频率
            time.sleep(0.5)
            # 数据请求
            resp = requests.get(data_dict['url'], headers=self.headers, proxies=proxies)
            # json字符串转换字典
            jsonp = json.loads(resp.text)
            # 判断
            if 'hasError' not in jsonp:
                logging.error('brand may be cookie error')
            else:
                # 添加json数据
                data_dict['jsonp'] = jsonp
                # logging.info('-------------shuju-----------:')
                # logging.info(data_dict)
                self.resp_queue.put(data_dict)
                self.url_queue.task_done()

    def parse_data(self):
        '''解析数据'''
        while self.resp_queue.not_empty:
            # 获取数据字典
            data_dict = self.resp_queue.get()
            # logging.info(len(data_dict))
            # 判断大盘和单品牌
            if 'dapan' == data_dict['mark']:
                # 大盘
                dapan_dict = dict()
                # 品类
                dapan_dict['category'] = data_dict['category']
                # 区分标记
                dapan_dict['mark'] = data_dict['mark']
                # 数据列表
                data_list = data_dict['jsonp']['content']['data']
                try:
                    for _, data in enumerate(data_list):
                        # 指标数据
                        dapan_dict[data['indexCode']] = data['values'][-1]
                except:
                    dapan_dict['uv'] = ''
                    dapan_dict['payItemQty'] = ''
                    dapan_dict['payPct'] = ''
                    dapan_dict['searchUvCnt'] = ''
                    logging.error(data_dict['jsonp'])
                # 时间
                dapan_dict['time_date'] = self.start_time
                # 数据暂存
                # logging.info('---------dapan---------------:')
                # logging.info(dapan_dict)
                self._list.append(dapan_dict)
                redis_store.rpush('midea', dapan_dict)
                self.resp_queue.task_done()

            elif 'brand' == data_dict['mark']:
                # 单品牌
                danpin_dict = dict()
                # 判断是否是4个指标还是5个指标
                try:
                    _ = data_dict['next']
                except:
                    # 品类
                    danpin_dict['category'] = data_dict['category']
                    # 区分标记
                    danpin_dict['mark'] = data_dict['mark']
                    # 数据列表
                    data_list = data_dict['jsonp']['content']['data']
                    try:
                        _ = data_list[-1]
                    except:
                        logging.error(data_dict['jsonp'])
                    else:
                        for _, data in enumerate(data_list):
                            _dict = dict()
                            _dict['uv'] = data['brandTrend']['uv'][-1]
                            _dict['payItemQty'] = data['brandTrend']['payItemQty'][-1]
                            _dict['payPct'] = data['brandTrend']['payPct'][-1]
                            _dict['payRate'] = data['brandTrend']['payRate'][-1]
                            danpin_dict[data['brandId']] = _dict
                            danpin_dict['next'] = 'ok'
                        # 单品牌需要五个指标，一次最多四个，需要再次请求
                        if '炒锅' == data_dict['category']:
                            nextUrl = self.brandcgUrl.format(cateId=data_dict['cateId'], dateRange=self.dateRange, dateType=self.date_type, index='searchUvCnt', t=time_stamp())

                        else:
                            nextUrl = self.brandUrl.format(cateId=data_dict['cateId'], dateRange=self.dateRange, dateType=self.date_type, index='searchUvCnt', t=time_stamp())

                        danpin_dict['url'] = nextUrl
                        # url加入事件队列中
                        # logging.info('===========danpin---2===========:')
                        # logging.info(danpin_dict)
                        self.url_queue.put(danpin_dict)
                        self.resp_queue.task_done()
                else:
                    # 获取第五个指标
                    data_list = data_dict['jsonp']['content']['data']
                    danpin_dict['category'] = data_dict['category']
                    danpin_dict['mark'] = data_dict['mark']
                    try:
                        _ = data_list[-1]
                    except:
                        logging.error(data_dict['jsonp'])
                    else:
                        for _, data in enumerate(data_list):
                            data_dict[data['brandId']]['searchUvCnt'] = data['brandTrend']['searchUvCnt'][-1]
                            danpin_dict[data['brandId']] = data_dict[data['brandId']]

                        danpin_dict['time_date'] = self.start_time

                        # 数据暂存
                        # logging.info('===========danpin---3===========:')
                        # logging.info(danpin_dict)
                        self._list.append(danpin_dict)
                        redis_store.rpush('midea', danpin_dict)

                        self.resp_queue.task_done()

            else:
                logging.error('brand may be cookie error')

            # self.resp_queue.task_done()


    def run(self):
        '''程序开始'''

        # 创建存储线程的列表
        thread_list = list()

        # 创建生成url线程
        t_url = threading.Thread(target=self.generate_url_list)
        thread_list.append(t_url)

        # 创建获取数据的线程
        for i in range(3):
            t_data = threading.Thread(target=self.get_data)
            thread_list.append(t_data)

        # 创建解析数据的线程
        for i in range(3):
            t_parse = threading.Thread(target=self.parse_data)
            thread_list.append(t_parse)

        # 开启线程
        for t in thread_list:
            # 守护线程的方式
            t.setDaemon(True)
            t.start()

        # sys.stdout.write(str(self._list) + '\n')
        # sys.stdout.flush()

        # 等待子线程结束
        self.url_queue.join()
        self.resp_queue.join()


        self._list.append('midea采集完成请导出')
        redis_store.rpush('midea', 'midea采集完成请导出')

        return self._list


if __name__ == '__main__':
    cookie = sys.argv[1]
    # print(cookie)
    qiushi = MideaSpider(cookie, '', '')
    qiushi.run()
