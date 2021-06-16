# -- coding: utf-8 --

import requests
from time import sleep
from dateutil import parser
from datetime import datetime, time
import pandas as pd

class AstockTrading(object):

    # 类的属性
    def __init__(self, strategy_name):
        self._Dt = []
        self._Open = []
        self._High = []
        self._Low = []
        self._Close = []
        self._volume = []
        self._tick = []
        self._last_bar_start_time = None  # 当前分时图的时间
        self._strategy_name = strategy_name
        self._isNewBar = False
        self._ma20 = None
        self._current_order = {}
        # self._current_order = {
        #     "order1":{
        #         "open price": 1,
        #         "open datetime": '2021/6/16 14:30',
        #         "comment": []
        #     }
        # }
        self._order_number = 0

    def set_period(self, x):
        if isinstance(x, int):
            self._period = x
        else:
            print("请输入整型数值！")

    def get_period(self):
        return self._period

    # 获取当前最新成交价格和交易时间
    def getTick(self):
        # 返回last交易信息<class 'tuple'>: (2193.0, '2021-06-15 15:00:01')
        stock_code = 'sh600519'  # 贵州茅台
        url = 'http://hq.sinajs.cn/?format=text&list=' + stock_code
        page = requests.get(url)
        stock_info_str = page.text
        stock_info = stock_info_str.split(',')
        # opening_price = float(stock_info[1]) #开盘价
        last_price = float(stock_info[3])  # 最新成交价

        # A股开盘时间：9:15
        # 集合竞价时间：9:15-9:25
        # 开盘价时间：9:25
        # 非交易时间：9:25-9:30

        # 2020/12/10 9:25
        trade_datetime = stock_info[30] + ' ' + stock_info[31]
        if trade_datetime.time() < time(9, 30):
            trade_datetime = datetime.combine(trade_datetime.date(), time(9, 30))
        self._tick = (last_price, trade_datetime)

    # 类的方法，从本地读取历史交易数据
    def get_history_data_from_local_machine(self):
        self._Dt = [2, 3, 4]
        self._Open = [2, 3, 4]
        self._High = [2, 3, 4]
        self._Low = [2, 3, 4]
        self._Close = [2, 3, 4]
        self._volume = [2, 3, 4]

    # 更新bar的开盘价、最高价、最低价和收盘价
    def bar_generate(self, tick):
        # open, high, low, close
        # Dt = [datetime(2020, 11, 27, 14, 55),
        #       datetime(2020, 11, 27, 14, 50),
        #       datetime(2020, 11, 27, 14, 45)]
        # Open = [45.79, 45.66, 45.72]
        # High = []
        # Low = []
        # Close = []

        gap = 5  # 间隔多少分钟处理一次
        if self._tick[0].minute % gap == 0 and self._tick[0].minute != self._last_bar_start_time:
            self._last_bar_start_minute = self._tick[0].minute
            self._Open.insert(0, tick[1])
            self._High.insert(0, tick[1])
            self._Low.insert(0, tick[1])
            self._Close.insert(0, tick[1])
            self._Dt.insert(0, tick[0])
            self._ma20 = Close[:19].sum() / 20
            self._isNewBar = True
        else:
            self._High[0] = max(self._High[0], self._tick[1])  # 保存当前最高价格
            self._Low[0] = min(self._Low[0], self._tick[1])  # 保存当前最低价格
            self._Close[0] = self._tick[1]  # 保存当前最新价格
            self._Dt[0] = self._tick[0]
            self._isNewBar = False

    def buy(self, price, volume):
        # 买入交易订单
        self._order_number += 1
        key = "order" + str(self._order_number)
        self._current_order[key] = {
            "open_datetime": self._Dt[0],
            "open_price": price,
            "volume": volume
        }

    def sell(self, key, price):
        # 卖出交易订单
        self._current_order[key]["close_price"] = price
        self._current_order[key]["close_datetime"] = self._Dt[0]
        self._history_order[key] = self._current_order.pop(key)

    def strategy(self):
        # last < 0.92 * ma20, buy
        # last > 1.08 * ma20, sell
        if self._isNewBar:
            last = self._Close[0]
            self._ma20 = self._Close[1:21].sum() / 20

        if 0 == len(self._current_order):
            if self._Close[0] < 0.95 * self._ma20:
                # 10,000/44.28 = 2258
                # 2258 -> 2200
                price = self._Close[0] + 0.01 #溢价0.01交易，确保交易成功
                cash = 100000 #买入金额
                volume = int(cash / self._Close[0] /100) * 100 #买入份额，多少手
                self.buy(price, volume)
        elif 1 == len(self._current_order):
            if self._Close[0] > 1.05 * self._ma20:
                key = self._current_order.keys()[0]
                price = self._Close[0] - 0.01 #折价0.01交易，确保交易成功
                cash = 100000 #买入金额
                volume = int(cash / self._Close[0] /100) * 100 #买入份额，多少手
                self.sell(key, price, volume)
                # if self.buy():  # 将之前买入的stock卖掉
                #     self.sell(key, price, volume)
                # else:
                #     pass
        else:
            raise ValueError("订单多余一个！")
            pass

    def runStrategy(self):
        self.getTick()
        self.bar_generate()
        self.strategy()

stock = AstockTrading('ma')
stock.get_history_data_from_local_machine()

df = pd.read_csv("C:\\Users\\Eli\\Desktop\\trader_in_stock\\600036_data\\600036_15m.csv")

while time(9, 26) < datetime.now().time() < time(11, 32)\
        or time(13, 0) < datetime.now().time() < time(15, 2):
        stock.getTick()
        stock.bar_generate()
        stock.strategy()
# 创建继承类，实现不同策略
class MaStrategy(AstockTrading):
    def __init__(self):
        super(MaStrategy, self).__init__()

    # 重定义父类的方法
    def get_history_data_from_local_machine(self):
        self._Open = [10, 20, 30]
        self._High = [20, 30, 30]

trade_time = time(9, 30) #获取交易时间
while time(9) < trade_time < time(15):
    # 获取最新成交价信息 (2193.0, '2021-06-15 15:00:01')
    last_tick = getTick()
    Dt, Open, High, Low, Close, volume  = bar_generate(last_tick, Dt_, Open_, High_, Low_, Close_, volume_)
    strategy(Dt, Open, High, Low, Close, volume)
    print(last_tick)
    trade_time = parser.parse(last_tick[1]).time()
    sleep(3)

print('任务完成！')





