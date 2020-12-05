from app import db
from datetime import datetime
import time

class Ag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)
    ag_future_price = db.Column(db.Integer, nullable=False)
    ag_future_averge_price = db.Column(db.Integer, nullable=False)
    ag_future_previous_settlement_price = db.Column(db.Integer, nullable=False)
    ag_fund_price = db.Column(db.Float)
    ag_fund_previous_net_value = db.Column(db.Float)
    ag_fund_net_value = db.Column(db.Float, default=0.0)

    def update_ag_fund_net_value(self, net_value):
        self.ag_fund_net_value = net_value
