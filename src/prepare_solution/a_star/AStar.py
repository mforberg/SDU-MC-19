from variables.MC_LIBRARY import buildings

"""
Can find Manhattan distance for all buildings
Can add list of blocked coordinates based on final solution
Can find if a tile (x,z) is walkable compared to our final list of buildings com
"""

list_of_blocked_coordinates = list()

def run(list_of_buildings, height_map, level):

    list_of_all_building_paths = list()
    goal = find_well(list_of_buildings) #the well is the goal

    for building in list_of_buildings:
        if building.type_of_house == "well":
            continue #don't generate paths from well to well
        """- - - - - - - - - - - - - - - - - - - - """
        """ Generate paths for each building"""
        building_path = list() # should be list of x,z,y that is the path from current building to well



def find_well(list_of_buildings):
    for building in list_of_buildings: # the well is the goal, locate it first
        if building.type_of_house == "well": #
            goal = building
            break
    return goal

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

def is_walkable(x, z):
    for tuple in list_of_blocked_coordinates:
        # construct a rectangle based on the specifications of the building
        min_x = tuple[0]
        max_x = tuple[2]
        min_z = tuple[1]
        max_z = tuple[3]
        # if the overlap return faæse
        if x > min_x & x < max_x & z > min_z & z < max_z:
            return False
    #does not overlap -> it is walkable
    return True

def find_neighbors(x,z):
    print "should do stuff"







