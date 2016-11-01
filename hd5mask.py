#!/usr/bin/python
import os
import csv
import h5py
import argparse
import numpy as np

help = {
    'mask': 'input h5 mask (default mask.h5)',
    'given': 'input h5 to mask (default given.h5)',
    'home': 'parent directory of files (default none)',
    'out': 'output directory of files (default masked)',
    'hd5mask': 'Mask hdf5 files'
}
paths = {}

# Arguement Parsing
parser = argparse.ArgumentParser(description=help['hd5mask'])
parser.add_argument('given', default = 'given.h5', nargs='?', help= help['given'])
parser.add_argument('mask', default = 'mask.h5', nargs='?', help=help['mask'])
parser.add_argument('-o' ,metavar='path', default = 'mask', help=help['out'])
parser.add_argument('-d' ,metavar='path', default = '', help=help['home'])
args = vars(parser.parse_args())
for key in ['given','mask','o']:
    h5path = os.path.join(args['d'],args[key])
    paths[key] = os.path.realpath(os.path.expanduser(h5path))
outfile = os.path.join(paths['o'],args['given'])

# Open Ground Truth and Predictions
with h5py.File(paths['mask'], 'r') as mf:
    mask = mf[mf.keys()[0]]
    with h5py.File(paths['given'], 'r') as gf:
        given = gf[gf.keys()[0]]
        with h5py.File(outfile, 'w') as gof:
            written = gof.create_dataset("main", mask.shape, dtype=np.uint32)
            for depth in range(mask.shape[0]):
                written[depth,:,:] = given[depth,:,:]*mask[depth,:,:]
                print str(100*depth/mask.shape[0])+'%'

