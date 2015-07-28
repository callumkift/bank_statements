#!/usr/bin/env python

def formatlist(form_list):

    a = rem_res(form_list)

    return a


def rem_res(res_list):
    """
    Removes transactions from list that have not gone through - they are reserved.
    :param res_list: A list of transactions.
    :return: The transaction list with reserved payments removed.
    """

    res_elements = []

    for i in range(len(res_list)):
        if res_list[i][0] == "Reserveret":
            res_elements.append(i)

    res_elements.reverse()
    # Reversed so that it deletes the correct elements

    for j in range(len(res_elements)):
        del res_list[res_elements[j]]

    return res_list



def cleanlist():

    return