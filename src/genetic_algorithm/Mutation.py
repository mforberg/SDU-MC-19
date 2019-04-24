import random
from variables.GA_VALUES import *
from variables.MC_LIBRARY import buildings


def mutate_population(population):
    mutation_count_coord = 0
    mutation_count_building = 0

    for solution in population:
        building_list = solution
        """The amount of houses in a single solution"""
        gene_size = len(solution)
        """The percent chance of mutation"""
        mutation_rate = float(1) / (gene_size * MUTATION_RATE_MODIFIER)
        mutation_trigger = mutation_rate * 100
        for i in building_list:

            random_number_x = random_number_between_one_to_hundred()
            random_number_z = random_number_between_one_to_hundred()
            random_number_house = random_number_between_one_to_hundred()

            mutation_count_coord += mutate_coordinate(random_number_x, mutation_trigger, i.x)  # mutate x
            mutation_count_coord += mutate_coordinate(random_number_z, mutation_trigger, i.z)  # mutate z

            if random_number_house <= mutation_trigger:
                if i.type_of_house == "well":  # Do not mutate the well
                    continue
                mutation_count_building += 1
                i.type_of_house = mutate_house(i.type_of_house)


def random_number_between_one_to_hundred():
    return random.randint(1, 100)


def mutate_coordinate(random_number, mutation_trigger, coordinate):
    mutation_count = 0
    if random_number <= mutation_trigger:
        mutation_count += 1

        add_or_subtract_decider = random_number_between_one_to_hundred()
        if add_or_subtract_decider > 50:
            coordinate += decide_block_amount()
        else:
            coordinate -= decide_block_amount()
    return mutation_count


# TODO: Possibly change decide_block_amount() back to 1 instead of 1..3, ~900 mutations seems excessive
def decide_block_amount():
    """ Not gonna lie, I gave up a little on making this pretty """
    max_block_move = 3
    total_block_move = (max_block_move*(max_block_move+1))/2

    random_number = random.randint(1, total_block_move)
    if random_number <= 3:
        return 1
    elif random_number <= 5:
        return 2
    elif random_number <= 6:
        return 3
    else:
        return 0  # something wrong happened if you hit this


def mutate_house(house_to_mutate):
    if USE_SIZE_FOR_TYPE_MUTATION:
        sorted_buildings = get_buildings_by_size()
    else:
        sorted_buildings = get_buildings_by_mutation_number()
    for item in xrange(0, len(sorted_buildings)):  # item is tuple (area_size/number, type)
        if sorted_buildings[item][1] == house_to_mutate:
            index_plus_1 = item+1
            index_minus_1 = item-1
            random_number = random_number_between_one_to_hundred()
            # Special case: Small houses shouldn't become churches
            if sorted_buildings[item][1] == sorted_buildings[0][1]:
                return sorted_buildings[index_plus_1][1]
            # Special case: Churches shouldn't become small houses
            if sorted_buildings[item][1] == sorted_buildings[5][1]:
                return sorted_buildings[index_minus_1][1]
            if random_number > 50:
                return sorted_buildings[index_plus_1][1]
            else:
                return sorted_buildings[index_minus_1][1]


def get_buildings_by_size():
    size_list = list()
    for item in buildings:
        if item == "well":
            continue
        area = buildings[item]["zWidth"] * buildings[item]["xLength"]
        area_tuple = (area, item)
        size_list.append(area_tuple)
    size_list.sort()
    returned_list = size_list
    return returned_list


def get_buildings_by_mutation_number():
    number_list = list()
    for item in buildings:
        if item == "well":
            continue
        number = buildings[item]["mutationNumber"]
        number_tuple = (number, item)
        number_list.append(number_tuple)
    number_list.sort()
    returned_list = number_list
    return returned_list
