import math
from variables.GA_VALUES import *
from src.MapAnalysis import *


def population_fitness(population, height_map, box_x, box_z):
    full_pop_with_fitness = list()
    for solution in population:
        fitness = solution_fitness(solution, height_map, box_x, box_z)
        inner_list = list()
        inner_list.append(solution)
        inner_list.append(fitness)
        full_pop_with_fitness.append(inner_list)
    return full_pop_with_fitness


def solution_fitness(solution, height_map, box_x, box_z):
    fitness_score = 0
    fitness_score += normal_houses_in_solution(solution)
    fitness_score += y_difference(solution, height_map)
    fitness_score += building_variance(solution)
    fitness_score += distance_score_and_area_check(solution, height_map)

    fitness_score -= weight_smaller_solutions(box_x, box_z, solution)

    return fitness_score


def building_variance(solution):
    unique_buildings = set()
    for building in solution:
        unique_buildings.add(building.type_of_house)
    float_length = len(unique_buildings)
    percent_of_max_possible = float(float_length) / len(get_placeable_buildings())
    score = VARIANCE_WEIGHT * (VARIANCE_MAX_SCORE * math.pow(percent_of_max_possible, 2))
    return score


def distance_score_and_area_check(solution, height_map):
    already_calculated = list()
    score = 0
    area_score = 0
    for building in solution:
        area_score += check_area(building, height_map)
        if building.type_of_house == "well":
            continue
        for building2 in solution:
            if building == building2 or building2 in already_calculated:
                continue
            elif building2.type_of_house == "well":
                score += (DISTANCE_TO_WELL_WEIGHT * distance_between(building, building2))
            else:
                score += (DISTANCE_WEIGHT * distance_between(building, building2))
        already_calculated.append(building)
    return score + area_score


def distance_between(house1, house2):
    distance = house1.distance_between_building(house2)
    """distance score is calculated using an quadratic equation"""
    value = A * math.pow(distance, 2) + B * distance + C
    """if value is at the cut, we want to give it a max score"""
    if value > VALUE_CUT_FOR_MAX:
        value = MAX_VALUE_QE
    score = DISTANCE_MAX_SCORE * (value/MAX_VALUE_QE)
    """we don't want score under zero"""
    if score < 0:
        score = 0
    return score


def check_area(building, height_map):
    building_area = buildings[building.type_of_house]["xLength"] * buildings[building.type_of_house]["zWidth"]
    average = find_average_height(building, height_map)
    amount_of_water_and_lava = find_amount_of_water_and_lava(building, height_map)
    """water/lava score is calculated here"""
    water_lava_score = amount_of_water_and_lava * WATER_AND_LAVA_WEIGHT
    changed_blocks = 0
    for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
        for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
            height = height_map[x, z][0]
            difference = abs(height - average)
            changed_blocks += difference
    """changed block score is calculated here"""
    actual_percentage = changed_blocks / building_area
    if actual_percentage < CHANGED_BLOCKS_PERCENTAGE:
        actual_percentage = CHANGED_BLOCKS_PERCENTAGE
    difference_in_percentage = actual_percentage - CHANGED_BLOCKS_PERCENTAGE
    score = AREA_MAX_SCORE - (AREA_MAX_SCORE * difference_in_percentage)
    """subtract the water/lava score"""
    score = (score * AREA_WEIGHT) - water_lava_score
    """we don't want score under zero"""
    if score < 0:
        score = 0
    return score


def normal_houses_in_solution(solution):
    amount_of_normal_houses = 0
    for building in solution:
        if building.type_of_house == "normalHouse":
            amount_of_normal_houses += 1
    score = NORMAL_HOUSE_WEIGHT * (NORMAL_HOUSE_MAX_SCORE - (NORMAL_HOUSE_MAX_SCORE * abs(NORMAL_HOUSE_PERCENTAGE - (
            amount_of_normal_houses / len(solution)))))
    return score


def y_difference(solution, height_map):
    average_list = list()
    well_average = 0
    for building in solution:
        if building.type_of_house == "well":
            well_average = find_average_height(building, height_map)
            continue
        average_list.append(find_average_height(building, height_map))
    total_difference = 0
    for number in average_list:
        total_difference += abs(well_average - number)
    score = Y_DIFFERENCE_WEIGHT * (Y_MAX_SCORE - (total_difference * POINTS_PER_DIFFERENCE_IN_Y))
    """we don't want score under zero"""
    if score < 0:
        score = 0
    return score


def weight_smaller_solutions(box_x, box_z, solution):
    building_difference = len(solution) - get_minimum_amount_of_houses(box_x, box_z)
    subtract_value = building_difference * DECREASE_PER_EXTRA_BUILDING
    return subtract_value
