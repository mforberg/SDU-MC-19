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
    fitness_score += y_difference(solution, height_map)
    fitness_score += well_distance_score(solution)
    fitness_score += check_area_for_water_and_changed_blocks_score(solution, height_map)
    fitness_score += force_building_probability(solution)
    fitness_score -= weight_solutions(box_x, box_z, solution)
    return fitness_score


def well_distance_score(solution):
    well = None
    """finding the well and get the total values"""
    for building in solution:
        if building.type_of_house == "well":
            well = building
    """calculate the score of distance to well"""
    well_score = calculate_average_distance_to_well_score(solution, well)
    return well_score


def calculate_average_distance_to_well_score(solution, well):
    total_distance = 0
    for building in solution:
        if building.type_of_house == "well":
            continue
        total_distance += well.distance_between_building(building)
    avg_distance = total_distance / len(solution)
    """depending on what side of the vertex_x it is, use different equations"""
    if avg_distance < VERTEX_X:
        """distance score is calculated using a linear equation"""
        value = L_A * avg_distance
    else:
        """distance score is calculated using a quadratic equation"""
        value = Q_A * math.pow(avg_distance, 2) + Q_B * avg_distance + Q_C
    """if value is at the cut, we want to give it a max score"""
    value_cut_for_max = VERTEX_Y - (VERTEX_Y * PERCENTAGE_FOR_MAX_VALUE_QE)
    if value > value_cut_for_max:
        value = VERTEX_Y
    score = MAX_SCORE * (value/VERTEX_Y)
    """we don't want score under zero"""
    if score < 0:
        score = 0
    score *= DISTANCE_TO_WELL_WEIGHT
    return score


def check_area_for_water_and_changed_blocks_score(solution, height_map):
    amount_of_water_and_lava = 0
    total_percentage_changed = 0
    for building in solution:
        building_area = buildings[building.type_of_house]["xLength"] * buildings[building.type_of_house]["zWidth"]
        target_height = find_most_common_height_around_the_building(height_map, building)
        """finding water and lava"""
        amount_of_water_and_lava += find_amount_of_water_and_lava(building, height_map)
        """finding changed blocks"""
        changed_blocks = 0.0
        for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
                height = height_map[x, z][0]
                difference = abs(height - target_height)
                changed_blocks += float(difference)
        total_percentage_changed += changed_blocks / building_area
    """changed block score is calculated here (for the whole solution)"""
    average_percentage = total_percentage_changed / len(solution)
    value = -(COEFFICIENT_MODIFIER_FOR_CHANGED_BLOCKS * MAX_SCORE) * average_percentage + MAX_SCORE
    building_score = AREA_WEIGHT * value
    """water/lava score is calculated here"""
    water_lava_score = amount_of_water_and_lava * WATER_AND_LAVA_WEIGHT
    """subtract the water/lava score"""
    score = building_score - water_lava_score
    """we don't want score under zero"""
    if score < 0:
        score = 0
    return score


def y_difference(solution, height_map):
    total_height = 0
    well_average = 0
    for building in solution:
        if building.type_of_house == "well":
            well_average = find_most_common_height_around_the_building(height_map, building)
            continue
        total_height += find_most_common_height_around_the_building(height_map, building)
    total_average_height = total_height / (len(solution) - 1)  # skip well
    actual_difference = abs(total_average_height - well_average)
    score = Y_DIFFERENCE_WEIGHT * (MAX_SCORE - (actual_difference * POINTS_PER_DIFFERENCE_IN_Y))
    """we don't want score under zero"""
    if score < 0:
        score = 0
    return score


def force_building_probability(solution):
    type_dict = {}
    total_probability_value = 0
    for building_type in buildings:
        if building_type == "well":
            continue
        total_probability_value += buildings[building_type]["probability"]
        type_dict[building_type] = 0
    for building in solution:
        if building.type_of_house == "well":
            continue
        type_dict[building.type_of_house] += 1
    total_difference = 0.0
    for building_type in buildings:
        if building_type == "well":
            continue
        value = type_dict[building_type]
        percentage_of_solution = float(value) / (len(solution) - 1)  # skip well
        percentage_of_probability = buildings[building_type]["probability"] / float(total_probability_value)
        total_difference += abs(percentage_of_probability - percentage_of_solution)
    score = MAX_SCORE - (MAX_SCORE * total_difference)
    score *= FORCE_PROBABILITY_WEIGHT
    if score < 0:
        score = 0
    return score


def weight_solutions(box_x, box_z, solution):
    building_difference = len(solution) - get_minimum_amount_of_houses(box_x, box_z)
    subtract_value = building_difference * DECREASE_PER_EXTRA_BUILDING
    return subtract_value
