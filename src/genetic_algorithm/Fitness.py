import math
from variables.GA_VALUES import *
from src.MapAnalysis import *
from src.genetic_algorithm.CheckCriterias import *


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
    #fitness_score += distance_score_and_area_check(solution)
    fitness_score += area_coverage_score_and_well_distance(solution)
    fitness_score += check_area_score(solution, height_map)
    fitness_score -= weight_smaller_solutions(box_x, box_z, solution)

    return fitness_score


def extra_population_fitness(extra_population, box_x, box_z, starting_point):
    full_extra_pop_with_fitness = list()
    for solution in extra_population:
        fitness = extra_solution_fitness(solution, box_x, box_z, starting_point)
        inner_list = list()
        inner_list.append(solution)
        inner_list.append(fitness)
        full_extra_pop_with_fitness.append(inner_list)
    return full_extra_pop_with_fitness


def extra_solution_fitness(solution, box_x, box_z, starting_point):
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
                collision_negative_score += ((float(1)/len(solution)) * COLLISION_MAX_SCORE)
        already_calculated.append(building)
    box_score = WITHIN_BOX_WEIGHT * (WITHIN_BOX_MAX_SCORE - out_of_box_negative_score)
    if box_score < 0:
        box_score = 0
    collision_score = COLLISION_WEIGHT * (COLLISION_MAX_SCORE - collision_negative_score)
    if collision_score < 0:
        collision_score = 0
    score = box_score + collision_score
    return score


def building_variance(solution):
    unique_buildings = set()
    for building in solution:
        unique_buildings.add(building.type_of_house)
    float_length = len(unique_buildings)
    percent_of_max_possible = float(float_length) / len(get_available_buildings())
    score = VARIANCE_WEIGHT * (VARIANCE_MAX_SCORE * math.pow(percent_of_max_possible, 2))
    return score


# def distance_score_and_area_check(solution):
#     already_calculated = list()
#     score = 0
#     area_score = 0
#     for building in solution:
#         if building.type_of_house == "well":
#             continue
#         for building2 in solution:
#             if building == building2 or building2 in already_calculated:
#                 continue
#             elif building2.type_of_house == "well":
#                 score += (DISTANCE_TO_WELL_WEIGHT * distance_between(building, building2))
#             else:
#                 score += (DISTANCE_WEIGHT * distance_between(building, building2))
#         already_calculated.append(building)
#     return score + area_score


def area_coverage_score_and_well_distance(solution):
    well_score = 0
    well = None
    total_x_max = 0
    total_x_min = 0
    total_z_max = 0
    total_z_min = 0
    """finding the well and get the total values"""
    for building in solution:
        if building.type_of_house == "well":
            well = building
        total_x_min += building.x
        total_x_max += buildings[building.type_of_house]["xLength"]
        total_z_min += building.z
        total_z_max += buildings[building.type_of_house]["zWidth"]
    """calculating the area coverage score"""
    avg_x = ((total_x_max / len(solution)) - (total_x_min / len(solution)))
    avg_z = ((total_z_max / len(solution)) - (total_z_min / len(solution)))
    distance = math.sqrt(math.pow(avg_x, 2) + math.pow(avg_z, 2))
    # print distance
    # value = 0
    # if distance > 160:
    #     value = 200
    # if distance > 170:
    #     value = 400
    # if distance > 180:
    #     value = 600
    # if distance > 190:
    #     value = 800
    # if distance > 200:
    #     value = 100
    value = AREA_COVERAGE_POINTS_PER_UNIT * distance
    # value = A * math.pow(distance, 2) + B * distance + C
    # if value < 0:
    #     value = 0
    #print value
    area_coverage_score = AREA_WEIGHT * (AVG_AREA_COVERAGE_MAX_SCORE - value)
    #print area_coverage_score
    """calculate distance to well"""
    for building in solution:
        if building.type_of_house == "well":
            continue
        well_score += DISTANCE_TO_WELL_WEIGHT * distance_between(well, building)
    #print well_score
    return area_coverage_score + well_score


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


def check_area_score(solution, height_map):
    score = 0
    for building in solution:
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
        building_score = AREA_MAX_SCORE - (AREA_MAX_SCORE * difference_in_percentage)
        """subtract the water/lava score"""
        building_score = (building_score * AREA_WEIGHT) - water_lava_score
        """we don't want score under zero"""
        if building_score < 0:
            building_score = 0
        score += building_score
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
