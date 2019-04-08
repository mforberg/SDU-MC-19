from variables.MC_LIBRARY import *
import Generation


def check_population(population, boxX, boxZ, startingPoint):
    checkedPopulation = list()
    for solution in population:
        if check_solution(solution, boxX, boxZ, startingPoint):
            checkedPopulation.append(solution)
        else:
            checkedPopulation.append(Generation.generate_solution(boxX, boxZ, startingPoint))
    return checkedPopulation


def check_solution(solution, boxX, boxZ, startingPoint):
    blockedCoordinates = list()
    for building in solution:
        if not check_if_within_box(building, boxX, boxZ, startingPoint):
            return False
        """check if buildings share the same coordinates"""
        for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
                convertedCoordinate = (x, z)
                if convertedCoordinate in blockedCoordinates:
                    return False
                blockedCoordinates.append(convertedCoordinate)
    return True


def check_if_within_box(building, boxX, boxZ, startingPoint):
    if building.x < startingPoint["x"] or building.z < startingPoint["z"]:
        return False
    if building.x + buildings[building.typeOfHouse]["xLength"] > startingPoint["x"] + boxX:
        return False
    if building.z + buildings[building.typeOfHouse]["zWidth"] > startingPoint["z"] + boxZ:
        return False
    return True
