from src.MapAnalysis import *
from variables.MC_LIBRARY import MAX_HEIGHT
# noinspection PyUnresolvedReferences
import utilityFunctions
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as aM

# naturally occurring materials we want
blocks = [
    am.Grass.ID,
    am.Dirt.ID,
    am.Stone.ID,
    am.Sand.ID,
    am.Gravel.ID,
    am.Snow.ID
]


def modify_area(height_map, solution, level):
    use_average = False
    for building in solution:
        """use the average height to create the ground for the building to be build on. This might cause unreachable
        buildings in hill areas"""
        if use_average:
            target_height = find_average_height(building, height_map)
        else:
            target_height = find_most_common_height_around_the_building(height_map, building)
        reference_block = get_reference_block(level, building, target_height)
        for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
                zero_difference = False
                while not zero_difference:
                    current_difference = target_height - height_map[x, z][0]
                    """
                    if there is no difference, set a block 
                    (used because the else statement does not put a block there when it gets to the correct floor)
                    else if target_height is bigger than the height_map location
                    else the target_height is smaller than the height_map location, clear everything down
                    """
                    if current_difference == 0:
                        utilityFunctions.setBlock(level, (reference_block, 0), x, height_map[x, z][0], z)
                        zero_difference = True  # Break
                    elif current_difference > 0:
                        if reference_block == aM.Grass.ID:
                            utilityFunctions.setBlock(level, (aM.Dirt.ID, 0), x, height_map[x, z][0], z)
                        else:
                            utilityFunctions.setBlock(level, (reference_block, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] += 1
                    else:
                        for y in xrange(MAX_HEIGHT, target_height, -1):
                            utilityFunctions.setBlock(level, (aM.Air.ID, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] = target_height


def get_reference_block(level, building, target_height):
    reference_blocks = list()
    for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
        for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
            if level.blockAt(x, target_height, z) in blocks:
                reference_blocks.append(level.blockAt(x, target_height, z))
    if len(reference_blocks) < 1:
        return aM.Dirt.ID
    else:
        return max(set(reference_blocks), key=reference_blocks.count)
