#!/usr/bin/python
import os
import csv
import h5py
import argparse
import numpy as np

help = {
    'truth': 'input h5 with ground truth synapses (default truth.h5)',
    'guess': 'input h5 with predicted synapses (default guess.h5)',
    'home': 'parent directory of files (default none)',
    'out': 'output directory of files (default out)',
    'hd5syn': 'detect synapse overlap'
}
paths = {}
match = {}
where = {}
areas = {}
overlaps = {}
onlyGuess = set()
groundTruth = set()
allstacks = tuple()
pixelOverlap = set()

# Arguement Parsing
parser = argparse.ArgumentParser(description=help['hd5syn'])
parser.add_argument('truth', default = 'truth.h5', nargs='?', help= help['truth'])
parser.add_argument('guess', default = 'guess.h5', nargs='?', help=help['guess'])
parser.add_argument('-o' ,metavar='path', default = 'out', help=help['out'])
parser.add_argument('-d' ,metavar='path', default = '', help=help['home'])
args = vars(parser.parse_args())
for key in ['truth','guess','o']:
    h5path = os.path.join(args['d'],args[key])
    paths[key] = os.path.realpath(os.path.expanduser(h5path))

# Open Ground Truth and Predictions
with h5py.File(paths['truth'], 'r') as tf:
    truth = tf[tf.keys()[0]]
    with h5py.File(paths['guess'], 'r') as gf:
        guess = gf[gf.keys()[0]]

        # Go through every slice
        allstacks += truth.shape
        for stacki in range(allstacks[0]):
            tstack = truth[stacki,:,:].flatten()
            gstack = guess[stacki,:,:].flatten()

            #tnot: Not in true data
            tnot = np.logical_not(tstack)
            #tygy: In true data and guess data
            tygy = np.logical_and(tstack,gstack)
            #tngy: In guess data, but not true data
            tngy = np.logical_and(tnot,gstack)

            # All pixels in both images
            bothin = np.nonzero(tygy)[0]
            # All pixels in just the guess
            justgin = np.nonzero(tngy)[0]
            # All pixels in true data
            alltin = np.nonzero(tstack)[0]

            for b in bothin:
                # True ID value
                tb = tstack[b]
                # Guess value
                gb = gstack[b]
                # Link guess to true ID
                match[gb] = tb
                # Count overlap with ID
                if tb in overlaps:
                    # Count overlaps per guess
                    if gb in overlaps:
                        overlaps[tb][gb] += 1
                    else:
                        overlaps[tb][gb] = 1
                else:
                    overlaps[tb] = {}
                    overlaps[tb][gb] = 1


            for b in justgin:
                # Save the position of
                where[gstack[b]] = [stacki,b]

            for b in alltin:
                # True ID value
                tb = tstack[b]
                # Count any voxel in ID
                if tb in areas:
                    areas[tb] += 1
                else:
                    areas[tb] = 1

            pixelOverlap = pixelOverlap.union(set(tstack[bothin]))
            groundTruth = groundTruth.union(set(tstack[alltin]))
            onlyGuess = onlyGuess.union(set(gstack[justgin]))
            print str(100*stacki/allstacks[0])+'%'

    TP = set()
    FP = set()

    for tid in pixelOverlap:
        maxover = max(overlaps[tid].values())
        if 10*maxover >= areas[tid]:
            TP = TP.union({tid})

    FN = groundTruth.difference(TP)

    for n in onlyGuess:
        if n not in match:
            FP = FP.union({n})

with open(os.path.join(paths['o'],'outTenthMax.csv'), 'wb') as csvfile:
     cw = csv.writer(csvfile, delimiter=' ',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
     cw.writerow(['GT_Total','True_Positives','False_Positives','False_Negatives'])
     cw.writerow([len(groundTruth),len(TP),len(FP),len(FN)])

with open(os.path.join(paths['o'],'extraTenthMax.csv'), 'wb') as csvfile:
     cw = csv.writer(csvfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
     cw.writerow(['ID','Z','Y','X'])
     for extra in list(FP):
         xyz = np.unravel_index(where[extra][1],allstacks[1:])
         cw.writerow(list((extra,where[extra][0])+xyz))
