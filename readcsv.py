#!/usr/bin/env python

import os

def findcsvfiles(path2files):

    csvfiles = []

    if os.path.isdir(path2files):
        for file in os.listdir(path2files):
            if file.endswith(".csv"):
                csvfiles.append(path2files + "")
    else:
        print "Error: Directory does not exist."
    return