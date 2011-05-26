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

class Events(object):
    def __init__(self):
        self.events = []
        
    def add(self, event):
        self.events.append(event)

    def __getitem__(self, index):
        return self.events[index]
    
    def __repr__(self):
        return "<Event(count=%d)>" % len(self.events)

    def __str__(self):
        return self.__repr__()    

    def findTXEvents(self, nodeid):
        tx = [r for r in self.events if r.rxnode.id==nodeid]
        return EventList(tx)

    def findRXEvents(self, nodeid):
        rx = [r for r in self.events if r.rxnode.id==nodeid]
        return EventList(rx)

    def findTXRXEvents(self,rxnodeid,txnodeid):
        txrx = [r for r in self.events if (r.rxnode.id==rxnodeid and r.txnode.id==txnodeid) ]
        return EventList(txrx)
        
class EventList(list):
    def __init__(self, events):
        self.events = events
    def __repr__(self):
        return "<EventList(count=%d)>" % (len(self.events))
    def __str__(self):
        return self.__repr__()

    
        
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
        
    def __repr__(self):
        return "<TXRXEvent(id=%d,txnode=%d,rxnode=%d)>" % (self.id, self.txnode.id, self.rxnode.id)
    
    def __str__(self):
        return self.__repr__()
    

class TXRXTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()