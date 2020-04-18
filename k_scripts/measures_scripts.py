import numpy as np
from networkx.algorithms.operators import difference
import network_scripts as ns

def E_measure():
    '''
        Compute E-measure of uncertainty        
    '''
    pass

def R_measure():
    '''
        Compute R-measure of unertainty 
    '''
    pass


def error_type_I(ref_struct, sample_struct):
    '''
        Compute the first type error: the nubmer of wrongly included edges

        ref_struct: structure obtained from reference network
        sample_struct: structure obtained from sample network

    '''
    pass


def error_type_II(ref_struct, sample_struct):
    '''
        Compute the first type error: the nubmer of wrongly NOT included edges

        ref_struct: structure obtained from reference network
        sample_struct: structure obtained from sample network

    '''
    pass

def E_measure_MST(ref_network, sample_network):
    '''
        Uncertainty measuring of MST filtering structure.
        For MST E_measure = R_measure, and # of errors of both types are equals.
        So measure for MST is just E_measure = E(X) = 1/(N-1)*error_type_I

        Return: the value of statistical uncertainty for MST for given n
    '''

    #TODO TEST IT!

    ref_mst = ns.build_MST(ref_network)
    sample_mst = ns.build_MST(sample_network)
    return difference(sample_mst, ref_mst).number_of_edges() # Edges presented in sample_mst but not in  ref_mst - I type error
