from flask import Flask
import os
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymongo

app = Flask(__name__, static_folder='../static', static_url_path='')

ENV = ""

if ENV == "debug":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123456@localhost:5432/postgres'
    app.debug = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root1234@154.8.158.147:3306/ag'
    app.debug = False

mongo_ag_tick = pymongo.MongoClient(os.getenv('MONGODB_URL'))["ag"]["ag_tick"]
mongo_faster_ag_tick = pymongo.MongoClient(os.getenv('MONGODB_FASTER_URL'))["temp"]["agreal"]

@ app.route('/')
def index():
    return app.send_static_file('index.html')

# 跨域支持


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET'
    return resp


app.after_request(after_request)


api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, routes, schedule_jobs


if __name__ == '__main__':
    app.run()
