import numpy as np

class CompareAlgs:
    def __init__(self, measurements, h0):
        self.measurements = measurements
        self.h0 = h0
        self.comparision_matrix = {}
        self.init_comparision_matrix()

    def init_comparision_matrix(self):
        self.comparision_matrix = {}
        for alg in self.h0:
            self.comparision_matrix[alg] = {}
            for alg2 in self.h0:
                self.comparision_matrix[alg][alg2] = -1

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

    def compare(self, alg1, alg2, q_max=75, q_min=25):
        # print(alg1, alg2)
        if self.comparision_matrix[alg1][alg2] != -1:
            return self.comparision_matrix[alg1][alg2]

        t_alg1 = self.get_measurements(alg1)
        t_alg2 = self.get_measurements(alg2)

        q1_max, q1_min = self.get_quartiles(t_alg1, q_max, q_min)
        q2_max, q2_min = self.get_quartiles(t_alg2, q_max, q_min)
        # print(alg1, q1_max, q1_min)
        # print(alg2, q2_max, q2_min)

        ret = 1  # alg1 ~ alg2
        if q1_max < q2_min:
            ret = 0  # alg1 is faster than alg2
        elif q2_max < q1_min:
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