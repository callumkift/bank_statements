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

    # mspend = []
    # tspend = []


    for key, values in trans_data_dict.iteritems():
        labels.append(key)
        mspend.append(values[0])
        tspend.append(values[1])

        # mspend.append([key, values[0]])
        # tspend.append([key, values[1]])

    # mspend = 100 * np.array(mspend) / np.sum(mspend)
    # tspend = 100 * np.array(tspend) / np.sum(tspend)
    #
    # for i in range(len(labels)):
    #     print labels[i], mspend[i], tspend[i]
    #
    # plt.pie(mspend, autopct='%1.1f%%', labeldistance=1.50)
    # plt.legend(loc=1)
    # plt.axis("equal")
    # plt.show()

    fig, ax = plt.subplots()

    ax.bar(np.arange(len(labels)), mspend)
    ax.set_xticklabels(labels, rotation=90)
    ax.set_ylabel("Amount Spent DKK")
    ax.set_title("Monthly Spend")
    plt.show()
    return
