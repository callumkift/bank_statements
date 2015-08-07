#!/usr/bin/env python
"""
Contains methods that deal with visualisation of info.
"""

import matplotlib.pyplot as plt
import pylab as P
import datetime as dt
import numpy as np
import dbcalls as dbc


def generalview(tt2s):
    # Create general overview
    now = dt.datetime.now()
    lastmonthmonth = now.month - 1
    lastmonthyear = now.year

    trans_data_dict = dbc.getgeneral(tt2s)

    # Changes dictionary items to key = [last month amount, total amount]
    for key, value in trans_data_dict.iteritems():
        vdate, vamount = zip(*value)
        total_amount = np.sum(vamount)
        month_amount = 0

        for i in range(len(vdate)):
            date = dt.datetime.strptime(vdate[i], "%Y-%m-%dT%H:%M:%S")
            if date.month == lastmonthmonth and date.year == lastmonthyear:
                month_amount += vamount[i]

        trans_data_dict[key] = [abs(month_amount), abs(total_amount)]


    # Making Pie Chart

    labels = []
    mspend = []
    tspend = []

    for key, values in trans_data_dict.iteritems():
        labels.append(key)
        mspend.append(values[0])
        tspend.append(values[1])

    fig, axarr = plt.subplots(1,2)

    ind = np.arange(len(labels))
    width = 0.8

    axarr[0].bar(ind, mspend, color="red")
    axarr[0].set_xticks(ind + (width / 2))
    axarr[0].set_xticklabels(labels, rotation=45)
    axarr[0].set_ylabel("Amount Spent DKK")
    axarr[0].set_title("Monthly Spend")

    axarr[1].bar(ind, tspend, color="green")
    axarr[1].set_xticks(ind + (width / 2))
    axarr[1].set_xticklabels(labels, rotation=45)
    axarr[1].set_ylabel("Amount Spent DKK")
    axarr[1].set_title("Total Spend")

    plt.suptitle("Spending Types")
    plt.show()
    return
