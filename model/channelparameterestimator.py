#!/usr/bin/env python
# encoding: utf-8
"""
channelparameterestimator.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import unittest
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
          

class ChanParamEstTests(unittest.TestCase):
    def setUp(self):
        node = Node(1)
        nodes = Nodes([node])

if __name__ == '__main__':
    unittest.main()
