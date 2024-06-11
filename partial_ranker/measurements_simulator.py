# Partial Ranker
#
# Copyright (C) 2019-2024, Aravind Sankaran
# IRTG-2379: Modern Inverse Problems, RWTH Aachen University, Germany
# HPAC, Umeå University, Sweden
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributors:
# - Aravind Sankaran

import numpy as np

class MeasurementsSimulator:
    """
    Class for simulating measurements.

    Attributes:
        obj_params (dict): Keys are object IDs (str), and values are lists of distribution parameters (e.g., for normal distribution is values are [mean, std])           
        dist (str): The distribution type used for generating measurements. Currently supports only 'normal'.
        measurements (dict): A dictionary to store measurements.
                        Keys are object IDs (str), and values are lists of measurement values.
    """
    
    def __init__(self, obj_params:dict, dist='normal', seed=0):
        """Initializes the MeasurementsSimulator object.

        Args:
            obj_params (dict):  Keys are object IDs (str), and values are lists of distribution parameters (e.g., for normal distribution is values are [mean, std])
            dist (str, optional): The distribution type used for generating measurements. Currently supports only 'normal'. Defaults to 'normal'.
            seed (int, optional): The numpy seed used to generate measurements. Defaults to 0.
        """
        self.obj_params = obj_params
        self.dist = dist
        self.measurements = {}
        np.random.seed(seed)

    def normal(self, mean:float, std:float) -> float:
        """
        Generates a random number from a normal distribution.

        Args:
            mean (float): The mean of the normal distribution.
            std (float): The standard deviation of the normal distribution.

        Returns:
            float: A random number from the normal distribution.
        """
        return np.random.normal(mean, std)

    def add_measurement(self, obj_id, x:float) -> None:
        """
        Adds a measurement to the measurements dictionary.

        Args:
            obj_id (str | int): The ID of the object.
            x (float): The measurement value to add.

        Adds the measurement value `x` to the measurements dictionary under the object ID `obj_id`.
        """
        try:
            self.measurements[obj_id].append(x)
        except KeyError:
            self.measurements[obj_id] = []
            self.measurements[obj_id].append(x)

    def measure(self, reps:int) -> None:
        """
        Measures objects multiple times.

        Args:
            reps (int): The number of repetitions for measuring each object.

        Generates measurements for each object based on the specified distribution parameters and number of repetitions.
        """
        for obj_id, params in self.obj_params.items():
            for i in range(reps):
                if self.dist == 'normal':
                    x = self.normal(*params)
                    self.add_measurement(obj_id, x)

    def get_measurements(self) -> dict:
        """
        Retrieves measurements.

        Returns:
            dict: A dictionary containing measurements.
                Keys are object IDs (str), and values are lists of measurement values.

        Returns the measurements dictionary.
        """
        return self.measurements
