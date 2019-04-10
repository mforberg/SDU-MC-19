from variables.MC_LIBRARY import *
import Generation


def check_population(population, boxX, boxZ, startingPoint):
    checkedPopulation = list()
    for solution in population:
        if check_solution(solution, boxX, boxZ, startingPoint):
            checkedPopulation.append(solution)
        else:
            """If the solution does not meet the criterias"""
            checkedPopulation.append(Generation.generate_solution(boxX, boxZ, startingPoint))
    return checkedPopulation


def check_solution(solution, boxX, boxZ, startingPoint):
    #blockedCoordinates = list()
    already_calculated = list()
    for building in solution:
        if not check_if_within_box(building, boxX, boxZ, startingPoint):
            return False
        for building2 in solution:
            if building == building2 or building2 in already_calculated:
                continue
            if building.check_if_house_is_within(building2):
                return False
        # """check if buildings share the same coordinates"""
        # for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
        #     for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
        #         converted_coordinate = (x, z)
        #         if converted_coordinate in blockedCoordinates:
        #             return False
        #         blockedCoordinates.append(converted_coordinate)
    return True


def check_if_within_box(building, box_x, box_z, starting_point):
    if building.x < starting_point["x"] or building.z < starting_point["z"]:
        return False
    if building.x + buildings[building.typeOfHouse]["xLength"] > starting_point["x"] + box_x:
        return False
    if building.z + buildings[building.typeOfHouse]["zWidth"] > starting_point["z"] + box_z:
        return False
    return True
