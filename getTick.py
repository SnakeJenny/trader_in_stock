# -- coding: utf-8 --

import requests
from time import sleep
from dateutil import parser
from datetime import datetime, time

# 获取当前最新成交价格和交易时间
def getTick():
    # 返回last交易信息<class 'tuple'>: (2193.0, '2021-06-15 15:00:01')
    stock_code = 'sh600519' #贵州茅台
    url = 'http://hq.sinajs.cn/?format=text&list=' + stock_code
    page = requests.get(url)
    stock_info_str = page.text
    stock_info = stock_info_str.split(',')
    # opening_price = float(stock_info[1]) #开盘价
    last_price = float(stock_info[3]) #最新成交价
    trade_datetime = stock_info[30] + ' ' + stock_info[31]
    tick = (last_price, trade_datetime)
    return tick

def get_history_data_from_local_machine():


    return Dt_, Open_, High_, Low_, Close_, volume_
    # open, high, low, close
def bar_generate(tick, Dt, Open, High, Low, Close, volume):
    # Dt = [datetime(2020, 11, 27, 14, 55),
    #       datetime(2020, 11, 27, 14, 50),
    #       datetime(2020, 11, 27, 14, 45)]
    # Open = [45.79, 45.66, 45.72]
    # High = []
    # Low = []
    # Close = []

    gap = 5 #间隔多少分钟处理一次
    last_bar_start_time = None #当前分时图的时间
    if tick[0].minute % gap == 0 and tick[0].minute != last_bar_start_time:
        last_bar_start_minute = tick[0].minute
        Open.insert(0, tick[1])
        High.insert(0, tick[1])
        Low.insert(0, tick[1])
        Close.insert(0, tick[1])
        Dt.insert(0, tick[0])
        ma20 = Close[:19].sum() / 20
    else:
        High[0] = max(High[0], tick[1]) #保存当前最高价格
        Low[0] = min(Low[0], tick[1])  #保存当前最低价格
        Close[0] = tick[1] #保存当前最新价格
        Dt[0] = tick[0]

    return Dt, Open, High, Low, Close, volume

def buy():
    pass

def sell():
    pass

def strategy(Dt, Open, High, Low, Close, volume):
    # last < 0.92 * ma20, buy
    # last > 1.08 * ma20, sell
    last = Close[0]
    ma20 = Close[1:21].sum() / 20
    if last < 0.95 * ma20:
        buy()
    elif last > 1.05 * ma20:
        if buy(): #将之前买入的stock卖掉
            sell()
        else:
            pass
    else:

        pass


Dt_, Open_, High_, Low_, Close_, volume_ = get_history_data_from_local_machine()


trade_time = time(9, 30) #获取交易时间
while time(9) < trade_time < time(15):
    # 获取最新成交价信息 (2193.0, '2021-06-15 15:00:01')
    last_tick = getTick()
    strategy(last_tick)
    print(last_tick)
    trade_time = parser.parse(last_tick[1]).time()
    sleep(3)

print('任务完成！')





