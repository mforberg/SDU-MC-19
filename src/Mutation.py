import random
from variables.GA_VALUES import *
from variables.MC_LIBRARY import buildings


def mutate_population(population):
    mutation_count_coord = 0
    mutation_count_building = 0
    mutation_trigger = MUTATION_RATE * 100

    for solution in population:
        building_list = solution
        for i in building_list:

            random_number_x = random_number_between_one_to_hundred()
            random_number_z = random_number_between_one_to_hundred()
            random_number_house = random_number_between_one_to_hundred()

            mutation_count_coord += mutate_coordinate(random_number_x, mutation_trigger, i.x) #mutate x
            mutation_count_coord += mutate_coordinate(random_number_z, mutation_trigger, i.z) #mutate z

            if random_number_house <= mutation_trigger:
                if i.typeOfHouse == "well": #Do not mutate the well
                    continue
                mutation_count_building += 1
                i.typeOfHouse = mutate_house(i.typeOfHouse)

    full_count = mutation_count_building+mutation_count_coord
    number = float(full_count) / ((POPULATION_SIZE * GENE_SIZE * 2) + GENE_SIZE*POPULATION_SIZE) * 100
    percent = round(number, 3)
    #print "{0} coordinates mutated, {1} buildings mutated".format(mutation_count_coord, mutation_count_building)
    print "MUTATION TRIGGERED {0}/{1} TIMES ({2}%)".format(full_count, (POPULATION_SIZE * GENE_SIZE * 2)+GENE_SIZE*POPULATION_SIZE, percent)

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
        return 0 # something fucky happened if you hit this


def mutate_house(house_to_mutate):
    sorted_buildings = get_buildings_by_size()
    for item in xrange(0, len(sorted_buildings)): #item is tuple (area_size, type)
        if sorted_buildings[item][1] == house_to_mutate:
            index_plus_1 = item+1
            index_minus_1 = item-1
            random_number = random_number_between_one_to_hundred()
            if sorted_buildings[item][1] == sorted_buildings[0][1]: # Special case: Small houses shouldn't become churches
                return sorted_buildings[index_plus_1][1]
                break
            if sorted_buildings[item][1] == sorted_buildings[5][1]: # Special case: Churches shouldn't become small houses
                return sorted_buildings[index_minus_1][1]
                break

            if random_number > 50:
                return sorted_buildings[index_plus_1][1]
            else:
                return sorted_buildings[index_minus_1][1]
            break


def get_buildings_by_size():
    size_list = list()
    for item in buildings:
        if item == "well":
            continue
        area = buildings[item]["zWidth"] * buildings[item]["xLength"]
        tuple = (area, item)
        size_list.append(tuple)
    size_list.sort()
    returned_list = size_list
    return returned_list

