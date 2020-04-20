
import numpy as np
import networkx as nx

def create_network(W):
    '''
        Create weighted graph without loob by weight matrix. Weight matrix is correlation matrix
        W: weights
    '''
     # TODO Add nodes' names ?
    edjes = [ (*nodes,weight) for nodes,weight in np.ndenumerate(W)]
    g = nx.Graph()
    g.add_weighted_edges_from(edjes)
    g.remove_edges_from(nx.selfloop_edges(g))
    return g


def create_sample_network(sampler, sampler_params):
    '''
        Create sample network from given distribution
        sampler: callable generator like np.random.multivariate_normal
        sampler_params: params to run sampler with (like mean and covariation matrix), including number of samples

        Example:
        a = [0]*N
        Cov = R.cov()
        n_sample = np.random.multivariate_normal(mean=a, cov=Cov, size = 10)
    '''

    n_sample = sampler(*sampler_params)
    C = np.corrcoef(n_sample.T)
    return create_network(C)


def build_MST(g):
    '''
        Create maximum spanning tree by given graph
        g: Undirected raph
    '''
    return nx.algorithms.tree.mst.maximum_spanning_tree(g)
    
