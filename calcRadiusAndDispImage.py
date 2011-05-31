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
import Tkinter, ImageTk

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
    if args.txnodeid is None:
        txnodes = dp.nodes.nodes.keys()
    else:
        txnodes = [dp.nodes[args.txnodeid].id]

    for txnodeid in txnodes:
        radii=[]
        nodes=[]
        txevents = dp.events.findTXEvents(txnodeid)
        for rxnodeid in args.rxnodes:
            events = txevents.findRXEvents(rxnodeid)
            nodes.append(dp.nodes[rxnodeid])
            r = radiusCalc.getRadiusFromEvents(events)

    
            if not r is None:
                radii.append(r)
        img = field.drawNodesAndRadii(nodes, radii, dp.nodes[txnodeid])
        imgs.append(img)   
    
    
    writeGif("out.gif",imgs,0.5,True,False)
    img = Image.open("out.gif")
    if args.display:
        
        root = Tkinter.Tk()

        img1 = ImageTk.PhotoImage(imgs[0])
        width1 = img1.width()
        height1= img1.height()
        canvas1 = Tkinter.Canvas(width=width1, height=height1)
        canvas1.pack()
    
    
        for i in imgs:
            tki = ImageTk.PhotoImage(i)
            canvas1.create_image(width1/2.0,height1/2.0, image=tki)
            canvas1.update()
            time.sleep(0.5)

        root.mainloop()



