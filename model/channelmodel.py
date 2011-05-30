#!/usr/bin/env python
# encoding: utf-8
"""
channelmodel.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import unittest
import numpy as np
from utils.logger import logger
from utils.units import meter2cm, cm2meter

"""
def estDistance(kappa, eta, rxpwr, txpwr, d0=1.0):
    return meter2cm(d0*np.exp((txpwr-rxpwr+kappa)/(10.0*eta)))

def estPwr(kappa, eta, d, ptx=4, d0=1.0):
    d = cm2meter(d)
    return ptx+kappa-10*eta*np.log(d/d0)
"""

class ChannelModel(object):
    def __init__(self, kappa, etta):
        self.kappa = kappa
        self.eta = etta
        
    @staticmethod
    def estDistance(kappa, eta,rxpwr, txpwr, d0=1.0):
        return meter2cm(d0*np.exp((txpwr-rxpwr+kappa)/(10.0*eta)))
    
    @staticmethod
    def estPwr(kappa,eta,d,ptx=4,d0=1.0):
        d = cm2meter(d)
        return ptx+kappa-10*eta*np.log(d/d0)
    
    def calcRadius(self, rxpwr, txpwr):
        return self.estDistance(self.kappa, self.eta, rxpwr, txpwr)


    
     

    
