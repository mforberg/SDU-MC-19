import AStar
import PrepareAStar
from heapq import *
from variables.MC_LIBRARY import *
import copy


list_of_blocked_coordinates = list()


def path_for_clusters(list_of_clusters, height_map, level, box_length, box_width, starting_point):
    list_of_building_paths = list()
    blocked_tiles(list_of_clusters)
    heaps = distance_for_cluster(list_of_clusters, height_map)
    list_of_goals = goals_for_well(list_of_clusters, height_map)
    poo = 0
    for item in list_of_clusters:
        for i in item:
            poo += 1
    print poo, "<--- poo"
    for x in xrange(0, len(list_of_clusters)):
        list_of_goals_copy = copy.deepcopy(list_of_goals)
        print " - - - - - - -"
        # for heap in heaps[x]:
        while heaps[x]:
            building = heappop(heaps[x])[1]
            print building.type_of_house
            if building.type_of_house == "well":
                continue
            AStar.run2(building, height_map, level, box_length, box_width, starting_point, list_of_goals_copy, list_of_blocked_coordinates)


def distance_for_cluster(list_of_clusters, height_map):
    goal = find_goal_in_cluster(list_of_clusters)
    goal_coords = (goal.x, goal.z, height_map[goal.x, goal.z][0])
    building_clusters = [[] for x in xrange(len(list_of_clusters))]
    for cluster in xrange(0, len(list_of_clusters)):
        for building in list_of_clusters[cluster]:
            x = building.x
            z = building.z
            y = height_map[x, z][0]

            building_coords = (x, z, y)
            distance = AStar.manhattan_distance_between(building_coords, goal_coords)
            heappush(building_clusters[cluster], (distance, building))
    return building_clusters


def points_to_buildings(list_of_clusters, list_of_buildings):
    building_clusters = [[] for x in xrange(len(list_of_clusters))]  # Will create k lists in a list

    for cluster in xrange(0, len(list_of_clusters)):
        for point in list_of_clusters[cluster]:
            point_tuple = (point[0], point[1], point[2])
            for building in list_of_buildings:
                if point_tuple == building.path_connection_point:
                    building_clusters[cluster].append(building)
                    break

    return building_clusters

def blocked_tiles(list_of_clusters):
    for cluster in list_of_clusters:
        for building in cluster:
            if building.type_of_house == "well":
                continue
            max_x = building.x + buildings[building.type_of_house]["xLength"]
            max_z = building.z + buildings[building.type_of_house]["zWidth"]
            rectangle = (building.x, building.z, max_x, max_z)  # min_x, min_z, max_x, max_z
            list_of_blocked_coordinates.append(rectangle)





def find_goal_in_cluster(list_of_clusters):
    for cluster in list_of_clusters:
        for building in cluster:
            if building.type_of_house == "well":
                goal = building
                return goal

def goals_for_well(list_of_clusters, height_map):
    goal = find_goal_in_cluster(list_of_clusters)
    well_goals = list()

    goal_y = height_map[goal.x, goal.z][0]
    print buildings["well"]["xLength"]
    print buildings["well"]["zWidth"]

    center_x = goal.x + ((buildings["well"]["xLength"] - (2*BUFFER)) / 2) + 1
    center_z = goal.z + ((buildings["well"]["zWidth"] - (2*BUFFER)) / 2) + 1
    top_x = goal.x + buildings["well"]["xLength"] - (2 * BUFFER) + 1
    top_z = goal.z + buildings["well"]["zWidth"] - (2 * BUFFER) + 1

    north_goal = (top_x, center_z, goal_y)
    south_goal = (goal.x, center_z, goal_y)
    west_goal = (center_x, top_z, goal_y)
    east_goal = (center_x, goal.z, goal_y)

    well_goals.append(north_goal)
    well_goals.append(south_goal)
    well_goals.append(west_goal)
    well_goals.append(east_goal)
    return well_goals
