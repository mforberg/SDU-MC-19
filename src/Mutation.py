import random
from variables.GA_VALUES import *

# TODO: Possibly change decide_block_amount() back to 1 instead of 1..3, ~900 mutations seems excessive
def mutate_population(population):
    mutation_count = 0
    mutation_trigger = MUTATION_RATE * 100

    for solution in population:
        buildinglist = solution

        for i in buildinglist:
            random_number_x = random.randint(1, 100)

            if random_number_x <= mutation_trigger:
                mutation_count += 1

                add_or_subtract_decider = random.randint(1, 100)
                if add_or_subtract_decider > 50:
                    i.x += decide_block_amount()
                else:
                    i.x -= decide_block_amount()
            random_number_z = random.randint(1, 100)

            if random_number_z <= mutation_trigger:
                mutation_count += 1

                add_or_subtract_decider = random.randint(1, 100)
                if add_or_subtract_decider >= 50:
                    i.z += decide_block_amount()
                else:
                    i.z -= decide_block_amount()

    number = float(mutation_count) / (POPULATION_SIZE * GENE_SIZE * 2) * 100
    percent = round(number, 3)
    print "MUTATION TRIGGERED {0}/{1} TIMES ({2}%)".format(mutation_count, POPULATION_SIZE * GENE_SIZE * 2, percent)


def decide_block_amount():
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
        return 0

