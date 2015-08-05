#!/usr/bin/env python
"""
Contains methods that calls and connects to the database.
"""

import sqlite3
import os


def createdb():
    """
    Creates database and tables if the database does not exist.
    :return:
    """
    dbname = "TransactionDB.sqlite"
    path2dir = "/Users/callumkift/dev_projects/nordea_banking/"
    path2db = path2dir + dbname

    if os.path.exists(path2db):
        print "check - db exists"
        return
    else:

        conn = sqlite3.connect(path2db)
        c = conn.cursor()

        c.execute("CREATE TABLE TransactionType(id INTEGER PRIMARY KEY, type TEXT, UNIQUE(type))")

        c.execute('''CREATE TABLE TransactionPlace(id INTEGER PRIMARY KEY, tt_id INTEGER, description TEXT,
                        FOREIGN KEY(tt_id) REFERENCES TransactionType(id))''')

        c.execute('''CREATE TABLE TransactionInfo(id INTEGER PRIMARY KEY, tt_id INTEGER, tp_id INTEGER, date TEXT,
                        amount REAL, balance REAL, FOREIGN KEY(tt_id) REFERENCES TransactionType(id),
                        FOREIGN KEY(tp_id) REFERENCES TransactionPlace(id))''')
        conn.close()

        print "check - db and tables created"
        return
