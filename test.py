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
    def estDistance(kappa, eta, rxpwr, txpwr, d0=1.0):
        return meter2cm(d0*np.exp((txpwr-rxpwr+kappa)/(10.0*eta)))
    
    def estPwr(kappa, eta, d, ptx=4, d0=1.0):
        return ptx+kappa-10*eta*np.log10(d/d0)


    v0 = [-35.0, 2.0]
    fp = lambda v,x,y: estDistance(v[0],v[1],x,y)

    e = lambda v,x,y,z: (fp(v,x,y)-z)

    fig1 = pyplot.figure(1)
    fig1.show()

    dps, rxp = dp.events.getAvgRXPwrByDistance()
    dps, txp = dp.events.getAvgTXPwrByDistance()    
    v, success = leastsq(e, v0, args=(rxp,txp,dps), maxfev=10000)
    pyplot.figure(1)

    ds = dp.events.distances
    rxpwrs = dp.events.rxpwrs
    pyplot.scatter(dp.events.distances, dp.events.rxpwrs)
    pyplot.plot(dps, rxp, c='r')  
    pyplot.scatter(dps,rxp,c='r')

    
    ds = np.array(100,1000,5)
    
    kappa, eta = v
    
    estrx = estPwr(kappa,eta,ds)

    pyplot.plot(ds,estrx,c='g')

