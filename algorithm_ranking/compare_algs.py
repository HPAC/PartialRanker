import numpy as np

class CompareAlgs:
    def __init__(self, measurements, h0):
        self.measurements = measurements
        self.h0 = h0
        self.comparision_matrix = {}
        self.num_comparisons = 0
        #self.init_comparision_matrix()
        self.t_up = {}
        self.t_low = {}

    def init_comparision_matrix(self, q_max, q_min):
        self.num_comparisons = 0
        self.comparision_matrix = {}
        for alg in self.h0:
            self.comparision_matrix[alg] = {}
            for alg2 in self.h0:
                self.comparision_matrix[alg][alg2] = -1
        self.compute_quantiles(q_max,q_min)
    
    def compute_quantiles(self, q_max, q_min):
        for alg, measrements in self.measurements.items():
            t_alg = self.get_measurements(alg)
            self.t_up[alg], self.t_low[alg]  = self.get_quartiles(t_alg,q_max, q_min) 


    def get_measurements(self, alg):
        return self.measurements[alg]

    def remove_outliers(self, x):
        x = np.array(x)
        q1, q2 = np.percentile(x, [25, 75])
        iqr = q2 - q1
        fence_low = q1 - 1.5 * iqr
        fence_high = q2 + 1.5 * iqr
        return x[(x > fence_low) & (x < fence_high)]

    def get_quartiles(self, measurements, q_max=75, q_min=25):
        #return np.percentile(self.remove_outliers(measurements), [q_max, q_min])
        return np.percentile(measurements, [q_max, q_min])

    def compare(self, alg1, alg2):
        # print(alg1, alg2)
        if self.comparision_matrix[alg1][alg2] != -1:
            return self.comparision_matrix[alg1][alg2]

        #t_alg1 = self.get_measurements(alg1)
        #t_alg2 = self.get_measurements(alg2)
        self.num_comparisons = self.num_comparisons + 1

        #t1_up, t1_low = self.get_quartiles(t_alg1, q_max, q_min)
        #t2_up, t2_low = self.get_quartiles(t_alg2, q_max, q_min)
        
        t1_up = self.t_up[alg1]
        t1_low = self.t_low[alg1]
        t2_up = self.t_up[alg2]
        t2_low = self.t_low[alg2]

        # print(alg1, q1_max, q1_min)
        # print(alg2, q2_max, q2_min)

        ret = 1  # alg1 ~ alg2
        if t1_up < t2_low:
            ret = 0  # alg1 is faster than alg2
        elif t2_up < t1_low:
            ret = 2  # alg2 is faster than alg1

        self.comparision_matrix[alg1][alg2] = ret
        if ret == 0:
            self.comparision_matrix[alg2][alg1] = 2
        elif ret == 2:
            self.comparision_matrix[alg2][alg1] = 0
        else:
            self.comparision_matrix[alg2][alg1] = ret

        # print(ret)
        # print("\n")
        return ret