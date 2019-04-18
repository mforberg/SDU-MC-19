# noinspection PyUnresolvedReferences
import utilityFunctions
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials
from variables.MC_LIBRARY import *


def deforest_area(list_of_buildings, list_of_roads, heightmap, level):
    print "do stuff"
    find_bounds(list_of_buildings)


def find_bounds(list_of_buildings):
    for b in list_of_buildings:
        print b.type_of_house
    min_x = list_of_buildings[0].x
    max_x = list_of_buildings[0].x

    min_z = list_of_buildings[0].z
    max_z = list_of_buildings[0].z

    for building in list_of_buildings:

        if building.x < min_x:
            min_x = building.x
        if building.x > max_x:
            max_x = building.x
        if building.z < min_z:
            min_z = building.z
        if building.z > max_z:
            max_z = building.z

    print min_x, max_x, min_z, max_z


def clear_building_area(building, height_map, level):
    start_x = building.x
    end_x = building.x + buildings[building.type_of_house]["xLength"]
    start_z = building.z
    end_z = building.z + buildings[building.type_of_house]["zWidth"]
    clear_area_for_blocks(start_x, end_x, start_z, end_z, height_map, level)


def clear_area_for_blocks(start_x, end_x, start_z, end_z, height_map, level):
    blocks_found = True
    go_up = True
    height_indicator = 0
    while blocks_found:
        if go_up:
            height_indicator += 1
            go_up = False
        blocks_found = False
        for x in xrange(start_x, end_x):
            for z in xrange(start_z, end_z):
                y = height_map[x, z][0]
                if level.blockAt(x, y + height_indicator, z) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, y, z)
                blocks_found = True
                go_up = True
