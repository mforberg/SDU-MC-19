# noinspection PyUnresolvedReferences
import utilityFunctions
from variables.MC_LIBRARY import *
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
# noinspection PyUnresolvedReferences
from mcplatform import *
from src.Building import *


def build(level, height_map, solution):

    for building in solution:
        if building.type_of_house == "well":
            well = building
            break

    for building in solution:

        height_of_building = buildings[building.type_of_house]["yHeight"]
        length_of_building = buildings[building.type_of_house]["xLength"] - (2 * BUFFER)
        width_of_building = buildings[building.type_of_house]["zWidth"] - (2 * BUFFER)

        house_type = buildings[building.type_of_house]["floorAndRoof"]
        y = height_map[building.x + BUFFER, building.z + BUFFER][0]

        if building.type_of_house == "blackSmith":
            build_floor_bs(level, length_of_building, width_of_building, height_of_building, y, building)

            build_black_smith(level, length_of_building, width_of_building, height_of_building, y, building)
            #build_door(level, y, well, building)
        else:
            build_walls(level, length_of_building, width_of_building, height_of_building, y, building)
            if house_type:
                build_floor(level, length_of_building, width_of_building, height_of_building, y, building)

                #build_door(level, length_of_building, width_of_building, y, well, building)


def build_walls(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x + BUFFER, building.x + BUFFER + length_of_building):
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height, building.z +
                                          BUFFER, box_height)
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                          building.z + width_of_building + BUFFER - 1, box_height)
    for z in range(building.z + BUFFER, building.z + BUFFER + width_of_building):
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + length_of_building + BUFFER - 1,
                                          height_of_building + box_height, z,
                                          box_height)
        utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + BUFFER, height_of_building + box_height,
                                          z, box_height)


def build_floor(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x + BUFFER, building.x + length_of_building + BUFFER):
        for z in range(building.z + BUFFER, building.z + width_of_building + BUFFER):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)


def build_black_smith(level, length_of_building, width_of_building, height_of_building, box_height, building):

    remove_top_square_x = building.x + BUFFER + length_of_building - 3
    remove_top_square_z = building.z + BUFFER + 2

    for x in range(building.x + BUFFER, remove_top_square_x):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height, building.z +
                                              BUFFER, box_height)
    for x in range(building.x + BUFFER, building.x + BUFFER + length_of_building):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                              building.z + width_of_building - 1 + BUFFER,
                                              box_height)
    for x in range(remove_top_square_x, building.x + length_of_building + BUFFER):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, height_of_building + box_height,
                                              remove_top_square_z,
                                              box_height)

    for z in range(building.z + BUFFER, building.z + width_of_building + BUFFER):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + BUFFER, height_of_building +
                                              box_height, z, box_height)
    for z in range(building.z + BUFFER, remove_top_square_z + 1):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0),
                                              remove_top_square_x, height_of_building + box_height, z,
                                              box_height)
    for z in range(building.z + width_of_building - 1 + BUFFER, remove_top_square_z, -1):
            utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), building.x + length_of_building - 1 + BUFFER,
                                              height_of_building + box_height, z, box_height)


def build_floor_bs(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x + BUFFER, building.x + length_of_building - 2 + BUFFER):
        for z in range(building.z + BUFFER, building.z + width_of_building + BUFFER):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)
    for x in range(building.x + length_of_building - 2 + BUFFER, building.x + length_of_building + BUFFER):
        for z in range(building.z + width_of_building - 1 + BUFFER, building.z + BUFFER + 1, -1):
            utilityFunctions.setBlock(level, (am.Wood.ID, 0), x, box_height, z)
            utilityFunctions.setBlock(level, (am.Obsidian.ID, 0), x, box_height + height_of_building, z)


def build_door(level, box_height, well, building):
    length_of_building = buildings[building.type_of_house]["xLength"] - (2 * BUFFER)
    width_of_building = buildings[building.type_of_house]["zWidth"] - (2 * BUFFER)

    if building.z < well.z:
        building.z = building.z + width_of_building - 1

    door_position = length_of_building / 2
    for i in range(1, 3):
        utilityFunctions.setBlock(level, (64, 1), building.x + door_position, box_height + i, building.z)

    Building.set_connection_point(well)
