#!/usr/bin/env python

from json import dumps

from flask import Flask, request, Response
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
        stmt = "select * from cases limit 10" # temp limit, can update
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
        stmt = "select * from cases"
        if (case_id is not None):
            stmt += " where [Case ID]=" + str(case_id)
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
        stmt = "select * from cases"
        if (zip_cd is not None):
            stmt += " where [Zip Code]=" + str(zip_cd)
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
        stmt = "select * from cases"
        if (naic_cd is not None):
            stmt += " where [Full NAICS Code]=" + str(naic_cd)
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

class CountySummaries(Resource):
    def get(self, naic_cd=None):
        conn = e.connect()
        stmt = """SELECT [Combined State County FIPS], 
        Sum(Backwages) as Backwages, Sum([Employees Owed Backwages]) as [Employees Owed Backwages],
        Sum([Civil Money Penalties]) as [Civil Money Penalties], County
        FROM cases
        WHERE [Combined State County FIPS] IS NOT NULL
        GROUP BY [Combined State County FIPS], County
        ORDER BY Backwages Desc;"""
        

        query = conn.execute(stmt)
        rows = query.cursor.fetchall()
        keys = [member[0] for member in query.cursor.description]
        print keys, rows

        return_result = []
        
        import cStringIO, csv
        dest = cStringIO.StringIO()
        writer = csv.writer(dest)

        #WRITE THE CSV FILE IN THE FORMAT WE NEED. CURRENTLY WE DON'T HAVE total_pop SO
        #FOR NOW I'M SUBSTITUTING CMPs AS A PLACEHOLDER.
        writer.writerow(['id', 'wages', 'count', 'total_pop', 'name'])
        
        writer.writerows(rows)

            
        return Response(dest.getvalue(), mimetype='text/csv')           
        dest.close()
            
#       return return_result

# Add all REST definitions here
api.add_resource(Case, '/cases/<case_id>')
api.add_resource(CaseList, '/cases')
api.add_resource(CasesByZip, '/zip_cd/<zip_cd>/cases')
api.add_resource(CasesByNAICCd, '/naic_cd/<naic_cd>/cases')
api.add_resource(CountySummaries, '/counties')

if __name__ == '__main__':
    app.run()