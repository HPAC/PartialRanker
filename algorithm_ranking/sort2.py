from .rank_variants import RankVariants
import pandas as pd
import numpy as np

class RankVariantsSort2(RankVariants):
    def __init__(self, alg_measurements, alg_seq_h0):
        super().__init__(alg_measurements, alg_seq_h0)
        
    def sort_h0_by_iqr(self, ascending=True):
        algs = []
        iqrs = []
        for k,v in self.compare_algs.measurements.items():
            algs.append(k)
            q75,q25 = np.percentile(v,[75,25])
            iqrs.append(q75-q25)
        df = pd.DataFrame({"algs":algs,"iqr":iqrs})
        df = df.sort_values(by=['iqr'],ascending=ascending)
        self.alg_seq_h0 = df['algs'].tolist()
        return df

    
    def rank_variants(self,q_max=75, q_min=25, debug=False):
        self.compare_algs.init_comparision_matrix(q_max,q_min)

        p = len(self.alg_seq_h0)

        r = np.array([i for i in range(p)])

        algs = {}
        
        algs_sorted = self.alg_seq_h0.copy()
            
        if debug:
            print(algs_sorted)
            print(r)
            print("\n")

        for i in range(p):
            for j in range(0, p - i - 1):
                
                ret = self.compare_algs.compare(algs_sorted[j], algs_sorted[j + 1])

                # if alg j+1 is faster than alg j
                if ret == 2:
                    # swap alg positions
                    algs_sorted[j], algs_sorted[j + 1] = algs_sorted[j + 1], algs_sorted[j]

                    # update rank
                    if r[j + 1] == r[j]:
                            r[j + 1] = r[j + 1] + 1

                # alg j+1 is as good as alg j
                if ret == 1:
                    # update rank
                    if r[j + 1] != r[j]:
                        r[j + 1:] = r[j + 1:] - 1
                        
                
                if debug:
                    print("compare {} and {}".format(algs_sorted[j], algs_sorted[j+1]))
                    print(algs_sorted)
                    print(r)
                    print("\n")

        columns = ['case:concept:name', 'case:rank:q{}-q{}'.format(int(q_max),int(q_min))]

        return pd.DataFrame([(algs_sorted[i], r[i]) for i in range(p)], columns=columns)
    
