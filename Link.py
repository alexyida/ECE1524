class Link(object):
    def __init__(self, link_id, link_from, link_to, bw):
        self.link_id = link_id
        self.link_from = link_from
        self.link_to = link_to
        self.bw = bw
        
    def weight(self):
        return 9920000 / self.bw