# noinspection PyUnresolvedReferences
import utilityFunctions
from variables.MC_LIBRARY import buildings as building_copy
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
# noinspection PyUnresolvedReferences
from mcplatform import *


def build(level, heightmap, buildings):

    for building in buildings:
        if building.typeOfHouse == "well":
            well_z = building.z

    for building in buildings:

        height_of_building = building_copy[building.typeOfHouse]["yHeight"]
        length_of_building = building_copy[building.typeOfHouse]["xLength"]
        width_of_building = building_copy[building.typeOfHouse]["zWidth"]

        house_type = building_copy[building.typeOfHouse]["floorAndRoof"]
        y = heightmap[building.x, building.z][0]

        if building.typeOfHouse == "blackSmith":
            build_floor_bs(level, length_of_building, width_of_building, height_of_building, y, building)
            build_black_smith(level, length_of_building, width_of_building, height_of_building, y, building)
            build_door(level, length_of_building, width_of_building, y, well_z, building)
        else:
            build_walls(level, length_of_building, width_of_building, height_of_building, y, building)
            if house_type:
                build_floor(level, length_of_building, width_of_building, height_of_building, y, building)

                build_door(level, length_of_building, width_of_building, y, well_z, building)


def build_walls(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x, building.x + length_of_building):
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height, building.z,
                                          box_height)
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                          building.z + width_of_building - 1,
                                          box_height)
    for z in range(building.z, building.z + width_of_building):
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + length_of_building - 1,
                                          height_of_building + box_height, z,
                                          box_height)
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x, height_of_building + box_height, z,
                                          box_height)


def build_floor(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x, building.x + length_of_building):
        for z in range(building.z, building.z + width_of_building):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)


def build_black_smith(level, length_of_building, width_of_building, height_of_building, box_height, building):

    removeTopSquareX = building.x + length_of_building - 3
    removeTopSquareZ = building.z + 2

    for x in range(building.x, removeTopSquareX):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height, building.z,
                                              box_height)
    for x in range(building.x, building.x + length_of_building):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                              building.z + width_of_building - 1,
                                              box_height)
    for x in range(removeTopSquareX, building.x + length_of_building):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                              removeTopSquareZ,
                                              box_height)

    for z in range(building.z, building.z + width_of_building):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x, height_of_building + box_height, z,
                                              box_height)
    for z in range(building.z, removeTopSquareZ + 1):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0),
                                              removeTopSquareX, height_of_building + box_height, z,
                                              box_height)
    for z in range(building.z + width_of_building - 1, removeTopSquareZ, -1):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + length_of_building - 1,
                                              height_of_building + box_height, z, box_height)


def build_floor_bs(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x, building.x + length_of_building - 2):
        for z in range(building.z, building.z + width_of_building):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)
    for x in range(building.x + length_of_building - 2, building.x + length_of_building):
        for z in range(building.z + width_of_building - 1, building.z + 1, -1):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)


def build_door(level, length_of_building, width_of_building, box_height, well_z, building):
    if building.z < well_z:
        building.z = building.z + width_of_building - 1

    door_position = length_of_building / 2
    for i in range(1, 3):
        utilityFunctions.setBlock(level, (64, 1), building.x + door_position, box_height + i, building.z)
