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
    dp = DatasetParser(args.filename)


if __name__ == '__main__':
    args = parser.parse_args()
    dp = DatasetParser(args.filename)
    p = cpe.ChanParamEst(dp.events)
    
    if args.doPlot is True:
        p.plot()
        
    if args.ofilename is not None:
        d = shelve.open(args.ofilename)
        d['kappa'] = p.kappa
        d['eta'] = p.eta
        d.close()
    """
    def estDistance(kappa, eta, rxpwr, txpwr, d0=1.0):
        return meter2cm(d0*np.exp((txpwr-rxpwr+kappa)/(10.0*eta)))
    
    def estPwr(kappa, eta, d, ptx=4, d0=1.0):
        d = cm2meter(d)
        return ptx+kappa-10*eta*np.log(d/d0)


    v0 = [-50.0, 2.0]
    fp = lambda v,x,y: estDistance(v[0],v[1],x,y)

    e = lambda v,x,y,z: (fp(v,x,y)-z)

    fig1 = pyplot.figure(1)
    fig1.show()
    
    dps, rxp = dp.events.getAvgRXPwrByDistance()
    dps, txp = dp.events.getAvgTXPwrByDistance()    
    v, success = leastsq(e, v0, args=(rxp,txp,dps), maxfev=10000)

    ds = dp.events.distances
    rxpwrs = dp.events.rxpwrs
    pyplot.scatter(dp.events.distances, dp.events.rxpwrs)
    pyplot.plot(dps, rxp, c='r')  
    pyplot.scatter(dps,rxp,c='r')

    
    ds = np.arange(100,1300,5)
    
    kappa, eta = v
    
    estrx = estPwr(kappa,eta,ds)
    
    pyplot.plot(ds,estrx,c='g', linewidth=5)
    """
    print "KAPPA = %5.3f, ETA= %5.3f" % (p.kappa,p.eta) 
    raw_input("Press key to continue")
