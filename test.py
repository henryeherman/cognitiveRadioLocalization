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
from utils.datasetParser import DatasetParser 
from model import channelparameterestimator as ce



parser = argparse.ArgumentParser(description="Read in dataset and generate nodes")
parser.add_argument('-f', '--filename', dest='filename', action='store', required=True)
        
def main():
    args = parser.parse_args()
    dp = DatasetParser(args.filename)


if __name__ == '__main__':
    args = parser.parse_args()
    dp = DatasetParser(args.filename)
    

