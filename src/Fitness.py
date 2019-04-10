import math
import MapAnalysis
from variables.MC_LIBRARY import *


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
    """ GLOBAL WEIGHTS """
    variance_weight = 1.0
    variance_max_score = 1000
    """ END OF WEIGHTS """
    already_calculated = list()
    unique_buildings = set()
    for building in solution:
        fitness_score += check_area(building, height_map)
        if building.typeOfHouse == "well":
            continue
        for building2 in solution:
            if building == building2 or building2 in already_calculated:
                continue
            elif building2.typeOfHouse == "well":
                fitness_score += 2 * (distance_between(building, building2))
            else:
                fitness_score += distance_between(building, building2)
        already_calculated.append(building)

        """" FITNESS FOR BUILDING VARIANCE """
        unique_buildings.add(building.typeOfHouse)
    float_length = len(unique_buildings)
    percent_of_max_possible = float(float_length) / len(get_placeable_buildings())
    fitness_score += variance_weight * (variance_max_score * math.pow(percent_of_max_possible, 2))
    """ END OF VARIANCE FITNESS """
    return fitness_score


def distance_between(house1, house2):
    distance = house1.distance_between_building(house2)
    """distance score is calculated using an quadratic equation"""
    a = float(-4) / 45
    b = float(16) / 3
    c = 0
    score = a * math.pow(distance, 2) + b * distance + c
    """we don't want score too much under zero"""
    if score < 0:
        score = 0
    # if score < 0:
    #     score = 0
    # elif score > 50:
    #     score = 100
    return score


def check_area(building, height_map):
    # totalArea = buildings[building.typeOfHouse]["xLength"] * buildings[building.typeOfHouse]["zWidth"]
    # listOfHeights = []
    # unique = set()
    # amount = 0
    # amountOfWater = 0
    # for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
    #     for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
    #         """check for water"""
    #         if heightMap[x, z][1] == 9:
    #             amountOfWater += 1
    #         amount += heightMap[x, z][0]
    #         listOfHeights.append(heightMap[x, z][0])
    #         unique.add(heightMap[x, z][0])
    # average = int(round(amount / float(totalArea)))
    # blocksModified = 0
    # for number in unique:
    #     blocksModified += listOfHeights.count(number) * abs(average - number)
    analysis = MapAnalysis.find_average_height(building, height_map, True)
    average = analysis[0]
    amount_of_water = analysis[1]

    """the score is calculated here. Maximum score is 100"""
    score = 100 - int(round(average / 10))
    """subtract extra for water"""
    score -= amount_of_water * 6
    """we don't want score too much under zero"""
    if score < 0:
        score = 0
    return score
