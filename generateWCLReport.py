#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
import shelve
import time
import argparse
import platform
import random
from utils.datasetParser import DatasetParser 
from model import channelparameterestimator as ce
from scipy.optimize import leastsq
from utils.units import meter2cm, cm2meter
import numpy as np
from matplotlib import pyplot
from model import cpe
from utils.logger import logger
from model.channelmodel import ChannelModel
from model.rxradius import RadiusCalculator
from model.fields import Field
from utils.images2gif import writeGif
from PIL import Image
from scipy import ndimage
from model.weightedCentroidReport import Report

parser = argparse.ArgumentParser(description="Read in dataset and generate nodes")
parser.add_argument('-f', '--filename', dest='filename', action='store', required=True)
parser.add_argument('rxnodes', metavar='N', type=int, nargs='+',
                    help='RX node ids to include in super sensor')
parser.add_argument('-t', '--tx', dest='txnodeid', type=int, action='store', help="Selected TX Node", required=False, default=None)
parser.add_argument('--disp', dest="display", action="store_true", default=False, help="Diplay animations")
parser.add_argument('-N', '--Num', dest='sensorsize', type=int, action='store', help="Node number", required=False, default=None)

def main():
    pass

def plotReport(rep):
    pyplot.figure(1)
    pyplot.imshow(rep.drawRegion(25),origin=(0,0))
    pyplot.figure(2)
    pyplot.imshow(rep.field.drawNodes(rep.rxnodes, rep.txnode),origin=(0,0))

if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        parser.print_usage()
        parser.exit(-1, "Dataset filename does not exist")

    dp = DatasetParser(args.filename)
    dp.events.normalizeRssi()

    field = Field(dp.nodes)
    
    imgs = []
    dimgs = []
    errors = []

    if args.txnodeid is None:
        txnodes = dp.nodes.nodes.values()
    else:
        txnodes = [dp.nodes[args.txnodeid]]
    reports = dict()    
    
    if not args.sensorsize is None:
        rxnodeids = random.sample([n.id for n in dp.nodes.nodes.values()],args.sensorsize)
    else:
        rxnodeids = args.rxnodes

    for txnode in txnodes:
        es = dp.events.findRXListTXEvents(rxnodeids, txnode.id)
        rep = Report(field, es)
        reports[txnode.id] = rep
        errors.append(rep.error)
        if args.display:
            pyplot.ion()
            plotReport(rep)
            pyplot.draw()
            time.sleep(0.5)
    errs = np.array(errors)
    mean_err = np.mean(errs)
    std_err = np.std(errs)
    logger.info("Mean Error: %3.2f  Std: %3.2f" % (mean_err, std_err))
    raw_input("Press key to continue")
