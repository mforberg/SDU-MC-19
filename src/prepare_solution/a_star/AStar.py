from variables.MC_LIBRARY import buildings
from src.prepare_solution.a_star.PrepareAStar import find_well
from heapq import *
from Queue import PriorityQueue
import utilityFunctions
from pymclevel import alphaMaterials as am
from src.genetic_algorithm.CheckCriterias import check_if_within_box
import time



"""
Can find Manhattan distance for all buildings
Can add list of blocked coordinates based on final solution
Can find if a tile (x,z) is walkable compared to our final list of buildings com
"""

list_of_blocked_coordinates = list()


def run(list_of_buildings, height_map, level, box_length, box_width, starting_point):
    list_of_all_building_paths = list()
    blocked_tiles(list_of_buildings)
    sorted_buildings = sort_buildings_by_distance(list_of_buildings, height_map)
    goal = heappop(sorted_buildings)[1]  # the well is the goal
    while sorted_buildings:
        building = heappop(sorted_buildings)[1]
        if building.type_of_house == "well":
            continue  # don't generate paths from well to well
        """- - - - - - - - - - - - - - - - - - - - """
        """ Generate paths for each building"""
        building_path = list()  # should be list of x,z,y that is the path from current building to well

        open_heap = []

        coords_for_building = building.path_connection_point
        start = (coords_for_building[0], coords_for_building[1]+building.buffer_direction, coords_for_building[2])  # x,z,y
        goal_y = height_map[goal.x, goal.z][0]
        center_x = goal.x + (buildings["well"]["xLength"]/2)
        center_z = goal.z + (buildings["well"]["zWidth"]/2)
        coords_for_well = (center_x, center_z, goal_y)
        end = (coords_for_well[0], coords_for_well[1], coords_for_well[2])  # x,z,y
        parent_dict = {}
        close_list = set()
        utilityFunctions.setBlock(level, (am.Wood.ID, 0), start[0], start[2], start[1] )

        g_scores = {start: 0}
        f_scores = {start: manhattan_distance_between(start, end)}

        heappush(open_heap, (f_scores[start], start))
        while open_heap:
            current_node = heappop(open_heap)[1] #check what this does
            if current_node == end:
                backtracking = []
                while current_node in parent_dict:
                    utilityFunctions.setBlock(level, (am.Wood.ID, 0), current_node[0], current_node[2], current_node[1])
                    backtracking.append(current_node)
                    current_node = parent_dict[current_node]
                list_of_all_building_paths.append(backtracking)
                break
            close_list.add(current_node)
            neighbors = find_neighbors_for_current_node(current_node, height_map, box_length, box_width, starting_point, level)
            for neighbor in xrange(0, len(neighbors)):
                current_neighbor = neighbors[neighbor]

                #Cost is calculated for the neighbor nodes
                cost_so_far = g_scores[current_node]

                h_cost = manhattan_distance_between(current_neighbor, end)
                g_cost = cost_so_far + 1 #TODO: Should account for water

                if current_neighbor in close_list and g_cost >= g_scores.get(current_neighbor, 0):
                    continue

                if current_neighbor not in [i[1] for i in open_heap] or g_cost < g_scores.get(current_neighbor, 0):
                    parent_dict[current_neighbor] = current_node
                    g_scores[current_neighbor] = g_cost
                    f_scores[current_neighbor] = g_cost + h_cost
                    heappush(open_heap, (f_scores[current_neighbor], current_neighbor))

    return list_of_all_building_paths


def sort_buildings_by_distance(list_of_buildings, height_map):
    well = find_well(list_of_buildings)
    well_coords = (well.x, well.z, height_map[well.x, well.z][0])
    sorted_buildings = []
    for building in list_of_buildings:
        x = building.x
        z = building.z
        y = height_map[x, z][0]
        building_coords = (x, z, y)

        distance = manhattan_distance_between(building_coords, well_coords)
        heappush(sorted_buildings, (distance, building))
    return sorted_buildings


def manhattan_distance_between(current, goal):  # current, goal = tuple (x, z, y)
    x = abs(current[0] - goal[0])
    z = abs(current[1] - goal[1])
    y = abs(current[2] - goal[2])
    return x + z + y


def manhattan_distance(list_of_buildings):
    well = find_well(list_of_buildings)
    for building in list_of_buildings:
        if building.type_of_house == "well":
            continue
        connection_point = building.path_connection_point  # (x, z, y)
        distance = abs(connection_point[0] - well.x) + abs(connection_point[1] - well.z)
        print distance


def blocked_tiles(list_of_buildings):
    for building in list_of_buildings:
        if building.type_of_house == "well":
            continue
        max_x = building.x + buildings[building.type_of_house]["xLength"]
        max_z = building.z + buildings[building.type_of_house]["zWidth"]
        rectangle = (building.x, building.z, max_x, max_z)  # min_x, min_z, max_x, max_z
        list_of_blocked_coordinates.append(rectangle)
    return list_of_blocked_coordinates


# TODO: remove level and util
def is_walkable(node, level):
    for rectangle in list_of_blocked_coordinates:
        # construct a rectangle based on the specifications of the building
        min_x = rectangle[0]
        max_x = rectangle[2]
        min_z = rectangle[1]
        max_z = rectangle[3]

        # if the overlap return false
        if node[0] >= min_x and node[0] < max_x and node[1] >= min_z and node[1] < max_z:
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), node[0], node[2], node[1])
            return False
    # does not overlap -> it is walkable
    return True


def altitude_check(node, neighbor):
    max_height = 2
    altitude_difference = abs(neighbor[2] - node[2])
    if max_height > altitude_difference:
        return True
    return False


def find_neighbors_for_current_node(node, height_map, box_length, box_width, starting_point, level):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbor_list = list()
    for x, z in neighbors:
        neighbor_x = node[0] + x
        neighbor_z = node[1] + z
        try:
            neighbor_y = height_map[neighbor_x, neighbor_z][0]
        except KeyError:
            neighbor_y = height_map[0, 0][0]
        neighbor = (neighbor_x, neighbor_z, neighbor_y)

        # TODO: check if the node is null(it is out of bounce of the world)


        if within_bounds(neighbor, box_length, box_width, starting_point):
            continue
        if not is_walkable(neighbor, level):
            continue
        if not altitude_check(node, neighbor):
            continue
        neighbor_list.append(neighbor)
    return neighbor_list


def within_bounds(node, box_length, box_width, starting_point):
    max_z = box_width + starting_point["z"]
    max_x = box_length + starting_point["x"]

    if abs(starting_point["x"]) < abs(node[0]) < max_x and abs(starting_point) < abs(node[1]) < max_z:
        return True
    return False
