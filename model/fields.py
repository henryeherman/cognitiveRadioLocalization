#!/usr/bin/env python
# encoding: utf-8
"""
fields.py

Created by Henry Herman on 2011-05-25.
Copyright (c) 2011 UCLA. All rights reserved.
"""

import sys
import os
from utils.units import meter2cm, cm2meter
import numpy as np
from matplotlib import pyplot
from utils.logger import logger
from PIL import Image, ImageDraw
import random

class Field(object):
    NR = 20 
    def __init__(self, nodes, padding=200):
        self.nodes = nodes
        
        self.extents = self.nodes.extents
        self.xmax = np.int16(np.ceil(self.extents[0][0]))
        self.xmin = np.int16(np.ceil(self.extents[0][1]))
        self.ymax = np.int16(np.ceil(self.extents[1][0]))
        self.ymin = np.int16(np.ceil(self.extents[1][1]))
        self.pad = padding
    
    def getEmptyField(self):
        self._img = Image.new('L',((self.xmax-self.xmin+2*self.pad),
                            (self.ymax-self.ymin+2*self.pad)))
        return self._img
   
 
    img = property(getEmptyField)
    
    def getEmptyColorField(self):
        self._cimg = Image.new('RGB',((self.xmax-self.xmin+2*self.pad),
                            (self.ymax-self.ymin+2*self.pad)))
        return self._cimg

    cimg = property(getEmptyColorField)    

    def drawRadii(self, radii=[]):
        draw = ImageDraw.Draw(self.img)
        for r in radii:
            x,y = self._conv_node(r.rxnode)
            x = np.int16(np.floor(x))
            y = np.int16(np.floor(y))
            rad = np.int16(np.round(r.r))
            draw.arc((x-rad,y-rad,x+rad,y+rad), 0,360,255)
        return np.asarray(self._img)


    def drawNodes(self, nodes=[]):
        draw = ImageDraw.Draw(self.cimg)
        
        for node in nodes:
            val1 = random.randint(0,255)
            val2 = random.randint(0,255)
            val3 = random.randint(0,255)
            x,y = self._conv_node(node)
            draw.ellipse((x-Field.NR,y-Field.NR,x+Field.NR,y+Field.NR),
                            (val1,val2,val3)) 
            draw.text((x,y),"%d"%node.id)
        return np.asarray(self._cimg)


    def drawNodesAndRadii(self, nodes=[], radii=[], txnode=None):
        draw = ImageDraw.Draw(self.cimg)
        
        for node in nodes:
            val1 = random.randint(0,255)
            val2 = random.randint(0,255)
            val3 = random.randint(0,255)
            x,y = self._conv_node(node)
            draw.ellipse((x-Field.NR,y-Field.NR,x+Field.NR,y+Field.NR),
                            (val1,val2,val3))
            
            draw.text((x-Field.NR/2,y-Field.NR/2),"RX:%d"%node.id)

        for r in radii:
            x,y = self._conv_node(r.rxnode)
            x = np.int16(np.floor(x))
            y = np.int16(np.floor(y))
            draw.arc((x-r.r,y-r.r,x+r.r,y+r.r), 0,360,(255,255,255))
    
        if not txnode is None:
            x,y = self._conv_node(txnode)
            x = np.int16(np.floor(x))
            y = np.int16(np.floor(y))
            draw.rectangle((x-Field.NR,y-Field.NR,x+Field.NR,y+Field.NR),
                            outline=(255,255,0), fill=(255,0,255))
            draw.text((x-Field.NR/2,y-Field.NR/2), "TX:%d" % txnode.id)

         

        return np.asarray(self._cimg)

    def drawTXRegion(self,pos,size):
        draw = ImageDraw.Draw(self.cimg)
        x,y = pos
        x,y = self._conv_coord(x,y)
        x = np.int16(np.floor(x))
        y = np.int16(np.floor(y))
        logger.info("x:%f,y:%f" % (x,y))
        draw.rectangle((x-size,y-size,x+size,y+size),
        outline=(255,255,0), fill=(255,0,255))
        
        draw.text((x-size/2,y-size/2), "Rep")
        return np.asarray(self._cimg)
        

    def _conv_coord(self,x,y):
        return x+self.pad, y+self.pad

    def _conv_node(self,node):
        x,y,z = node.pos
        return (x+self.pad-self.xmin,y+self.pad-self.ymin)



if __name__ == '__main__':
    pass
