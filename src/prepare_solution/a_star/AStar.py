from variables.MC_LIBRARY import buildings
from src.prepare_solution.a_star.PrepareAStar import find_well
from heapq import *
from Queue import PriorityQueue

"""
Can find Manhattan distance for all buildings
Can add list of blocked coordinates based on final solution
Can find if a tile (x,z) is walkable compared to our final list of buildings com
"""

list_of_blocked_coordinates = list()

def run(list_of_buildings, height_map):

    list_of_all_building_paths = list()
    goal = find_well(list_of_buildings) #the well is the goal

    for building in list_of_buildings:
        if building.type_of_house == "well":
            continue #don't generate paths from well to well
        """- - - - - - - - - - - - - - - - - - - - """
        """ Generate paths for each building"""
        building_path = list() # should be list of x,z,y that is the path from current building to well

        open_list = PriorityQueue()
        neighbor_list = list()

        coords_for_building = building.path_connection_point
        start = (coords_for_building[0], coords_for_building[1], coords_for_building[2]) #x,z,y
        goal_y = height_map[goal.x, goal.z][0]
        coords_for_well = (goal.x, goal.z, goal_y)
        end = (coords_for_well[0], coords_for_well[1], coords_for_well[2]) #x,z,y
        open_list.put((0, start))
        while not open_list.empty():
            current_node = open_list.get()
            if current_node == end:
                break
            neighbors = find_neighbors_for_current_node(current_node, end, height_map)
            for neighbor in xrange(0,len(neighbors)):
                current_neighbor = neighbors[neighbor]

                # have to check if neighbor has been seen before, how do???
                if not current_neighbor in neighbor_list:
                    neighbor_list.append(current_neighbor)

                x = current_neighbor[0]
                z = current_neighbor[1]
                y = current_neighbor[2]




def manhattan_distance_between(current, goal): # current, goal = tuple (x, z, y)
    x = abs(current[0] - goal[0])
    z = abs(current[1] - goal[1])
    y = abs(current[2] - goal[2])
    return x + z + y

def manhattan_distance(list_of_buildings):
    well = find_well(list_of_buildings)
    for building in list_of_buildings:
        if building.type_of_house == "well":
            continue
        connection_point = building.path_connection_point # (x, z, y)
        distance = abs(connection_point[0] - well.x) + abs(connection_point[1] - well.z)
        print distance


def blocked_tiles(list_of_buildings):
    for building in list_of_buildings:
        max_x = building.x + buildings[building.type_of_house]["xLength"]
        max_z = building.z + buildings[building.type_of_house]["zWidth"]
        tuple = (building.x, building.z, max_x, max_z) # min_x, min_z, max_x, max_z
        list_of_blocked_coordinates.append(tuple)

def is_walkable(node):
    for tuple in list_of_blocked_coordinates:
        # construct a rectangle based on the specifications of the building
        min_x = tuple[0]
        max_x = tuple[2]
        min_z = tuple[1]
        max_z = tuple[3]
        # if the overlap return false
        if node[0] > min_x & node[0] < max_x & node[1] > min_z & node[1] < max_z:
            return False
    #does not overlap -> it is walkable
    return True

def altitude_check(node, neighbor):
    max_height = 2
    altitude_difference = abs(neighbor[2] - node[1][2])
    if max_height > altitude_difference:
        return True
    return False


def find_neighbors_for_current_node(node, goal, height_map):

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbor_list = list()
    for x, z in neighbors:
        cost_so_far = node[0]
        neighbor_x = node[1][0] + x
        neighbor_z = node[1][1] + z
        neighbor_y = height_map[neighbor_x, neighbor_z][0]
        neighbor = (neighbor_x, neighbor_z, neighbor_y)
        if not is_walkable(neighbor):
            continue
        if not altitude_check(node, neighbor):
            continue
        #neighbor_manhattan_cost = manhattan_distance_between(neighbor, goal)

        #cost_so_far += 1 # TODO: should account for water
        #actual_cost = neighbor_manhattan_cost + cost_so_far

        #neighbor_with_cost = (actual_cost, neighbor)
        neighbor_list.append(neighbor)
    return neighbor_list







