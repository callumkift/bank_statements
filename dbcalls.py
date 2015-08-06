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

        conn = connect()
        c = conn.cursor()

        c.execute("CREATE TABLE TransactionType(id INTEGER PRIMARY KEY, type TEXT, UNIQUE(type))")

        c.execute('''CREATE TABLE TransactionPlace(id INTEGER PRIMARY KEY, tt_id INTEGER, description TEXT,
                        FOREIGN KEY(tt_id) REFERENCES TransactionType(id))''')

        c.execute('''CREATE TABLE TransactionInfo(id INTEGER PRIMARY KEY, tt_id INTEGER, tp_id INTEGER, date TEXT,
                        amount REAL, balance REAL, FOREIGN KEY(tt_id) REFERENCES TransactionType(id),
                        FOREIGN KEY(tp_id) REFERENCES TransactionPlace(id))''')
        conn.commit()
        conn.close()

        print "check - db and tables created"

        add_default_tt()

        return


def connect():
    """
    Connects to database
    :return: connection to sqlite database
    """
    dbname = "TransactionDB.sqlite"
    path2dir = "/Users/callumkift/dev_projects/nordea_banking/"
    path2db = path2dir + dbname

    return sqlite3.connect(path2db)


def add_default_tt():
    """
    Adds default values into TransactionType table
    :param db: Database to connect to
    :return:
    """
    d_tt = ["Supermarket", "ATM", "Kiosk", "Shopping", "Night Out", "Transport", "Money In",
            "House", "Misc"]  # List of default transaction types
    conn = connect()
    c = conn.cursor()

    for i in range(len(d_tt)):
        c.execute("INSERT INTO TransactionType(type) VALUES(?)", (d_tt[i],))

    conn.commit()
    conn.close()
    return


def add2db(trans_list):
    """
    Adds info into db. Checks to see if transaction already exists.
    :param trans_list: List of transaction data
    :return:
    """
    nt = len(trans_list)

    conn = connect()
    c = conn.cursor()

    for i in range(nt):
        des = trans_list[i][1]
        amo = trans_list[i][3]
        bal = trans_list[i][4]
        dt = trans_list[i][5].isoformat()

        # Check if a similar transaction has happened before
        c.execute("SELECT * FROM TransactionPlace WHERE description = (?) LIMIT 1", (des,))
        tp_return = c.fetchall()

        if len(tp_return) == 0:
            # No similar transaction
            print "\nNo description match for: %s" % des
            # Need user to add transaction type
            c.execute("SELECT * FROM TransactionType")
            tt_in_db = c.fetchall()

            print "System does not know what type of transaction this is. Here are the current types:"
            for i in range(len(tt_in_db)):
                print tt_in_db[i][0], tt_in_db[i][1]
            # User picks existing type of transaction or adds new type
            while True:
                user_type = raw_input("\nPlease choose corresponding number or add new type name: ")
                try:
                    tt_num = int(user_type)
                    if tt_num <= tt_in_db[-1][0] and tt_num > 0:
                        tt_id = tt_num
                        break
                    else:
                        print "Incorrect number input"
                except ValueError as e:
                    c.execute("INSERT INTO TransactionType(type) VALUES(?)", (user_type, ))
                    conn.commit()
                    c.execute("SELECT id FROM TransactionPlace WHERE id = (SELECT MAX(id) FROM TransactionPlace)")
                    tt_id = c.fetchall()[0][0]
                    print "\nnew type\n"
                    break

            # Adds transaction to database
            c.execute("INSERT INTO TransactionPlace(tt_id, description) VALUES(?,?)", (tt_id, des, ))
            conn.commit()
            c.execute("SELECT id FROM TransactionPlace WHERE id = (SELECT MAX(id) FROM TransactionPlace)")
            tp_id = c.fetchall()[0][0]
            c.execute('''INSERT INTO TransactionInfo(tt_id, tp_id, date, amount, balance)
                                VALUES(?,?,?,?,?)''', (tt_id, tp_id, dt, amo, bal,))
            conn.commit()


        else:
            # Similar transaction exists
            tp_id = tp_return[0][0]
            tt_id = tp_return[0][1]

            # check if exact transaction exists, so that it doesn't duplicate transaction

            c.execute('''SELECT * FROM TransactionInfo
                            WHERE date = (?)
                            AND amount = (?)
                            AND balance = (?)''', (dt, amo, bal,))

            ti_return = c.fetchall()

            if len(ti_return) == 0:
                # Adds transaction to database
                c.execute('''INSERT INTO TransactionInfo(tt_id, tp_id, date, amount, balance)
                                VALUES(?,?,?,?,?)''', (tt_id, tp_id, dt, amo, bal,))
                conn.commit()
            else:
                # Ignores transaction
                print "Transaction already exists."

    conn.close()

    return
