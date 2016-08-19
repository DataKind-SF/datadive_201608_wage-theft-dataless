import csv
import logging
from io import open
import sqlite3
import sys
file_name = sys.argv[1]
if len(file_name) == 0:
    raise Exception("No filename given as a paramater")

table_name = sys.argv[2]
if len(table_name) == 0:
    raise Exception("No table name given as a paramater")

primary_key = sys.argv[3]
if len(table_name) == 0:
    raise Exception("No primary key given as a paramater")
        
def _get_col_datatypes(fin):
    dr = csv.DictReader(fin) # comma is default delimiter
    fieldTypes = {}
    for entry in dr:
        feildslLeft = [f for f in dr.fieldnames if f not in fieldTypes.keys()]
        if not feildslLeft: break # We're done
        for field in feildslLeft:
            data = entry[field]

            # Need data to decide
            if len(data) == 0:
                continue

            if data.isdigit():
                fieldTypes[field] = "INTEGER"
            else:
                fieldTypes[field] = "TEXT"
        # TODO: Currently there's no support for DATE in sqllite

    if len(feildslLeft) > 0:
        raise Exception("Failed to find all the columns data types - Maybe some are empty?")

    return fieldTypes

def escapingGenerator(f):
    for line in f:
        yield line.encode("ascii", "xmlcharrefreplace").decode("ascii")

def csvToDb(csvFile, tableName, primary_key, outputToFile=False):

    with open(csvFile, mode='r', encoding="ISO-8859-1") as fin:
        dt = _get_col_datatypes(fin)

        fin.seek(0)

        reader = csv.DictReader(fin)

        # Keep the order of the columns name just as in the CSV
        fields = reader.fieldnames
        cols = []

        # Set field and type
        for f in fields:
            if (f == primary_key):
                cols.append("%s %s PRIMARY KEY" % (f, dt[f]))
            else:
                cols.append("%s %s" % (f, dt[f]))

        # Generate create table statement:
        stmt = "CREATE TABLE " + tableName + " (%s)" % ",".join(cols)

        if outputToFile:
            con = sqlite3.connect(outputToFile)
        else:
            con = sqlite3.connect(":memory")
        cur = con.cursor()
        cur.execute(stmt)

        fin.seek(0)


        reader = csv.reader(escapingGenerator(fin))
        reader.next() # Skip first line


        # Generate insert statement:
        stmt = "INSERT INTO " + tableName + " VALUES(%s);" % ','.join('?' * len(cols))

        cur.executemany(stmt, reader)
        con.commit()
        con.close()

    return con

if __name__ == "__main__":
    path = ("../") # path = ('/Users/brian/Dropbox/datadive_wagetheft/data/') #TODO: Move to configure
    csvToDb(csvFile=path+file_name, 
            tableName=table_name, 
            primary_key=primary_key, 
            outputToFile="./db.sqlite")
