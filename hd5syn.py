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
TP = set()
onlyGuess = set()
groundTruth = set()
allstacks = tuple()

parser = argparse.ArgumentParser(description=help['hd5syn'])
parser.add_argument('truth', default = 'truth.h5', nargs='?', help= help['truth'])
parser.add_argument('guess', default = 'guess.h5', nargs='?', help=help['guess'])
parser.add_argument('-o' ,metavar='path', default = 'out', help=help['out'])
parser.add_argument('-d' ,metavar='path', default = '', help=help['home'])
args = vars(parser.parse_args())
for key in ['truth','guess','o']:
    h5path = os.path.join(args['d'],args[key])
    paths[key] = os.path.realpath(os.path.expanduser(h5path))

with h5py.File(paths['truth'], 'r') as tf:
    truth = tf[tf.keys()[0]]
    with h5py.File(paths['guess'], 'r') as gf:
        guess = gf[gf.keys()[0]]

        allstacks += truth.shape
        for stacki in range(allstacks[0]):
            tstack = truth[stacki,:,:].flatten()
            gstack = guess[stacki,:,:].flatten()

            tnot = np.logical_not(tstack)
            tygy = np.logical_and(tstack,gstack)
            tngy = np.logical_and(tnot,gstack)

            bothin = np.nonzero(tygy)[0]
            justgin = np.nonzero(tngy)[0]
            alltin = np.nonzero(tstack)[0]

            for b in bothin:
                match[gstack[b]] = tstack[b]

            for b in justgin:
                where[gstack[b]] = [stacki,b]

            TP = TP.union(set(tstack[bothin]))
            groundTruth = groundTruth.union(set(tstack[alltin]))
            onlyGuess = onlyGuess.union(set(gstack[justgin]))
            print str(100*stacki/allstacks[0])+'%'

    FP = set().union(onlyGuess)
    FN = groundTruth.difference(TP)

    for n in onlyGuess:
        if n in match:
            found = {match[n]}
            FP = FP.difference(found)

with open(os.path.join(paths['o'],'out.csv'), 'wb') as csvfile:
     cw = csv.writer(csvfile, delimiter=' ',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
     cw.writerow(['True_Positives','False_Positives','False_Negatives'])
     cw.writerow([len(TP),len(FP),len(FN)])

with open(os.path.join(paths['o'],'extra.csv'), 'wb') as csvfile:
     cw = csv.writer(csvfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
     cw.writerow(['ID','Z','X','Y'])
     for extra in list(FP):
         xyz = np.unravel_index(where[extra][1],allstacks[1:])
         cw.writerow(list((extra,where[extra][0])+xyz))
