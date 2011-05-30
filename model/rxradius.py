#!/usr/bin/env python
# encoding: utf-8
"""
rxradius.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import unittest
import numpy as np
from utils.logger import logger

class RadiusCalcError(Exception):
    pass


class Radius(object):
    def __init__(self, rxnode, txnode, r, rxpwr, txpwr):
        self.rxnode = rxnode
        self.r = r
        self.rxpwr = rxpwr
        
        self.txnode = txnode
        self.txpwr = txpwr
        
    def __repr__(self):
        return "<Radius(rxnode=%s, radius=%3.2f)>" % (self.rxnode.id, self.r) 
    def __str__(self):
        return self.__repr__()
    
    def getPos(self):
        return self.rxnode.pos

    pos = property(getPos)

class RadiusCalculator(object):

    def __init__(self, distfxn):
       self.distfxn = distfxn
       
    def getRadiusFromEvents(self, events):
        rxnodes = events.rxnodes
        txnodes = events.txnodes
        if len(rxnodes) == 0:
            return None        

        if not len(rxnodes)== 1:
            raise RadiusCalcError("Too many RxNodes, expects 1, recieved %d" % len(rxnodes))
        else:
            rxnode = rxnodes[0]

        if not len(txnodes)==1:
            raise RadiusCalcError("Too many TxNodes, expected 1, recieved %d" % len(txnodes))
        else:
            txnode = txnodes[0]

        rxpwr = events.avgrxpwr 
        txpwr = events.avgtxpwr
        radius = self.distfxn(rxpwr,txpwr)      
        return Radius(rxnode, txnode, radius, rxpwr, txpwr)


class RadisTest(unittest.TestCase):
    def setUp(self):
        pass
if __name__ == '__main__':
    unittest.main()
