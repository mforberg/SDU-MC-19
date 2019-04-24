from src.MapAnalysis import *
# noinspection PyUnresolvedReferences
import utilityFunctions
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as aM


def modify_area(height_map, solution, level):
    use_average = False
    for building in solution:
        reference_block = get_reference_block(height_map, building)
        """use the average height to create the ground for the building to be build on. This might cause unreachable
        buildings in hill areas"""
        if use_average:
            target_height = find_average_height(building, height_map)
        else:
            target_height = find_most_common_height_around_the_building(height_map, building)
        for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
                zero_difference = False
                while not zero_difference:
                    current_difference = target_height - height_map[x, z][0]
                    """
                    if there is no difference, set a block 
                    (used because the else statement does not put a block there when it gets to the correct floor)
                    else if target_height is bigger than the height_map location
                    else the target_height is smaller than the height_map location
                    """
                    if current_difference == 0:
                        utilityFunctions.setBlock(level, (reference_block, 0), x, height_map[x, z][0], z)
                        break
                    elif current_difference > 0:
                        utilityFunctions.setBlock(level, (reference_block, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] += 1
                    else:
                        utilityFunctions.setBlock(level, (reference_block, 0), x, height_map[x, z][0], z)
                        height_map[x, z][0] -= 1


def find_most_common_height_around_the_building(height_map, building):
    all_heights = list()
    for x in xrange(building.x - 1, building.x + buildings[building.type_of_house]["xLength"] + 1):
        if (x, building.z - 1) in height_map:
            all_heights.append(height_map[x, building.z - 1][0])
        if (x, building.z + buildings[building.type_of_house]["xLength"] + 1) in height_map:
            all_heights.append(height_map[x, building.z + buildings[building.type_of_house]["xLength"] + 1][0])
    for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
        if (building.x, z) in height_map:
            all_heights.append(height_map[building.x, z][0])
        if (building.x + buildings[building.type_of_house]["zWidth"] + 1, z) in height_map:
            all_heights.append(height_map[building.x + buildings[building.type_of_house]["zWidth"] + 1, z][0])
    return max(set(all_heights), key=all_heights.count)


def get_reference_block(height_map, building):
    reference_blocks = list()
    for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
        for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
            reference_blocks.append(height_map[building.x, building.z][1])
    return max(set(reference_blocks), key=reference_blocks.count)