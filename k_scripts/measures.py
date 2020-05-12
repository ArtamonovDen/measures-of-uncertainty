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

#-------------------------------------------------- MST ----------------------------------------------------------------

def E_measure_MST(reference_network, sampler, sampler_params, sim_measure='pearson'):
    '''
        Calculate E_measure for MST as E[X]
        For MST E_measure = R_measure, and # of errors of both types are equals.
        So measure for MST is just E_measure = E[X] = E[1/(N-1)*error_type_I]
    '''

    Xs = list()
    ref_mst = ns.build_MST(reference_network)
    N = reference_network.number_of_nodes() 
    for i in range(500): # Calculate E[X] as mean of different Xs
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

def E_measure_MG(reference_network, threshold, sampler, sampler_params,sim_measure='pearson'):
    '''
        Calculate E_measure for MG as E[X]
        For MG E_measure = R_measure
   
    '''
    ref_mg = ns.build_MG(reference_network,threshold)
    M = ref_mg.number_of_edges()
    N = ref_mg.number_of_nodes()
    M_compl = N*(N-1)/2 - M
    Xs = list()   

    for i in range(500): # Calculate E[X] as mean of different Xs
        sample_network = ns.create_sample_network(sampler, sampler_params,sim_measure='pearson')    
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


#-------------------------------------------------- Maximum Clique ----------------------------------------------------------------

def E_measure_MC(ref_clique, N_ref, threshold, sampler, sampler_params):
    '''
        Calculate E-measure for Maximum Clique structure. 
        Returns tuple means of errors: (Fraction of errors of type I, Fraction of errors of type II, Total Fraction of errors)
        The last one is E-measure for MC structure
        N_ref - number of nodes in clique
    '''

    M2 = N_ref * (N_ref-1)/2
    assert int(M2) == len(ref_clique.edges) # should be equeal as it's a clique
    Xs = list()   

    for i in range(500): # Calculate E[X] as mean of different Xs
        sample_network = ns.create_sample_network(sampler, sampler_params)    
        smpl_clique, N_smpl = ns.build_MC(ns.build_MG(sample_network,threshold))
        Xs.append(
            X_totoal_MC(ref_clique, smpl_clique, M2)
        )
    return np.mean(Xs, axis=0)


def X_totoal_MC(ref_clique, smpl_clique, M2):
    '''
        Calculate total fraction of error for MC structure as (I_type_error + II_type_error)/2
        Returns (I_type_error, II_type_error, Total error)
    '''
    x1 = X_type_I_MC(ref_clique, smpl_clique)
    x2 = X_type_II_MC(ref_clique, smpl_clique, M2)
    return x1, x2, (x1+x2)/2


def X_type_I_MC(ref_clique, smpl_clique):
    '''
        Calculate Fraction of errors of type I X_1/M1, where X_1 - is calculated error_type_I, 
        and M1 = C(2|Cl_s), Cl_s - # of all possible edges in sample-structure clique. Note, that M1 is a random variable as well
    '''
    M1 = len(smpl_clique.edges) # == N_smlp * (N_smlp-1)/2 as it's clique
    return error_type_I(ref_clique, smpl_clique) / M1


def X_type_II_MC(ref_clique, smpl_clique, M2):
    '''
        Calculate Fraction of errors of type II as X_2/M2, where X_2 is calculated error_type_II,
        and M2 = C(2|Cl_ref), Cl_ref - # of all possible edges in ref-structure clique. M2 is a constant
    '''
    return error_type_II(ref_clique, smpl_clique) / M2