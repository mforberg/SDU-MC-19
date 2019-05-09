from variables.GA_VALUES import *
from src.genetic_algorithm.CheckCriterias import *


def population_fitness(extra_population, box_x, box_z, starting_point):
    full_extra_pop_with_fitness = list()
    for solution in extra_population:
        fitness = solution_fitness(solution, box_x, box_z, starting_point)
        inner_list = list()
        inner_list.append(solution)
        inner_list.append(fitness)
        full_extra_pop_with_fitness.append(inner_list)
    return full_extra_pop_with_fitness


def solution_fitness(solution, box_x, box_z, starting_point):
    already_calculated = list()
    collision_negative_score = 0
    out_of_box_negative_score = 0
    for building in solution:
        """score is calculated based if they are within the box there are no collision"""
        """within box"""
        if not check_if_within_box(building, box_x, box_z, starting_point):
            out_of_box_negative_score += NOT_WITHIN_BOX_MINUS_PER_HOUSE
        """collision"""
        for building2 in solution:
            if building == building2 or building2 in already_calculated:
                continue
            if building.check_if_house_is_within(building2):
                collision_negative_score += ((float(1)/len(solution)) * MAX_SCORE)
        already_calculated.append(building)
    box_score = WITHIN_BOX_WEIGHT * (MAX_SCORE - out_of_box_negative_score)
    if box_score < 0:
        box_score = 0
    collision_score = COLLISION_WEIGHT * (MAX_SCORE - collision_negative_score)
    if collision_score < 0:
        collision_score = 0
    score = box_score + collision_score
    return score
