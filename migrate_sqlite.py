import sqlite3
import psycopg2

def handle_db():
    """
    migrate the sqlite to postgresql
    """
    # conn1 = sqlite3.connect('app.db')
    # conn2 = psycopg2.connect(database="postgres", user="postgres", password="123456", host="localhost", port="5432")

    # cursor1 = conn1.cursor()
    # cursor2 = conn2.cursor()


    # cursor1.execute('select * from ag')
    # values = cursor1.fetchall()

    # for item in values:
    #     # print(item)
    #     cursor2.execute("insert into ag (date, ag_future_price, ag_future_averge_price, ag_future_previous_settlement_price, ag_fund_price, ag_fund_previous_net_value, ag_fund_net_value) values ('"+item[1]+"', "+str(item[4])+", "+str(item[5])+", "+str(item[6])+", "+str(item[7])+", "+str(item[8])+", "+str(item[9])+")")
    #     # cursor2.execute("insert into ag (date, ag_future_price, ag_future_averge_price, ag_future_previous_settlement_price, ag_fund_price, ag_fund_previous_net_value, ag_fund_net_value) values ('"+item[1]+"', "+item[4]+", "+item[5]+", "+item[6]+", "+item[7]+", "+item[8]+", "+item[9]+")")

    # cursor1.close()
    # conn1.close()

    # conn2.commit()
    # conn2.close()
    print("data migrated !!!")
