#!/usr/bin/env python3
# RATISS-skynet : diagnostic LCT par couche (phase 1, preuve par le fonctionnement).

import os
import sys
import json
import hashlib
import argparse

sys.path.insert( 0 , os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )

import numpy as np

from skynet.activations import SyntheticActivations
from skynet.topo_score import lct_score


def sha256_hex( payload ):
    m = hashlib.sha256()
    m.update( payload.encode( "utf-8" ) )
    return m.hexdigest()


def main():
    parser = argparse.ArgumentParser( description = "Diagnostic LCT par couche sur activations" )
    parser.add_argument( "--layers" , type = int , default = 8 )
    parser.add_argument( "--hidden" , type = int , default =  64 )
    parser.add_argument( "--batch" , type = int , default =  64 )
    parser.add_argument( "--seed" , type = int , default =  42 )
    parser.add_argument( "--out" , type = str , default = "artifacts/lct_diagnostic.json" )
    args = parser.parse_args()

    print( "RATISS-skynet : diagnostic LCT sur activations" )
    print( "=" *  60 )

    synth = SyntheticActivations( n_layers = args.layers , hidden_size = args.hidden , batch = args.batch , seed = args.seed )
    block = synth.block()

    rows = []
    for i in range( block.n_layers_method() ):
        mat = block.per_layer[i]
        psig , edge , ent , betti = lct_score( mat )
        rows.append( { "layer" : i , "psig" : round( psig , 4 ) , "edge" : round( edge ,  4 ) , "entropy" : round( ent ,  4 ) , "H1" : betti } )
        print( "layer" , i , "psig = {:.4f} , edge = {:.4f} , ent = {:.4f} , H1 = " .format( psig , edge , ent ) , betti )

    payload = json.dumps( rows , sort_keys = True , indent =  2 )
    proof = sha256_hex( payload )

    out = { "generator" : "SyntheticActivations(CPU)" ,
             "n_layers" : args.layers ,
             "hidden_size" : args.hidden ,
             "batch" : args.batch ,
             "seed" : args.seed ,
             "rows" : rows ,
             "sha256_proof" : proof }
    os.makedirs( os.path.dirname( args.out ) , exist_ok = True )
    with open( args.out , "w" , encoding = "utf-8" ) as f:
        json.dump( out , f , indent =  2 )

    print( "=" *  60 )
    print( "preuve SHA-256 :" , proof )
    print( "rapport ecrit dans :" , args.out )


if __name__ == "__main__":
    main()
