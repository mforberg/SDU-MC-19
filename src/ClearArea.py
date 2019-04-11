from variables.MC_LIBRARY import *
import MapAnalysis
# noinspection PyUnresolvedReferences
import utilityFunctions
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am


def modify_area(height_map, solution, level):
    for building in solution:
        average_height = MapAnalysis.find_average_height(building, height_map, False)
        for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
                zero_difference = False
                while not zero_difference:
                    current_difference = average_height - height_map[x, z][0]
                    """
                    if there is no difference
                    else if average_height is bigger than the height_map location
                    else the average_height is smaller than the height_map location
                    """
                    if current_difference == 0:
                        break
                    elif current_difference > 0:
                        utilityFunctions.setBlock(level, (am.Dirt.ID, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] += 1
                    else:
                        utilityFunctions.setBlock(level, (am.Air.ID, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] -= 1