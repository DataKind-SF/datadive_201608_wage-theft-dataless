#!/usr/bin/env python

from json import dumps

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine

# Create a engine for connecting to SQLite3.

e = create_engine('sqlite:///./db.sqlite')

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser(bundle_errors=True)

class CaseList(Resource):
    def get(self):
        conn = e.connect()
        stmt = "select * from whd_whisard limit 10"
        query = conn.execute(stmt)
        result = query.cursor.fetchall()
        keys = result[0]
        rows = result[1:]

        return_result = []

        for row in rows:
            result_dict = {}
            for key, value in zip(keys, row):
                result_dict[key] = value
            return_result.append(result_dict)

        return return_result

class Case(Resource):
    def get(self, case_id=None):
        conn = e.connect()
        stmt = "select * from whd_whisard"
        if (case_id is not None):
            stmt += " where case_id=" + str(case_id)
        query = conn.execute(stmt)

        result = query.cursor.fetchall()[0]
        key = conn.execute('select * from whd_whisard limit 1').cursor.fetchall()[0]
        result_dict = {}

        for key, value in zip(key, result):
            result_dict[key] = value
        return result_dict

# Add all REST definitions here
api.add_resource(Case, '/cases/<case_id>')
api.add_resource(CaseList, '/cases')
# api.add_resource(CasesByCounty, '/counties/<county_id>/cases')
# api.add_resource(CasesByNAICId3, '/naic_id_3/<naic_id_2>/cases')


if __name__ == '__main__':
    app.run()
