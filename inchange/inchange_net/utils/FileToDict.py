# -*- coding: utf-8 -*-
from inchange_net import constants

line_list = [line.strip() for line in open(constants.BRAND_DIR + 'brand_model.txt') if line]

def file_dict(bm):
    '''提取需要的品牌和型号相关的信息'''

    global line_list

    for line in line_list:
        bm_dict = dict()
        device_category, brand, model = line.split(' ')

        if brand == bm['brandName'] and model == bm['modelName']:
            bm_dict['modelName'] = bm['modelName']
            bm_dict['brandName'] = bm['brandName']
            bm_dict['brandId'] = bm['brandId']
            bm_dict['spuId'] = bm['spuId']
            bm_dict['modelId'] = bm['modelId']
            bm_dict['device_category'] = device_category
            line_list.pop(line_list.index(line))
            print('after pop:', len(line_list))
            return bm_dict, line_list

    return None, line_list

if __name__ == '__main__':
    bm = dict()
    # Midea/美的 MB-WYJ301
    bm['modelName'] = 'MB-WYJ301'
    bm['brandName'] = 'Midea/美的'
    bm['brandId'] = '1'
    bm['spuId'] = '1'
    bm['modelId'] = '1'
    data = file_dict(bm)
    print(data)
    bm['modelName'] = 'L6-C3'
    bm['brandName'] = 'Joyoung/九阳'
    bm['brandId'] = '1'
    bm['spuId'] = '1'
    bm['modelId'] = '1'
    data = file_dict(bm)
    print(data)
    bm['modelName'] = 'L6-C3'
    bm['brandName'] = 'Joyoung/九阳'
    bm['brandId'] = '1'
    bm['spuId'] = '1'
    bm['modelId'] = '1'
    data = file_dict(bm)
    print(data)
