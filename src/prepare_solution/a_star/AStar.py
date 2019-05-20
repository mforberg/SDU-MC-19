from heapq import *
import copy

"""
Can find Manhattan distance for all buildings
Can add list of blocked coordinates based on final solution
Can find if a tile (x,z) is walkable compared to our final list of buildings com
"""

WATER_COST = 4  # water 5 times as expensive as ground
ALTITUDE_COST = 25


def run(building, height_map, box_length, box_width, starting_point, list_of_goals, list_of_blocked_coordinates):
        """- - - - - - - - - - - - - - - - - - - - """
        """ Generate paths for each building"""

        list_of_all_building_paths = list()
        open_heap = []
        parent_dict = {}
        close_list = set()
        distance_heap = []
        list_of_goals_copy = copy.deepcopy(list_of_goals)

        coords_for_building = building.path_connection_point
        coords_for_start_z = coords_for_building[1] + building.buffer_direction
        coords_for_start_y = height_map[coords_for_building[0], coords_for_start_z][0]
        start = (coords_for_building[0], coords_for_start_z, coords_for_start_y,
                 coords_for_building[1] + building.ladder_direction, coords_for_building[2])

        # Find goal with smallest distance from start
        g_scores = {start: 0}
        for goal in list_of_goals:
            distance = manhattan_distance_between(start, goal)
            heappush(distance_heap, (distance, goal))
        while distance_heap:
            end = heappop(distance_heap)[1]
            f_scores = {start: manhattan_distance_between(start, end)}
            heappush(open_heap, (f_scores[start], start))

            # Start A*
            while open_heap:
                current_node = heappop(open_heap)[1]

                if current_node in list_of_goals: # Check if node is goal
                    backtracking = []
                    while current_node in parent_dict:
                        backtracking.append(current_node)
                        current_node = parent_dict[current_node]
                    backtracking.append(start)  # Add start node
                    list_of_all_building_paths.append(backtracking)
                    for node in backtracking:
                        list_of_goals.append(node)
                    return list_of_all_building_paths

                close_list.add(current_node)
                neighbors = find_neighbors_for_current_node(current_node, height_map, box_length, box_width,
                                                            starting_point, list_of_blocked_coordinates)

                for neighbor in xrange(0, len(neighbors)):
                    current_neighbor = neighbors[neighbor]
                    block_type_neighbor = height_map[current_neighbor[0], current_neighbor[1]][1]

                    # Cost is calculated for the neighbor nodes
                    cost_so_far = g_scores[current_node]

                    h_cost = manhattan_distance_between(current_neighbor, end)

                    if block_type_neighbor == 8 or block_type_neighbor == 9:  # 8 = flowing water, 9 = still water
                        g_cost = cost_so_far + WATER_COST
                    else:
                        if not altitude_check(current_node, current_neighbor):
                            altitude_diff = abs(current_node[2] - current_neighbor[2])
                            g_cost = cost_so_far + ((altitude_diff*10)-10 + ALTITUDE_COST)
                        else:
                            g_cost = cost_so_far + 1

                    if current_neighbor in close_list and g_cost >= g_scores.get(current_neighbor, 0):
                        continue

                    if current_neighbor not in [i[1] for i in open_heap] or g_cost < g_scores.get(current_neighbor, 0):
                        parent_dict[current_neighbor] = current_node
                        g_scores[current_neighbor] = g_cost
                        f_scores[current_neighbor] = g_cost + h_cost
                        heappush(open_heap, (f_scores[current_neighbor], current_neighbor))
            if len(list_of_goals) > len(list_of_goals_copy):
                # Goal has been found for this node, makes sure to check for evey goal
                break
            continue
        return list_of_all_building_paths


def manhattan_distance_between(current, goal):  # current, goal = tuple (x, z, y)
    x = abs(current[0] - goal[0])
    z = abs(current[1] - goal[1])
    y = abs(current[2] - goal[2])
    return x + z + y


def is_walkable(node, list_of_blocked_coordinates):
    # Check for coordinate being walkable
    for rectangle in list_of_blocked_coordinates:
        # construct a rectangle based on the specifications of the building
        min_x = rectangle[0]
        max_x = rectangle[2]
        min_z = rectangle[1]
        max_z = rectangle[3]
        # if the overlap return false
        if node[0] >= min_x and node[0] < max_x and node[1] >= min_z and node[1] < max_z:
            return False
    # does not overlap -> it is walkable
    return True


def altitude_check(node, neighbor):
    max_height = 2
    altitude_difference = abs(neighbor[2] - node[2])
    if max_height > altitude_difference:
        return True
    return False


def lava_check(height_map, neighbor):
    block_type = height_map[neighbor[0], neighbor[1]]
    lava_still = 11  # still lava ID is 11, water is 9
    lava_flowing = 10  # lava can be flowing, different ID
    if block_type[1] == lava_still or block_type[1] == lava_flowing:
        return False
    return True


def find_neighbors_for_current_node(node, height_map, box_length, box_width, starting_point, list_of_blocked_coordinates):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbor_list = list()
    for x, z in neighbors:
        neighbor_x = node[0] + x
        neighbor_z = node[1] + z
        try:
            neighbor_y = height_map[neighbor_x, neighbor_z][0]
        except KeyError:
            # (x,z) is out of bounds, so set a random height value, it is never used as first check skips to next neighbor
            neighbor_y = 0
        neighbor = (neighbor_x, neighbor_z, neighbor_y)

        if not within_bounds(neighbor, box_length, box_width, starting_point): # always check bounds first :)
            continue
        if not lava_check(height_map, neighbor):
            continue
        if not is_walkable(neighbor, list_of_blocked_coordinates):
            continue
        neighbor_list.append(neighbor)
    return neighbor_list


def within_bounds(node, box_length, box_width, starting_point):
    # Check if node is within the box given
    max_z = box_width + starting_point["z"]
    max_x = box_length + starting_point["x"]

    if node[0] >= starting_point["x"] and node[0] < max_x and node[1] >= starting_point["z"] and node[1] < max_z:
        return True
    return False



