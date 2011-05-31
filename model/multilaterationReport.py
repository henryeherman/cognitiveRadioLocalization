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

parser = argparse.ArgumentParser(description="Read in dataset and generate nodes")
parser.add_argument('-f', '--filename', dest='filename', action='store', required=True)
parser.add_argument('-l', '--loadParams', dest='paramfilename', action='store', help="Load channel parameters from a file", default=None) 
parser.add_argument('rxnodes', metavar='N', type=int, nargs='+',
                    help='RX node ids to include in super sensor')
parser.add_argument('-t', '--tx', dest='txnodeid', type=int, action='store', help="Selected TX Node", required=False, default=None)
parser.add_argument('--disp', dest="display", action="store_true", default=False, help="Diplay animations")


def main():
    pass


if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.exists(args.filename):
        parser.print_usage()
        parser.exit(-1, "Dataset filename does not exist")

    dp = DatasetParser(args.filename)

    if not args.paramfilename is None:
        logger.info("Loading Channel Parameters")
        d = shelve.open(args.paramfilename)
        kappa = d['kappa']
        eta = d['eta'] 
        d.close()
    else:
        logger.info("Calculating Channel Params")
        p = cpe.ChanParamEst(dp.events)
        kappa = p.kappa
        eta = p.eta 
    print "KAPPA = %5.3f, ETA= %5.3f" % (kappa,eta) 
    raw_input("Press key to continue")


    cm = ChannelModel(kappa, eta)
    radiusCalc = RadiusCalculator(cm.calcRadius)
    field = Field(dp.nodes)
    
    imgs = []
    dimgs = []
    if args.txnodeid is None:
        txnodes = dp.nodes.nodes.keys()
    else:
        txnodes = [dp.nodes[args.txnodeid].id]

    raw_reports = dict()

    for txnodeid in txnodes:
        radii=[]
        nodes=[]
        radius_imgs = []
        dist_imgs =[]
        txevents = dp.events.findTXEvents(txnodeid)
        for rxnodeid in args.rxnodes:
            events = txevents.findRXEvents(rxnodeid)
            nodes.append(dp.nodes[rxnodeid])
            r = radiusCalc.getRadiusFromEvents(events)
            if not r is None:
                radii.append(r)
                rimg = np.asarray(field.drawRadii([r]))
                radius_imgs.append(rimg)
                rimg=rimg/rimg.max()
                rimg=1-rimg
                dist_img = ndimage.distance_transform_edt(rimg)
                dist_imgs.append(np.power(dist_img,2))
        try:
            rep = np.zeros_like(dist_imgs[0])
            for dist_img in dist_imgs:
                rep = rep + dist_img
            raw_reports[txnodeid] = rep                               
        except IndexError:
            pass
        img = field.drawNodesAndRadii(nodes, radii, dp.nodes[txnodeid])
        imgs.append(img)   
    pyplot.ion() 
    if args.display:
        for txid in txnodes:
            pyplot.figure(1)
            pyplot.imshow(field.drawNodes([dp.nodes[txid]]))
            pyplot.figure(2)
            pyplot.imshow(raw_reports[txid])
            pyplot.draw()
            time.sleep(0.5)

