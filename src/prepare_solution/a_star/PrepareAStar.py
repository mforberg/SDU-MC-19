from src.Building import *


def set_all_connections_points(list_of_buildings, height_map):
    for building in list_of_buildings: # find the well
        if building.type_of_house == "well":
            well = building
            break

    for building in list_of_buildings: # set connection points for all buildings
        if building.type_of_house == well: # don't set connection point for well to begin with
            continue
        building.set_connection_point(well, height_map)


def find_well(list_of_buildings):
    for building in list_of_buildings: # the well is the goal, locate it first
        if building.type_of_house == "well": #
            goal = building
            break
    return goal
