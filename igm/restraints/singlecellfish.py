from __future__ import division, print_function

import numpy as np
import h5py

from ..model.particle import Particle
from .restraint import Restraint
from ..model.forces import HarmonicUpperBound, HarmonicLowerBound

class SingleCellFish(Restraint):
    """
    Add single cell pairwise distances to a structure.
    Use a combo of upper and lower harmonic restraint
 
    Parameters
    ----------
    distance_file : TRACING activation position file
    struct_id (int): single structure index
    tol : float
        defining tolerance within which the position from imaging data is defined
    k (float): elastic constant for restraining
    """
    
    def __init__(self, distance_file, tol,struct_id, k):
        
        """ Initialize TRACING restraint parameters and input file """

        self.tol = tol
        self.struct_id        = struct_id
        self.k                = k
        self.forceID          = []
        self.distance_file  = h5py.File(distance_file, 'r')
    #-
    
    def _apply(self, model):

        """ Apply TRACING restraints """ 

        pair           = self.distance_file['pair'][()]    # list of (phased) loci to restrain
        target         = self.distance_file['target'][()]   # list of associated target distances
        assignment     = self.distance_file['assignment'][()]   # list of structure indexes thye have to be restrained in

        here_pairs     = np.where(assignment == self.struct_id)[0]   # positions in list of loci to be restrained in current structure
        #print(locus[here_loci])

        # loop over those loci in the Activation File that need to be restrained in structure 'struct_id' (see ImagingActivationStep.py)

        for i, (m,n) in enumerate(pair[here_pairs]):

            print(i, m, n, target[here_pairs][i])
            f = model.addForce(HarmonicUpperBound((m,n), k = self.k, d = target[here_pairs][i] + self.tol, note = Restraint.FISH_PAIR))
            self.forceID.append(f)

            f = model.addForce(HarmonicLowerBound((m,n), k = self.k, d = max(0,target[here_pairs][i] - self.tol), note = Restraint.FISH_PAIR))
            self.forceID.append(f)

