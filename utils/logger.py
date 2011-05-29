#!/usr/bin/env python
# encoding: utf-8
"""
logger.py

Created by Henry Herman on 2011-05-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import logging
import logging.config

logging.config.fileConfig("config/log.config")

logger = logging.getLogger()

