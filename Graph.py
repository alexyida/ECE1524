import queue
import random
import numpy as np
from PriorityQueue import *

class Graph(object):

    # connectivity measure
    NODE_CONNECTIVITY = 0
    LINK_CONNECTIVITY = 1
    ALGEBRAIC_CONNECTIVITY = 2
    BETWEENNESS_CONNECTIVITY = 3
    
    # betweenness measure
    NODE_BETWEENNESS = 0
    LINK_BETWEENNESS = 1
    
    def __init__(self, node_list, link_list):
        self.node_list = node_list
        self.link_list = link_list
        
    def is_connected(self):
        for node in self.node_list:
            if not self.can_reach_all_other_nodes(node):
                return False
        return True
    
    def can_reach_all_other_nodes(self, v):
        """Breadth-first search (BFS)"""
        
        for node in self.node_list:
            node.distance = float("inf")
            
        q = queue.Queue()
        
        v.distance = 0
        q.put(v)
        
        while not q.empty():
            u = q.get()
            
            for node in self.get_adjacent_node_list(u):
                if node.distance == float("inf"):
                    node.distance = u.distance + 1
                    q.put(node)
        
        for node in self.node_list:
            if node.distance == float("inf"):
                return False
        return True
    
    def get_adjacent_node_list(self, node):
        adjacent_node_list = []
        
        for link in self.link_list:
            if link.link_from == node:
                adjacent_node_list.append(link.link_to)
                
        return adjacent_node_list
            
    def find_node(self, node_id):
        for node in self.node_list:
            if node.node_id == node_id:
                return node
    
    def find_link(self, link_from, link_to):
        for link in self.link_list:
            if link.link_from == link_from and link.link_to == link_to:
                return link
        return None
    
    def find_link_by_id(self, link_id):
        for link in self.link_list:
            if link.link_id == link_id:
                return link
        return None

    def get_link_index(self, link):
        return self.link_list.index(link)

            
    def connectivity(self, connectivity_measure):
        if connectivity_measure == self.ALGEBRAIC_CONNECTIVITY:
            return self.algebraic_connectivity()
        
        if connectivity_measure == self.BETWEENNESS_CONNECTIVITY:
            return self.betweenness_connectivity()
        
        num_of_nodes = len(self.node_list)
        
        # When there is 0 or 1 node in the graph, treat the graph as connected.
        # In this case, node connectivity is infinity.
        if num_of_nodes == 0 or num_of_nodes == 1:
            return float("inf")
        
        if not self.is_connected():
            return 0
        
        minimum = float("inf")
        
        if connectivity_measure == self.NODE_CONNECTIVITY:
            l = self.node_list
        else: # connectivity_measure == self.LINK_CONNECTIVITY
            l = self.link_list
        
        for item in l:
            if connectivity_measure == self.NODE_CONNECTIVITY:
                new_graph = self.create_new_graph_removing_node(item)
            else: # connectivity_measure == self.LINK_CONNECTIVITY
                new_graph = self.create_new_graph_removing_link(item)
            if not new_graph.is_connected():
                return 1
            else:
                connectivity = 1 + new_graph.connectivity(connectivity_measure)
            
            if connectivity < minimum:
                minimum = connectivity
            
        return minimum
            
    def create_new_graph_removing_node(self, node):
        node_list_copy = self.node_list[:]
        node_list_copy.remove(node)
        
        link_list_copy = self.link_list[:]
        for link in self.link_list:
            if link.link_from == node or link.link_to == node:
                link_list_copy.remove(link)
                
        return Graph(node_list_copy, link_list_copy)
    
    def create_new_graph_removing_link(self, link):
        node_list_copy = self.node_list[:]
        
        link_list_copy = self.link_list[:]
        link_list_copy.remove(link)
                
        return Graph(node_list_copy, link_list_copy)  
    
    def generate_adjacency_matrix(self):
        #print(len(self.node_list))
        #print(len(self.link_list))
        m = np.zeros(shape=((len(self.node_list), len(self.link_list))))
        for i in range(0, len(self.link_list)):
            m[self.node_list.index(self.link_list[i].link_from)][i] = 1
            m[self.node_list.index(self.link_list[i].link_to)][i] = -1            
        return m
    
    def generate_diagonal_weight_matrix(self):
        w1 = np.zeros(shape=((len(self.link_list), len(self.link_list))))
        for i in range(0, len(self.link_list)):
            w1[i][i] = self.link_list[i].weight()
        return w1
    
    def generate_laplacian(self):
        m = self.generate_adjacency_matrix()
        mt = np.transpose(m)
        
        w1 = self.generate_diagonal_weight_matrix()
        
        return np.dot(np.dot(m, w1), mt)
    
    def algebraic_connectivity(self):
        # w: eigenvalues, v: eigenvectors
        w, v = np.linalg.eig(self.generate_laplacian())

        w = np.sort(w)
        # w[0] should be roughly equal to 0
        # print(w[0])
        return w[1]
    
    def generate_link_impact_list(self, connectivity_measure):
        impact_list = []
        
        for link in self.link_list:
            new_graph = self.create_new_graph_removing_link(link)
            
            impact = self.connectivity(connectivity_measure) - \
                new_graph.connectivity(connectivity_measure)
            impact_list.append((link.link_id, impact))
        
        impact_list.sort(key = lambda x : x[1], reverse = True)
        return impact_list
    
    def get_link_vitality(self, connectivity_measure):
        return self.generate_link_impact_list(connectivity_measure)[0][1]
    
    def generate_node_impact_list(self, connectivity_measure):
        impact_list = []
        
        for node in self.node_list:
            new_graph = self.create_new_graph_removing_node(node)
            
            impact = self.connectivity(connectivity_measure) - \
                new_graph.connectivity(connectivity_measure)
            impact_list.append((node.node_id, impact))
        
        impact_list.sort(key = lambda x : x[1], reverse = True)
        return impact_list
    
    def get_node_vitality(self, connectivity_measure):
        return self.generate_node_impact_list(connectivity_measure)[0]    
    
    def generate_betweenness_list(self):
        """return tuple (node_betweenness_list, link_betweenness_list)"""
        predecessors = {}
        distance = {}
        number_of_shortest_paths = {}
        dependency = {}
        node_betweenness = {}
        link_betweenness = {}
        
        q = PriorityQueue()
        stack = []
        
        for node in self.node_list:
            node_betweenness[node] = 0    
        for link in self.link_list:
            link_betweenness[link] = 0            
        
        for src in self.node_list:
            # single-source shortest-paths problem
            
            # init
            for w in self.node_list:
                predecessors[w] = []
                
            for dst in self.node_list:
                distance[dst] = float("inf")
                number_of_shortest_paths[dst] = 0
                distance[src] = 0
                number_of_shortest_paths[src] = 1
                q.put((distance[src], src))
                
            while not q.empty():
                v = q.get()[1]
                stack.append(v)
                for w in self.get_adjacent_node_list(v):
                    # path discovery - shorter path to w?
                    if distance[w] > \
                       distance[v] + self.find_link(v, w).weight():
                        distance[w] = \
                            distance[v] + self.find_link(v, w).weight()
                        q.put((distance[w], w))
                        number_of_shortest_paths[w] = 0
                        predecessors[w] = []
                    
                    # path counting - is link (v, w) on a shortest path?
                    if distance[w] == distance[v] + \
                            self.find_link(v, w).weight():
                        number_of_shortest_paths[w] = \
                            number_of_shortest_paths[w] + \
                            number_of_shortest_paths[v]
                        predecessors[w].append(v)
                    
            # accumulation - back-propagation of dependencies
            for node in self.node_list:
                dependency[node] = 0            
            while len(stack) != 0:
                w = stack.pop()
                for v in predecessors[w]:
                    c = number_of_shortest_paths[v] /\
                        number_of_shortest_paths[w] *\
                        (1 + dependency[w])    
                    link_betweenness[self.find_link(v, w)] += c
                    dependency[v] = dependency[v] + c
                        
                if w != src:
                    node_betweenness[w] += dependency[w]               
                    
        node_betweenness_list = []
        for key in node_betweenness:
            node_betweenness_list.append((key.node_id, node_betweenness[key]))
            
        node_betweenness_list.sort(key = lambda x : x[1], reverse = True)
        
        link_betweenness_list = []
        for key in link_betweenness:
            link_betweenness_list.append((key.link_id, link_betweenness[key]))
            
        link_betweenness_list.sort(key = lambda x : x[1], reverse = True)        
    
        return node_betweenness_list, link_betweenness_list
                     
    def get_highest_betweenness_node(self, betweenness_measure):
        return self.generate_betweenness_list()[betweenness_measure][0][0]
        
    def betweenness_connectivity(self):
        # only need NODE_BETWEENNESS for Assignment 1
        betweenness_list =\
            self.generate_betweenness_list()[Graph.NODE_BETWEENNESS]
        total = 0
        for item in betweenness_list:
            total += item[1]
            
        return float(total) / len(betweenness_list)
    
    def shortest_path(self, source):
        metric = {}
        prev = {}
        q = []
        for node in self.node_list:
            metric[node] = float("inf")
            prev[node] = None
            q.append(node)
            
        metric[source] = 0
        while len(q) > 0:
            q.sort(key = lambda x : metric[x])
            u = q.pop(0)
            for v in self.get_adjacent_node_list(u):
                alt = metric[u] + self.find_link(u, v).metric
                if alt < metric[v]:
                    metric[v] = alt
                    prev[v] = u
                    
        return metric, prev

    def shortest_path_max_available(self, source, link_util):
        max_bw = 0
        for v in self.get_adjacent_node_list(source):
            link = self.find_link(source, v)
            bw = link.bw * (1 - link_util[self.get_link_index(link)])
            if bw > max_bw:
                max_bw = bw
                hop = v

        metric, prev = self.shortest_path(hop)
        prev[hop] = source
                    
        return metric, prev

    def shortest_path_valiant(self, source):
        max_random = 0
        for v in self.get_adjacent_node_list(source):
            link = self.find_link(source, v)
            r = random.random()
            if r > max_random:
                max_random = r
                hop = v

        metric, prev = self.shortest_path(hop)
        prev[hop] = source
                    
        return metric, prev

    def shortest_path_no_KSCY_HSTN(self, source):
        metric = {}
        prev = {}
        q = []
        for node in self.node_list:
            metric[node] = float("inf")
            prev[node] = None
            q.append(node)
            
        metric[source] = 0
        while len(q) > 0:
            q.sort(key = lambda x : metric[x])
            u = q.pop(0)
            for v in self.get_adjacent_node_list(u):
                alt = metric[u] + self.find_link(u, v).metric
                # If there is an ingress traffic to Kansas City, 
                # it cannot choose Houston as next hop.
                if u == source and u.node_id == "KSCYng" and v.node_id == "HSTNng":
                    alt = float("inf")
                if alt < metric[v]:
                    metric[v] = alt
                    prev[v] = u
                    
        return metric, prev
