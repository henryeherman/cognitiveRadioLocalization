#!/usr/bin/env python
# encoding: utf-8
"""
datasetParser.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import shelve
import argparse
from utils.datasetParser import DatasetParser 
from model import channelparameterestimator as ce
from scipy.optimize import leastsq
from utils.units import meter2cm, cm2meter
import numpy as np
from matplotlib import pyplot
from model import cpe

parser = argparse.ArgumentParser(description="Read in dataset and generate nodes")
parser.add_argument('-f', '--filename', dest='filename', action='store', required=True)
parser.add_argument('-o', '--output', dest='ofilename', action='store', required=False, default=None, help="Store Parameters in file")
parser.add_argument('-p', '--plot', dest='doPlot', action='store_true', help="Plot Data and fitted curve")


def main():
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        parser.print_usage()
        parser.exit(-1, "Dataset filename does not exist")

    dp = DatasetParser(args.filename)
    p = cpe.ChanParamEst(dp.events)
    
    if args.doPlot is True:
        p.plot()
        
    if args.ofilename is not None:
        try:
            d = shelve.open(args.ofilename)
            d['kappa'] = p.kappa
            d['eta'] = p.eta
            d.close()
        except:
            parser.print_usage()
            if os.path.exists(args.ofilename):            
                msg = "File %s is not a valid parameter storage file" % args.ofilename
            else:
                msg = "Unknown persistant channel parameters failed for file %s" % args.ofilename
            parser.exit(-1,msg)
                
    print "KAPPA = %5.3f, ETA= %5.3f" % (p.kappa,p.eta) 
    raw_input("Press key to continue")

if __name__ == '__main__':
    main()
