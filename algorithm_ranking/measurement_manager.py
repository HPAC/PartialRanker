from abc import ABC, abstractmethod

class MeasurementsManager(ABC):
    def __init__(self):
        self.alg_measurements = {}
        super().__init__()

    @abstractmethod
    def measure(self, rep_steps, run_id):
        #runner.generate measurement script
        #runner.measure_variants
        pass

    @abstractmethod
    def get_alg_measurements(self):
        #case_duration_manager.get_measurements
        pass