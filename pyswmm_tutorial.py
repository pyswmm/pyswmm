#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 00:45:16 2017

@author: pluto
"""

from pyswmm.simulation import Simulation

sim = Simulation('test_inp.inp')
sim.execute()