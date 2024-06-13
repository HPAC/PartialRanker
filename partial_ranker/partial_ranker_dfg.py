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

import pandas as pd
from .graph import Graph

class PartialRankerDFG:
    """DFG based partial ranking methodology (Methodology 1 in the paper).
    The ranks of an object corresponds to the depth of the object in a dependency graph which indicates the better-than relations. 
    The algorithm is implemented in the method ``compute_ranks()``.
    
    Input:
        comparer (partial_ranker.QuantileComparer):
            The ``QuantileComparer`` object that contains the results of pair-wise comparisons.
            i.e, ``comparer.compare()`` should have been called.
        
    **Attributes and Methods**:
    
    Attributes:
        dependencies (dict[str,list[str]]): A dictionary with objects as keys, whose value holds the list of objects that are better than the object indicated in the key. If ``obj_i`` is better than ``obj_j``, then the value of ``obj_j`` in the dictionary is a list containing ``obj_i``.
        
            - e.g.; in the dict ``{'obj1': ['obj2', 'obj3], 'obj2': ['obj4'], ...}``, ``obj2`` and ``obj3`` are better than ``obj1``, ``obj4`` is better than ``obj2``, etc.
    """
    def __init__(self,comparer):
        self.objs = list(comparer.C.keys())
        self._obj_rank = {}
        self._rank_objs = {}
        cm = pd.DataFrame(comparer.C)
        self.dependencies = dict(cm.apply(lambda row: row[row == 0].index.tolist(), axis=1))
    
    def compute_ranks(self) -> None:
        """Computes the partial ranks of the objects according to Methodology 1. 
        The internal variables that stores the rank of the objects are updated.
        
        Returns:
            None
        """
        self._obj_rank = {}
        self._rank_objs = {}
        for obj in self.objs:
            d = self._get_depth(obj)
            self._rank_objs[d] = self._rank_objs.get(d,[]) + [obj]
    
    def _get_depth(self,obj):
        if obj in self._obj_rank:
            return self._obj_rank[obj]
        else:
            v = self.dependencies[obj]
            if not v:
                self._obj_rank[obj] = 0
            else:
                self._obj_rank[obj] = max([self._get_depth(i) for i in v]) + 1
            return self._obj_rank[obj]
        
    def get_ranks(self) -> dict[int,list[str]]:
        """
        Returns:
            dict[int,List[str]]: A dictionary consisting of the list of objects at each rank.
            e.g.; ``{0: ['obj1'], 1: ['obj2', 'obj3'], ...}``.
        """
        return self._rank_objs
    
    def get_rank_obj(self,obj:str) -> int:
        """  
        Args:
            obj (str): Object name.
        
        Returns:
            int: The partial rank of a given object.
        """
        return self._obj_rank[obj]
    
    def get_dfg(self):
        """
        Returns:
            partial_ranker.Graph: A Graph object that represents the rank relation among the objects according to Methodology 1.
        """
        g = Graph(self.dependencies, self.get_ranks()) 
        return g
    
        
