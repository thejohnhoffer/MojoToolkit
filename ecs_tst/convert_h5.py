#!/usr/bin/env python

from np2imgo import Imgo
from np2sego import Sego
from os import getcwd
import glob
import h5py
import re

in_folder = '/data/ecs_tst/'
out_folder = '/data/ecs_tst/mojo'

find = lambda r,x: (x[i] for i in range(len(x)) if re.search(r,x[i]))

def convert(in_folder, out_folder):
    files = glob.glob( in_folder + '/*.h5')
    if not files : return 'no h5 found'
    for fil in files:
        f = h5py.File(fil, 'r')

        group = f[f.keys()[0]]
        shape = group.shape

        if fil.find('image')>0:
	    imout = Imgo(out_folder)
	    for zi in range(shape[0]):
		imout.run(group[zi,:,:],zi)
	    imout.save(shape)

        if fil.find('segmentation')>0:
	    segmentation = Sego(out_folder)
	    for zi in range(shape[0]):
                segmentation.run(group[zi,:,:],zi)
	    segmentation.save(shape)

        f.close()

err = convert(in_folder, out_folder)
if err: print 'err '+str(err)
