# -*- coding: utf-8 -*-
import os


# 基础路径, 入口程序所在路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 下载文件路径
DOWNLOAD_DIR = BASE_DIR + "/datas/download/"

# 上传文件路径
UPLOAD_DIR = BASE_DIR + "/datas/upload/"

# 缓存文件路径
TEMP_DIR = BASE_DIR + "/datas/temp/"

# sanyo dir
SANYO_DIR = BASE_DIR + '/datas/Data/sanyo/'

# tmall dir
TMALL_DIR = BASE_DIR + '/datas/Data/tmall/'
# 九阳brandId：30850 美的brandId：30652 苏泊尔brandId：30844
BRANDIDS = ['30850', '30652', '30844']
# 猫超品牌型号文件存放路径
BRAND_DIR = BASE_DIR + "/utils/"

# midea
# midea dir
MIDEA_DIR = BASE_DIR + '/datas/Data/midea/'
# 炒锅，煎锅，奶锅，汤锅，蒸锅
MIDEA_CATEID = ['炒锅/50002804', '煎锅/50004390', '奶锅/50005480', '汤锅/50002808', '蒸锅/50002807']
MIDEA_INDEXS = ['payPct,payRate,uv,payItemQty']

# sycm dir
SYCM_DIR = BASE_DIR + '/Sycm'

# 允许的文件格式
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx', 'xls'}

# ua列表
MY_USER_AGENT_PC = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
]


# 生意参谋洗衣机/冰箱品牌ID
BS_BRANDS = {
    "Haier/海尔": 11016,
    "Littleswan/小天鹅": 30657,
    "Midea/美的": 30652,
    "SIEMENS/西门子": 80946,
    "Samsung/三星": 81156,
    "Bosch/博世": 3223459,
    "Whirlpool/惠而浦": 66878525,
    "Royalstar/荣事达": 30654,
    "DIQUA/帝度": 50878944,
    "Sanyo/三洋": 10728,
    "TCL": 10858,
    "Panasonic/松下": 81147,
    "Leader/统帅": 113190408,
}

CATEIDS = [
    {'washer': 350301},
    {'fridge': 50003881},
]

WASHER_BRANDS = ['Haier/海尔', 'Littleswan/小天鹅', 'Midea/美的', 'SIEMENS/西门子', 'Sanyo/三洋', 'TCL', 'Panasonic/松下', 'Leader/统帅', 'Bosch/博世', 'Royalstar/荣事达', 'Whirlpool/惠而浦']
FRIDGE_BRANDS = ['Haier/海尔', 'SIEMENS/西门子', 'Midea/美的', 'Samsung/三星', 'Bosch/博世', 'Whirlpool/惠而浦', 'Royalstar/荣事达', 'DIQUA/帝度']

# 登录错误次数最大值
LOGIN_ERROR_MAX_NUM = 5

# 设置登录时输错信息, 达到上限后, 封锁ip的时间
LOGIN_ERROR_FORBID_TIME = 60 * 60 * 24

# 设置图片验证码在Redis中的过期时间, 三分钟后过期
IMAGE_CODE_REDIS_EXPIRE = 180

# 设置短信验证码在Redis中的过期时间, 三分钟后过期
SMS_CODE_REDIS_EXPIRE = 180

# 七牛云的访问域名
QINIU_URL_DOMAIN = "http://p24iqa82n.bkt.clouddn.com/"

# 上传七牛云token过期时间
QINIU_UPLOAD_TOKEN_TIME = 3600

# 城区信息的redis缓存时间， 单位：秒
AREA_INFO_REDIS_EXPIRES = 3600

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页的数量
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面数据Redis缓存时间
HOUSE_LIST_PAGE_REDIS_EXPIRES = 3600