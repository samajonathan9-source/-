import os
import sys
import pathlib

ROOT = pathlib.Path( __file__ ).resolve().parents[1]
sys.path.insert( 0 , str( ROOT ) )

import numpy as np

from skynet.topo_score import lct_score
from skynet.activations import SyntheticActivations


def test_pipeline_tourne():
    synth = SyntheticActivations( n_layers =  8 , hidden_size =  32 , batch =  32 , seed =  1 )
    block = synth.block()
    assert block.n_layers_method() ==  8
    for mat in block.per_layer:

        res = lct_score( mat )
        assert len( res ) ==  4


def test_bruit_plat():
    rng = np.random.default_rng( 0 )
    mat = rng.normal( loc =  0.0 , scale =  1.0 , size = ( 40 ,  16 ) )
    psig = lct_score( mat )[0]
    assert psig <  0.5
