import requests
import time
import math
from datetime import datetime
from app.models import Ag

def get_live_data_of_ag(no_cache=False):
    nowtime = time.localtime()
    market_open_time = time.strptime('{}-{}-{} 1:00:00'.format(nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    market_close_time = time.strptime('{}-{}-{} 7:01:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    if no_cache or (time.localtime() > market_open_time and time.localtime() < market_close_time):
        # fetch the price of AG future
        ag_future_price = requests.get('https://hq.sinajs.cn/?_={}&list=nf_AG0'.format(
            int(time.time()))).text.split('=')[1].split('";')[0].split(',')
        # # fetch price and net value of 161226
        ag_fund = requests.get('https://hq.sinajs.cn/?_={}&list=sz161226,f_161226'.format(
            int(time.time()))).text.split('\n')
        ag_fund_price = ag_fund[0].split('=')[1].split(',')[3]  # 白银基金现价
        # 白银基金净值time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ag_fund_net_value = ag_fund[1].split('=')[1].split(',')[1]
        return {
            'date': ag_fund[0].split('=')[1].split(',')[-3],
            'time': ag_fund[0].split('=')[1].split(',')[-2],
            'ag_future_price': round(float(ag_future_price[8])),
            'ag_future_averge_price': round(float(ag_future_price[-1])),
            'ag_future_previous_settlement_price': round(float(ag_future_price[10])),
            'ag_fund_price': float(ag_fund_price),
            'ag_fund_previous_net_value': float(ag_fund_net_value)
        }
    else:
        ag = Ag.query.order_by(Ag.id.desc()).first()
        return {
            'date': ag.date,
            # 'time': ag.create_time.strftime('%H:%M:%S'),
            'time': '15:00:00',
            'ag_future_price': ag.ag_future_price,
            'ag_future_averge_price': ag.ag_future_averge_price,
            'ag_future_previous_settlement_price': ag.ag_future_previous_settlement_price,
            'ag_fund_price': ag.ag_fund_price,
            'ag_fund_previous_net_value': ag.ag_fund_previous_net_value,
        }


def get_ag_fund_net_value():
    ag_fund = requests.get('https://hq.sinajs.cn/?_={}&list=f_161226'.format(
        int(time.time()))).text.split('=')[1].split('";')[0].split(',')
    return {
        'ag_fund_price': ag_fund[1],
        'ag_fund_previous_net_value': ag_fund[3],
        'date': ag_fund[4],
    }
