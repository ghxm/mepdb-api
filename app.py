from flask import Flask, request
from flask_restful import Resource, Api, reqparse, original_flask_make_response
from sqlalchemy import create_engine
from json import dumps
import pandas as pd
import configparser

# Create a engine for connecting to SQLite3.

import os
import sys

#BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
#sys.path.insert(0, os.path.abspath(BASE_DIR))

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

os.environ["TZ"] = "UTC"

e = create_engine('sqlite:///'+ config['SQL']['sqlite_db'])

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('format', type=str, default = "json")
parser.add_argument('date', type=int, default = None)


class Attributes(Resource):
    def get(self):

        args = parser.parse_args()
        # Connect to databse
        conn = e.connect()
        # Perform query and return JSON data
        #query = conn.execute("select * from attributes")

        df = pd.read_sql_query("select * from attributes", conn)

        if args['format'] == "csv":
            return original_flask_make_response(df.to_csv())
        else:
            return original_flask_make_response(df.to_json(orient="records"))

        #return {'meps': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}

class Roles(Resource):
    def get(self):

        args = parser.parse_args()
        # Connect to databse
        conn = e.connect()
        # Perform query and return JSON data
        #query = conn.execute("select * from attributes")

        df = pd.read_sql_query("select * from roles", conn)

        if args['format'] == "csv":
            return original_flask_make_response(df.to_csv())
        else:
            return original_flask_make_response(df.to_json(orient="records"))

        #return {'meps': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}

class Meps(Resource):
    def get(self):

        args = parser.parse_args()
        # Connect to databse
        conn = e.connect()
        # Perform query and return JSON data
        #query = conn.execute("select * from attributes")

        df = pd.read_sql_query("select * from attributes LEFT JOIN roles ON attributes.mep_id = roles.mep_id", conn)

        if args['format'] == "csv":
            return original_flask_make_response(df.to_csv())
        else:
            return original_flask_make_response(df.to_json(orient="records"))

        #return {'meps': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}


class Meps_Detail(Resource):
    def get(self, mep_id):

        conn = e.connect()
        query = conn.execute("select * from attributes where mep_id=%s" % mep_id)
        # Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result
        # We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient

api.add_resource(Attributes, '/meps/attributes')
api.add_resource(Roles, '/meps/roles')
api.add_resource(Meps, '/meps')
api.add_resource(Meps_Detail, '/meps/<string:mep_id>')

if __name__ == '__main__':
    app.run()