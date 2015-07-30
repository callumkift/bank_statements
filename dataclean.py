#!/usr/bin/env python
"""
Contains methods that deal with the cleaning of the data from the CSV files.
"""

import datetime as dt
import re
import string


def formatlist(form_list):
    """
    Formats and cleans up the transactions data.
    :param form_list: A list of transactions.
    :return: The transaction list with cleaned up data.
    """

    res_elements = []
    reserved = "Reserveret"

    for i in range(len(form_list)):
        # Identifies reserved transactions
        if form_list[i][0] == reserved:
            res_elements.append(i)
        else:
            formatdate(form_list[i])
            acttranstime(form_list[i])
            cleandescription(form_list[i])

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

    trans_element[0] = dt.datetime(int(date1[2]), int(date1[1]), int(date1[0]))
    trans_element[2] = dt.datetime(int(date2[2]), int(date2[1]), int(date2[0]))

    return trans_element


def acttranstime(trans_element):
    """
    In the transaction description is the true transaction datetime. This is removed from the description
    and added as a new element to the transaction. If the true datetime does not exist, then the recorded
    transaction time is the added element.
    is added.
    :param trans_element: Individual transaction
    :return: Individual transaction with added true transaction datetime
    """

    pte = filter(lambda x: x in string.printable, trans_element[1])

    ft = re.findall(r"\w{3}\s\d{2}\.\d{2}.{1,2}\w{2}\.\s\d{2}\.\d{2}.*", pte)
    if len(ft) == 0:
        ft = re.findall(r"\w{3}\s\d{2}\.\d{2}.*", pte)

    if ft:
        att = ft[0]
        pte = pte.replace(att, "")
        trans_element.append(format_att(att, trans_element[0]))
    else:
        trans_element.append(trans_element[0])

    trans_element[1] = pte

    return trans_element


def format_att(unformat_dt, rec_dt):
    """
    Formats the true datetime of the transaction from string.
    :param unformat_dt: String with the unformated datetime and extra characters.
    :param rec_dt: Datetime of recorded transaction
    :return: True datetime of transaction.
    """

    year = rec_dt.year
    fd = re.findall(r"\d{2}", unformat_dt)

    if len(fd) == 2:
        # If only date is included
        return dt.datetime(year, int(fd[1]), int(fd[0]))
    elif len(fd) == 4:
        # If time is also included
        return dt.datetime(year, int(fd[1]), int(fd[0]), int(fd[2]), int(fd[3]))
    else:
        return rec_dt


def cleandescription(trans_element):
    """
    Cleans up the transaction description
    :param trans_element: Individual transaction
    :return: Cleaned up individual transaction
    """
    
    trans_descr = trans_element[1].rstrip()
    npk = "Nordea pay kb"
    np = "Nordea pay"

    if npk in trans_descr:
        trans_descr = trans_descr.replace(npk, "")
    if np in trans_descr:
        trans_descr = trans_descr.replace(np, "")

    trans_descr = re.sub(r"[\.\,]", "", trans_descr)

    trans_descr = re.sub(r"\s+", " ", trans_descr)

    trans_element[1] = trans_descr.strip()

    return trans_element
