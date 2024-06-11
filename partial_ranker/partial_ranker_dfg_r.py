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
from .partial_ranker_dfg import PartialRankerDFG
from .graph import Graph

class PartialRankerDFGReduced:

    def __init__(self,comparer):
        self.objs = comparer.objs
        self.comparer = comparer
        self.pr_dfg = PartialRankerDFG(comparer)
        self.graph_H = None
        
        self._obj_rank = {}
        self._rank_objs = {}
        
    def compute_ranks(self):
        self._obj_rank = {}
        self._rank_objs = {}
        
        self.pr_dfg.compute_ranks()
        self.graph_H = Graph(self.pr_dfg.dependencies, self.pr_dfg.get_ranks())
        
        T = self.graph_H.get_separable_arrangement()
        R = [0]*len(T)
        self._update_rank_data(T[0],R[0])
        for i in range(1,len(T)):
            if self.comparer.C[T[i-1]][T[i]] == 0:
                R[i] = R[i-1] + 1
            else:
                R[i] = R[i-1]
            
            self._update_rank_data(T[i],R[i])  
            
            
    def _update_rank_data(self,obj,rank):
        self._obj_rank[obj] = rank
        self._rank_objs[rank] = self._rank_objs.get(rank,[]) + [obj] 
        
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
        g = Graph(self.pr_dfg.dependencies, self.get_ranks()) 
        return g
