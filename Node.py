class Node(object):
    def __init__(self, node_id):
        self.node_id = node_id
        
    # use lat and lng for Google Maps API    
    def set_location(self, lat, lng):
        self.lat = lat
        self.lng = lng