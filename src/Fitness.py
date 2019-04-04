import math
from variables.MC_LIBRARY import *


def population_fitness(population, heightMap):
    fullpop_with_fitness = list()
    for solution in population:
        fitness = solution_fitness(solution, heightMap)
        innerList = list()
        innerList.append(solution)
        innerList.append(fitness)
        fullpop_with_fitness.append(innerList)
    return fullpop_with_fitness


def solution_fitness(solution, heightMap):
    fitnessScore = 0
    """ GLOBAL WEIGHTS """
    variance_weight = 1.0
    variance_max_score = 1000
    """ END OF WEIGHTS """
    alreadyCalculated = list()
    unique_buildings = set()
    for building in solution:
        fitnessScore += check_area(building, heightMap)
        if building.typeOfHouse == "well":
            continue
        for building2 in solution:
            if building == building2 or building2 in alreadyCalculated:
                continue
            elif building2.typeOfHouse == "well":
                fitnessScore += 2 * (distance_between(building, building2))
            else:
                fitnessScore += distance_between(building, building2)
        alreadyCalculated.append(building)

        """" FITNESS FOR BUILDING VARIANCE """
        unique_buildings.add(building.typeOfHouse)
    float_length = len(unique_buildings)
    percent_of_max_possible = float(float_length) / len(get_placeable_buildings())
    fitnessScore += variance_weight *(variance_max_score * math.pow(percent_of_max_possible, 2))

    """ END OF VARIANCE FITNESS """
    return fitnessScore


def distance_between(house1, house2):
    distance = house1.distance_between_building(house2)
    """distance score is calculated using an quadratic equation"""
    a = float(-4) / 45
    b = float(16 ) /3
    c = 0
    distanceScore = a * math.pow(distance, 2) + b * distance + c
    """we dont want score under zero"""
    if distanceScore < 0:
        distanceScore = 0
    elif distanceScore > 50:
        distanceScore = 100
    return distanceScore


def check_area(building, heightMap):
    totalArea = buildings[building.typeOfHouse]["xLength"] * buildings[building.typeOfHouse]["zWidth"]
    listOfHeights = []
    unique = set()
    amount = 0
    amountOfWater = 0
    for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
        for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
            """check for water"""
            if heightMap[x, z][1] == 9:
                amountOfWater += 1
            amount += heightMap[x, z][0]
            listOfHeights.append(heightMap[x, z][0])
            unique.add(heightMap[x, z][0])
    average = int(round(amount / float(totalArea)))
    blocksModified = 0
    for number in unique:
        blocksModified += listOfHeights.count(number) * abs(average - number)
    """the score is calculated here. Maximum score is 100"""
    score = 100 - int(round(blocksModified / 10))
    """subtract extra for water"""
    score -= amountOfWater * 6
    """we dont want score under zero"""
    if score < 0:
        score = 0
    return score
