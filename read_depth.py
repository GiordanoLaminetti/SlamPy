#!/usr/bin/python

from PIL import Image
import numpy as np


def read_depth_KITTI(filename):
    """ loads depth map D from png file and returns it as a numpy array,

    """
    depth_png = np.array(Image.open(filename), dtype=int)
    # make sure we have a proper 16bit depth map here.. not 8bit!
    assert(np.max(depth_png) > 255)

    depth = depth_png.astype(np.float) / 256.
    depth[depth_png == 0] = -1.
    return depth


def read_depth_TUM(filename):
    """ loads depth map D from png file and returns it as a numpy array,

    """
    depth_png = np.array(Image.open(filename), dtype=int)
    # make sure we have a proper 16bit depth map here.. not 8bit!
    assert(np.max(depth_png) > 255)

    depth = (depth_png.astype(np.float) / 256) / 5000.
    return depth
