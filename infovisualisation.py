#!/usr/bin/env python
"""
Contains methods that deal with visualisation of info.
"""

import matplotlib.pyplot as plt
import dbcalls as dbc

def generalview(tt2s):
    # Create general overview

    trans_data = dbc.getgeneral(tt2s)


    print trans_data
    return