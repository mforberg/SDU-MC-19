from variables.MC_LIBRARY import *
import src.genetic_algorithm.Generation


def check_population(population, box_x, box_z, starting_point):
    checked_population = list()
    for solution in population:
        if check_solution(solution, box_x, box_z, starting_point):
            checked_population.append(solution)
        else:
            """If the solution does not meet the criterias"""
            checked_population.append(src.genetic_algorithm.Generation.generate_solution(box_x, box_z, starting_point))
    return checked_population


def check_solution(solution, box_x, box_z, starting_point):
    already_calculated = list()
    for building in solution:
        if not check_if_within_box(building, box_x, box_z, starting_point):
            return False
        for building2 in solution:
            if building == building2 or building2 in already_calculated:
                continue
            if building.check_if_house_is_within(building2):
                return False
    return True


def check_if_within_box(building, box_x, box_z, starting_point):
    if building.x < starting_point["x"] or building.z < starting_point["z"]:
        return False
    if building.x + buildings[building.type_of_house]["xLength"] > starting_point["x"] + box_x:
        return False
    if building.z + buildings[building.type_of_house]["zWidth"] > starting_point["z"] + box_z:
        return False
    return True
