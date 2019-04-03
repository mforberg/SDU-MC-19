import random
from variables.GA_VALUES import *

def mutate_population(population):
    mutation_count = 0

    for solution in population:
        buildinglist = solution

        mutation_trigger = int(MUTATION_RATE * 100)

        for i in buildinglist:
            randomnumber = random.randint(1, 100)
            if randomnumber == mutation_trigger:
                mutation_count += 1

                x_or_z_decider = random.randint(1, 100)
                add_or_subtract_decider = random.randint(1, 100)

                if x_or_z_decider <= 50:
                    if add_or_subtract_decider >= 50:
                        i.x = i.x + 1
                    else:
                        i.x = i.x - 1
                else:
                    if add_or_subtract_decider >= 50:
                        i.z = i.z + 1
                    else:
                        i.z = i.z - 1
    number = float(mutation_count) / ((POPULATION_SIZE * GENE_SIZE)) * 100
    percent = round(number, 3)
    print "MUTATION TRIGGERED {0}/{1} TIMES ({2}%)".format(mutation_count, POPULATION_SIZE * GENE_SIZE, percent)
    return population