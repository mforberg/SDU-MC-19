# noinspection PyUnresolvedReferences
import utilityFunctions
# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials
from variables.MC_LIBRARY import *


def deforest_area(list_of_buildings, list_of_roads, height_map, level):
    for building in list_of_buildings:
        clear_building_area(building, height_map, level)
    for road in list_of_roads:
        clear_road(road, level, height_map)


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
    start_y = height_map[start_x, start_z][0]
    end_y = height_map[start_x, start_z][0] + buildings[building.type_of_house]["yHeight"]
    if buildings[building.type_of_house]["xLength"] < 3 or buildings[building.type_of_house]["zWidth"] < 3 \
            or buildings[building.type_of_house]["yHeight"] < 4:
        clear_everything(start_x, end_x, start_z, end_z, start_y, end_y, level)
    else:
        check_area_and_clear_blocks(start_x, end_x, start_z, end_z, start_y, end_y, level)


def check_area_and_clear_blocks(start_x, end_x, start_z, end_z, start_y, end_y, level):
    true_checks = 0
    bottom_block = False
    top_block = False
    """bottom/top check"""
    for x in xrange(start_x, end_x):
        for z in xrange(start_z, end_z):
            """check bottom"""
            if level.blockAt(x, start_y + 1, z) != alphaMaterials.Air.ID:
                bottom_block = True
                true_checks += 1
            """check top"""
            if level.blockAt(x, end_y, z) != alphaMaterials.Air.ID:
                top_block = True
                true_checks += 1
    x_min = False
    x_max = False
    """x_min/x_max check"""
    for z in xrange(start_z, end_z):
        for y in xrange(start_y + 2, end_y - 1):
            """check min_x"""
            if level.blockAt(start_x, y, z) != alphaMaterials.Air.ID:
                x_min = True
                true_checks += 1
            """check max_x"""
            if level.blockAt(end_x, y, z) != alphaMaterials.Air.ID:
                x_max = True
                true_checks += 1
    z_min = False
    z_max = False
    """z_min/z_max check"""
    for x in xrange(start_x + 1, end_x - 1):
        for y in xrange(start_y + 2, end_y - 1):
            """check min_z"""
            if level.blockAt(x, y, start_z) != alphaMaterials.Air.ID:
                z_min = True
                true_checks += 1
            """check max_z"""
            if level.blockAt(x, y, end_z) != alphaMaterials.Air.ID:
                z_max = True
                true_checks += 1
    """if there are more than one side where blocks are, just clear the whole area"""
    if true_checks > 1:
        clear_everything(start_x, end_x, start_z, end_z, start_y, end_y, level)
    elif true_checks == 1:
        """boolean checks from earlier"""
        if bottom_block:
            clear_bottom_up(start_x, end_x, start_z, end_z, start_y, end_y, level)
        elif top_block:
            clear_up_down(start_x, end_x, start_z, end_z, start_y, end_y, level)
        elif x_min:
            clear_x_min_to_max(start_x, end_x, start_z, end_z, start_y, end_y, level)
        elif x_max:
            clear_x_max_to_min(start_x, end_x, start_z, end_z, start_y, end_y, level)
        elif z_min:
            clear_z_min_to_max(start_x, end_x, start_z, end_z, start_y, end_y, level)
        elif z_max:
            clear_z_max_to_min(start_x, end_x, start_z, end_z, start_y, end_y, level)


def clear_everything(start_x, end_x, start_z, end_z, start_y, end_y, level):
    blocks_found = True
    go_up = True
    height_indicator = 0
    while blocks_found or start_y + height_indicator < end_y:
        if go_up or start_y + height_indicator < end_y:
            height_indicator += 1
            go_up = False
        blocks_found = False
        for x in xrange(start_x, end_x):
            for z in xrange(start_z, end_z):
                if level.blockAt(x, start_y + height_indicator, z) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, start_y + height_indicator, z)
                blocks_found = True
                go_up = True


def clear_bottom_up(start_x, end_x, start_z, end_z, start_y, end_y, level):
    blocks_found = True
    go_up = True
    height_indicator = 0
    while blocks_found and start_y + height_indicator <= end_y:
        if go_up:
            height_indicator += 1
            go_up = False
        blocks_found = False
        for x in xrange(start_x, end_x):
            for z in xrange(start_z, end_z):
                if level.blockAt(x, start_y + height_indicator, z) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, start_y + height_indicator, z)
                blocks_found = True
                go_up = True


def clear_up_down(start_x, end_x, start_z, end_z, start_y, end_y, level):
    blocks_found = True
    go_down = False
    height_indicator = 0
    while blocks_found and end_y + height_indicator > start_y:
        if go_down:
            height_indicator -= 1
            go_down = False
        blocks_found = False
        for x in xrange(start_x, end_x):
            for z in xrange(start_z, end_z):
                if level.blockAt(x, end_y + height_indicator, z) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, end_y + height_indicator, z)
                blocks_found = True
                go_down = True


def clear_x_min_to_max(start_x, end_x, start_z, end_z, start_y, end_y, level):
    blocks_found = True
    x_increase = False
    x_incrementer = 0
    while blocks_found and start_x + x_incrementer <= end_x:
        if x_increase:
            x_incrementer += 1
            x_increase = False
        blocks_found = False
        for y in xrange(start_y + 2, end_y - 1):
            for z in xrange(start_z, end_z):
                if level.blockAt(start_x + x_incrementer, y, z) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), start_x + x_incrementer, y, z)
                blocks_found = True
                x_increase = True


def clear_x_max_to_min(start_x, end_x, start_z, end_z, start_y, end_y, level):
    blocks_found = True
    x_decrease = False
    x_decrement = 0
    while blocks_found and end_x + x_decrement >= start_x:
        if x_decrease:
            x_decrement -= 1
            x_decrease = False
        blocks_found = False
        for y in xrange(start_y + 2, end_y - 1):
            for z in xrange(start_z, end_z):
                if level.blockAt(end_x + x_decrement, y, z) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), end_x + x_decrement, y, z)
                blocks_found = True
                x_decrease = True


def clear_z_min_to_max(start_x, end_x, start_z, end_z, start_y, end_y, level):
    blocks_found = True
    z_increase = False
    z_incrementer = 0
    while blocks_found and start_z + z_incrementer <= end_z:
        if z_increase:
            z_incrementer += 1
            z_increase = False
        blocks_found = False
        for y in xrange(start_y + 2, end_y - 1):
            for x in xrange(start_x + 1, end_x - 1):
                if level.blockAt(x, y, start_z + z_incrementer) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, y, start_z + z_incrementer)
                blocks_found = True
                z_increase = True


def clear_z_max_to_min(start_x, end_x, start_z, end_z, start_y, end_y, level):
    blocks_found = True
    z_decrease = False
    z_decrement = 0
    while blocks_found and end_z + z_decrement >= start_z:
        if z_decrease:
            z_decrement -= 1
            z_decrease = False
        blocks_found = False
        for y in xrange(start_y + 2, end_y - 1):
            for x in xrange(start_x + 1, end_x - 1):
                if level.blockAt(x, y, end_z + z_decrement) == alphaMaterials.Air.ID:
                    continue
                utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, y, end_z + z_decrement)
                blocks_found = True
                z_decrease = True


def clear_road(road, level, height_map):
    minimum_clear_height = 4
    for block in road:
        go_higher = False
        block_x = block[0]
        block_z = block[1]
        bonus_y = 0
        while go_higher or bonus_y <= minimum_clear_height:
            bonus_y += 1
            go_higher = False
            for x in xrange(block_x - BUFFER, block_x + BUFFER + 1):
                for z in xrange(block_z - BUFFER, block_z + BUFFER + 1):
                    y = height_map[x, z][0] + bonus_y
                    if level.blockAt(x, y, z) != alphaMaterials.Air.ID:
                        utilityFunctions.setBlock(level, (alphaMaterials.Air.ID, 0), x, y, z)
                        go_higher = True
