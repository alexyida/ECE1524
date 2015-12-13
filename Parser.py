import xml.etree.ElementTree as ET
from Node import *
from Link import *
from Graph import *
import sqlite3
import json
import os

class Parser(object):
    @staticmethod
    def parse_topology(generate_json):
        """"generate JSON file for visualization if generate_json == True"""
        
        tree = ET.parse("abilene-TM" + os.sep + "topo" + os.sep + "Abilene-Topo-10-04-2004.xml")
        root = tree.getroot()
        
        topology = root.find("topology")
        
        node_list = []
        link_list = []
        graph = Graph(node_list, link_list)
        
        if generate_json:
            f = open("data.json", "w")
            output = {"nodes":{}, "links":[]}
        
        for node in topology.iter("node"):
            new_node = Node(node.attrib["id"])
            node_list.append(new_node)   
            
            if generate_json:
                location = node.find("location")
                new_node.set_location(float(location.attrib["latitude"]),
                                      float(location.attrib["longitude"]))
                output["nodes"][new_node.node_id] =\
                    (float(location.attrib["latitude"]), 
                     float(location.attrib["longitude"])) 
                        
        for link in topology.iter("link"):
            link_id = link.attrib["id"]
            link_from = graph.find_node(link.find("from").attrib["node"])
            link_to = graph.find_node(link.find("to").attrib["node"])
            bw = int(link.find("bw").text)
            new_link = Link(link_id, link_from, link_to, bw)
            link_list.append(new_link)
            
            if generate_json:
                output["links"].append(\
                    ((link_from.lat, link_from.lng), 
                     (link_to.lat, link_to.lng)))
                
        igp = root.find("igp").find("links")
        for link in igp.iter("link"):
            link_id = link.attrib["id"]
            link_obj = graph.find_link_by_id(link_id)
            if link_obj != None:
                link_obj.metric = float(link.find("static").find("metric").text)
            
        if generate_json:    
            json.dump(output, f)            
            f.close()
            
        return graph
    
    @staticmethod
    def parse_traffic():
        conn = sqlite3.connect('tm.db')   
        c = conn.cursor()
        
        c.execute('''DROP TABLE IF EXISTS tm''')
        
        # Create table
        c.execute('''CREATE TABLE tm
                     (tm_date date, tm_time time, src text, dst text, traffic real)''')
        
        year = "2004"
        year_path = "abilene-TM" + os.sep + "TM" + os.sep + year
        for month in os.listdir(year_path):
            month_path = year_path + os.sep + month
            # print logs for each month
            print("=+=+ Now parsing month " + month)
            for xml in os.listdir(month_path):
                xml_path = month_path + os.sep + xml
                if os.path.isfile(xml_path) and xml_path.endswith("xml"):
                    file_name = xml.split(".")[0].split("-")
                    day = file_name[-2]
                    time = file_name[-1]
                    time = time[:2] + "-" + time[2:]
                    date = year + "-" + month + "-" + day
                    
                    tree = ET.parse(xml_path)
                    root = tree.getroot()
                            
                    intra_tm = root.find("IntraTM")
                    
                    for src in intra_tm.findall("src"):
                        
                        for dst in src.findall("dst"):             
                            # Insert a row of data
                            values = (date,time,src.attrib["id"], dst.attrib["id"], float(dst.text))
                            c.execute("INSERT INTO tm VALUES (?,?,?,?,?)", values)
                            
        # Save (commit) the changes
        conn.commit()                
                
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()         
                
        
    
