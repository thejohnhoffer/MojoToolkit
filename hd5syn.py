#!/usr/bin/python
import os
import cv2
import h5py
import glob
import argparse
import numpy as np

help = {
    'truth': 'input h5 with ground truth synapses (default truth.h5)',
    'guess': 'input h5 with predicted synapses (default guess.h5)',
    'home': 'parent directory of files (default nome)',
    'hd5syn': 'detect synapse overlap'
}
paths = {}
overlap = {}

parser = argparse.ArgumentParser(description=help['hd5syn'])
parser.add_argument('truth', default = 'truth.h5', nargs='?', help= help['truth'])
parser.add_argument('guess', default = 'guess.h5', nargs='?', help=help['guess'])
parser.add_argument('-d' ,metavar='path', default = '', help=help['home'])
args = vars(parser.parse_args())
for key in ['truth','guess']:
    h5path = os.path.join(args['d'],args[key])
    paths[key] = os.path.realpath(os.path.expanduser(args[key]))

with h5py.File(paths['truth'], 'r') as tf:
    truth = tf[tf.keys()[0]]
    with h5py.File(paths['guess'], 'r') as gf:
        guess = gf[gf.keys()[0]]
