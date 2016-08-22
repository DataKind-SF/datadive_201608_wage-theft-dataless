#!/usr/bin/env python

from json import dumps

from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine

from flask_restful import reqparse


# Create a engine for connecting to SQLite3.

e = create_engine('sqlite:///./db.sqlite')

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('return_format', type=str, help='csv is currently the only valid input')


class CaseList(Resource):
    def get(self):
        conn = e.connect()
        stmt = "select * from cases limit 10" # temp limit, can update

        return get_data(sql_query = stmt)
    
class Case(Resource):
    def get(self, case_id=None):

        stmt = "select * from cases"
        if (case_id is not None):
            stmt += " where [Case ID]=" + str(case_id)

        return get_data(sql_query = stmt)

class CasesByZip(Resource):
    def get(self, zip_cd=None):

        stmt = "select * from cases"
        if (zip_cd is not None):
            stmt += " where [Zip Code]=" + str(zip_cd)

        return get_data(sql_query = stmt)
    
class CasesByNAICCd(Resource):
    def get(self, naic_cd=None):
        stmt = "select * from cases"
        if (naic_cd is not None):
            stmt += " where [Full NAICS Code]=" + str(naic_cd)
        
        return get_data(sql_query = stmt)
# Returns a summary for all counties of the backwages, number of employees owed backwages, and civil money penalties
# found due in each county
class CountiesSummary(Resource):
    def get(self):
        stmt = """SELECT [Combined State County FIPS], 
        Sum(Backwages) as Backwages, Sum([Employees Owed Backwages]) as [Employees Owed Backwages],
        Sum([Civil Money Penalties]) as [Civil Money Penalties], County
        FROM cases
        WHERE [Combined State County FIPS] IS NOT NULL
        GROUP BY [Combined State County FIPS], County
        ORDER BY Backwages Desc;"""
        
        args = parser.parse_args()
        if args['return_format'] == "csv":
            
            # TODO: currently we don't have data for the total_pop column in the view
            # so for now I'm substituting CMPs as a placeholder
            csv_string = get_data_csv(sql_query = stmt, column_headers = ['id', 'wages', 'count', 'total_pop', 'name'])
            return Response(csv_string, mimetype='text/csv')           
        else:
            return get_data(sql_query = stmt)


# Returns a summary for all the states of the backwages, number of employees owed backwages, and civil money penalties
# found due in each state     
class StatesSummary(Resource):
    def get(self):
        stmt = """SELECT [State FIPS Code], [State], Sum([Civil Money Penalties]) as [Civil Money Penalties], 
            Sum(Backwages) as Backwages, Sum([Employees Owed Backwages]) as [Employees Owed Backwages]
            FROM cases
            WHERE [State] IS NOT NULL
            GROUP BY [State FIPS Code], [State]
            ORDER BY Backwages Desc;"""
        
        args = parser.parse_args()
        if args['return_format'] == "csv":
            csv_string = get_data_csv(sql_query = stmt, column_headers = ['State FIPS Code', 'State', 'Civil Money Penalties', 'Backwages', 'Employees Owed Backwages'])
            return Response(csv_string, mimetype='text/csv')           
        else:
            return get_data(sql_query = stmt)
         
          
# This is a general function that takes as its input a SQL query string and returns
# a data structure containing the results of that query.
def get_data(sql_query):
    conn = e.connect()
    query = conn.execute(sql_query)
    rows = query.cursor.fetchall()
    keys = [member[0] for member in query.cursor.description]

    results = []

    for row in rows:
        result_dict = {}
        for key, value in zip(keys, row): # column_name, column_value
            result_dict[key] = value
        results.append(result_dict)
    
    return results


# This is a general function that takes as its input a SQL query string and
# a list of the column headers and returns a string that contains the contents of
# a CSV file.
def get_data_csv(sql_query, column_headers):

        conn = e.connect()

        query = conn.execute(sql_query)
        rows = query.cursor.fetchall()
        keys = [member[0] for member in query.cursor.description]
        print keys, rows

        return_result = []
        
        import cStringIO, csv
        dest = cStringIO.StringIO()
        writer = csv.writer(dest)

        writer.writerow(column_headers)
        
        writer.writerows(rows)
        return_string = dest.getvalue()
        dest.close()
        
        return return_string
   

# Add all REST definitions here
api.add_resource(Case, '/cases/<case_id>')
api.add_resource(CaseList, '/cases')
api.add_resource(CasesByZip, '/zip_cd/<zip_cd>/cases')
api.add_resource(CasesByNAICCd, '/naic_cd/<naic_cd>/cases')
api.add_resource(CountiesSummary, '/counties')
api.add_resource(StatesSummary, '/states')

if __name__ == '__main__':
    app.run()