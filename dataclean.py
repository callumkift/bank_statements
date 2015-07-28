#!/usr/bin/env python
import datetime as dt

def formatlist(form_list):
    """
    Formats and cleans up the transactions data.
    :param form_list: A list of transactions.
    :return: The transaction list with cleaned up data.
    """

    res_elements = []

    for i in range(len(form_list)):
        # Identifies reserved transactions
        if form_list[i][0] == "Reserveret":
            res_elements.append(i)
        else:
            formatdate(form_list[i])

    res_elements.reverse()
    # Reversed so that it deletes the correct elements

    # Removes reserved transactions
    for j in range(len(res_elements)):
        del form_list[res_elements[j]]

    return form_list


def formatdate(trans_element):
    """
    Formats the date elements. Strings -> datetime.date()
    :param trans_element: Individual transaction
    :return: Transaction element
    """

    date1 = trans_element[0].split("-")
    date2 = trans_element[2].split("-")

    trans_element[0] = dt.date(int(date1[2]), int(date1[1]), int(date1[0]))
    trans_element[2] = dt.date(int(date2[2]), int(date2[1]), int(date2[0]))

    return trans_element



def cleanlist():

    return