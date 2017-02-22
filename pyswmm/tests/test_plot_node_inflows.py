# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------

# Standard library imports
import os
import random

# Third party imports
from matplotlib._png import read_png
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Local imports
from pyswmm.swmm5 import PySWMM
from pyswmm.tests.data import (DATA_PATH, IMAGE_NODE_INFLOWS_PATH,
                               MODEL_NODE_INFLOWS_PATH)
from pyswmm.utils.fixtures import get_model_files
import pyswmm.toolkitapi as tka


def test_plot_node_inflows():
    swmmobject = PySWMM(*get_model_files(MODEL_NODE_INFLOWS_PATH))
    swmmobject.swmm_open()
    swmmobject.swmm_start()

    fig = plt.figure()
    ax = fig.add_subplot(2, 3, (1, 2))
    ax.set_ylabel('Flow Rate')
    line, = ax.plot([], [], label='C3')
    ax.grid()
    ax.legend()

    ax2 = fig.add_subplot(2, 3, (4, 5), sharex=ax)
    ax2.set_ylabel('Toolkit API\nInflow')
    line2, = ax2.plot([], [], label='J1')
    ax2.grid()

    xdata, ydata = [], []
    ydata2 = []

    ax3 = fig.add_subplot(2, 3, (3, 6))

    arr_lena = read_png(IMAGE_NODE_INFLOWS_PATH)
    imagebox = OffsetImage(arr_lena, zoom=0.67)
    ab = AnnotationBbox(
        imagebox,
        (0.5, 0.5),
        xybox=(0.5, 0.5),
        xycoords='data',
        boxcoords="offset points",
        pad=0.0, )

    ax3.add_artist(ab)
    ax3.axis('off')

    def data_gen(t=0):
        i = 0
        while(True):
            if i >= 80:
                swmmobject.setNodeInflow('J1', random.randint(1, 5))
            time = swmmobject.swmm_stride(1500)
            i += 1

            if i > 0 and time == 0.0:
                break
            if i > 0 and time > 0:
                yield time

    def run(t):
        xdata.append(t)
        new_y = swmmobject.getLinkResult('C2', tka.LinkResults.newFlow)
        ydata.append(new_y)

        new_y2 = swmmobject.getNodeResult('J1', tka.NodeResults.newLatFlow)
        ydata2.append(new_y2)

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ymin2, ymax2 = ax2.get_ylim()

        # ax
        if new_y > ymax:
            ax.set_ylim(-0.1, 1.5*ymax)
        if t >= xmax:
            ax.set_xlim(xmin, 1.5*xmax)
            ax.figure.canvas.draw()
        line.set_data(xdata, ydata)

        # ax1
        if new_y2 > ymax2:
            ax2.set_ylim(-0.1, 1.2 * ymax2)
        line2.set_data(xdata, ydata2)

    ani = animation.FuncAnimation(
        fig,
        run,
        data_gen,
        blit=False,
        repeat=False,
        save_count=800,
        interval=10, )

    show_figure = False
    if show_figure:
        plt.show()
    else:
        movie_path = os.path.join(DATA_PATH, "node_inflows.mp4")
        ani.save(movie_path, fps=20, dpi=170, bitrate=50000)
    plt.close()

    swmmobject.swmm_end()
    swmmobject.swmm_report()
    swmmobject.swmm_close()
    print("Check Passed")
