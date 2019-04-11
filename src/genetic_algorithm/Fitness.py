import math
import src.MapAnalysis
from variables.MC_LIBRARY import *
from variables.GA_VALUES import *


def population_fitness(population, height_map):
    full_pop_with_fitness = list()
    for solution in population:
        fitness = solution_fitness(solution, height_map)
        inner_list = list()
        inner_list.append(solution)
        inner_list.append(fitness)
        full_pop_with_fitness.append(inner_list)
    return full_pop_with_fitness


def solution_fitness(solution, height_map):
    fitness_score = 0
    already_calculated = list()
    unique_buildings = set()
    for building in solution:
        fitness_score += check_area(building, height_map)
        if building.type_of_house == "well":
            continue
        for building2 in solution:
            if building == building2 or building2 in already_calculated:
                continue
            elif building2.type_of_house == "well":
                fitness_score += DISTANCE_TO_WELL_WEIGHT * (distance_between(building, building2))
            else:
                fitness_score += distance_between(building, building2)
        already_calculated.append(building)
        """" FITNESS FOR BUILDING VARIANCE """
        unique_buildings.add(building.type_of_house)
    float_length = len(unique_buildings)
    percent_of_max_possible = float(float_length) / len(get_placeable_buildings())
    fitness_score += VARIANCE_WEIGHT * (VARIANCE_MAX_SCORE * math.pow(percent_of_max_possible, 2))
    """ END OF VARIANCE FITNESS """
    return fitness_score


def distance_between(house1, house2):
    distance = house1.distance_between_building(house2)
    """distance score is calculated using an quadratic equation"""
    score = A * math.pow(distance, 2) + B * distance + C
    score *= DISTANCE_WEIGHT
    """we don't want score too much under zero"""
    if score < 0:
        score = 0
    return score


def check_area(building, height_map):
    analysis = src.MapAnalysis.find_average_height(building, height_map, True)
    average = analysis[0]
    amount_of_water = analysis[1]

    """the score is calculated here"""
    """subtract extra for water"""
    score = AREA_MAX_SCORE - (int(round(average / CHANGED_BLOCK_PER_POINT)) + amount_of_water * WATER_WEIGHT)
    score = score * AREA_WEIGHT
    """we don't want score too much under zero"""
    if score < 0:
        score = 0
    return score
