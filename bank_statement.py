#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  This script was created so that one can analyse their bank statements.
#
#  Creator: Callum Kift
#  email: callumkift@gmail.com
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

import readcsv
import dataclean
import dbcalls as dbc
import infovisualisation as iv

if __name__ == '__main__':
    path2csv = "/Users/callumkift/dev_projects/"

    dtt = ["Supermarket", "ATM", "Kiosk", "Shopping", "Night Out", "Food", "Transport", "Money In",
           "House", "Rent and Bills", "Hobbies", "Misc"]  # List of default transaction types

    dbc.createdb(dtt)

    csvfiles = readcsv.findcsvfiles(path2csv)  # List of paths to CSV files
    translist = readcsv.readcsvfiles(csvfiles)  # List of transactions from all CSV files

    cleanlist = dataclean.formatlist(translist)  # Cleans up the transaction data

    dbc.add2db(cleanlist)

    # TEST

    # dbname = "TransactionDB.sqlite"
    # path2dir = "/Users/callumkift/dev_projects/nordea_banking/"
    # path2db = path2dir + dbname
    #
    # conn = sqlite3.connect(path2db)
    # c = conn.cursor()
    #
    # c.execute("SELECT * FROM TransactionInfo")
    # stuff = c.fetchall()
    # conn.close()
    #
    # stuff_added = len(stuff)
    #
    # print "Number of transactions read from CSVs: %d" % len(cleanlist)
    # print "Number of transactions in DB: %d\n" % stuff_added
    #
    # for i in range(stuff_added):
    #     print stuff[i]

    # tt2show = ["Supermarket", "Kiosk", "Shopping", "Night Out", "Food", "Transport", "House", "Rent and Bills"]

    iv.generalview()
