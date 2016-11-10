#!/usr/bin/python
import os
import cv2
import h5py
import glob
import argparse
import numpy as np

help = {
    'out': 'output h5 filename (default out.h5)',
    'sep': 'separator for filenames (default _)',
    'png2hd5': 'Stack all pngs into one h5 file!',
    'pngs': 'input folder with all pngs (default pngs)',
    'type': 'datatype for output file (default uint32)',
    'format': 'Little Endian channel order as rgba,bgr (default none)',
    'dep': 'How many separators from start of name until depth (default 0)'
}
paths = {}
stack = {}
rgba = {
    'r':0,
    'g':1,
    'b':2,
    'a':3
}
parser = argparse.ArgumentParser(description=help['png2hd5'])
parser.add_argument('-d', metavar='int', type=int, default = 0, help=help['dep'])
parser.add_argument('-t' ,metavar='path', default = 'uint32', help=help['type'])
parser.add_argument('-f', metavar='string', default = '', help=help['format'])
parser.add_argument('pngs', default = 'pngs', nargs='?', help= help['pngs'])
parser.add_argument('out', default = 'out.h5', nargs='?', help=help['out'])
parser.add_argument('-s' ,metavar='char', default = '_', help=help['sep'])

# attain all arguments 
args = vars(parser.parse_args())
[sep,dep,format] = [args['s'], args['d'], args['f']]
for key in ['pngs','out']:
    paths[key] = os.path.realpath(os.path.expanduser(args[key]))

# read all pngs in pngs folder
for f in glob.glob( paths['pngs'] + '/*.png'):
    stack[f] = os.path.basename(f).split('.')[0].split(sep)[dep]

# open an output file
with h5py.File(paths['out'], 'w') as hf:
    imageFiles = sorted(stack)
    shape = (len(imageFiles),) + cv2.imread(imageFiles[0],0).shape
    written = hf.create_dataset("main", shape, dtype=getattr(np,args['t']))

    # Add each png file as a slice
    for depth,file in enumerate(imageFiles):
        if not format:
            written[depth,:,:] = cv2.imread(file,0)
	else:
            # pixel to integer
            volume = cv2.imread(file)
            slice = np.zeros(volume.shape[:2])
            for ci,char in enumerate(format):
                colorbyte = volume[:,:,rgba[char]]*(256**ci)
                slice = slice + colorbyte 
            written[depth,:,:] = slice
	
	# simple progress indicator
        if depth%(shape[0]/10) == 1:
            print str(100*depth/shape[0])+'%'
