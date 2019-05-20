# noinspection PyUnresolvedReferences
import utilityFunctions
from variables.MC_LIBRARY import *
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
# noinspection PyUnresolvedReferences
from mcplatform import *

gravel = (am.Gravel.ID, 0)
ladder = am.Ladder.ID


def build_roads(list_of_coordinates, level):
    list_of_used_coordinates = []

    for roads in list_of_coordinates:
        for coordinates in roads:
            direction_lib = [5, 4, 3, 2]  # 5 = East, 4 = West, 3 = South, 2 = North
            reverse_list = coordinates[::-1]
            start_node = reverse_list[0]  # Get the start coordinate
            parent_node = coordinates[0]  # To check for altitude change
            check_start_node(start_node, direction_lib, level)  # Need to know if start node is level with the house coordinate
            for current_node in coordinates:
                if current_node not in list_of_used_coordinates:  # Will skip goal nodes which have been inserted
                    direction_lib = [5, 4, 3, 2]  # 5 = East, 4 = West, 3 = South, 2 = North

                    parent_node_y = parent_node[2]
                    current_node_x = current_node[0]
                    current_node_z = current_node[1]
                    current_node_y = current_node[2]
                    height_difference = calculate_difference(parent_node_y, current_node_y)

                    utilityFunctions.setBlock(level, gravel, current_node_x, current_node_y, current_node_z)
                    list_of_used_coordinates.append(current_node)

                    # If the height difference is equal or larger than 2, ladder it needed
                    if abs(height_difference) >= 2:
                        parent_node_x = parent_node[0]
                        parent_node_z = parent_node[1]

                        length_difference = calculate_difference(current_node_x, parent_node_x)
                        width_difference = calculate_difference(current_node_z, parent_node_z)

                        direction_node = current_node  # Going downhill
                        if height_difference < 0:
                            direction_lib = [4, 5, 2, 3]  # 4 = West, 5 = East, 2 = North, 3 = South
                            direction_node = parent_node  # Going uphill
                            # Making sure there are blocks where the ladder is created
                            insert_road(current_node_x, current_node_z, current_node_y, height_difference, level)

                        height_difference = abs(height_difference)

                        insert_ladder(length_difference, width_difference, height_difference, direction_node, direction_lib, level)
                parent_node = current_node
    del list_of_used_coordinates[:]


def insert_ladder(length_difference, width_difference, height_difference, direction_node, direction_lib, level):
    # Will decide where to place the ladder from the four directions
    if length_difference > 0:
        utilityFunctions.setBlockToGround(level, (ladder, direction_lib[0]), direction_node[0],
                                          direction_node[2] + height_difference + 1, direction_node[1],
                                          direction_node[2] + 1)
    elif length_difference < 0:
        utilityFunctions.setBlockToGround(level, (ladder, direction_lib[1]), direction_node[0],
                                          direction_node[2] + height_difference + 1, direction_node[1],
                                          direction_node[2] + 1)
    elif width_difference > 0:
        utilityFunctions.setBlockToGround(level, (ladder, direction_lib[2]), direction_node[0],
                                          direction_node[2] + height_difference + 1, direction_node[1],
                                          direction_node[2] + 1)
    else:
        utilityFunctions.setBlockToGround(level, (ladder, direction_lib[3]), direction_node[0],
                                          direction_node[2] + height_difference + 1, direction_node[1],
                                          direction_node[2] + 1)


def insert_road(current_node_x, current_node_z, current_node_y, height_difference, level):
    # Will create a pillar of road material
     for node_y in range(current_node_y + height_difference, current_node_y + 1):
         utilityFunctions.setBlock(level, gravel, current_node_x, node_y, current_node_z)


def calculate_difference(first_coord, second_coord):
    # The difference between two coordinates
    return first_coord - second_coord


def check_start_node(start_node, direction_lib, level):
    start_node_x = start_node[0]
    start_node_z = start_node[1]
    start_node_y = start_node[2]

    building_z = start_node[3]
    building_y = start_node[4]

    height_difference = abs(calculate_difference(start_node_y, building_y))
    width_difference = calculate_difference(start_node_z, building_z)
    length_difference = 0  # Will always be 0 in this case

    if start_node_y > building_y:
        building_node = (start_node_x, building_z, building_y)
        direction_lib = [4, 5, 2, 3]  # 4 = West, 5 = East, 2 = North, 3 = South
        insert_ladder(length_difference, width_difference, height_difference, building_node, direction_lib, level)
    elif start_node_y < building_y:
        insert_ladder(length_difference, width_difference, height_difference, start_node, direction_lib, level)

