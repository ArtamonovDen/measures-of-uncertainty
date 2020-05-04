import numpy as np
from networkx.algorithms.operators import difference
import k_scripts.network as ns

def error_type_I(ref_struct, sample_struct):
    '''
        Compute the first type error: the number of wrongly included edges

        ref_struct: structure obtained from reference network
        sample_struct: structure obtained from sample network

    '''
    return difference(sample_struct, ref_struct).number_of_edges() # Edges presented in sample_struct but not presented in ref_struct


def error_type_II(ref_struct, sample_struct):
    '''
        Compute the second type error: the number of wrongly NOT included edges

        ref_struct: structure obtained from reference network
        sample_struct: structure obtained from sample network

    '''
    return difference(ref_struct, sample_struct).number_of_edges() # Edges presented in ref_struct but not presented in sample_struct

def E_measure_MST(reference_network, sampler, sampler_params):
    '''
        Calculate E_measure for MST as E[X]
        For MST E_measure = R_measure, and # of errors of both types are equals.
        So measure for MST is just E_measure = E[X] = E[1/(N-1)*error_type_I]
    '''

    Xs = list()
    for i in range(1000): # Calculate E[X] as mean of different Xs
        sample_network = ns.create_sample_network(sampler, sampler_params)    
        Xs.append(
            X_error_rate_MST(reference_network,sample_network)
            )
    return np.mean(Xs)


def X_error_rate_MST(ref_network, sample_network):
    '''
        Calculate X random variable X where E-measure is E[X].
        For MST X = 1/(N-1)*error_type_I
    '''
    
    ref_mst = ns.build_MST(ref_network)
    sample_mst = ns.build_MST(sample_network)
    error_type_I(ref_mst, sample_mst)
    N = ref_network.number_of_nodes() 
    return error_type_I(ref_mst,sample_mst) / (N-1) # Edges presented in sample_mst but not in  ref_mst - I type error
    
