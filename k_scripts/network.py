
import numpy as np
import networkx as nx
import pandas
import k_scripts.utils as ku

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


def create_sample_network(sampler, sampler_params,method='pearson'):
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
    similarity_function = ku.get_corr_func(method)
    C = similarity_function(n_sample)
    return create_network(C)


def build_MST(g):
    '''
        Create maximum spanning tree by given graph
        g: Undirected graph
    '''
    return nx.algorithms.tree.mst.maximum_spanning_tree(g)


def build_MG(g,threshold):
    '''
        Create Market graph from given graph
        by removing edges having weight less than specified threshold

        g: Undirected graph
        threshold: real number from 0 to 1
    '''
    mg = nx.Graph()
    mg.add_nodes_from(g.nodes)
    mg.add_weighted_edges_from((u,v,d['weight']) for u,v,d in g.edges(data=True) if d['weight']>threshold   )
    return mg


def build_MC(g):
    '''
        Return maximum by # of nodes clique subgragh. If there are several maximum clicques, 
        the one returned has max weight.
        Returns (maximum clique graph with all nodes from g , number of nodes in clique.
        To clear clique from extra nodes use clique.nodes[:N_clique_nodes]
    '''
    cliques = list(nx.algorithms.clique.find_cliques(g))
    cliques.sort(key = lambda c: len(c)) 
    max_clique_size = len(cliques[-1])
    max_clique_t = (0,None)
    for clique in cliques[::-1]:
        if len(clique) < max_clique_size:
            break
        weight = g.subgraph(clique).size(weight='weight')
        max_clique_t = max( 
            (weight, g.subgraph(clique)),
            max_clique_t,
            key = lambda c: c[0] # compare by weight
        )
    max_clique = max_clique_t[1].copy()
    max_clique.add_nodes_from(g.nodes) # Add all nodes to make it possible to compare cliques
    return max_clique, max_clique_t[1].number_of_nodes()    

def build_MIS():
    pass
    # nx.algorithms.maximal_independent_set(g)

    #https://networkx.github.io/documentation/networkx-2.1/_modules/networkx/algorithms/approximation/independent_set.html  
