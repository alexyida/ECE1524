"""A helper class for betweenness"""

class PriorityQueue(object):
    def __init__(self):
        self.l = []
        
    def put(self, item):
        for i in range(0, len(self.l)):
            if item[1] == self.l[i][1]:
                self.l[i] = item
                return
                
        self.l.append(item)
        
    def get(self):
        self.l.sort(key = lambda x : x[0])
        return self.l.pop(0)
        
    def empty(self):
        return len(self.l) == 0