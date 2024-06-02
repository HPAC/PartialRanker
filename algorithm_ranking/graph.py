import pandas as pd
import graphviz
import numpy as np

class Node:
    def __init__(self,name):
        self.name = name
        self.in_nodes = set()
        self.out_nodes = set()
        self.redun = set()
        self.depth = -1
        
    def add_in_node(self, node):
        self.in_nodes.add(node)
        
    def remove_in_node(self, node):
        self.in_nodes.remove(node)
        
    def add_out_node(self, node):
        self.out_nodes.add(node)
        
    def remove_out_node(self, node):
        self.out_nodes.remove(node)
        
    def get_depth(self):
        if self.depth == -1:
            depth = 0
            if self.in_nodes:
                depth = max([ n.get_depth() + 1 for n in self.in_nodes])
            self.depth = depth
        return self.depth
    
    
    def get_depth_n_collect_redun(self):
        self.redun = set()
        depths = []
        nodes = []
        max_depth = 0
        if self.in_nodes:
            for n in self.in_nodes:
                if n.depth == -1:
                    depths.append(n.get_depth_n_collect_redun()+1)
                else:
                    depths.append(n.depth+1)
                nodes.append(n.name)
            max_depth = max(depths)
            idxs = np.where(np.array(depths) != max_depth)[0]
            for i in idxs:
                self.redun.add(nodes[i])
        self.depth = max_depth
        return self.depth
        
    def depth(self):
        self.redun = set()
        depths = []
        nodes = []
        max_depth = 0
        if self.in_nodes:
            for n in self.in_nodes:
                depths.append(n.depth()+1)
                nodes.append(n.name)
            max_depth = max(depths)
            idxs = np.where(np.array(depths) != max_depth)[0]
            for i in idxs:
                self.redun.add(nodes[i])
        return max_depth
                    
                          
    def __str__(self):
        return "{}".format(self.name)

class Graph:
    def __init__(self,debug=False):
        self.nodes = {}
        self.edges_in = {}
        self.edges_out = {}
        self.node_depth = {}
        self.graph_depth = 0
        self.debug = debug
        self.is_tr_reduced = False
    
    def add_node(self,node):
        self.nodes[node]  = Node(node)
        self.edges_in[node] = []
        self.edges_out[node] = []
        self.node_depth[node] = 0
        
        
    def add_edge(self, node_x, node_y):
        if node_y not in self.edges_out[node_x]:
            if self.debug:
                print("Adding edge from {} to {}".format(node_x,node_y))
            self.edges_out[node_x].append(node_y)
            self.nodes[node_x].add_out_node(self.nodes[node_y])

            self.edges_in[node_y].append(node_x)
            self.nodes[node_y].add_in_node(self.nodes[node_x])
    
        
    def remove_edge(self, node_x, node_y):
        if self.debug:
            print("Removing edge from {} to {}".format(node_x,node_y))
        try:
            self.edges_out[node_x].remove(node_y)
            self.nodes[node_x].remove_out_node(self.nodes[node_y])    
            
            self.edges_in[node_y].remove(node_x)
            self.nodes[node_y].remove_in_node(self.nodes[node_x]) 
            
        except ValueError:
            print("Edge does not exist")
     
    def reset_node_depths(self):
        for alg,node in self.nodes.items():
            node.depth = -1
    
    def calculate_node_depth(self):
        self.reset_node_depths()
        self.graph_depth = 0
        for alg,node in self.nodes.items():
            self.node_depth[alg] = node.get_depth()
            if self.graph_depth < self.node_depth[alg]:
                self.graph_depth = self.node_depth[alg]
            
    def transitivity_reduction(self):
        self.reset_node_depths()
        self.graph_depth = 0
        for alg,node in self.nodes.items():
            #print("For node {}".format(alg))
            if node.depth == -1:
                self.node_depth[alg] = node.get_depth_n_collect_redun()
            else:
                self.node_depth[alg] = node.depth
                
            if self.graph_depth < self.node_depth[alg]:
                self.graph_depth = self.node_depth[alg]
                
        for alg,node in self.nodes.items():
            for in_node in node.redun:
                self.remove_edge(in_node,node.name)

        self.is_tr_reduced = True
            
    def get_nodes_at_depth(self,depth):
        #self.calculate_node_depth()
        df = pd.DataFrame(self.node_depth.items())
        return list(df.loc[df[1] == depth][0])
    
    def visualize(self,highlight_nodes=[]):
        g = graphviz.Digraph()
        for node in self.nodes.keys():
            color='#f0efed'
            if node in highlight_nodes:
                color = '#f2ecc7'
            g.node(node,style='filled',color=color)
        for node1,v in self.edges_out.items():
            for node2 in v:
                if node2 in highlight_nodes:
                    g.edge(node1, node2, style='filled', color='blue')
                else:
                    g.edge(node1, node2)
        return g

    def get_separable_arrangement(self):
        if not self.is_tr_reduced:
            self.transitivity_reduction()
        h0_ = []
        for rank in range(self.graph_depth + 1):
            nodes = []
            num_in_nodes = []
            num_out_nodes = []
            for node in self.get_nodes_at_depth(rank):
                nodes.append(node)
                num_in_nodes.append(len(self.nodes[node].in_nodes))
                num_out_nodes.append(len(self.nodes[node].out_nodes))
            df = pd.DataFrame(list(zip(nodes, num_out_nodes, num_in_nodes)))
            h0_ = h0_ + list(df.sort_values([1,2],ascending=[False,True])[0])
        return h0_
        