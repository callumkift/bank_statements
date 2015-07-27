#!/usr/bin/env python

import os

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
            print "Error: No CSV files found in given directory."
            return
    else:
        print "Error: Directory does not exist."
        return

def readcsvfiles(csvlist):

    if len(csvlist) != 0:
        for i in range(len(csvlist)):
            print csvlist[i]
    else:
        print "Error: No CSV files in list. Are there CSV files in given directory?"
        return