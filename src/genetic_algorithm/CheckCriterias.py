from variables.MC_LIBRARY import *
import src.genetic_algorithm.Generation
import copy


def check_population(population, box_x, box_z, starting_point):
    checked_population = list()
    for solution in population:
        if check_solution(solution, box_x, box_z, starting_point):
            checked_population.append(solution)
        else:
            """If the solution does not meet the basics"""
            checked_population.append(src.genetic_algorithm.Generation.generate_solution(box_x, box_z, starting_point))
    return checked_population


def fi2pop_check(population, box_x, box_z, starting_point, extra_population):
    feasible_solution = list()
    unfeasible_solution = list()
    for solution in population:
        if check_solution(solution, box_x, box_z, starting_point):
            feasible_solution.append(solution)
        else:
            unfeasible_solution.append(solution)
    for solution in extra_population:
        if check_solution(solution, box_x, box_z, starting_point):
            feasible_solution.append(solution)
        else:
            unfeasible_solution.append(solution)
            # """If the solution does not meet the basics"""
            # working_extra_solution = find_working_extra_solution(extra_population, box_x, box_z, starting_point)
            # if working_extra_solution is None:
            #     feasible_solution.append(
            #         src.genetic_algorithm.Generation.generate_solution(box_x, box_z, starting_point))
            # else:
            #     """change the two solutions"""
            #     solution_copy = copy.deepcopy(solution)
            #     extra_copy = copy.deepcopy(working_extra_solution)
            #     extra_population.remove(working_extra_solution)
            #     extra_population.append(solution_copy)
            #     feasible_solution.append(extra_copy)
    return {"feasible": feasible_solution, "unfeasible": unfeasible_solution}


def find_working_extra_solution(extra_population, box_x, box_z, starting_point):
    for solution in extra_population:
        if check_solution(solution, box_x, box_z, starting_point):
            return solution


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
