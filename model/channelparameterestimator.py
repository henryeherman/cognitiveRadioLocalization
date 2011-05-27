#!/usr/bin/env python
# encoding: utf-8
"""
channelparameterestimator.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
from utils.units import meter2cm
import numpy
from scipy import optimize


class ChanParamEst(object):
    def __init__(self, events, etabounds, kappabounds):
        self.lowerEtaBound=etabounds[0]
        self.upperEtaBound=etabounds[1]
        self.upperKappaBound=kappabounds[1]
        self.lowerKappaBound=kappabounds[0]
        self.events = events
    
    def getParams(self, txnode, rxnode):
        e = self.events.findTXRXEventsByNode(txnode,rxnode)
        return e
    
#diffpwr is txpwr-rxpwr
def estDistance(kappa, eta, diffpwr, d0=1):
    return meter2cm(d0*np.exp((diffpwr+K)/10*eta))

v0 = [-35, 2]
fp = lambda v, x: estDistance(v[0],v[1],x)





if __name__ == '__main__':
    unittest.main()
