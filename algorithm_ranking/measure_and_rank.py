from ast import Raise
import numpy as np
import pandas as pd
from .rank_variants import RankVariants
from .sort1 import RankVariantsSort1
from .sort2 import RankVariantsSort2
from .sort3 import RankVariantsSort3

def measure_and_rank(measurements_manager, h0, rep_steps=3, eps=0.001, max_rep=50, method="sort2"):

    initial_ranks = []
    for i, j in enumerate(h0):
        initial_ranks.append([j, i])
    mean_rank_h0 = pd.DataFrame(initial_ranks, columns=['case:concept:name', 'case:mean-rank'])
    mean_rank_log = []
    mean_rank_log.append(mean_rank_h0.set_index('case:concept:name'))

    dy = np.ones(len(h0)-1)
    run_id = 0
    norm = 1
    while norm > eps and run_id * rep_steps < max_rep:
        measurements_manager.measure(run_id=run_id, rep_steps=rep_steps)
        alg_measurements = measurements_manager.get_alg_measurements()

        if method == "sort1":
            rank_variants = RankVariantsSort1(alg_measurements, h0)
        elif method == "sort2":
            rank_variants = RankVariantsSort2(alg_measurements, h0)
        elif method == "sort3":
            rank_variants = RankVariantsSort3(alg_measurements, h0)
        else:
            raise Exception("Method not found")
        

        s, mr = rank_variants.calculate_mean_rank()

        mean_rank_log.append(mr.set_index('case:concept:name'))
        print(mr)
        df = mean_rank_h0.merge(mr, on=['case:concept:name'])
        x = df.iloc[:, -1].values
        dx = np.convolve(x, [1, -1], 'valid')

        norm = np.linalg.norm(dx - dy, 2) / len(h0)
        print("norm: {}".format(norm))

        dy = dx.copy()
        h0 = list(mr.sort_values(by=['case:mean-rank'])['case:concept:name'])

        run_id = run_id + 1

    num_measurements = (run_id) * rep_steps
    print("Number of measurements: {}".format(num_measurements))

    return s, mr, pd.concat(mean_rank_log, axis=1)