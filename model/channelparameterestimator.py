#!/usr/bin/env python
# encoding: utf-8
"""
channelparameterestimator.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import shelve
from utils.units import meter2cm, cm2meter
import numpy as np
from scipy import optimize
from scipy.optimize import leastsq
from matplotlib import pyplot
from utils.logger import logger
from channelmodel import ChannelModel



class ChanParamEst(object):
    def __init__(self, events, estkappa=-35.0, esteta=2.0, maxloop=1000):
        self.estkappa = estkappa
        self.esteta = esteta
        self.eta = self.esteta
        self.kappa = self.estkappa
        self.events = events
        self.maxloop = maxloop

        self.fp = lambda v,x,y: ChannelModel.estDistance(v[0],v[1],x,y)
        self.err = lambda v,x,y,z: (self.fp(v,x,y)-z)
        self.v0 = [self.estkappa, self.esteta]
        logger.info("Sorting By Distance")
        self._sortByDistance()
        logger.info("Calculating Optimized Parameters")
        self._optimizeParams()
            
    def _sortByDistance(self): 
        self.dps, self.rxp = self.events.getAvgRXPwrByDistance()
        dps, self.txp = self.events.getAvgTXPwrByDistance()
        
    def _optimizeParams(self):
        v, success = leastsq(self.err, self.v0, args=(self.rxp,self.txp,self.dps), maxfev=self.maxloop)
        self.kappa = v[0]
        self.eta = v[1]

    def plot(self):
        logger.info("Plotting Data")
        self.fig1 = pyplot.figure(1)
        self.fig1.show()
        rxpwrs = self.events.rxpwrs
        pyplot.scatter(self.events.distances, self.events.rxpwrs)
        pyplot.plot(self.dps, self.rxp, c='r')  
        pyplot.scatter(self.dps,self.rxp,c='r')
        ds = np.arange(100,1300,5)
        estrx = ChannelModel.estPwr(self.kappa,self.eta,ds)
        pyplot.plot(ds,estrx,c='g', linewidth=3)


if __name__ == '__main__':
    pass
