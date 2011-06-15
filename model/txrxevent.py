#!/usr/bin/env python
# encoding: utf-8
"""
txrxevent.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import unittest
import numpy as np
from utils.logger import logger


class EventList(list):
    def __repr__(self):
        return "<EventList(count=%d)>" % (len(self))
    def __str__(self):
        return self.__repr__()
       
    def add(self, event):
        self.append(event)
       
    def getrxpwr(self):
        return np.array([e.rxpwr for e in self])
    
    def gettxpwr(self):
        return np.array([e.txpwr for e in self])
    
    def getpathlosses(self):
        pls = [r.pathloss for r in self]
        return np.array(pls)

    def getdistances(self):
        return np.array([e.distance for e in self])

    def findTXEvents(self, nodeid):
        tx = [r for r in self if r.txnode.id==nodeid]
        return EventList(tx)

    def findRXEvents(self, nodeid):
        rx = [r for r in self if r.rxnode.id==nodeid]
        return EventList(rx)

    def findRXTXEvents(self,rxnodeid,txnodeid):
        txrx = [r for r in self if (r.rxnode.id==rxnodeid and r.txnode.id==txnodeid) ]
        return EventList(txrx)

    def findRXListTXEvents(self, rxnodeids, txnodeid):
        temp = EventList()
        for rxnodeid in rxnodeids:
            temp.extend(self.findRXTXEvents(rxnodeid, txnodeid))
        return EventList(temp)       

    def findEventByDistance(self, distance):
        es = [r for r in self if (r.distance==distance) ]
        return EventList(es)

    
    def getAverageDistance(self):
        return np.mean(self.distances)
        
    def getAverageRXpwr(self):
        return np.mean(self.rxpwrs)
    
    def getAverageTXpwr(self):
        return np.mean(self.txpwrs)

    def getAvgPathloss(self):
        return np.mean(self.pathlosses)

    def getAvgPathlossByDistance(self):
        avgloss = []
        uniqueDistances = list(set(self.distances))
        uniqueDistances.sort()
        logger.info("Found %d unique distances" % len(uniqueDistances))
        logger.info("Calculating Average Pathloss for each distance") 
        for distance in uniqueDistances:
            es = self.findEventByDistance(distance)
            avgloss.append(es.avgpathloss)
        
        return uniqueDistances, np.array(avgloss)
 
    def getAvgRXPwrByDistance(self):
        avgrxs = []
        uniqueDistances = list(set(self.distances))
        uniqueDistances.sort()
        logger.info("Found %d unique distances" % len(uniqueDistances))
        logger.info("Calculating Average RXPwr for each distance") 
        for distance in uniqueDistances:
            es = self.findEventByDistance(distance)
            avgrxs.append(es.avgrxpwr)
        
        return uniqueDistances, np.array(avgrxs)
    
    def getAvgTXPwrByDistance(self):
        avgtxs = []
        uniqueDistances = list(set(self.distances))
        uniqueDistances.sort()
        logger.info("Found %d unique distances" % len(uniqueDistances))
        logger.info("Calculating Average TXPwr for each distance") 
        for distance in uniqueDistances:
            es = self.findEventByDistance(distance)
            avgtxs.append(es.avgtxpwr)
        
        return uniqueDistances, np.array(avgtxs)
       
    def getRxNodes(self):
        return list(set([e.rxnode for e in self]))

    def getTxNodes(self):
        return list(set([e.txnode for e in self]))
        

    def getRSSI(self):
        return np.array([e.rssi for e in self])

    def getAverageRSSI(self):
        return np.mean(self.rssi)

    def normalizeRssi(self):
        for node in self.rxnodes:
            es = self.findRXEvents(node.id)
            rssiMax = es.rssi.max()
            for e in es:
                e.rssi = e.rssi/rssiMax

    rxpwrs = property(getrxpwr)
    txpwrs = property(gettxpwr)
    distances = property(getdistances)
    avgdistance = property(getAverageDistance)
    avgrxpwr = property(getAverageRXpwr)
    avgtxpwr = property(getAverageTXpwr)
    avgrssi = property(getAverageRSSI)
    pathlosses = property(getpathlosses)
    avgpathloss = property(getAvgPathloss)
    rxnodes = property(getRxNodes)
    txnodes = property(getTxNodes)
    rssi = property(getRSSI)
    
    
        
class TXRXEvent(object):
    EVENTID = 0
    def __init__(self,txnode,rxnode,rxpwr=0,txpwr=0,rssi=0,pktno=0,timestamp=0,carrierfreq=0):
        self.txnode = txnode
        self.rxnode = rxnode
        self.rxpwr = float(rxpwr)
        self.txpwr = float(txpwr)
        self.rssi = float(rssi)
        self.pktno = float(pktno)
        self.timestamp = float(timestamp)
        self.freq = float(carrierfreq)
        self.id = TXRXEvent.EVENTID
        self.id= TXRXEvent.EVENTID+1
    
    def getDistance(self):
        return self.txnode.distanceFromNode(self.rxnode)
        
    distance = property(getDistance)    
        
    def __repr__(self):
        return "<TXRXEvent(id=%d,txnode=%d,rxnode=%d)>" % (self.id, self.txnode.id, self.rxnode.id)
    
    def __str__(self):
        return self.__repr__()

    def getPathLoss(self):
        return self.txpwr - self.rxpwr
    
    pathloss = property(getPathLoss)
    
class TXRXTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
