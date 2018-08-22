# -*- coding: utf-8 -*-
import time
import csv
import re
import logging
# from save_gmv import SaveGmv
from inchange_net.utils.save_gmv import SaveGmv


def sale_gmv(filenames, upload_dir, download_dir):
    save_g = SaveGmv(download_dir)

    # 存放荣事达官旗2表格中提取的订单编号和购买数量
    a = dict()
    # 存放两张荣事达官旗的表格匹配后最终的结果
    b = dict()
    # 存放荣事达官旗表格中的提取的型号，支付金额
    d = dict()
    # 存放荣事达官旗外其他品牌官旗的数据
    e = dict()
    # 存放荣事达官旗外其他品牌分销的数据
    # f = dict()
    # 存放荣事达分销
    rsdfx = dict()
    # 存放含'荣事达'前缀
    rsd_list = list()

    for filename in filenames:
        logging.info(filename)
        # 提取文件名前缀
        pre_name = filename.split('.')[0]
        logging.info(pre_name)
        rsd_list.append(pre_name) if '荣事达' in pre_name else None
        file_path = upload_dir + filename
        logging.info(file_path)
        # 打开文件
        with open(file_path, 'r', encoding='gbk') as csvFile:
            num = 0

            # 以字典的方式读取文件内容
            readers = csv.DictReader(csvFile)
            # 遍历生成器为列表
            row_list = [row for row in readers]
            # 判断打开的文件名称
            if '荣事达官旗2' == pre_name:
                logging.info('in 荣事达官旗2')
                # print(pre_name)
                # 遍历字典列表
                for ind, row in enumerate(row_list):

                    # a['orderNum'] = row['订单编号']
                    # 购买数量
                    buyNum = row['购买数量']
                    # 已经打开过荣事达官旗.csv
                    if d:
                        try:
                            # 根据订单编号获取型号和价格
                            data_dict = d[row['订单编号']]
                        except Exception as err:
                            logging.error(err)
                            logging.error(d)
                            # order_num = row['订单编号'].split('"')[1]
                            # data_dict = d[order_num]
                        else:
                            # 型号
                            model = data_dict['model']
                            # 价格
                            price = data_dict['price']
                            # 该订单编号下的数量乘价格
                            totalPrice = int(buyNum) * price
                            # 筛选不符合项
                            if model in row['标题']:
                                # 已存在的型号，直接叠加
                                if model in b:
                                    b[model]['buyNum'] += int(buyNum)
                                    b[model]['totalPrice'] += totalPrice
                                # 未存在的型号，新创建
                                else:
                                    if 'BCD' in model:
                                        b['shop_name'] = '荣事达'
                                        # b['nick'] = '官旗'
                                        b[model] = {'buyNum': int(buyNum), 'totalPrice': totalPrice, 'type': '冰箱',
                                                    'nick': '荣事达官方旗舰店'}
                                    else:
                                        b['shop_name'] = '荣事达'
                                        # b['nick'] = '官旗'
                                        b[model] = {'buyNum': int(buyNum), 'totalPrice': totalPrice, 'type': '洗衣机',
                                                    'nick': '荣事达官方旗舰店'}
                    # 未打开过荣事达官旗.csv
                    else:
                        if row['订单编号'] in a:
                            # print(row['标题'])
                            pass
                        else:
                            a[row['订单编号']] = buyNum
                logging.info(b)
                logging.info(a)
                logging.info('out 荣事达官旗2')
            elif '荣事达官旗' == pre_name:
                logging.info('in 荣事达官旗')
                # print(pre_name)
                for ind, row in enumerate(row_list):
                    # 存放部分数据
                    c = dict()
                    try:
                        _ = row['买家实际支付金额']
                    except Exception as err:
                        logging.error(err)
                        logging.error(row)
                        logging.error(pre_name)
                    # 对价格进行处理
                    if '.' in row['买家实际支付金额']:
                        price_int = int(''.join(row['买家实际支付金额'].split('.')))
                        price = price_int / (10 ** len(row['买家实际支付金额'].split('.')[1]))
                    else:
                        price = int(row['买家实际支付金额'])
                    # 通过宝贝标题提取型号
                    model = re.findall(r'.*荣事达 (.*?) .*', row['宝贝标题 '])
                    # 已经打开过荣事达官旗2.csv
                    if a:
                        # 筛选符合的订单
                        try:
                            buyNum = a[row['订单编号']]
                            model = model[0]
                        except Exception as err:
                            logging.error(err)
                        else:
                            # 总计价格
                            totalPrice = int(buyNum) * price
                            # 存入字典
                            c['buyNum'] = int(buyNum)
                            c['totalPrice'] = totalPrice
                            # c['shop_name'] = '荣事达官旗'
                            # print(row['宝贝标题 '])
                            c['nick'] = '荣事达官方旗舰店'
                            if 'BCD' in model:
                                c['type'] = '冰箱'
                            else:
                                c['type'] = '洗衣机'
                            # 暂存数据
                            if model in b:
                                b[model]['buyNum'] += int(buyNum)
                                b[model]['totalPrice'] += totalPrice
                            else:
                                b['shop_name'] = '荣事达'
                                # b['nick'] = '官旗'
                                b[model] = c
                    else:
                        if not model:
                            pass
                        else:

                            c['model'] = model[0]
                            c['price'] = price
                            if 'BCD' in model[0]:
                                c['type'] = '冰箱'
                            else:
                                c['type'] = '洗衣机'
                            d[row['订单编号']] = c
                logging.info(d)
                logging.info(b)
                logging.info('out 荣事达官旗')
            else:
                for ind, row in enumerate(row_list):
                    try:
                        name___ = row['分销商会员名']
                    except Exception as err:
                        logging.error(pre_name)
                        logging.error(err)
                    if '-' == row['分销商会员名']:
                        # e = dict()

                        if '.' in row['分销商销售收入']:
                            price_int = int(''.join(row['分销商销售收入'].split('.')))
                            price = price_int / (10 ** len(row['分销商销售收入'].split('.')[1]))
                        else:
                            price = int(row['分销商销售收入'])

                        # 计数，可以一个用户买两件商品
                        num += 1
                        # 遍历key，将主信息填入分信息中
                        for key in row.keys():
                            # print('key', row[key])
                            # if row_list[ind - num][key] is not '-':
                            if row[key] is '-':
                                row[key] = row_list[ind - num][key]

                        buyNum = int(row['有效采购数量'])
                        totalPrice = buyNum * price

                        item_dict = dict()

                        if '三洋' in row['产品名称']:
                            e['shop_name'] = '三洋'
                        elif '帝度' in row['产品名称']:
                            e['shop_name'] = '帝度'
                        elif '惠而浦' in row['产品名称']:
                            e['shop_name'] = '惠而浦'
                        elif '荣事达' in row['产品名称']:
                            e['shop_name'] = '荣事达'
                        # print(row['分销商会员名'])
                        if 'BCD' in row['产品名称']:
                            # 冰箱
                            # print('qijianbcd:', row['分销商销售收入'], row['收件人'], ind)
                            # nick_sum_bcd += int(''.join(row['分销商销售收入'].split('.')))
                            # nick_sum_bcd += price

                            # e['nick'] = '官旗'
                            item_dict['nick'] = row['分销商会员名']
                            item_dict['type'] = '冰箱'
                            item_dict['buyNum'] = buyNum
                            item_dict['totalPrice'] = totalPrice
                            # if row['商家编码'] in e:
                            #     pass
                            # else:
                            #     e[row['商家编码']] = item_dict

                        else:
                            # 洗衣机
                            # print('qijian:', row['分销商销售收入'], row['收件人'], ind)
                            # nick_sum += price

                            # e['nick'] = '官旗'
                            item_dict['nick'] = row['分销商会员名']
                            # e['model'] = row['商家编码']
                            item_dict['type'] = '洗衣机'
                            item_dict['buyNum'] = buyNum
                            item_dict['totalPrice'] = totalPrice

                        # print('item_dict:', item_dict)

                        data_list = list()
                        model = row['商家编码']
                        if model:
                            # e[row['商家编码']] = data_list
                            pass
                        else:
                            match_norm = r'.*{} (.*?) .*'.format(e['shop_name'])
                            models = re.findall(match_norm, row['产品名称'])
                            # print('models:', models)
                            if models:
                                model = models[0]
                        # logging.info(model)
                        try:
                            # print('bianma:', row['商家编码'])

                            # ok = [nick_dict for nick_dict in e[row['商家编码']] if row['分销商会员名'] == nick_dict['nick']]
                            ok = [nick_dict for nick_dict in e[model] if row['分销商会员名'] == nick_dict['nick']]
                            # logging.info(ok)
                            # for nick_dict in e[row['商家编码']]:
                            #     print('nick_dict:', nick_dict)
                            #     if row['分销商会员名'] == nick_dict['nick']:
                            #         ok = [nick_dict]
                        except Exception as err:

                            data_list.append(item_dict)
                            # model = row['商家编码']
                            # e[row['商家编码']] = data_list
                            e[model] = data_list
                            logging.error(err)


                        else:

                            # if row['商家编码'] in e:
                            if model in e:
                                if ok:
                                    ok[0]['buyNum'] += buyNum
                                    ok[0]['totalPrice'] += totalPrice

                                    new_dict = dict()
                                    new_dict['nick'] = ok[0]['nick']
                                    new_dict['type'] = ok[0]['type']
                                    new_dict['buyNum'] = ok[0]['buyNum']
                                    new_dict['totalPrice'] = ok[0]['totalPrice']
                                    # e[row['商家编码']].remove(ok[0])
                                    e[model].remove(ok[0])
                                    # e[row['商家编码']].append(new_dict)
                                    e[model].append(new_dict)
                                    # print('append:', e)
                                else:
                                    e[model].append(item_dict)
                    else:
                        num = 0

            if '荣事达官旗' in pre_name:
                # if b:
                #     print(b)
                if (b and rsdfx) or (3 == len(rsd_list)):
                # if b and rsdfx:

                    bkeys = list(b.keys())

                    fkeys = list(rsdfx.keys())

                    jihe = set(bkeys + fkeys)
                    try:
                        jihe.remove('shop_name')
                    except Exception as err:
                        logging.error(err)
                    # print(jihe)
                    for i in jihe:
                        l = list()
                        if i in bkeys and i in fkeys:
                            l.append(b[i])
                            l += rsdfx[i]
                            b[i] = l
                        elif i in fkeys:
                            b[i] = rsdfx[i]
                        elif i in bkeys:
                            l.append(b[i])
                            b[i] = l
                    logging.info(str(b))
                    save_g.saveGmv(b)
                    b = dict()
                    rsdfx = dict()
            elif '荣事达' == pre_name:
                # print(e)
                rsdfx = e
                e = dict()
                if (b and rsdfx) or (3 == len(rsd_list)):
                # if b and rsdfx:
                    bkeys = list(b.keys())

                    fkeys = list(rsdfx.keys())

                    jihe = set(bkeys + fkeys)
                    try:
                        jihe.remove('shop_name')
                    except Exception as err:
                        logging.error(err)
                    # print(jihe)
                    for i in jihe:
                        l = list()
                        if i in bkeys and i in fkeys:
                            l.append(b[i])
                            l += rsdfx[i]
                            b[i] = l
                        elif i in fkeys:
                            b[i] = rsdfx[i]
                        elif i in bkeys:
                            l.append(b[i])
                            b[i] = l
                    logging.info(str(b))
                    save_g.saveGmv(b)
                    b = dict()
                    rsdfx = dict()

            else:
                # logging.info(str(e))
                save_g.saveGmv(e)
                e = dict()
                # f = dict()


# if __name__ == '__main__':
    # filenames = ['荣事达.csv', '荣事达官旗.csv', '荣事达官旗2.csv', '三洋.csv', '帝度.csv', '惠而浦.csv']
    # filenames = ['荣事达官旗.csv', '荣事达官旗2.csv', '荣事达.csv']
    # sale_gmv(filenames, '', '')
