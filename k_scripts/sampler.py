import numpy as np


def multivariate_t(means, C, df, n):
    '''
        Generate random vector of Student distribution

        inspired by: https://github.com/statsmodels/statsmodels/blob/master/statsmodels/sandbox/distributions/multivariate.py#L88
        with help of lovely https://en.wikipedia.org/wiki/Multivariate_t-distribution

        X ~ t(v, mu, Sigma) is
         X = mu + y/sqrt(u/v) where y ~ N(0, Sigma) and u ~ Chi-squared(v)
         with 
         v: degrees of freedom
         mu: vector with means
         Sigma: covariance matrix

    '''

    u = np.random.chisquare(df, n)
    u = np.tile(u.reshape(n,1), len(means)) # some broadcast
    
    y = np.random.multivariate_normal(np.zeros(len(means)), C, n)
    return y / np.sqrt(u/df) + means



def mixed_t_normal(means, C, df, n, t_ratio = 0.3):
    '''
        Generate sample of mixed multivariate Student and Normal distributions in defined ratio

        means: the array of means of variables
        C: covariance matrix
        df: degrees of freedom
        n: number of samples
        t_ration: the piece of samples generated from Student distribution. E.g. if t_ratio=0, each of n
            samples is generated from Normal distribution, and, on the opposite, if t_ration=1 all sample
            is generated from Student distribution  
    '''
    n_student = round(n * t_ratio)
    n_normal = n - n_student

    N = C.shape[0] # the num of stocks
    x_normal = np.random.multivariate_normal(means, C, n_normal)
    x_student = multivariate_t(means, C, df, n_student)

    return np.concatenate([x_normal, x_student])

