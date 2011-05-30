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
from model.nodes import Nodes, Node
from model.txrxevent import TXRXEvent, EventList
import csv
from logger import logger


class DatasetParser(object):
    
    TX = 'TXID'
    RX = 'RXID'
    TX_X = 'TXX'
    TX_Y = 'TXY'
    TX_Z = 'TXZ'
    RX_X = 'RXX'
    RX_Y = 'RXY'
    RX_Z = 'RXZ'
    RX_PWR = 'RXPWR'
    NA = 'NA'
    RSSI = 'RSSI'
    PKTNO = 'PKTNO'
    TS = 'TS'
    TX_PWR = 'TXPWR'
    FREQ = 'FREQ'
    HW = 'HW'
    def __init__(self, filename):
        self.file = open(filename)
        self.nodes = Nodes()
        self.events = EventList()
        self.__loadcsv()
        self.__getNodes()
        self.__getEvents()
    def __loadcsv(self):
        self.csv = csv.DictReader(self.file, fieldnames=[DatasetParser.TX,
                                        DatasetParser.RX,
                                        DatasetParser.TX_X,
                                        DatasetParser.TX_Y,
                                        DatasetParser.TX_Z,
                                        DatasetParser.RX_X,
                                        DatasetParser.RX_Y,
                                        DatasetParser.RX_Z,
                                        DatasetParser.RX_PWR,
                                        DatasetParser.NA,
                                        DatasetParser.RSSI,
                                        DatasetParser.PKTNO,
                                        DatasetParser.TS,
                                        DatasetParser.TX_PWR,
                                        DatasetParser.FREQ,
                                        DatasetParser.HW],
                                        delimiter=',')
        
    def __getNodes(self):
        for line in self.csv:
            node = Node(line[DatasetParser.RX], 
                        line[DatasetParser.RX_X],
                        line[DatasetParser.RX_Y],
                        line[DatasetParser.RX_Z])
            self.nodes.add(node)
        self.file.seek(0)
    def __getEvents(self):

        for line in self.csv:
            event = TXRXEvent(self.nodes.get(line[DatasetParser.TX]), self.nodes.get(line[DatasetParser.RX]),
                            line[DatasetParser.RX_PWR],
                            line[DatasetParser.TX_PWR],
                            line[DatasetParser.RSSI],
                            line[DatasetParser.PKTNO],
                            line[DatasetParser.TS],
                            line[DatasetParser.FREQ])
            self.events.add(event)
        self.file.seek(0)
        logger.info("Parsed %d events" % len(self.events))
        
        
def main():
    parser = argparse.ArgumentParser(description="Read in dataset and generate nodes")
    parser.add_argument('-f', '--filename', dest='filename', action='store', required=True)
    args = parser.parse_args()
    datasetParser = DatasetParser(args.filename)


if __name__ == '__main__':
    main()


