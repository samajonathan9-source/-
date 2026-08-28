# RATISS-skynet - activations synthetiques for Phase 1 POC (CPU-only).

import numpy as np


class ActivationBlock:

    def __init__(self):
        self.per_layer = []
        self.layer_names = []

    def n_layers_method(self):
        return len(self.per_layer)


class SyntheticActivations:

    def __init__(self, n_layers, hidden_size, batch, seed):
        self.n_layers = n_layers

        self.hidden_size = hidden_size
        self.batch = batch

        rng = np.random.default_rng(seed)
        self.rng = rng

        mid1 = n_layers //2 -  1
        mid2 = n_layers //2 +  1
        self.critical = set(range(mid1, mid2))

        self.layer_names = []
        self.per_layer = []

        idx =  0
        while idx < n_layers:

            width = hidden_size
            if width >  32:
                width =  32

            acts = rng.normal( loc=0.0 , scale=0.1 , size=( batch , width ) )
            if idx in self.critical:

                n_groups =  3
                shared = rng.normal( loc=0.0 , scale=1.0 , size=( batch , n_groups ) )
                per = width // n_groups

                gidx =  0
                while gidx <  3:

                    cstart = gidx * per
                    cend = cstart + per

                    col = cstart
                    while col < cend:

                        acts[:, col] = shared[:, gidx] *  1.5
                        acts[:, col] = acts[:, col] + rng.normal( loc=0.0 , scale=0.035 , size=batch)
                        col = col +  1
                    gidx = gidx +  1

            self.layer_names.append("layer_" + str(idx))
            self.per_layer.append(acts)

            idx = idx +  1

    def block(self):
        blk = ActivationBlock()
        blk.per_layer = self.per_layer
        blk.layer_names = self.layer_names
        return blk
