import random
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from .compare_algs import CompareAlgs

class RankVariants(ABC):
    def __init__(self, alg_measurements, alg_seq_h0):
        self.measurements = alg_measurements
        self.alg_seq_h0 = alg_seq_h0
        self.compare_algs = CompareAlgs(alg_measurements,alg_seq_h0)

    
    @abstractmethod
    def rank_variants(self,q_max=75, q_min=25):
        pass


    def calculate_ranks(self, q_maxs=[95, 90, 85, 80, 75, 70, 65, 55],
                        q_mins=[5, 10, 15, 20, 25, 30, 35, 45]):
        #q_maxs = [95, 90, 85, 80, 75, 70, 65, 55]
        #q_mins = [5, 10, 15, 20, 25, 30, 35, 45]
        #q_maxs = [55, 55, 55, 55, 55]
        #q_mins = [5, 10, 20, 30, 40]
        #q_maxs = [75, 70, 65, 55]
        #q_mins = [25, 30, 35, 45]
        ranks = []
        for q_max, q_min in zip(q_maxs, q_mins):
            ranks.append(self.rank_variants(q_max, q_min).set_index('case:concept:name'))

        return pd.concat(ranks, axis=1)

    def calculate_roc(self):

        df_ranks = self.calculate_ranks()
        max_rank = df_ranks.max().max()
        if max_rank == 0:
            max_rank = 1
        x = df_ranks.apply(lambda x: x * (1. / len(df_ranks.columns))).sum(axis=1) / (max_rank)
        df_roc = pd.DataFrame(x)
        df_roc = df_roc.reset_index()
        df_roc = df_roc.rename(columns={0: 'case:roc'})

        df_roc.sort_values(by=['case:roc'], inplace=True)
        return df_ranks, df_roc

    def calculate_mean_rank(self, q_maxs=[95, 90, 85, 80, 75, 70, 65, 55],
                            q_mins=[5, 10, 15, 20, 25, 30, 35, 45] ):

        df_ranks = self.calculate_ranks(q_maxs, q_mins)

        x = df_ranks.sum(axis=1) / float(len(df_ranks.columns))
        df_mean = pd.DataFrame(x)
        df_mean = df_mean.reset_index()
        df_mean = df_mean.rename(columns={0: 'case:mean-rank'})

        df_mean.sort_values(by=['case:mean-rank'], inplace=True)
        return df_ranks, df_mean