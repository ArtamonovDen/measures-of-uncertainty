import json 
from tqdm import tqdm
import time
import numpy as np
import k_scripts.finance_scripts as fs
import k_scripts.network_scripts as ns
import k_scripts.sampler_scripts as ss
import k_scripts.measures_scripts as ms



def mst_normal(N_min=10,N_max=1000, N_step=100, serialize=True, path='./experiments/normal_mst_DE/'):

    sampler = np.random.multivariate_normal
    reference_network = ns.create_network(R.corr().values)
    mean = [0] * Cov.shape[0]
    Cov = Cov.values

    errors = dict()
    for N in tqdm(np.arange(N_min,N_max,N_step)):
        local_error = list()
        for i in range(1000):
            sample_network = ns.create_sample_network(sampler,  [mean, Cov,N])    
            local_error.append(ms.E_measure_MST(reference_network,sample_network))
        errors[int(N)] = float(np.mean(local_error))

        if serialize:
            file = path + f'mst_normal_{N_min}-{N_max}.json'
            with open(file, 'w') as f:
                json.dump(result, f) 
        return result