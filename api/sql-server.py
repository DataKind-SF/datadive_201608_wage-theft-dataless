from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.

e = create_engine('sqlite:///./db.sqlite')

app = Flask(__name__)
api = Api(app)

class Whd(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from whd_whisard limit 10")
        result = query.cursor.fetchall()
        keys = result[0]
        rows = result[1:]

        # keys.times(len(rows))
        # return [zip(keys.repeat(len(rows)), rows)]
        # return [ {key : v} for row in rows for key,v in keys, row ]
        # return { keys[i]: [rows[j][i] for j in range(len(rows))] for i in range(len(rows))}
        return [ {k : v} for i in range(len(rows)) for k,v in zip(keys, rows[i])  ]


        # return {'cases': [i for i in query.cursor.fetchall()]}

api.add_resource(Whd, '/cases')

if __name__ == '__main__':
    app.run()
