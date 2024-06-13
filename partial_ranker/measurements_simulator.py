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
    Class for simulating measurements values using a normal distribution. Given a dictionary with object IDs as keys, and [mean, std] as values,
    measurement values are generated and stored.

    Inputs:
        **obj_params (dict[str,List[float]])**: Keys are object IDs (str) whose value indicates the mean and standard deviation of the normal distribution represented as [mean, std].            
        
            - e.g., for noramal distribution, ``{'obj1': [1.0, 0.1], 'obj2': [2.0, 0.2], ...}``, the mean and std are 1.0 and 0.1 for object 'obj1', and 2.0 and 0.2 for object 'obj2'.        
        
        **seed (int)**: The numpy seed used to generate measurements. Defaults to 0.
        
    **Attributes and Methods**:
    
    Attributes:
        measurements (dict[str,List[float]]): A dictionary to store measurements. Keys are object IDs (str), and values are lists of measurement values.
        
            - e.g., ``{'obj1': [1.0, 2.0, 3.0], 'obj2': [4.0, 5.0, 6.0, 9.0], ...}``
    """
    
    def __init__(self, obj_params:dict, seed=0):

        self.obj_params = obj_params
        self.dist = 'normal'
        self.measurements = {}
        np.random.seed(seed)

    def normal(self, mean:float, std:float) -> float:
        """
        Args:
            mean (float): The mean of the normal distribution.
            std (float): The standard deviation of the normal distribution.

        Returns:
            float: A random number from the normal distribution.
        """
        return np.random.normal(mean, std)

    def add_measurement(self, obj_id, x:float) -> None:
        """
        Adds a measurement to the measurements dictionary  under the object ID `obj_id`.

        Args:
            obj_id (str | int): The ID of the object.
            x (float): The measurement value to add.

        Returns:
            None
        """
        try:
            self.measurements[obj_id].append(x)
        except KeyError:
            self.measurements[obj_id] = []
            self.measurements[obj_id].append(x)

    def measure(self, reps:int) -> None:
        """
        Generates measurements for each object based on the specified distribution parameters and number of repetitions.

        Args:
            reps (int): The number of repetitions for measuring each object.

        Returns:
            None
        """
        for obj_id, params in self.obj_params.items():
            for i in range(reps):
                if self.dist == 'normal':
                    x = self.normal(*params)
                    self.add_measurement(obj_id, x)

    def get_measurements(self) -> dict:
        """
        Returns:
            dict[str,List[float]]: A dictionary containing measurements.
                Keys are object IDs (str), and values are lists of measurement values.
        """
        return self.measurements
