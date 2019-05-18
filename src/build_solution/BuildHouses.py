# noinspection PyUnresolvedReferences
import utilityFunctions
from variables.MC_LIBRARY import *
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials as am
# noinspection PyUnresolvedReferences
from mcplatform import *

wood = (am.WoodPlanks.ID, 0)
cobble = (am.Cobblestone.ID, 0)
crops = (am.Crops.ID, 0)
dirt = (am.Farmland.ID, 7)
water = (am.WaterActive.ID, 0)
air = (am.Air.ID, 0)


def build(level, height_map, solution):

    for building in solution:
        height_of_building = buildings[building.type_of_house]["yHeight"]
        length_of_building = buildings[building.type_of_house]["xLength"] - (2 * BUFFER)
        width_of_building = buildings[building.type_of_house]["zWidth"] - (2 * BUFFER)

        house_type = buildings[building.type_of_house]["floorAndRoof"]
        y = height_map[building.x + BUFFER, building.z + BUFFER][0]

        if building.type_of_house == "blackSmith":
            build_floor_bs(level, length_of_building, width_of_building, height_of_building, y, building)

            build_black_smith(level, length_of_building, width_of_building, height_of_building, y, building)
            build_door(level, building)
        else:
            if house_type:
                build_walls(level, length_of_building, width_of_building, height_of_building, y, building, wood)
                build_floor(level, length_of_building, width_of_building, height_of_building, y, building)

                build_door(level, building)
            else:

                if building.type_of_house == "well":
                    water_in_well(level, length_of_building, width_of_building, y, building)
                else:
                    plant_in_farm(level, length_of_building, width_of_building, height_of_building, y, building)
                build_walls(level, length_of_building, width_of_building, height_of_building, y, building, cobble)


def build_walls(level, length_of_building, width_of_building, height_of_building, box_height, building, material):
    for x in range(building.x + BUFFER, building.x + BUFFER + length_of_building):
        utilityFunctions.setBlockToGround(level, material, x, height_of_building + box_height, building.z +
                                          BUFFER, box_height)
        utilityFunctions.setBlockToGround(level, material, x, height_of_building + box_height,
                                          building.z + width_of_building + BUFFER - 1, box_height)
    for z in range(building.z + BUFFER, building.z + BUFFER + width_of_building):
        utilityFunctions.setBlockToGround(level, material, building.x + length_of_building + BUFFER - 1,
                                          height_of_building + box_height, z,
                                          box_height)
        utilityFunctions.setBlockToGround(level, material, building.x + BUFFER, height_of_building + box_height,
                                          z, box_height)


def build_floor(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x + BUFFER, building.x + length_of_building + BUFFER):
        for z in range(building.z + BUFFER, building.z + width_of_building + BUFFER):
            utilityFunctions.setBlock(level, wood, x, box_height, z)
            utilityFunctions.setBlock(level, cobble, x, box_height + height_of_building, z)


def build_black_smith(level, length_of_building, width_of_building, height_of_building, box_height, building):

    remove_top_square_x = building.x + BUFFER + length_of_building - 3
    remove_top_square_z = building.z + BUFFER + 2

    for x in range(building.x + BUFFER, remove_top_square_x):
            utilityFunctions.setBlockToGround(level, wood, x, height_of_building + box_height, building.z +
                                              BUFFER, box_height)
    for x in range(building.x + BUFFER, building.x + BUFFER + length_of_building):
            utilityFunctions.setBlockToGround(level, wood, x, height_of_building + box_height,
                                              building.z + width_of_building - 1 + BUFFER,
                                              box_height)
    for x in range(remove_top_square_x, building.x + length_of_building + BUFFER):
            utilityFunctions.setBlockToGround(level, wood, x, height_of_building + box_height,
                                              remove_top_square_z,
                                              box_height)

    for z in range(building.z + BUFFER, building.z + width_of_building + BUFFER):
            utilityFunctions.setBlockToGround(level, wood, building.x + BUFFER, height_of_building +
                                              box_height, z, box_height)
    for z in range(building.z + BUFFER, remove_top_square_z + 1):
            utilityFunctions.setBlockToGround(level, wood,
                                              remove_top_square_x, height_of_building + box_height, z,
                                              box_height)
    for z in range(building.z + width_of_building - 1 + BUFFER, remove_top_square_z, -1):
            utilityFunctions.setBlockToGround(level, wood, building.x + length_of_building - 1 + BUFFER,
                                              height_of_building + box_height, z, box_height)


def build_floor_bs(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x + BUFFER, building.x + length_of_building - 2 + BUFFER):
        for z in range(building.z + BUFFER, building.z + width_of_building + BUFFER):
            utilityFunctions.setBlock(level, wood, x, box_height, z)
            utilityFunctions.setBlock(level, cobble, x, box_height + height_of_building, z)
    for x in range(building.x + length_of_building - 2 + BUFFER, building.x + length_of_building + BUFFER):
        for z in range(building.z + width_of_building - 1 + BUFFER, building.z + BUFFER + 1, -1):
            utilityFunctions.setBlock(level, wood, x, box_height, z)
            utilityFunctions.setBlock(level, cobble, x, box_height + height_of_building, z)


def build_door(level, building):
    door_coordinate = building.path_connection_point  # (x, z, y)
    for i in range(1, 3):
        utilityFunctions.setBlock(level, (64, 1), door_coordinate[0], door_coordinate[2] + i, door_coordinate[1])


def water_in_well(level, length_of_building, width_of_building, box_height, building):
    for x in range(building.x + BUFFER + 1, building.x + length_of_building + BUFFER - 1):
        for z in range(building.z + BUFFER + 1, building.z + width_of_building + BUFFER - 1):
            utilityFunctions.setBlock(level, cobble,  x, box_height, z)
            utilityFunctions.setBlockToGround(level, water, x, box_height + 2, z, box_height + 1)


def plant_in_farm(level, length_of_building, width_of_building, height_of_building, box_height, building):
    for x in range(building.x + BUFFER + 1, building.x + length_of_building + BUFFER - 1):
        for z in range(building.z + BUFFER + 1, building.z + width_of_building + BUFFER - 1):
            utilityFunctions.setBlock(level, crops, x, box_height + height_of_building, z)
            utilityFunctions.setBlockToGround(level, dirt, x, box_height + 2, z, box_height)
    center_x = building.x + (length_of_building / 2) + 1
    center_z = building.z + (width_of_building / 2) + 1
    utilityFunctions.setBlock(level, water, center_x, box_height + 1, center_z)
    utilityFunctions.setBlock(level, air, center_x, box_height + height_of_building, center_z)

