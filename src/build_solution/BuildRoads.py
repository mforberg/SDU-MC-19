# noinspection PyUnresolvedReferences
import utilityFunctions
from variables.MC_LIBRARY import *
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
# noinspection PyUnresolvedReferences
from mcplatform import *

gravel_material = (am.Gravel.ID, 0)
ladder = am.Ladder.ID

def build_roads(list_of_coordinates, level):
    direction_lib = [5, 4, 3, 2]

    for roads in list_of_coordinates:
        for coordinates in roads:
            parent_node = coordinates[0]
            print parent_node, "parent"
            for current_node in coordinates:
                current_node_x = current_node[0]
                current_node_z = current_node[1]
                current_node_y = current_node[2]
                height_difference = parent_node[2] - current_node_y

                utilityFunctions.setBlock(level, gravel_material, current_node_x, current_node_y, current_node_z)

                if abs(height_difference) >= 2:
                    parent_node_x = parent_node[0]
                    parent_node_z = parent_node[1]

                    length_difference = current_node_x - parent_node_x
                    width_difference = current_node_z - parent_node_z

                    direction_node = current_node  # Going downhill
                    if height_difference < 0:
                        direction_lib = [4, 5, 2, 3]
                        direction_node = parent_node  # Going uphill

                    height_difference = abs(height_difference)

                    if length_difference == 1:
                        utilityFunctions.setBlock(level, (ladder, direction_lib[0]), direction_node[0], direction_node[2] + 1, direction_node[1])
                    elif length_difference == -1:
                        utilityFunctions.setBlockToGround(level, (ladder, direction_lib[1]), direction_node[0], direction_node[2] + height_difference+1, direction_node[1], direction_node[2]+1)
                    elif width_difference == 1:
                        utilityFunctions.setBlockToGround(level, (ladder, direction_lib[2]), direction_node[0], direction_node[2] + height_difference+1, direction_node[1], direction_node[2]+1)
                    else:
                        utilityFunctions.setBlockToGround(level, (ladder, direction_lib[3]), direction_node[0], direction_node[2] + height_difference+1, direction_node[1], direction_node[2]+1)
                parent_node = current_node


def direction(height_difference, current_node, parent_node, direction_lib):
    if height_difference < 0:
        direction_lib = [4, 5, 2, 3]
        return parent_node  # Going uphill
    return current_node  # Going downhill


