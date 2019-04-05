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

            if random_number_x <= mutation_trigger:
                mutation_count += 1

                add_or_subtract_decider = random_number_between_one_to_hundred()
                if add_or_subtract_decider > 50:
                    i.x += decide_block_amount()
                else:
                    i.x -= decide_block_amount()
            random_number_z = random_number_between_one_to_hundred()

            if random_number_z <= mutation_trigger:
                mutation_count += 1

                add_or_subtract_decider = random_number_between_one_to_hundred()
                if add_or_subtract_decider > 50:
                    i.z += decide_block_amount()
                else:
                    i.z -= decide_block_amount()

            random_number_house = random_number_between_one_to_hundred()

            if random_number_house <= 100: # TODO: make correct trigger amount |testing purposes atm
                mutation_count += 1
                if i.typeOfHouse == "well": #Do not mutate the well
                    continue
                i.typeOfHouse = mutate_house(i.typeOfHouse)

    number = float(mutation_count) / (POPULATION_SIZE * GENE_SIZE * 2) * 100
    percent = round(number, 3)
    print "MUTATION TRIGGERED {0}/{1} TIMES ({2}%)".format(mutation_count, POPULATION_SIZE * GENE_SIZE * 2, percent)

def random_number_between_one_to_hundred():
    return random.randint(1, 100)

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
def mutate_house(house_to_mutate):
    sorted_buildings = get_buildings_by_size()
    for item in xrange(0, len(sorted_buildings)): #item is tuple (area_size, type)
        if sorted_buildings[item][1] == house_to_mutate:
            index_plus_1 = item+1
            if index_plus_1 <= len(sorted_buildings)-1:
                return sorted_buildings[index_plus_1][1]
            else:
                print "OUT OF BOUNDS"
                return sorted_buildings[item][1]

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

