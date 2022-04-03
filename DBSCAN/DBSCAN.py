# -*- coding: utf-8 -*-
"""
Homework 4 : Clustering
@author: Yun-Hsuan, Liang  N26101892
"""
import numpy as np
import matplotlib.pyplot as plt

node_list = []
core_point_list = []
non_core_point_list = []

RADIUS = 4.5
MIN_NEIGHBOR_NUM = 3

class node():
    def __init__(self):
        self.id = -1
        self.x = 0
        self.y = 0
        self.neighbor_number = 0
        self.cluster = int(0)
        
def get_data_attribute(input_file):
    input_file = open(input_file, "r", encoding="utf-8")
    id = 0
    for line in input_file:
        new_node = node()
        str = line[:-1].split(' ')
        new_node.id = id
        new_node.x = float(str[0])
        new_node.y = float(str[1])
        node_list.append(new_node)
        id += 1
    return node_list, id


def is_neighbor(node1, node2, radius):
    if node1.x == node2.x and node1.y == node2.y :
        return False
    distance = ( (node1.x - node2.x)**2 + (node1.y - node2.y)**2 )**0.5
    if distance >= radius :
        return False # too far, not neighbor 
    return True


def checkif_core_point():
    for node1 in node_list:
        for its_neighbor in node_list:
            if is_neighbor(node1, its_neighbor, RADIUS) :
                node1.neighbor_number += 1
        if node1.neighbor_number > MIN_NEIGHBOR_NUM : # mark as a core point
            core_point_list.append(node1)
        else:
            non_core_point_list.append(node1)

def print_list(node_list) :
    for node in node_list :
        print(node.id, node.x, node.y, node.cluster, node.neighbor_number)

"""
def visit_neighbor(start_node, search_node_list) :
    if len(search_node_list) == 0:
        return
    for its_neighbor in search_node_list :
        if is_neighbor(start_node, its_neighbor, RADIUS):
            its_neighbor.cluster = start_node.cluster
            node_list[ its_neighbor.id ].cluster = start_node.cluster
            break
"""

def DBscan():
    i = 1
    while not len(core_point_list) == 0:
        rand_point = core_point_list[0] 
        if rand_point.cluster == 0 :
            rand_point.cluster = i
            i += 1

        for point in core_point_list:
            if is_neighbor(point, rand_point, RADIUS*2): # if the point belongs to that cluster
                point.cluster = rand_point.cluster
                node_list[ point.id ].cluster = rand_point.cluster
        
        core_point_list.remove(rand_point)
                
        for point in non_core_point_list: # scan all the non-core node
            for other_point in core_point_list:
                if is_neighbor(point, other_point, RADIUS*2) and not other_point.cluster == 0 :
                    point.cluster = other_point.cluster
                    node_list[ point.id ].cluster = other_point.cluster
                    non_core_point_list.remove(point)
                    break

def output(length):
    output_file_name = input("Please enter the output file name:")
    file_output = open(output_file_name, "w")
    for i in range(1, length):
        file_output.write(str(node_list[i].x)+" "+str(node_list[i].y)+" "+str(node_list[i].cluster)+'\n')
        print(str(node_list[i].x), str(node_list[i].y), str(node_list[i].cluster) )
    create_scatter_graph()
    file_output.close()
       
def create_scatter_graph() :
    plt.figure(figsize=(6, 6), dpi=80)
    plt.title("Scatter Plot")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    colors = np.array(["red","green","orange","yellow","pink","black","blue","purple"])
    for node in node_list :
        plt.scatter(node.x, node.y, c=colors[node.cluster % 8])
    plt.savefig("output.png")
    plt.show()
    
    
if __name__ == '__main__':
    input_file = input("Enter the input file name (e.g. Clustering_test1):")
    node_list, node_length = get_data_attribute(input_file)
    
    checkif_core_point() 
    core_point_list = sorted(core_point_list, key = lambda s: (s.x, s.y) )

    DBscan()
    # node_list = sorted(node_list, key = lambda s: s.cluster)
    output(node_length)
    
    
    
    
    