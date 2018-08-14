'''
作者：zsj
'''

import datetime
import re
import time
import calendar


'''
t = time.strptime('2018-04-28', '%Y-%m-%d')
int(time.mktime(t))---> 时间戳格式

某年某月有几天
import calendar
monthRange = calendar.monthrange(2013,6) --> int
print monthRange
输出：
(5, 30) --> int
输出的是一个元组，第一个元素是上一个月的最后一天为星期几(0-6),星期天为0;第二个元素是这个月的天数

'''
__cur = datetime.datetime.now()

def cookie_input():
    cookie_in = input('输入账号对应的cookie 值:')
    return cookie_in

def __time_range(index):
    '''处理三个模式'''
    global __cur

    enddate = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    # 最近一天，即今天的昨天
    if '1' == index:
        startdate = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        return startdate, enddate
    # 最近的7天，即今天的之前的7天
    elif '2' == index:
        startdate = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        return startdate, enddate
    # 本月累计，即本月1号到昨天
    elif '4' == index:
        if enddate.split('-')[1] == str(__cur.month):
            startdate = datetime.date(year=__cur.year, month=__cur.month, day=1).strftime('%Y-%m-%d')
        else:
            startdate = datetime.date(year=__cur.year, month=int(enddate.split('-')[1]), day=1).strftime('%Y-%m-%d')
        return startdate, enddate
    # 自然月
    elif '5' == index:

        if enddate.split('-')[1] == str(__cur.month):
            startdate = datetime.date(year=__cur.year, month=__cur.month, day=1).strftime('%Y-%m-%d')
        else:
            startdate = datetime.date(year=__cur.year, month=int(enddate.split('-')[1]), day=1).strftime('%Y-%m-%d')


        return startdate, enddate

def __diy_time(startdate, enddate):
    '''起止日期的时间戳处理'''
    print(startdate, enddate)
    try:
        start_date = time.strptime(startdate, '%Y-%m-%d')
        start = int(time.mktime(start_date))
    except:
        start = 0

    try:
        end_date = time.strptime(enddate, '%Y-%m-%d')
        end = int(time.mktime(end_date))
    except:
        end = 0


    return start, end

def __date_judge(date_time):
    '''日期格式判断'''

    global __cur

    if len(date_time) != 10:
        msg = '格式输入有误，请重新输入！'
        print('格式输入有误，请重新输入！')
        return False, msg
    elif '-' not in date_time:
        msg = '格式输入有误，请重新输入！'
        print('格式输入有误，请重新输入！')
        return False, msg
    elif len(date_time.split('-')) != 3:
        msg = '格式输入有误，请重新输入！'
        print('格式输入有误，请重新输入！')
        return False, msg
    else:
        # 判断日期是否超出当前时间
        # cur = datetime.datetime.now()
        # calendar.monthrange(2013, 6)
        # 获取年，月，日
        try:
            Year, Month, Day = re.findall(r'(\d+)-(\d+)-(\d+)', date_time)[0]
        except Exception as e:
            msg = '您输入的日期超出范围或日期有问题，请重新输入！'
            print('您输入的日期超出范围或日期有问题，请重新输入！')
            return False, msg
        # 将年，月，日转成整型，提供后续使用
        try:
            Year = int(Year)
            Month = int(Month)
            Day = int(Day)
        except:
            msg = '格式输入有误，请重新输入！'
            print('格式输入有误，请重新输入！')
            return False, msg
        # 判断输入的年，月，日是否为0
        if not Year * Month * Day:
            msg = '日期输入有误，请重新输入！'
            print('日期输入有误，请重新输入！')
            return False, msg
        else:
            # 某年某月天数，返回是星期（0-6）和天数
            _, days = calendar.monthrange(Year, Month)

            if Year > __cur.year:
                msg = '输入"年"超出范围，请重新输入！'
                print('输入"年"超出范围，请重新输入！')
                return False, msg
            # 当前年，月份超出范围
            elif Year == __cur.year and Month > __cur.month:
                msg = '输入"月"超出范围，请重新输入！'
                print('输入"月"超出范围，请重新输入！')
                return False, msg
            # 过去年，月份超出12
            elif Year < __cur.year and Month > 12:
                msg = '输入"月"超出范围，请重新输入！'
                print('输入"月"超出范围，请重新输入！')
                return False, msg
            # 当前月，天超出范围
            elif Month == __cur.month and Day >= __cur.day:
                msg = '输入"日"超出范围，请重新输入！'
                print('输入"日"超出范围，请重新输入！')
                return False, msg
            # 过去月，天超过天数
            elif Month < __cur.month and Day > days:
                msg = '输入"日"超出范围，请重新输入！'
                print('输入"日"超出范围，请重新输入！')
                return False, msg
            else:
                msg = 'ok'
                print(Year, Month, Day)
                return True, msg



def __date_format():
    '''时间格式化为2018-01-01'''
    while True:
        while True:
            # 起始日期
            startdate = input('请输入起始日期(格式例如 2018-01-01):')
            status, _ = __date_judge(startdate)
            if status:
                break
            else:
                continue

        while True:
            # 截止日期
            enddate = input('请输入截止日期(格式例如 2018-01-01):')
            status, _ = __date_judge(enddate)
            if status:
                break
            else:
                continue

        start, end = __diy_time(startdate, enddate)
        if start or end:
            pass
        else:
            print('日期输入有误，请重新输入！')
            continue

        recent_month, _ = __diy_time(((datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')), '2018-01-01')

        # 判断起止日期是否符合大小要求
        if start > end:
            print('起始日期大于截止日期，请重新输入！')
            continue
        elif start < recent_month:
            print('日期范围超出最近一月，请重新输入！')
            continue
        elif start != end:
            print('请将起止日期输入一致，请重新输入！')
            continue
        else:
            break

    return startdate, enddate

# def date_range():
#     '''dateRange时间范围'''
#     while True:
#         print('''
#         多个模式：
#             例如今天是2018年02月02日，
#             1、最近一天的数据
#             2、最近一周的数据
#             3、最近一个月中指定某一天：起始日期和截止日期输入一样，例如：2018-01-31
#             4、本月累计
#             自然日day 自然周week 自然月month 自定义range 最近一天recent1 最近7天recent7 最近30天recent30
#
#         ''')
#         index = input('请根据您的需求选择模式编号(1 or 2 or 3 or 4):')
#         if '1' == index:
#             dateType = 'recent1'
#             startdate, enddate = __time_range(index)
#             break
#         elif '2' == index:
#             dateType = 'recent7'
#             startdate, enddate = __time_range(index)
#             break
#         elif '3' == index:
#             dateType = 'day'
#             startdate, enddate = __date_format()
#             break
#         elif '4' == index:
#             dateType = 'range'
#             startdate, enddate = __time_range(index)
#             break
#         elif '5' == index:
#             dateType = 'month'
#             startdate, enddate = __time_range(index)
#             break
#         else:
#             print('编号输入有误，请您重新选择！')
#             continue
#
#     return startdate, enddate, dateType, index

def date_range_pre():
    '''时间范围dateRangePre'''
    return __time_range('1')

def time_stamp():
    '''时间戳'''
    return ''.join(str(time.time()).split('.'))[:13]

def sanyo_time(index):
    if '1' == index:
        dateType = 'recent1'

    else:
        dateType = 'range'

    startdate, enddate = __time_range(index)

    return startdate, enddate, dateType, index

def date_judge(date_time):
    '''判断日期格式'''
    return __date_judge(date_time)



if __name__ == '__main__':
    # d = DaterangeAndTimestamp()
    print(time_stamp())
    # s, e, i, num = date_range()
    s, e, i, num = sanyo_time('')
    # print(date_range())
    print(s, e, i)
    print(type(s))
    print(type(e))
    print(type(i))
