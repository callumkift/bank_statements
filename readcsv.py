#!/usr/bin/env python

import os
import string

def findcsvfiles(path2files):
    """
    Method finds the CSV files to read and extract data.
    :param path2files: Path to directory that contains CSV files
    :return: A list of CSV files to read.
    """
    csvfiles = []

    if os.path.isdir(path2files):
        for file in os.listdir(path2files):
            if file.endswith(".csv"):
                csvfiles.append(path2files + str(file))

        if len(csvfiles) != 0:
            print "CSV files returned"
            return csvfiles
        else:
            print "Error - findcsvfiles(path2files): No CSV files found in given directory."
            return
    else:
        print "Error - findcsvfiles(path2files): Directory does not exist."
        return


def readcsvfiles(csvlist):
    """
    Reads CSV files and puts transaction data into a list
    :param csvlist: list of transaction data
    :return: csvlist
    """
    
    csvdata = []

    if len(csvlist) != 0:
        for i in range(len(csvlist)):
            print csvlist[i]
            edl = extractdata(csvlist[i])

            for i in range(len(edl)):
                csvdata.append(edl[i])

        return csvdata
    else:
        print "Error - readcsvfiles(csvlist): No CSV files in list. Are there CSV files in given directory?"
        return


def extractdata(csvfile):
    """
    Extracts the data from the CSV file
    :param csvfile: CSV file
    :return: A list containing transaction data
    """

    csvdata_pf = []

    if os.path.exists(csvfile):
        with open(csvfile, "r") as f:
            f.readline()
            f.readline()
            for line in f:
                line = line.strip()
                column = line.split(";")
                if len(column) == 5:
                    csvdata_pf.append([column[0], str(column[1]), column[2], float(string.replace(column[3], ",", ".")), float(string.replace(column[4], ",", "."))])
                    # column[0] date transaction was recorded
                    # column[1] merchant information
                    # column[2] date transaction cleared
                    # column[3] transaction sum
                    # column[4] balance of account
                else:
                    print "Error - extractdata(csvfile): Wrong number of columns. Check file format."
        return csvdata_pf
    else:
        print "Error - extractdata(csvfile): Cannot find CSV file."
        return
