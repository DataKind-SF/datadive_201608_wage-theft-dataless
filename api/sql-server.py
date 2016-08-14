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
        stmt = "select * from whd_whisard limit 10" # temp limit, can update
        query = conn.execute(stmt)
        rows = query.cursor.fetchall()
        keys = [member[0] for member in query.cursor.description] # get all column names

        return_result = []

        for row in rows:
            result_dict = {}
            for key, value in zip(keys, row): # column_name, column_value
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
        key = [member[0] for member in query.cursor.description]
        result_dict = {}
        print key

        for key, value in zip(key, result):
            result_dict[key] = value
        return result_dict

class CasesByZip(Resource):
    def get(self, zip_cd=None):
        conn = e.connect()
        stmt = "select * from whd_whisard"
        if (zip_cd is not None):
            stmt += " where zip_cd=" + str(zip_cd)
        query = conn.execute(stmt)
        rows = query.cursor.fetchall()
        keys = [member[0] for member in query.cursor.description]
        print keys, rows

        return_result = []

        for row in rows:
            result_dict = {}
            for key, value in zip(keys, row):
                result_dict[key] = value
            return_result.append(result_dict)

        return return_result

class CasesByNAICCd(Resource):
    def get(self, naic_cd=None):
        conn = e.connect()
        stmt = "select * from whd_whisard"
        if (naic_cd is not None):
            stmt += " where naic_cd=" + str(naic_cd)
        query = conn.execute(stmt)
        rows = query.cursor.fetchall()
        keys = [member[0] for member in query.cursor.description]
        print keys, rows

        return_result = []

        for row in rows:
            result_dict = {}
            for key, value in zip(keys, row):
                result_dict[key] = value
            return_result.append(result_dict)

        return return_result

# Add all REST definitions here
api.add_resource(Case, '/cases/<case_id>')
api.add_resource(CaseList, '/cases')
api.add_resource(CasesByZip, '/zip_cd/<zip_cd>/cases')
api.add_resource(CasesByNAICCd, '/naic_cd/<naic_cd>/cases')


if __name__ == '__main__':
    app.run()