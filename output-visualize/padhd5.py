#!/usr/bin/python
import os
import cv2
import h5py
import glob
import argparse
import numpy as np

paths = {}
help = {
    'padhd5': 'Pad h5 file to nearest power of 2 with 0s!',
    'out': 'output h5 filename (default out.h5)',
    'inp': 'input h5 filename (default inp.h5)',
}
parser = argparse.ArgumentParser(description=help['padhd5'])
parser.add_argument('inp', default='inp.h5', nargs='?', help=help['inp'])
parser.add_argument('out', default='out.h5', nargs='?', help=help['out'])

# attain all arguments 
args = vars(parser.parse_args())
for key in ['out', 'inp']:
    paths[key] = os.path.realpath(os.path.expanduser(args[key]))

# open an input file
with h5py.File(paths['inp'], 'r') as hfi:
    with h5py.File(paths['out'], 'w') as hfo:
        group = hfi[hfi.keys()[0]]
        shape = list(group.shape)
        dtype = group.dtype

        # Get power of two just greater than array
        logs = np.ceil(np.log2(shape))
        padshape = [2 ** p for p in logs]
        padshape[0] = shape[0]

        # Fill the new array with the old array
        padded = np.zeros(padshape, dtype=dtype)
        written = hfo.create_dataset('main', padshape, dtype=dtype)

        written[:, :shape[1], :shape[2]] = group
