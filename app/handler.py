import requests
import time
import math
from datetime import datetime, timedelta, timezone, date as date_from_datetime
from app.models import Ag
from app import mongo_ag_tick, mongo_faster_ag_tick
import pymongo
from random import random

def get_live_data_of_ag(no_cache=False):
    nowtime = time.localtime()
    market_open_time = time.strptime('{}-{}-{} 1:00:00'.format(nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    market_close_time = time.strptime('{}-{}-{} 7:01:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    if no_cache or (time.localtime() > market_open_time and time.localtime() < market_close_time):
        faster_data = __get_faster_ag_live_data() #现请求毫秒级数据
        # fetch the price of AG future
        ag_future_price = requests.get('https://hq.sinajs.cn/?_={}&list=nf_AG0'.format(
            int(time.time()))).text.split('=')[1].split('";')[0].split(',')
        # # fetch price and net value of 161226
        ag_fund = requests.get('https://hq.sinajs.cn/?_={}&list=sz161226,f_161226'.format(
            int(time.time()))).text.split('\n')
        ag_fund_price = ag_fund[0].split('=')[1].split(',')[3]  # 白银基金现价
        # 白银基金净值time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ag_fund_net_value = ag_fund[1].split('=')[1].split(',')[1]
        if (datetime.strptime(faster_data["date"] + ' ' + faster_data["time"], "%Y-%m-%d %H:%M:%S") > datetime.strptime(ag_fund[0].split('=')[1].split(',')[-3] + ' ' + ag_fund[0].split('=')[1].split(',')[-2], "%Y-%m-%d %H:%M:%S")):
            return {
                'date': faster_data["date"],
                'time': faster_data["time"],
                'ag_future_price': faster_data["ag_future_price"],
                'ag_future_averge_price': faster_data["ag_future_averge_price"],
                'ag_future_previous_settlement_price': round(float(ag_future_price[10])),
                'ag_fund_price': faster_data["ag_fund_price"],
                'ag_fund_previous_net_value': float(ag_fund_net_value),
                'is_faster_data': True
            }
        else:
            return {
                'date': ag_fund[0].split('=')[1].split(',')[-3],
                'time': ag_fund[0].split('=')[1].split(',')[-2],
                'ag_future_price': round(float(ag_future_price[8])),
                'ag_future_averge_price': round(float(ag_future_price[-1])),
                'ag_future_previous_settlement_price': round(float(ag_future_price[10])),
                'ag_fund_price': float(ag_fund_price),
                'ag_fund_previous_net_value': float(ag_fund_net_value),
                'is_faster_data': False
            }
            
    else:
        ag = Ag.query.order_by(Ag.id.desc()).first()
        return {
            'date': ag.date,
            'time': ag.time,
            'ag_future_price': ag.ag_future_price,
            'ag_future_averge_price': ag.ag_future_averge_price,
            'ag_future_previous_settlement_price': ag.ag_future_previous_settlement_price,
            'ag_fund_price': ag.ag_fund_price,
            'ag_fund_previous_net_value': ag.ag_fund_previous_net_value,
        }


def __get_faster_ag_live_data():
    faster_tick_data = mongo_faster_ag_tick.find_one(sort=[('_id', pymongo.DESCENDING)])
    dt = datetime.fromtimestamp(int(str(faster_tick_data["dataTime"])[:10])).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    return {
        'date': dt.strftime("%Y-%m-%d"),
        'time': dt.strftime("%H:%M:%S"),
        'ag_future_price': round(faster_tick_data["agFuturePrice"]),
        'ag_future_averge_price': round(faster_tick_data["agFutureAveragePrice"]),
        'ag_fund_price': faster_tick_data["agFundPrice"],
    }

def get_ag_fund_net_value():
    ag_fund = requests.get('https://hq.sinajs.cn/?_={}&list=f_161226'.format(
        int(time.time()))).text.split('=')[1].split('";')[0].split(',')
    return {
        'ag_fund_price': ag_fund[1],
        'ag_fund_previous_net_value': ag_fund[3],
        'date': ag_fund[4],
    }


def get_ag_fund_cap():
    cap = requests.get('http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1945_LOF&txtQueryKeyAndJC=161226&random={}'.format(
        random()), headers={'Host': 'www.szse.cn',
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'X-Request-Type': 'ajax',
                            'X-Requested-With': 'XMLHttpRequest',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
                            'Content-Type': 'application/json',
                            'Referer': 'http://www.szse.cn/market/product/list/lofFundList/index.html',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'}).json()
    return {
        'ag_fund_cap': cap[0]['data'][0]['dqgm'],
        'ag_fund_cap_date': cap[0]['metadata']['subname']
    }

def get_tick_data_one():
    result = mongo_ag_tick.find_one(sort=[('_id', pymongo.DESCENDING)])
    return {
        "date": result["date"],
        "time": result["time"],
        "ag_future_price": result["ag_future_price"],
        "ag_future_averge_price": result["ag_future_averge_price"],
        "ag_future_previous_settlement_price": result["ag_future_previous_settlement_price"],
        "ag_fund_price": result["ag_fund_price"],
        "ag_fund_previous_net_value": result["ag_fund_previous_net_value"],
        "is_market_open_time": __is_market_open_time()
    }

def get_tick_data(date=None, limit=None):
    """
    select the data in mongodb
    """
    query = {}
    if date is not None:
        query["date"] = date
    result = []
    cursor = mongo_ag_tick.find(query)
    for x in cursor:
        result.append({
            "date": x["date"],
            "time": x["time"],
            "ag_future_price":x["ag_future_price"],
            "ag_future_averge_price": x["ag_future_averge_price"],
            "ag_future_previous_settlement_price": x["ag_future_previous_settlement_price"],
            "ag_fund_price": x["ag_fund_price"],
            "ag_fund_previous_net_value": x["ag_fund_previous_net_value"]
            })
    if len(result) == 0:
        if date is not None:
            y, m, d = date.split('-')
            today = date_from_datetime(int(y), int(m), int(d))
        else:
            today = date_from_datetime.today()
        yesterday = today - timedelta(days=1)
        return get_tick_data(date='{}-{}-{}'.format(yesterday.year, yesterday.month, yesterday.day))
    return result
    
    
def __is_market_open_time():
    """
    check whether now is market open time
    """
    nowtime = time.localtime()
    # market_open_time = time.strptime('{}-{}-{} 1:30:00'.format(
    #     nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    # market_close_time = time.strptime('{}-{}-{} 7:00:00'.format(
    #     nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    market_open_time = time.strptime('{}-{}-{} 1:30:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    market_close_time = time.strptime('{}-{}-{} 7:00:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    if nowtime >= market_open_time and nowtime <= market_close_time:
        return True
    return False
