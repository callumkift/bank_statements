#!/usr/bin/env python
"""
Contains methods that calls and connects to the database.
"""

import sqlite3
import os


def createdb(dtt):
    """
    Creates database and tables if the database does not exist.
    :param dtt: List of default transaction types
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

        add_default_tt(dtt)

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


def add_default_tt(dtt):
    """
    Adds default values into TransactionType table
    :param dtt: List of default transaction types
    :return:
    """
    conn = connect()
    c = conn.cursor()

    for i in range(len(dtt)):
        c.execute("INSERT INTO TransactionType(type) VALUES(?)", (dtt[i],))

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

    for i in range(20):
        des = trans_list[i][1]
        amo = trans_list[i][3]
        bal = trans_list[i][4]
        dt = trans_list[i][5].isoformat()


        # Check if a similar transaction has happened before
        c.execute("SELECT * FROM TransactionPlace WHERE description = (?) LIMIT 1", (des,))
        tp_return = c.fetchall()

        if len(tp_return) == 0:
            # No similar transaction
            if amo > 0.0:
                # Automatically designates Money In if amount is positive.
                mi = "Money In"

                c.execute("SELECT id FROM TransactionType WHERE type = (?)", (mi,))
                tt_id = c.fetchall()[0][0]

                # Adds transaction to database
                c.execute("INSERT INTO TransactionPlace(tt_id, description) VALUES(?,?)", (tt_id, des,))
                conn.commit()
                c.execute("SELECT id FROM TransactionPlace WHERE id = (SELECT MAX(id) FROM TransactionPlace)")
                tp_id = c.fetchall()[0][0]
                c.execute('''INSERT INTO TransactionInfo(tt_id, tp_id, date, amount, balance)
                                    VALUES(?,?,?,?,?)''', (tt_id, tp_id, dt, amo, bal,))
                conn.commit()
            else:
                print "\nNo description match for: %s, %.2f" % (des, amo)
                # Need user to add transaction type
                c.execute("SELECT * FROM TransactionType")
                tt_in_db = c.fetchall()

                print "System does not know what type of transaction this is. \nHere are the current types:"
                for i in range(len(tt_in_db)):
                    print "%2d %s" % (tt_in_db[i][0], tt_in_db[i][1])
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
                        c.execute("INSERT INTO TransactionType(type) VALUES(?)", (user_type,))
                        conn.commit()
                        c.execute("SELECT id FROM TransactionPlace WHERE id = (SELECT MAX(id) FROM TransactionPlace)")
                        tt_id = c.fetchall()[0][0]
                        print "\nNew type added\n"
                        break

                # Adds transaction to database
                c.execute("INSERT INTO TransactionPlace(tt_id, description) VALUES(?,?)", (tt_id, des,))
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
                # Adds transaction to database if it does not exist.
                c.execute('''INSERT INTO TransactionInfo(tt_id, tp_id, date, amount, balance)
                                VALUES(?,?,?,?,?)''', (tt_id, tp_id, dt, amo, bal,))
                conn.commit()

    conn.close()

    return


def getgeneral(tt2show):
    """
    Collects date, amount and type transaction-info from the DB for the types given in parameter
    :param tt2show: Transaction types to get data for
    :return: List of all data for each of the given types.
    """
    conn = connect()
    c = conn.cursor()

    gen_return = []

    for i in range(len(tt2show)):

        c.execute(
            '''SELECT TransactionInfo.date, TransactionInfo.amount, TransactionType.type
                FROM TransactionInfo JOIN TransactionType
                ON TransactionInfo.tt_id = TransactionType.id
                WHERE TransactionType.type = (?)''', (tt2show[i],))

        gen_return.append(c.fetchall())

    return gen_return
