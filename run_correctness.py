#!/usr/bin/env python3
import subprocess

__daemon__= subprocess.Popen('./correctness.py',shell=True,
        stdout=subprocess.PIPE)
__endpoint__ = subprocess.Popen('./endpoint.py',shell=True,
        stdout=subprocess.PIPE)
