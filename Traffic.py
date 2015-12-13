import sqlite3
import numpy as np
from scipy.optimize import nnls

class Traffic(object):
    def __init__(self, graph):
        self.graph = graph
    
    def worst_case_tm(self, month):
        worst_tm = np.zeros(shape=((len(self.graph.node_list), len(self.graph.node_list))))
        
        conn = sqlite3.connect('tm.db')  
        c = conn.cursor()

        for i in range(0, len(self.graph.node_list)):
            for j in range(0, len(self.graph.node_list)):
                values = ("2004-" + month + "-01", "2004-" + month + "-31", 
                          self.graph.node_list[i].node_id, 
                          self.graph.node_list[j].node_id)
                c.execute("SELECT MAX(traffic) FROM tm WHERE tm_date >= ? AND tm_date <= ? AND src = ? AND dst = ?", 
                          values)
                
                worst = c.fetchone()[0]
                worst_tm[i][j] = worst
        
                print("processed src {}, dst {}: worst-case {}".format(values[2], values[3], worst))                
        
        conn.close()

        return worst_tm
    
    def tm_for_date_time(self, date, time):
        tm = np.zeros(shape=((len(self.graph.node_list), len(self.graph.node_list))))
        
        conn = sqlite3.connect('tm.db')  
        c = conn.cursor()

        values = (date, time)        
        for row in c.execute("SELECT src, dst, traffic FROM tm WHERE tm_date = ? AND tm_time = ?", 
                             values):
            src = row[0]
            dst = row[1]
            traffic = row[2]
            
            i = self.graph.node_list.index(self.graph.find_node(src))
            j = self.graph.node_list.index(self.graph.find_node(dst))
            tm[i][j] = traffic
                
        conn.close()

        return tm        
        
    def get_routing_matrix(self):
        number_of_nodes = len(self.graph.node_list)
        routing_matrix = np.zeros(shape=(len(self.graph.link_list), number_of_nodes ** 2))
        
        for i in range(0, number_of_nodes):
            src = self.graph.node_list[i]
            metric, prev = self.graph.shortest_path(self.graph.node_list[i])
            for j in range(0, number_of_nodes):
                hop = self.graph.node_list[j]
                while hop != src:
                    if prev[hop] == None:
                        # no path
                        # print("No path from " + self.graph.node_list[i].node_id + " to " + self.graph.node_list[j].node_id)
                        for k in range(0, len(self.graph.link_list)):
                            routing_matrix[k][i * number_of_nodes + j] = 0
                        break                    
                    link = self.graph.find_link(prev[hop], hop)
                    routing_matrix[self.graph.link_list.index(link)][i * number_of_nodes + j] = 1
                    hop = prev[hop]
                    
        return routing_matrix

    def get_routing_matrix_max_available(self, link_util):
        number_of_nodes = len(self.graph.node_list)
        routing_matrix = np.zeros(shape=(len(self.graph.link_list), number_of_nodes ** 2))
        
        for i in range(0, number_of_nodes):
            src = self.graph.node_list[i]
            metric, prev = self.graph.shortest_path_max_available(self.graph.node_list[i], link_util)
            for j in range(0, number_of_nodes):
                hop = self.graph.node_list[j]
                while hop != src:
                    if prev[hop] == None:
                        # no path
                        # print("No path from " + self.graph.node_list[i].node_id + " to " + self.graph.node_list[j].node_id)
                        for k in range(0, len(self.graph.link_list)):
                            routing_matrix[k][i * number_of_nodes + j] = 0
                        break                    
                    link = self.graph.find_link(prev[hop], hop)
                    routing_matrix[self.graph.link_list.index(link)][i * number_of_nodes + j] = 1
                    hop = prev[hop]
                    
        return routing_matrix

    def get_routing_matrix_valiant(self):
        number_of_nodes = len(self.graph.node_list)
        routing_matrix = np.zeros(shape=(len(self.graph.link_list), number_of_nodes ** 2))
        
        for i in range(0, number_of_nodes):
            src = self.graph.node_list[i]
            metric, prev = self.graph.shortest_path_valiant(self.graph.node_list[i])
            for j in range(0, number_of_nodes):
                hop = self.graph.node_list[j]
                while hop != src:
                    if prev[hop] == None:
                        # no path
                        # print("No path from " + self.graph.node_list[i].node_id + " to " + self.graph.node_list[j].node_id)
                        for k in range(0, len(self.graph.link_list)):
                            routing_matrix[k][i * number_of_nodes + j] = 0
                        break                    
                    link = self.graph.find_link(prev[hop], hop)
                    routing_matrix[self.graph.link_list.index(link)][i * number_of_nodes + j] = 1
                    hop = prev[hop]
                    
        return routing_matrix

    def get_routing_matrix_no_KSCY_HSTN(self):
        number_of_nodes = len(self.graph.node_list)
        routing_matrix = np.zeros(shape=(len(self.graph.link_list), number_of_nodes ** 2))
        
        for i in range(0, number_of_nodes):
            src = self.graph.node_list[i]
            metric, prev = self.graph.shortest_path_no_KSCY_HSTN(self.graph.node_list[i])
            for j in range(0, number_of_nodes):
                hop = self.graph.node_list[j]
                while hop != src:
                    if prev[hop] == None:
                        # no path
                        # print("No path from " + self.graph.node_list[i].node_id + " to " + self.graph.node_list[j].node_id)
                        for k in range(0, len(self.graph.link_list)):
                            routing_matrix[k][i * number_of_nodes + j] = 0
                        break                    
                    link = self.graph.find_link(prev[hop], hop)
                    routing_matrix[self.graph.link_list.index(link)][i * number_of_nodes + j] = 1
                    hop = prev[hop]
                    
        return routing_matrix
    
    def get_link_load(self, tm):
        flattened_tm = tm.flatten("F")
        routing_matrix = self.get_routing_matrix()
                    
        return np.dot(routing_matrix, flattened_tm)

    def get_link_load_max_available(self, tm, link_util):
        flattened_tm = tm.flatten("F")
        routing_matrix = self.get_routing_matrix_max_available(link_util)
                    
        return np.dot(routing_matrix, flattened_tm)

    def get_link_load_valiant(self, tm):
        flattened_tm = tm.flatten("F")
        routing_matrix = self.get_routing_matrix_valiant()
                    
        return np.dot(routing_matrix, flattened_tm)

    def get_link_load_no_KSCY_HSTN(self, tm):
        flattened_tm = tm.flatten("F")
        routing_matrix = self.get_routing_matrix_no_KSCY_HSTN()
                    
        return np.dot(routing_matrix, flattened_tm)
            
    def get_link_util(self, link_load):
        link_util = np.zeros(shape=(len(link_load)))
        for i in range(0, len(link_load)):
            link_util[i] = link_load[i] / self.graph.link_list[i].bw
        return link_util    
    
    def estimate_tm_by_gravity(self, link_load):
        tm = np.zeros(shape=((len(self.graph.node_list), len(self.graph.node_list))))
        
        for i in range(0, len(self.graph.node_list)):
            metric, prev = self.graph.shortest_path(self.graph.node_list[i])
            for j in range(0, len(self.graph.node_list)):
                T_in_i = 0
                T_out_j = 0
                for m in range(0, len(self.graph.link_list)):
                    if self.graph.link_list[m].link_to == self.graph.node_list[i]:
                        T_in_i += link_load[m]
                    if self.graph.link_list[m].link_from == self.graph.node_list[j]:
                        T_out_j += link_load[m]
                
                T_out_k = T_out_j                
                hop = self.graph.node_list[j]
                while hop != self.graph.node_list[i]:
                    for m in range(0, len(self.graph.link_list)):
                        if self.graph.link_list[m].link_from == hop:
                            T_out_k += link_load[m]
                    hop = prev[hop]
                for m in range(0, len(self.graph.link_list)):
                    if self.graph.link_list[m].link_from == self.graph.node_list[i]:
                        pass                        
                        T_out_k += link_load[m]
                
                tm[i][j] = T_in_i * T_out_j / T_out_k
        return tm
        
    def estimate_tm_by_tomograph(self, link_load):
        routing_matrix = self.get_routing_matrix()
                        
        tm = nnls(routing_matrix, link_load)[0]
        tm = tm.reshape((len(self.graph.node_list), len(self.graph.node_list)), order='F')
        return tm
        
    def estimate_tm_by_tomogravity(self, link_load):
        routing_matrix = self.get_routing_matrix()
        gravity_tm = self.estimate_tm_by_gravity(link_load).flatten("F")
        
        link_load_diff = link_load - np.dot(routing_matrix, gravity_tm)
        tm_diff = np.dot(np.linalg.pinv(routing_matrix), link_load_diff)
        
        tm = gravity_tm + tm_diff     
        
        # setup for IPF        
        for i in range(0, len(tm)):
            if tm[i] < 0:
                tm[i] = 0
                
        MAX_ITER = 1000
        ESP = 2.e-10 
        counter = 0      
        error = float("inf")
        while counter < MAX_ITER and error > ESP:
            for j in range(0, len(self.graph.link_list)):
                scale = link_load[j] / np.dot(tm, routing_matrix[j])
                for m in range(0, len(tm)):
                    if routing_matrix[j][m] == 1:
                        tm[m] = tm[m] * scale
                        
            error = np.linalg.norm(np.dot(routing_matrix, tm) - link_load)
            counter += 1
        
        tm = tm.reshape((len(self.graph.node_list), len(self.graph.node_list)), order='F')        
                    
        return tm

    