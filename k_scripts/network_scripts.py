
import numpy as np
import networkx as nx

def create_reference_network(C):
    '''
        Create reference network by given Correlation matrix 
        C: Correlation matrix

    '''
    # TODO Add nodes' names
    edjes = [ (*nodes,weight) for nodes,weight in np.ndenumerate(C)]
    g = nx.Graph()
    g.add_weighted_edges_from(edjes)
    g.remove_edges_from(nx.selfloop_edges(g))
    return g

def build_MST(g):
    '''
        Create maximum spanning tree by given graph
        g: Undirected raph
    '''
    return nx.algorithms.tree.mst.maximum_spanning_tree(g)
    
