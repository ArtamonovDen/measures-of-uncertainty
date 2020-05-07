import numpy as np


def get_corr_func(method):
    '''
        Return correlation coefficient calculation function by method
        Each of returned functions get X, where each columns are returns of one stock, 
        and rows are prices of stocks for a day (daily observation)
    '''
    if method == 'kendall':
        from scipy.stats import kendall
   
    def _pearson(X):
        return np.corrcoef(X, rowvar=False)

    def _kendall(X):
        # kendallttau returns a tuple of the tau statistic and pvalue
        #rs = kendalltau(a, b)
        #return rs[0]
        raise NotImplementedError("Kendall is not implemented")

    def _signs(X):
        '''
            Signs coincidence correlation between two stocks x and y over t(i) periods  of time, where i=1,..,n, is
             Sum over t_i of I[x(t_i)*y(t_i)] devided by n. I[s] = 1 is s>=0 and 0 otherwise.
            So, to calcuelate sgn based correlation we need to create matrix Cs = NxN, where N is # of stocks, where
            Cs[i,j] is sign correlation between x_i and x_j stock

        '''
        N = X.shape[1]
        Cs = np.eye(N)
        for i in range(N-1):
            i_signs = np.sign(X[:,i] * X[:,i+1:].T) # a with b..c, b with c..d and so on ...
            i_signs[i_signs<0]=0
            Cs[i,i+1:] = i_signs.sum(axis=1)/(N)

        i_lower = np.tril_indices(N, -1)
        Cs[i_lower] = Cs.T[i_lower] # fill in simetric elements under main diagonal
        return Cs


    _cor_methods = {"pearson": _pearson, "kendall": _kendall, "signs":_signs}
    return _cor_methods[method]
