#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    exit.py
    ~~~~~~~~~
    This script is for exit monkey.
"""
import os
import sys
import monkey


def kill():
    monkey.init_adb()
    monkey.kill_monkey()
    print('stop monkey....')


os.chdir(os.path.normpath(os.path.dirname(sys.argv[0])))
kill()

