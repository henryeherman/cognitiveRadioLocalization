#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
from utils.units import meter2cm, cm2meter
import numpy as np
from matplotlib import pyplot
from utils.logger import logger
from fields import Field
from PIL import Image
from scipy import ndimage

class InvalidTXNodeError(Exception):
    pass

class Report(object):
    def __init__(self, field, events):
        self.field = field
        self.events = events
        self.rxnodes = self.events.rxnodes
        self.txnode = list(set(self.events.txnodes))
        if not(len(self.txnode) == 1):
            raise InvalidTXNodeError("Expected a single TXNode, recieved %d" % len(self.txnode))
        else:
            self.txnode = self.txnode[0]

        self.weightsum = 0
        self.weight_by_node = dict()
        
        #self.weight_min = self.events.rssi.min()
        #for rxnode in self.rxnodes:
        #    rxes = self.events.findRXEvents(rxnode.id)
        #    self.weightsum += rxes.avgrssi - self.rssi_min
        #    rxnode.weight = rxes.avgrssi - self.rssi_min
        for rxnode in self.rxnodes:
            rxes = self.events.findRXEvents(rxnode.id)
            #self.weightsum += rxes.avgrxpwr - self.weight_min
            rxnode.weight = rxes.avgrssi**1
            rxnode.avgrxpwr = rxes.avgrxpwr       
            rxnode.avgrssi = rxes.avgrssi 

        self.minweight = np.array([rxnode.weight for rxnode in self.rxnodes]).min()
        self.weights = []
        for rxnode in self.rxnodes:
            rxnode.weight = rxnode.weight #- self.minweight
            self.weights.append(rxnode.weight)
        temp = np.array(self.weights)
        self.limit = np.mean(temp) + np.std(temp)*0.5 
        for rxnode in self.rxnodes:
            if rxnode.weight < self.limit:
                if not rxnode.weight == temp.max():
                    rxnode.weight = 0 
        
            self.weightsum += rxnode.weight
             

        self._calX()
        self._calY()    
        
        logger.info("Error %3.2f cm" % self.error)

        logger.info("Number of Nodes used %d" %len([node.weight for node in self.rxnodes if node.weight!=0]))

    def _calX(self):
        self.xtempsum = 0
        for rxnode in self.rxnodes:
            self.xtempsum += rxnode.xpos_cm*rxnode.weight            
        try:
            self.x = self.xtempsum / self.weightsum
        except:
            import pdb
            pdb.set_trace()
    def _calY(self):
        self.ytempsum = 0
        for rxnode in self.rxnodes:
            self.ytempsum += rxnode.ypos_cm*rxnode.weight            
        self.y = self.ytempsum / self.weightsum
 
    def getPos(self):
        return self.x, self.y

    def getConvPos(self):
        return self.field.convCoord(self.raw_pos)

    raw_pos = property(getPos)
    pos = property(getConvPos) 

    def getReport(self):
        self.field.drawTXRegion(self.pos, 20)

    def drawRegion(self, size):
        logger.info("Number of Nodes used %d" %len([node.weight for node in self.rxnodes if node.weight!=0]))
        return self.field.drawTXRegion(self.pos, size)


    def getError(self):
        x,y = self.raw_pos
        z=0
        return self.txnode.distanceFromPos(x,y,z)


    report = property(getReport)
    error = property(getError)


if __name__ == '__main__':


    pass
