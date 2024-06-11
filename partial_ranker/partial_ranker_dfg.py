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
    """DFG based parial ranking methodology (Methodology 1 in the paper).
    
    Input:
        comparison_matrix (dict[str, dict[str, int]]): (Input) Comparison matrix from the Comparator.
        
    Attributes:
        dependencies (dict[str,list[str]]): If obj_i is better than obj_j, then the value of obj_j in the dictionary is a list containing obj_i. 
        e.g.; in the dict {'obj1': ['obj2', 'obj3], 'obj2': ['obj4'], ...}, obj2 and obj3 are better than obj1, obj4 is better than obj2, etc.
    """
    def __init__(self,comparer):
        self.objs = list(comparer.C.keys())
        self._obj_rank = {}
        self._rank_objs = {}
        cm = pd.DataFrame(comparer.C)
        self.dependencies = dict(cm.apply(lambda row: row[row == 0].index.tolist(), axis=1))
    
    def compute_ranks(self):
        """Computes the partial ranks of the objects according to Methodology 1. 
        The ranks of an object corresponds to the depth of the object in the dependency graph.
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
        
    def get_ranks(self):
        """Returns the partial ranks of the objects.
        
        Returns:
            dict[int,List[str]]: Dictionary with list of objects at each rank.
        """
        return self._rank_objs
    
    def get_rank_obj(self,obj):
        """Returns the partial rank of the object.
        
        Args:
            obj (str): Object name.
        
        Returns:
            int: Partial rank of the object.
        """
        return self._obj_rank[obj]
    
    def get_dfg(self):
        """Visualizes the dependency graph.
        """
        g = Graph(self.dependencies, self.get_ranks()) 
        return g
    
        
