#!/usr/bin/env python
"""
Contains methods that deal with visualisation of info.
"""

import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import dbcalls as dbc
import matplotlib.cm as cm


def generalview():
    # Create general overview
    now = dt.datetime.now()
    lastmonthmonth = now.month - 1
    lastmonthyear = now.year

    trans_data_dict = dbc.getgeneral()

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

    # Making Bar Chart
    labels = []
    mspend = []
    tspend = []

    m_in = 0
    t_in = 0

    for key, values in trans_data_dict.iteritems():
        if key != "Money In":
            labels.append(key)
            mspend.append(values[0])
            tspend.append(values[1])
        else:
            m_in = values[0]
            t_in = values[1]

    fig, axarr = plt.subplots(1, 2)

    ind = np.arange(len(labels))
    width = 0.8  # width of bar
    rot = 75  # Angle of text (x-axis)

    axarr[0].bar(ind, mspend, color="red")
    axarr[0].set_xticks(ind + (width / 2))
    axarr[0].set_xticklabels(labels, rotation=rot)
    axarr[0].set_ylabel("Amount Spent DKK")
    axarr[0].set_title(
        "Last Month (%d/%d) \n(Net In: %.2f DKK)" % (lastmonthmonth, lastmonthyear, m_in - np.sum(mspend)))

    axarr[1].bar(ind, tspend, color="green")
    axarr[1].set_xticks(ind + (width / 2))
    axarr[1].set_xticklabels(labels, rotation=rot)
    axarr[1].set_ylabel("Amount Spent DKK")
    axarr[1].set_title("Total Spend \n(Net In: %.2f DKK)" % (t_in - np.sum(tspend)))

    plt.suptitle("Where Money is Spent")
    plt.show()
    return


def dayview():
    """
    Plots a bar chart showing the spending per type of transaction per day.
    :return:
    """
    trans_data_dict = dbc.getgeneral()

    # Changes dictionary items to key = [monday_spend, tuesday_spend, wednesday_spend, etc.]
    for key, value in trans_data_dict.iteritems():
        vdate, vamount = zip(*value)
        mon_sum = 0
        tue_sum = 0
        wed_sum = 0
        thu_sum = 0
        fri_sum = 0
        sat_sum = 0
        sun_sum = 0

        for i in range(len(vdate)):
            date = dt.datetime.strptime(vdate[i], "%Y-%m-%dT%H:%M:%S")

            if date.weekday() == 0:
                mon_sum += vamount[i]
            elif date.weekday() == 1:
                tue_sum += vamount[i]
            elif date.weekday() == 2:
                wed_sum += vamount[i]
            elif date.weekday() == 3:
                thu_sum += vamount[i]
            elif date.weekday() == 4:
                fri_sum += vamount[i]
            elif date.weekday() == 5:
                sat_sum += vamount[i]
            elif date.weekday() == 6:
                sun_sum += vamount[i]

        trans_data_dict[key] = [abs(mon_sum), abs(tue_sum), abs(wed_sum), abs(thu_sum), abs(fri_sum), abs(sat_sum),
                                abs(sun_sum)]

    # Variables needed for graph
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]  # x-axis tick labels
    no_of_types = len(trans_data_dict.keys())  # number of transaction types
    ind = np.arange(len(days))  # index
    day_width = 0.95  # so that there is a gap between days
    width = day_width / no_of_types  # width of each type's bar
    colours = iter(cm.rainbow(np.linspace(0, 1, no_of_types)))  # Allows to automatically assign colours
    rot = 0  # Angle of text (x-axis)
    count = 0

    # Plotting
    ax = plt.subplot(111)
    for key, values in trans_data_dict.iteritems():
        if key != "Money In":
            ax.bar(ind + (count * width), values / np.sum(values), width, color=next(colours), label=key)
            count += 1
    ax.set_xticks(ind + (day_width / 2))

    ax.set_xticklabels(days, rotation=rot)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Normalised Spending")
    ax.set_title("Comparison Of Spending Type Per Day")

    # Shrink plot width to put legend outside
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.show()

    return
