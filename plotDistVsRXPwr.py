#!/usr/bin/env python
# encoding: utf-8
"""
datasetParser.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import argparse
from utils.datasetParser import DatasetParser 
from model import channelparameterestimator as ce
from scipy.optimize import leastsq
from utils.units import meter2cm
import numpy as np
from matplotlib import pyplot

parser = argparse.ArgumentParser(description="Read in dataset and generate nodes")
parser.add_argument('-f', '--filename', dest='filename', action='store', required=True)

#note


def main():
    args = parser.parse_args()
    dp = DatasetParser(args.filename)


if __name__ == '__main__':
    args = parser.parse_args()
    dp = DatasetParser(args.filename)
    es = dp.events.findRXEvents(25)
    xs = es.txpwrs - es.rxpwrs
    ds = es.distances

    
    #diffpwr is txpwr-rxpwr
    def estDistance(kappa, eta, diffpwr, d0=1):
        return meter2cm(d0*np.exp((diffpwr+kappa)/(10.0*eta)))
    
    v0 = [-35.0, 2.0]
    fp = lambda v,x: estDistance(v[0],v[1],x)

    e = lambda v,x,y: (fp(v,x)-y)
    fig1 = pyplot.figure(1)
    fig1.show()
    for node in dp.nodes.nodes.values():
        es = dp.events.findRXEvents(node.id);pyplot.scatter(es.distances,es.rxpwrs)
        #raw_input("PAUSE")
    results = dp.events.getAvgRXPwrByDistance()
    pyplot.scatter(*results,c='r')
    pyplot.plot(*results, c='r')
    
    raw_input("Press key to exit"); 
    
