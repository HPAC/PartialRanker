import pandas as pd
from .graph import Graph
from .rank_variants import RankVariants

class RankVariantsDFGTr(RankVariants):
    def __init__(self, alg_measurements, alg_seq_h0):
        super().__init__(alg_measurements, alg_seq_h0)
        
        self.graph = None
        self.algs_ft = {}
        self.init_graph()
        
    def init_graph(self,debug=False):
        self.graph = Graph(debug)

        for alg in self.alg_seq_h0:
            self.graph.add_node(alg)
            self.algs_ft[alg] = []     
        #self.graph.calculate_node_depth()
            
            
        
    def rank_variants(self, q_max=75, q_min=25, debug = False, redo_comparisons = True):
        
        if redo_comparisons:
            self.init_graph(debug)
            self.compare_algs.init_comparision_matrix()
        
        N = len(self.alg_seq_h0)
        for i in range(N):
            for j in range(0, N-i-1):
                
                alg_i =  self.alg_seq_h0[j]
                alg_j =  self.alg_seq_h0[j+i+1]
                
                self.deduce_transitivity(alg_i,alg_j)
                if self.compare_algs.comparision_matrix[alg_i][alg_j] != -1:
                    continue
                
                if debug:
                    print("comparing {} and {}".format(alg_i, alg_j))
                    
                ret = self.compare_algs.compare(alg_i, alg_j, q_max, q_min)
                
                if ret == 0:
                    self.graph.add_edge(alg_i, alg_j)
                    self.algs_ft[alg_j] = self.algs_ft[alg_j] + [alg_i] + self.algs_ft[alg_i]
                elif ret == 2:
                    self.graph.add_edge(alg_j, alg_i)
                    self.algs_ft[alg_i] = self.algs_ft[alg_i] + [alg_j] + self.algs_ft[alg_j]
                        
            
        return self.get_ranks_from_graph(q_max,q_min)
        
    def deduce_transitivity(self, alg_i, alg_j):
        if alg_i in self.algs_ft[alg_j]:
            self.compare_algs.comparision_matrix[alg_i][alg_j] = 'd'
            self.compare_algs.comparision_matrix[alg_j][alg_i] = 'd'
            
        elif alg_j in self.algs_ft[alg_i]:
            self.compare_algs.comparision_matrix[alg_i][alg_j] = 'd'
            self.compare_algs.comparision_matrix[alg_j][alg_i] = 'd'

    def get_ranks_from_graph(self,q_max,q_min):
        
        self.graph.transitivity_reduction()
        
        algs_sorted = []
        alg_ranks = []
        
        for rank in range(self.graph.graph_depth + 1):
            for alg in self.graph.get_nodes_at_depth(rank):
                algs_sorted.append(alg)
                alg_ranks.append(rank)
                
        
        columns = ['case:concept:name', 'case:rank:q{}-q{}'.format(int(q_max),int(q_min))]
        return pd.DataFrame([(algs_sorted[i], alg_ranks[i]) for i in range(len(alg_ranks))], columns=columns)
            
