# -*- coding: utf-8 -*-
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
from inchange_net.constants import MY_USER_AGENT_PC, CATEIDS, WASHER_BRANDS, BS_BRANDS, FRIDGE_BRANDS
from inchange_net.utils.DateRangeAndTimeStamp import time_stamp, sanyo_time
from config import Config



class BrandRatio(object):
    '''使用多线程获取数据, 用到队列queue存放需要执行的操作'''

    def __init__(self, cookie_str):

        try:
            redis_store.delete('sanyo')
        except Exception as err:
            logging.error(err)
        # 构建url
        self.base_url = 'https://sycm.taobao.com/mq/brandDetail/getSummary.json?brandId={brandId}&cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&seller=1&token=8a416f30f&_={t}'
        # 构建存储数据列表
        self._list = list()
        self._list.append('ratio开始采集')
        # Config.SESSION_REDIS.rpush('sanyo', 'ratio开始采集')
        try:
            redis_store.rpush('sanyo', 'ratio开始采集')
        except:
            logging.error(dir(redis_store))
        # 构建headers
        self.headers = {
            # 'User-Agent': random.choice(MY_USER_AGENT_PC),
            'Cookie': cookie_str,
            'Referer': 'https://sycm.taobao.com/mq/industry/brand/detail.htm?spm=a21ag.7749233.0.0.47564710CpQrAv',
        }

        # 保存数据文件
        # self.f = open('qiushi.json', 'w', encoding='UTF-8')

        # 创建存放需要执行操作的事件
        self.url_queue = Queue()
        self.resp_queue = Queue()
        # self.data_queue = Queue()

    # def __del__(self):
    #     self.f.close()

    def generate_url_list(self):
        '''构建url'''

        for i in ['1', '4']:
            # 时间范围
            start_time, end_time, dateType, index = sanyo_time(i)
            dateRange = start_time + '%7C' + end_time
            # print(dateRange)

            # print(dateRange)

            # 品牌分析
            for cate in CATEIDS:
                # 洗衣机
                if 'washer' in cate:
                    # 品牌分析
                    for washer in WASHER_BRANDS:
                        # 传递数据字典
                        brand_dict = dict()

                        brandId = BS_BRANDS[washer]

                        brand_url = self.base_url.format(brandId=brandId, cateId=cate['washer'], dateRange=dateRange,
                                                         dateType=dateType, t=time_stamp())

                        brand_dict['url'] = brand_url
                        brand_dict['cate'] = 'washer'
                        brand_dict['brand'] = washer
                        brand_dict['index'] = i

                        self.url_queue.put(brand_dict)


                # 冰箱
                elif 'fridge' in cate:
                    # 品牌分析
                    for fridge in FRIDGE_BRANDS:
                        # 传递数据字典

                        brand_dict = dict()

                        brandId = BS_BRANDS[fridge]

                        brand_url = self.base_url.format(brandId=brandId, cateId=cate['fridge'], dateRange=dateRange,
                                                         dateType=dateType, t=time_stamp())

                        brand_dict['url'] = brand_url
                        brand_dict['cate'] = 'fridge'
                        brand_dict['brand'] = fridge
                        brand_dict['index'] = i

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
            self.headers['User-Agent'] = random.choice(MY_USER_AGENT_PC)
            time.sleep(1)
            resp = requests.get(data_dict['url'], headers=self.headers, proxies=proxies)
            jsonp = json.loads(resp.text)
            # 添加json数据
            data_dict['jsonp'] = jsonp
            self.resp_queue.put(data_dict)
            self.url_queue.task_done()

    def parse_data(self):
        '''第一次解析'''
        while self.resp_queue.not_empty:
            data = self.resp_queue.get()

            if 'hasError' not in data['jsonp']:
                logging.error('brand may be cookie error')
                # 洗衣机品牌
            elif 'washer' == data['cate']:
                # print(data['cate'])

                item_washer = dict()
                washer_dict = data['jsonp']['content']['data']
                # print(washer_dict)
                if washer_dict:
                    # 交易指数tradeIndex 302518
                    item_washer['tradeIndex'] = washer_dict['tradeIndex']
                    # 支付商品数payItemCnt 230
                    item_washer['payItemCnt'] = washer_dict['payItemCnt']
                    # 客单价payPct 1270.86
                    item_washer['payPct'] = washer_dict['payPct']
                    # 支付转化率payRate 0.0224
                    item_washer['payRate'] = washer_dict['payRate']
                    # 访客数uv 72997
                    item_washer['uv'] = washer_dict['uv']
                    # 搜索点击人数searchUvCnt 29790
                    item_washer['searchUvCnt'] = washer_dict['searchUvCnt']
                    # 收藏人数favBuyerCnt 2987
                    item_washer['favBuyerCnt'] = washer_dict['favBuyerCnt']
                    # 加购人数addCartUserCnt 6350
                    item_washer['addCartUserCnt'] = washer_dict['addCartUserCnt']
                    # 卖家数sellerCnt 390
                    item_washer['sellerCnt'] = washer_dict['sellerCnt']
                    # 被支付卖家数paySellerCnt 65
                    item_washer['paySellerCnt'] = washer_dict['paySellerCnt']
                    # 重点卖家数majorSellerCnt 44
                    item_washer['majorSellerCnt'] = washer_dict['majorSellerCnt']
                    # 重点商品数majorItemCnt 50
                    item_washer['majorItemCnt'] = washer_dict['majorItemCnt']
                    # 品牌
                    item_washer['brand'] = data['brand']
                    # 分类
                    item_washer['cate'] = data['cate']
                    # 每日累计区分
                    item_washer['index'] = data['index']

                    # self.data_queue.put(item_washer)
                    self._list.append(item_washer)
                    redis_store.rpush('sanyo', item_washer)
                    logging.info(self._list)
                    self.resp_queue.task_done()

                else:
                    logging.error('brand may be cookie error')

            # 冰箱品牌
            elif 'fridge' == data['cate']:
                # print(data['cate'])
                item_fridge = dict()
                fridge_dict = data['jsonp']['content']['data']
                # print(fridge_dict)
                if fridge_dict:
                    # 交易指数tradeIndex 302518
                    item_fridge['tradeIndex'] = fridge_dict['tradeIndex']
                    # 支付商品数payItemCnt 230
                    item_fridge['payItemCnt'] = fridge_dict['payItemCnt']
                    # 客单价payPct 1270.86
                    item_fridge['payPct'] = fridge_dict['payPct']
                    # 支付转化率payRate 0.0224
                    item_fridge['payRate'] = fridge_dict['payRate']
                    # 访客数uv 72997
                    item_fridge['uv'] = fridge_dict['uv']
                    # 搜索点击人数searchUvCnt 29790
                    item_fridge['searchUvCnt'] = fridge_dict['searchUvCnt']
                    # 收藏人数favBuyerCnt 2987
                    item_fridge['favBuyerCnt'] = fridge_dict['favBuyerCnt']
                    # 加购人数addCartUserCnt 6350
                    item_fridge['addCartUserCnt'] = fridge_dict['addCartUserCnt']
                    # 卖家数sellerCnt 390
                    item_fridge['sellerCnt'] = fridge_dict['sellerCnt']
                    # 被支付卖家数paySellerCnt 65
                    item_fridge['paySellerCnt'] = fridge_dict['paySellerCnt']
                    # 重点卖家数majorSellerCnt 44
                    item_fridge['majorSellerCnt'] = fridge_dict['majorSellerCnt']
                    # 重点商品数majorItemCnt 50
                    item_fridge['majorItemCnt'] = fridge_dict['majorItemCnt']
                    # 品牌
                    item_fridge['brand'] = data['brand']
                    # 分类
                    item_fridge['cate'] = data['cate']
                    # 每日累计区分
                    item_fridge['index'] = data['index']

                    # self.data_queue.put(item_fridge)
                    self._list.append(item_fridge)
                    redis_store.rpush('sanyo', item_fridge)
                    logging.info(self._list)
                    self.resp_queue.task_done()

                else:
                    logging.error('brand may be cookie error')


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
            t_parse = threading.Thread(target=self.parse_data)
            thread_list.append(t_parse)

        # # 创建保存数据的线程
        # for i in range(3):
        #     t_save = threading.Thread(target=self.save_data)
        #     thread_list.append(t_save)

        # 开启线程
        # print('start run')
        for t in thread_list:
            # 守护线程的方式
            t.setDaemon(True)
            t.start()

        # sys.stdout.write(str(self._list) + '\n')
        # sys.stdout.flush()

        # 等待子线程结束
        # print('end run')
        self.url_queue.join()
        self.resp_queue.join()
        # self.data_queue.join()
        # print('end run')

        self._list.append('ratio采集完成请导出')
        redis_store.rpush('sanyo', 'ratio采集完成请导出')
        # print(len(self._list))
        logging.info(self._list)
        return self._list


if __name__ == '__main__':
    cookie = sys.argv[1]
    # print(cookie)
    qiushi = BrandRatio(cookie)
    qiushi.run()
