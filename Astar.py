import numpy as np
import math
import heapq
import time

import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
utility_dir = os.path.join(current_dir, 'Utility')
sys.path.append(utility_dir)
from plot_figure import Plot_figure
from bringup_grid_map import load_grid_map

"""
This python code is an algorithm that calculates a global path using A*, a global path planning algorithm.

Last modified date: 23.11.30

input: start position, goal position, grid map

output: global path

"""

class Node:
    def __init__(self, position, g_value, h_value, parent):
        
        self.g = g_value
        self.h = h_value
        self.f = self.g + self.h
        self.position = position
        self.parent = parent
    
    # To print the object itself created from the Node class
    def __str__(self):
        return f"Node(g_value={self.g}, h_value={self.h}, f_Value={self.f}, position={self.position}, parent={self.parent})"
    
    # For f value comparation
    def __lt__(self,other):
        return self.f < other.f
    
    # For position comparation
    def __eq__(self,other):
        return self.position == other.position

# Calculate the distance between two positions
def calculation_distance(current_position, goal_position):
    diff_x = goal_position[0] - current_position[0]
    diff_y = goal_position[1] - current_position[1]
    return round(math.sqrt(math.pow(diff_x, 2)+math.pow(diff_y, 2)), 1)


# A* algorithm
def astar(start_position, goal_position, grid_map):

    open_list = []
    closed_list = []
    
    open_list_fake = []
    closed_list_fake = []
    
    global_path = []
    direction = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]] # 8-direction

    dist = calculation_distance(start_position, goal_position)
    start_node = Node(start_position, 0, dist, None)

    heapq.heappush(open_list, (start_node.f, start_node))
    open_list_fake.append(start_node.position)
    
    while True:
        
        # Returns Node with the lowest f value in the current open_list
        if len(open_list) > 0:
            _, current_node = heapq.heappop(open_list)
            open_list_fake.remove(current_node.position)
            
            current_position = current_node.position
            current_g = current_node.g
            
            closed_list.append(current_node)
            closed_list_fake.append(current_node.position)
        
        # If there is no Node to return, no global path can be found
        else:
            print("[Error] Global path not found...")
            break
        
        # If the returned Node is the same as the Goal Node, 
        # use each Node's Parent Node to derive a global path.
        if current_node.position == goal_position:
            # Calculation global path
            while current_node.position != start_node.position:
                global_path.append(current_node.position)
                current_node = current_node.parent
            global_path.append(start_node.position)
            global_path.reverse()
            break
        
        # If the returned Node is not the Goal Node, 
        # start exploring neighboring Nodes around that Node.
        current_position = current_node.position
        current_g = current_node.g
        
        # Start exploring neighboring Nodes around that Node.
        for dir in direction:
            
            # Calculate Neighbor node position.
            neighbor_x = current_position[0] + dir[0]
            neighbor_y = current_position[1] + dir[1]
            neighbor_position = [neighbor_x, neighbor_y]

            # Check that the Neighbor node being explored is located in the grid map.
            if neighbor_position[0] < 1 or neighbor_position[0] > len(grid_map) or neighbor_position[1] < 1 or neighbor_position[1] > len(grid_map):
                continue
            
            # Check that the Neighbor node being explored is in the same location as the obstacle.
            if grid_map[neighbor_position[1]-1][neighbor_position[0]-1] == 1:
                continue
            
            # If the Neighbor node is not an obstacle -> Calculation distance (H = Euclidean distance)
            dist_g = current_g + calculation_distance(current_position, neighbor_position)
            dist_h = calculation_distance(neighbor_position, goal_position)

            # Create Neighbor node objects with classes
            neighbor_node = Node(neighbor_position, dist_g, dist_h, current_node)
            
            # If no Node exists in the open list
            if len(open_list) < 1:
                heapq.heappush(open_list, (neighbor_node.f, neighbor_node))
                open_list_fake.append(neighbor_node.position)
                
            # If there is a Node in the open list
            else:
                # If the Neighbor node exist in open list, compare f value to change parent node
                if neighbor_node.position in open_list_fake:
                    for _, node in open_list:
                        if node.position == neighbor_node.position and neighbor_node.f < node.f:
                            node.f = neighbor_node.f
                            node.parent = neighbor_node.parent
                            break
                        
                # If there are no Neighboring nodes in the open list that are being explored,
                else:
                    # If the closed list does not have a neighbor node that is being explored,
                    if  [neighbor_node.position] not in closed_list_fake:
                        heapq.heappush(open_list, (neighbor_node.f, neighbor_node))
                        open_list_fake.append(neighbor_node.position)
        
    return global_path


# main function
def main():
    
    ################################################## Load Grid map ##############################
    file_path = "Utility/grid_map_1.txt"
    #file_path = "Utility/grid_map_2.txt"
    grid_map = load_grid_map(file_path)
    
    if grid_map is not None:
        #print(f"File content:\n{grid_map}")
        print("[Info] Bring up grid map...!!")
    else:
        grid_map = np.zeros((30, 30))
    ###############################################################################################
    
    ################################## Start and Goal position setting ############################
    start, goal = [1, 1], [30, 30]
    
    print(f"[Info] Set start position: {start}, goal position: {goal}")
    print(f"[Info] Start global path planning from {start} to {goal} using the A* algorithm")
    ###############################################################################################
    
    # Check total calculation time
    start_time = time.time()
    
    ############### A* algorithm ###############
    global_path = astar(start, goal, grid_map)
    ############################################
    
    # Check total calculation time
    end_time = time.time()
    
    ####### 도출된 global path를 txt 파일로 저장 #######
    global_path_file = "global_path.txt"
    with open(global_path_file, "w") as file:
        file.write(str(global_path))
    print(f"[Info] Saved global path to txt file")
    ###################################################
    
    print(f"[Info] End global path planning !!")
    print(f"[Info] Global path: {global_path}")
    print(f"[Info] Total time: {round(end_time-start_time, 2)} [s]")
    
    ####### Plot figure using Matplotlib Tool #######
    plot = Plot_figure(start, goal, grid_map, global_path)
    plot.plot_figure()
    #################################################
    
if __name__ == '__main__':
    main()