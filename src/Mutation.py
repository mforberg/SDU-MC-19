import random
from variables.GA_VALUES import *

def mutate_population(population):
    mutation_count = 0

    for solution in population:
        buildinglist = solution
        mutation_trigger = int(MUTATION_RATE * 100)

        for i in buildinglist:
            random_number_x = random.randint(1, 100)

            if random_number_x <= mutation_trigger:
                mutation_count += 1

                add_or_subtract_decider = random.randint(1, 100)

                if add_or_subtract_decider > 50:
                    i.x = i.x + 1
                else:
                    i.x = i.x - 1
            random_number_z = random.randint(1, 100)

            if random_number_z <= mutation_trigger:
                mutation_count += 1

                add_or_subtract_decider = random.randint(1, 100)
                if add_or_subtract_decider >= 50:
                    i.z = i.z + 1
                else:
                    i.z = i.z - 1

    number = float(mutation_count) / (POPULATION_SIZE * GENE_SIZE * 2) * 100
    percent = round(number, 3)
    print "MUTATION TRIGGERED {0}/{1} TIMES ({2}%)".format(mutation_count, POPULATION_SIZE * GENE_SIZE * 2, percent)