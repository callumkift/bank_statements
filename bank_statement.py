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

import readfiles as rf
import dataclean as dclean
import dbcalls as dbc
import infovisualisation as iv

if __name__ == '__main__':
    path2csv = rf.getcsvpath()
    dtt = ["Supermarket", "ATM", "Kiosk", "Shopping", "Night Out", "Eating Out", "Transport", "Money In",
           "House", "Rent and Bills", "Hobbies", "Misc"]  # List of default transaction types

    dbc.createdb(dtt)

    csvfiles = rf.findcsvfiles(path2csv)  # List of paths to CSV files
    translist = rf.readcsvfiles(csvfiles)  # List of transactions from all CSV files
    cleanlist = dclean.formatlist(translist)  # Cleans up the transaction data

    dbc.add2db(cleanlist)
    iv.generalview()
    iv.dayview()
