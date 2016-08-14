Wage Theft API
====

Setup Checklist
-----
1. Get data (from dropbox)
2. Clone repo
3. Setup env from `python_requirements.txt`

To Create the Database
----
1. Run `csv-to-sqlite3` to setup DB (if not in GitHub)
  There are 4 parameters you need to specify:
  - csvFile: path to the csv file you want to convert to the sqlite DB
  - tableName: what table you want the csv file to be called in the DB
  - primary_key: the column that contains unique values you want to make your primary key
  - outputToFile: path to sqlite file

To start the server
----
1. Set up `export $FLASK_APP= sql-server.py`
2. Run `python -m flask run` from the `api/` directory
3. Query the data via REST `http://127.0.0.1:5000/cases/1513023`

TODOS
----
- [ ] play with api
- add to the api