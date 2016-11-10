#!/usr/bin/env python

from np2imgo import Imgo
from np2sego import Sego
from os import getcwd
import glob
import h5py
import re

in_folder = '/data/output-visualize/pad'
out_folder = '/data/output-visualize/mojo'

def convert(in_folder, out_folder):
    files = glob.glob(in_folder + '/*.h5')
    if not files: return 'no h5 found'
    for fil in files:
        f = h5py.File(fil, 'r')

        group = f[f.keys()[0]]
        shape = group.shape
        print group.dtype

        if fil.find('image') > 0:
            imout = Imgo(out_folder)
            for zi in range(shape[0]):
                imout.run(group[zi, :, :], zi)
            imout.save(shape[::-1])

        if fil.find('segmentation') > 0:
            segmentation = Sego(out_folder)
            for zi in range(shape[0]):
                segmentation.run(group[zi, :, :], zi)
            segmentation.save(shape[::-1])

        f.close()

err = convert(in_folder, out_folder)
if err: print 'err ' + str(err)
