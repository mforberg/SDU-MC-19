# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
# noinspection PyUnresolvedReferences
from mcplatform import *
from variables.MC_LIBRARY import *

am = alphaMaterials

# naturally occurring materials
blocks = [
    am.Grass.ID,
    am.Dirt.ID,
    am.Stone.ID,
    am.Bedrock.ID,
    am.Sand.ID,
    am.Gravel.ID,
    am.GoldOre.ID,
    am.IronOre.ID,
    am.CoalOre.ID,
    am.LapisLazuliOre.ID,
    am.DiamondOre.ID,
    am.RedstoneOre.ID,
    am.RedstoneOreGlowing.ID,
    am.Netherrack.ID,
    am.SoulSand.ID,
    am.Clay.ID,
    am.Glowstone.ID,
    am.Water.ID
]

# blocks we dont want to account for in the height map
skip_blocks = [
    am.Air.ID,
    am.Wood.ID,
    am.Leaves.ID
]

#zero indexed coordinates in the box
dimension_corrector = -1


def create_two_dimensional_height_map(level, box):
    position_dict = {}
    x_reference_point = 200
    """Find the reference point by going down the y-axiz untill there is a block that isn't in the skipBlocks"""
    for y in range(box.maxy + dimension_corrector, box.miny + dimension_corrector, -1):
        current_block = level.blockAt(box.maxx + dimension_corrector, y, box.maxz + dimension_corrector)
        if current_block in skip_blocks:
            continue
        x_reference_point = y
        break

    """From the reference point, start finding the heights"""
    for x in range(box.maxx + dimension_corrector, box.minx + dimension_corrector, -1):
        current_reference_point = x_reference_point
        only_update_once = True
        for z in range(box.maxz + dimension_corrector, box.minz + dimension_corrector, -1):
            current_block = level.blockAt(x, current_reference_point, z)
            """if air is found, go down until there is a non-air block"""
            if current_block in skip_blocks:
                while current_block in skip_blocks:
                    current_reference_point -= 1
                    current_block = level.blockAt(x, current_reference_point, z)
                y = current_reference_point
                position_dict[x, z] = [y, current_block]
                if only_update_once:
                    only_update_once = False
                    x_reference_point = y
            else:
                """if any other block is found, go up until air is found and -1 in the y-coordinate"""
                while current_block not in skip_blocks:
                    current_reference_point += 1
                    current_block = level.blockAt(x, current_reference_point, z)
                current_reference_point -= 1
                current_block = level.blockAt(x, current_reference_point, z)
                y = current_reference_point
                position_dict[x, z] = [y, current_block]
                if only_update_once:
                    only_update_once = False
                    x_reference_point = y
    return position_dict


def find_average_height(building, height_map, return_amount_of_water):
    total_area = buildings[building.typeOfHouse]["xLength"] * buildings[building.typeOfHouse]["zWidth"]
    list_of_heights = []
    amount = 0
    amount_of_water = 0
    for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
        for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
            """check for water"""
            if height_map[x, z][1] == 9:
                amount_of_water += 1
            amount += height_map[x, z][0]
            list_of_heights.append(height_map[x, z][0])
    average = int(round(amount / float(total_area)))
    if return_amount_of_water:
        return [average, amount_of_water]
    return average
