'''
PySWMM Test 2: Pump Setting and Simulation Results Streaming

Author: Bryant E. McDonnell (EmNet LLC)
Date: 11/15/2016

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib._png import read_png
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


import os
import sys

import random

#point to location of the pyswmm file
sys.path.append(os.getcwd()+'\\..\\pyswmm\\')

from swmm5 import pyswmm
from toolkitapi import *



swmmobject = pyswmm('./TestModel3_nodeInflows.inp',\
                    './TestModel3_nodeInflows.rpt',\
                    './TestModel3_nodeInflows.out')
swmmobject.swmm_open()

swmmobject.swmm_start()

fig = plt.figure()
ax = fig.add_subplot(2,3,(1,2))
ax.set_ylabel('Flow Rate')
line, = ax.plot([], [], label = 'C3')
ax.grid()
ax.legend()

ax2 = fig.add_subplot(2,3,(4,5), sharex=ax)
ax2.set_ylabel('Toolkit API\nInflow')
line2, = ax2.plot([], [], label = 'J1')
ax2.grid()

xdata, ydata = [], []
ydata2 = []

ax3 = fig.add_subplot(2,3,(3,6))

arr_lena = read_png("./TestModel3_nodeInflows.PNG")
imagebox = OffsetImage(arr_lena, zoom=0.67)
ab = AnnotationBbox(imagebox, (0.5,0.5),
                    xybox=(0.5,0.5),
                    xycoords='data',
                    boxcoords="offset points",
                    pad=0.0,
                    )
ax3.add_artist(ab)
ax3.axis('off')

def data_gen(t=0):
    i = 0
    while(True):
        if i >= 80:
            swmmobject.setNodeInflow('J1',random.randint(1,5))
        time = swmmobject.swmm_stride(1500)
        i+=1
            
        if i > 0 and time == 0.0:
            break
        if i > 0 and time > 0:
            yield time        
def run(t):
    
    xdata.append(t)
    new_y = swmmobject.getLinkResult('C2',LinkResults.newFlow)
    ydata.append(new_y)
    
    new_y2 = swmmobject.getNodeResult('J1',NodeResults.newLatFlow)
    ydata2.append(new_y2)
    
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ymin2, ymax2 = ax2.get_ylim()

    #ax
    if new_y > ymax:
        ax.set_ylim(-0.1, 1.5*ymax)
    if t >= xmax:
        ax.set_xlim(xmin, 1.5*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    #ax1
    if new_y2 > ymax2:
        ax2.set_ylim(-0.1, 1.2*ymax2)
    line2.set_data(xdata, ydata2)    


ani = animation.FuncAnimation(fig, run, data_gen, blit=False,repeat=False, save_count=800, interval = 10)

ShowFig = False
if ShowFig == True:
    plt.show()
else:
    ani.save("TestModel3_nodeInflows.mp4", fps=20,dpi=170, bitrate=50000)
    
#if 0 == 0:  
#    from JSAnimation import HTMLWriter
#    ani.save('LivePlotTest.html', writer=HTMLWriter(embed_frames=False),extra_args=['figsize',[15,6],'dpi',170])

plt.close()

swmmobject.swmm_end()
swmmobject.swmm_report()
swmmobject.swmm_close()

 
print("Check Passed")
