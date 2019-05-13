from variables.GA_VALUES import *
from src.MapAnalysis import *
# from variables.MC_LIBRARY import *
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
    # fitness_score += normal_houses_in_solution(solution)
    # fitness_score += building_variance(solution)
    fitness_score += y_difference(solution, height_map)
    fitness_score += coverage_score_and_well_distance(solution)
    fitness_score += check_area_for_water_and_changed_blocks_score(solution, height_map)
    fitness_score += force_building_probability(solution)
    fitness_score -= weight_solutions(box_x, box_z, solution)
    return fitness_score


# def building_variance(solution):
#     unique_buildings = set()
#     for building in solution:
#         unique_buildings.add(building.type_of_house)
#     float_length = len(unique_buildings) - 1  # we do not care about well
#     percent_of_max_possible = float(float_length) / len(get_available_buildings())
#     score = VARIANCE_WEIGHT * (MAX_SCORE * math.pow(percent_of_max_possible, 2))
#     print "variance: ", score
#     return score


def coverage_score_and_well_distance(solution):
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
    value = AREA_COVERAGE_POINTS_PER_UNIT * distance
    area_coverage_score = COVERAGE_WEIGHT * (MAX_SCORE - value)
    """calculate distance to well"""
    well_score = average_distance_to_well_score(solution, well)
    print "LOOK HERE ---------------------------------------------> ", area_coverage_score, "  well: ", well_score
    print "Area: ", area_coverage_score, "   Well: ", well_score
    return area_coverage_score + well_score


def average_distance_to_well_score(solution, well):
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
        """distance score is calculated using an quadratic equation"""
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
        #average = find_average_height(building, height_map)
        average = find_most_common_height_around_the_building(height_map, building)
        """finding water and lava"""
        amount_of_water_and_lava += find_amount_of_water_and_lava(building, height_map)
        """finding changed blocks"""
        changed_blocks = 0
        for x in xrange(building.x, building.x + buildings[building.type_of_house]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.type_of_house]["zWidth"]):
                height = height_map[x, z][0]
                difference = abs(height - average)
                changed_blocks += difference
        total_percentage_changed += changed_blocks / building_area
    """changed block score is calculated here (for the whole solution)"""
    actual_percentage = total_percentage_changed / len(solution)
    if actual_percentage < ALLOWED_CHANGED_BLOCKS_PERCENTAGE:
        actual_percentage = 0
    #difference_in_percentage = actual_percentage - CHANGED_BLOCKS_PERCENTAGE
    building_score = MAX_SCORE - (MAX_SCORE * actual_percentage)
    building_score *= AREA_WEIGHT
    """water/lava score is calculated here"""
    water_lava_score = amount_of_water_and_lava * WATER_AND_LAVA_WEIGHT
    print "water/lava: ", water_lava_score
    print "building score: ", building_score
    """subtract the water/lava score"""
    score = building_score - water_lava_score
    """we don't want score under zero"""
    if score < 0:
        score = 0
    return score


# def normal_houses_in_solution(solution):
#     amount_of_normal_houses = 0.0
#     for building in solution:
#         if building.type_of_house == "normalHouse":
#             amount_of_normal_houses += 1
#     percentage = amount_of_normal_houses / len(solution)
#     score = 0
#     if percentage > 0:
#         if percentage >= NORMAL_HOUSE_PERCENTAGE:
#             score = MAX_SCORE * (NORMAL_HOUSE_PERCENTAGE / percentage)
#         else:
#             score = MAX_SCORE * (percentage / NORMAL_HOUSE_PERCENTAGE)
#         score *= NORMAL_HOUSE_WEIGHT
#     print "normal houses in solution: ", score
#     return score


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
    print "y-difference: ", score
    """we don't want score under zero"""
    if score < 0:
        score = 0
    return score


def force_building_probability(solution):
    type_dict = {}
    #print "BANANANANANANANNANANNANANANNANANANANANANANAN"
    total_probability_value = 0
    for building_type in buildings:
        if building_type == "well":
            continue
        total_probability_value += buildings[building_type]["probability"]
        type_dict[building_type] = 0
    #print(type_dict)
    for building in solution:
        if building.type_of_house == "well":
            continue
        type_dict[building.type_of_house] += 1
    #print(type_dict)
    total_difference = 0.0
    for building_type in buildings:
        if building_type == "well":
            continue
        value = type_dict[building_type]
        #print value
        percentage_of_solution = float(value) / (len(solution) - 1)  # skip well
        #print "%"
        percentage_of_probability = buildings[building_type]["probability"] / float(total_probability_value)
        #print "DKAKLLDAK ", percentage_of_probability
        #print "odoajfojafoja ", abs(percentage_of_probability - percentage_of_solution)
        total_difference += abs(percentage_of_probability - percentage_of_solution)
    # print "building prop: ", total_difference
    # how to calculate :^)
    score = MAX_SCORE - (MAX_SCORE * total_difference)
    score *= FORCE_PROBABILITY_WEIGHT
    if score < 0:
        score = 0
    print "probability score: ", score
    return score


def weight_solutions(box_x, box_z, solution):
    building_difference = len(solution) - get_minimum_amount_of_houses(box_x, box_z)
    subtract_value = building_difference * DECREASE_PER_EXTRA_BUILDING
    return subtract_value
