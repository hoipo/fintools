import schedule
import time
import threading
from app import db, models, mongo_ag_tick
from app.models import Ag
from app.handler import get_live_data_of_ag, get_ag_fund_net_value



def run_continuously(schedule, interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)
    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def save_today_data():
    date = time.strftime("%Y-%m-%d", time.localtime())
    if Ag.query.filter_by(date=date).first() is None:
        data = get_live_data_of_ag(no_cache=True)
        ag = Ag(date=data['date'],
                    time=data['time'],
                    ag_future_price=data['ag_future_price'],
                    ag_future_averge_price=data['ag_future_averge_price'],
                    ag_future_previous_settlement_price=data['ag_future_previous_settlement_price'],
                    ag_fund_price=data['ag_fund_price'],
                    ag_fund_previous_net_value=data['ag_fund_previous_net_value'],
                    )
        db.session.add(ag)
        db.session.commit()
        print('已保存到数据库')


def save_todays_ag_fund_net_value():
    item = Ag.query.order_by(Ag.id.desc()).first()
    if item.ag_fund_net_value == 0.0:
        data = get_ag_fund_net_value()
        if data['date'] == item.date:
            item.update_ag_fund_net_value(data['ag_fund_price'])
            db.session.commit()
            print('已更新数据库')
        else:
            print('今天数据还没出来')
    else: 
        print('今天已经更新完数据')

def save_ag_tick_data():
    """
    记录每tick的数据
    """
    nowtime = time.localtime()
    market_open_time = time.strptime('{}-{}-{} 1:30:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    middle_close_time = time.strptime('{}-{}-{} 3:30:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    middle_open_time = time.strptime('{}-{}-{} 5:00:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    market_close_time = time.strptime('{}-{}-{} 7:00:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    market_close_time = time.strptime('{}-{}-{} 7:00:00'.format(
        nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday), '%Y-%m-%d %H:%M:%S')
    if (nowtime > market_open_time and nowtime < middle_close_time) or (nowtime > middle_open_time and nowtime < market_close_time):
        data = get_live_data_of_ag(no_cache=True)
        mongo_ag_tick.insert_one(data)


schedule.every().day.at('07:01').do(save_today_data)
schedule.every().day.at('07:30').do(save_today_data)

schedule.every().hour.do(save_todays_ag_fund_net_value)
schedule.every(30).seconds.do(save_ag_tick_data)


run_continuously(schedule)
