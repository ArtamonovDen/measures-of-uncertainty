import numpy as np


def get_corr_func(method):
    '''
        Return correlation coefficient calculation function by method
        Each of returned functions get X, where each columns are prices of one stock, 
        and rows are prices of stocks for a day
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
        raise NotImplementedError("Signs procedure is not implemented")

    _cor_methods = {"pearson": _pearson, "kendall": _kendall, "signs":_signs}
    return _cor_methods[method]
