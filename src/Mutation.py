import random
from variables.GA_VALUES import *
from variables.MC_LIBRARY import buildings


def mutate_population(population):
    mutation_count = 0
    mutation_trigger = MUTATION_RATE * 100

    mutate_house("normalHouse")

    for solution in population:
        buildinglist = solution

        for i in buildinglist: # TODO: separate repeated code into method

            random_number_x = random_number_between_one_to_hundred()
            random_number_z = random_number_between_one_to_hundred()

            mutate_coordinate(random_number_x, mutation_trigger, mutation_count, i.x) #mutate x
            mutate_coordinate(random_number_z, mutation_trigger, mutation_count, i.z) #mutate z

            random_number_house = random_number_between_one_to_hundred()

            if random_number_house <= mutation_trigger: # TODO: buildings might overlap post mutation not sure where to handle
                mutation_count += 1
                if i.typeOfHouse == "well": #Do not mutate the well
                    continue
                i.typeOfHouse = mutate_house(i.typeOfHouse)

    number = float(mutation_count) / (POPULATION_SIZE * GENE_SIZE * 2) * 100
    percent = round(number, 3)
    print "MUTATION TRIGGERED {0}/{1} TIMES ({2}%)".format(mutation_count, POPULATION_SIZE * GENE_SIZE * 2, percent)

def random_number_between_one_to_hundred():
    return random.randint(1, 100)


def mutate_coordinate(random_number, mutation_trigger, mutation_count, coordinate):
    if random_number <= mutation_trigger:
        mutation_count += 1

        add_or_subtract_decider = random_number_between_one_to_hundred()
        if add_or_subtract_decider > 50:
            coordinate += decide_block_amount()
        else:
            coordinate -= decide_block_amount()


# TODO: Possibly change decide_block_amount() back to 1 instead of 1..3, ~900 mutations seems excessive
def decide_block_amount():
    """ Not gonna lie, I gave up a little on making this pretty """
    max_block_move = 3
    total_block_move = (max_block_move*(max_block_move+1))/2

    random_number = random.randint(1,total_block_move)
    if random_number <= 3:
        return 1
    elif random_number <= 5:
        return 2
    elif random_number <= 6:
        return 3
    else:
        return 0 # something fucky happened if you hit this


# TODO: Random increment or decrement
# TODO: Fix ERROR -> return sorted_buildings[index_plus_1][1] IndexError: list index out of range
def mutate_house(house_to_mutate):
    sorted_buildings = get_buildings_by_size()
    for item in xrange(0, len(sorted_buildings)): #item is tuple (area_size, type)
        if sorted_buildings[item][1] == house_to_mutate:
            index_plus_1 = item+1
            index_minus_1 = item-1
            print index_plus_1, "<-->", len(sorted_buildings)
            if index_plus_1 <= len(sorted_buildings):
                return sorted_buildings[index_plus_1][1]
            else:
                print "- - - - - -"
                print index_minus_1, "<-->", len(sorted_buildings)
                print sorted_buildings[index_minus_1][1]
                return sorted_buildings[item-1][1]


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

