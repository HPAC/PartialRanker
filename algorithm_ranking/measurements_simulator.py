from .measurement_manager import MeasurementsManager
import numpy as np

class MeasurementsSimulator(MeasurementsManager):
    def __init__(self, config, distribution='normal',seed=0):
        super().__init__()
        self.distribution = distribution
        self.config = config
        np.random.seed(seed)

    def normal(self, mean, std):
        return np.random.normal(mean, std)

    def add_measurement(self, alg, x):
        try:
            self.alg_measurements[alg].append(x)
        except KeyError:
            self.alg_measurements[alg] = []
            self.alg_measurements[alg].append(x)

    def measure(self, rep_steps, run_id):
        for alg, params in self.config.items():
            for i in range(rep_steps):
                if self.distribution == 'normal':
                    x = self.normal(*params)
                    self.add_measurement(alg, x)

    def get_alg_measurements(self):
        return self.alg_measurements