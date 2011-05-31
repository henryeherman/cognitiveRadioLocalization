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

class InvalidReport(Exception):
    pass

class Report(object):
    
    def __init__(self, field, radii):
        self.radii = radii
        self.radii_imgs = []
        self.dist_imgs = []
        self.rxnodes = []    
        self.field=field
        while None in self.radii:
            self.radii.remove(None)
        txnodes = list(set([r.txnode for r in self.radii]))
        if len(txnodes)>1:
            raise InvalidReport("Expects Radii with a single TXNode")
        else:
            self.txnode = txnodes[0]

        self.generateDistanceImages()
        self.generateDistanceTransforms()
        self.generateRawReport()
        
    def generateDistanceImages(self):
        for radius in self.radii:
            self.rxnodes.append(radius.rxnode)
            img = np.asarray(self.field.drawRadii([radius]))
            img = img/img.max()
            self.radii_imgs.append(img)

    def generateDistanceTransforms(self):
        for img in self.radii_imgs:
            img = 1-img
            dist_img = ndimage.distance_transform_edt(img)
            self.dist_imgs.append(dist_img)

    def generateRawReport(self):
        self.raw_report = np.zeros_like(self.dist_imgs[0])
        for img in self.dist_imgs:
            self.raw_report = self.raw_report + np.power(img,2)

    def minimumOfReport(self):
        y,x = divmod(self.raw_report.argmin(),self.raw_report.shape[1])
        return x,y
        
    def drawRegion(self, size):
        return self.field.drawTXRegion(self.minimum, size)

    def getError(self):
        x,y = self.minimum
        z = 0
        return self.txnode.distanceFromPos(x,y,z)

    error = property(getError)
    minimum = property(minimumOfReport)


if __name__ == '__main__':
    pass
