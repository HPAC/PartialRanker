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

class PartialRankerMin:

    def __init__(self,comparer):
        self.comparer = comparer
        self.objs = self.comparer.objs
        
        cm = pd.DataFrame(self.comparer.C)  
        self.equivalence = dict(cm.apply(lambda row: row[row == 1].index.tolist(), axis=1))
        
        self._visited = set()
        self._obj_rank = {}
        self._rank_objs = {}
        
    def compute_ranks(self):
        U = []
        Q = []
        self._visited = set()
        self._obj_rank = {}
        self._rank_objs = {}
                
        for node in self.objs:
            if node not in self._visited:                    
                V = self._equiv_set(node,set())
                U.append(V)
                Q.append(self.comparer.t_low[list(V)[0]])

        sorted_zipped = sorted(zip(U,Q), key=lambda x: x[1])
        U = [x[0] for x in sorted_zipped]
        
        for i in range(len(U)):
            self._rank_objs[i] = U[i]
            for obj in U[i]:
                self._obj_rank[obj] = i
        
    
    def _equiv_set(self,node,V):
        if node in self._visited:
            return V
        self._visited.add(node)
        V.add(node)
        for v in self.equivalence[node]:
            if v not in V:
                V.add(v)
                V = self._equiv_set(v,V)
        return V
    
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
        cm = pd.DataFrame(self.comparer.C)
        dependencies = dict(cm.apply(lambda row: row[row == 0].index.tolist(), axis=1))
        g = Graph(dependencies, self.get_ranks()) 
        return g   
