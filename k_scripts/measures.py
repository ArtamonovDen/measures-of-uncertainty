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

def E_measure_MST(reference_network, sampler, sampler_params, sim_measure):
    '''
        Calculate E_measure for MST as E[X]
        For MST E_measure = R_measure, and # of errors of both types are equals.
        So measure for MST is just E_measure = E[X] = E[1/(N-1)*error_type_I]
    '''

    Xs = list()
    ref_mst = ns.build_MST(reference_network)
    N = reference_network.number_of_nodes() 
    for i in range(1000): # Calculate E[X] as mean of different Xs
        sample_network = ns.create_sample_network(sampler, sampler_params, sim_measure)    
        Xs.append(
            X_error_rate_MST(ref_mst, ns.build_MST(sample_network), N)
            )
    return np.mean(Xs)


def X_error_rate_MST(ref_mst, sample_mst, N):
    '''
        Calculate X random variable X where E-measure is E[X].
        For MST X = 1/(N-1)*error_type_I
    '''
    return error_type_I(ref_mst,sample_mst) / (N-1) # Edges presented in sample_mst but not in  ref_mst - I type error




#-------------------------------------------------- Market Graph ----------------------------------------------------------------

def E_measure_MG(reference_network, threshold, sampler, sampler_params):
    '''
        Calculate E_measure for MG as E[X]
        For MG E_measure = R_measure
   
    '''
    ref_mg = ns.build_MG(reference_network,threshold)
    M = ref_mg.number_of_edges()
    N = ref_mg.number_of_nodes()
    M_compl = N*(N-1)/2 - M
    Xs = list()   

    for i in range(1000): # Calculate E[X] as mean of different Xs
        sample_network = ns.create_sample_network(sampler, sampler_params)    
        Xs.append(
            X_error_rate_MG(ref_mg, ns.build_MG(sample_network,threshold), M, M_compl)
            )
    return np.mean(Xs)


def X_error_rate_MG(ref_mg, sample_mg, M, M_compl):
    '''
        Calculate X random variable X where E-measure is E[X].
        For MG: X = 1/2 * [ error_type_I / (C(2|n) - M) + error_type_II / M]
        where M - the number of edges in reference network, C(2|n) - the # of all possible edges in complete n-graph,
        M_compl = C(2|n) - M
    '''
    
    x1 = error_type_I(ref_mg, sample_mg)
    x2 = error_type_II(ref_mg, sample_mg)
    
    return (x1/M_compl + x2/M)/2 # Edges presented in sample_mst but not in  ref_mst - I type error
