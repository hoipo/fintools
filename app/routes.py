from app import app, db, api
from app.models import Ag
from flask_restful import Resource, fields, marshal_with, reqparse
from flask import jsonify
from app.utils import serialize
from app.handler import get_live_data_of_ag, get_tick_data, get_tick_data_one
from bson.json_util import dumps

ag_history_resource_fields = {
    'id': fields.Integer,
    'date': fields.String,
    'time': fields.String,
    'create_time': fields.DateTime(dt_format='iso8601'),
    'update_time': fields.DateTime(dt_format='iso8601'),
    'ag_future_price': fields.Integer,
    'ag_future_averge_price': fields.Integer,
    'ag_future_previous_settlement_price': fields.Integer,
    'ag_fund_price': fields.Float,
    'ag_fund_previous_net_value': fields.Float,
    'ag_fund_net_value': fields.Float,
    'ag_fund_cap': fields.String,
}

class _get_live_data_of_ag(Resource):
    def get(self):
        res = get_live_data_of_ag()
        return res

api.add_resource(_get_live_data_of_ag, '/api/get_live_data_of_ag')

class _get_ag_history(Resource):
    @marshal_with(ag_history_resource_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        limit = parser.parse_args().limit
        l = Ag.query.order_by(Ag.id.desc()).limit(limit or 20).all()
        return [serialize(i) for i in l]

api.add_resource(_get_ag_history, '/api/get_ag_history')


class _get_tick_data(Resource):    
    # @marshal_with(tick_data_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str)
        parser.add_argument('limit', type=str)
        date = parser.parse_args().date
        limit = parser.parse_args().limit
        lst = get_tick_data(date=date, limit=limit)
        return jsonify(lst)


api.add_resource(_get_tick_data, '/api/get_tick_data')

class _get_tick_data_one(Resource):
    # @marshal_with(tick_data_fields)
    def get(self):
        lst = get_tick_data_one()
        return jsonify(lst)


api.add_resource(_get_tick_data_one, '/api/get_tick_data_one')