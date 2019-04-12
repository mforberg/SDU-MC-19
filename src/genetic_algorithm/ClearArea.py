from variables.MC_LIBRARY import *
import src.MapAnalysis
# noinspection PyUnresolvedReferences
import utilityFunctions
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am


def modify_area(height_map, solution, level):
    for building in solution:
        average_height = src.MapAnalysis.find_average_height(building, height_map, False)
        for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
                zero_difference = False
                while not zero_difference:
                    current_difference = average_height - height_map[x, z][0]
                    """
                    if there is no difference, set a block 
                    (used because the else statement does not put a block there when it gets to the correct floor)
                    else if average_height is bigger than the height_map location
                    else the average_height is smaller than the height_map location
                    """
                    if current_difference == 0:
                        utilityFunctions.setBlock(level, (am.Dirt.ID, 0), x, height_map[x, z][0], z)
                        break
                    elif current_difference > 0:
                        utilityFunctions.setBlock(level, (am.Dirt.ID, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] += 1
                    else:
                        utilityFunctions.setBlock(level, (am.Air.ID, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] -= 1
