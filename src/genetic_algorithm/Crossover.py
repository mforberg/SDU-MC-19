import random
import copy
from variables.GA_VALUES import *


def create_new_population_from_old_one(old_generation):
    new_population = list()
    """Find the elites"""
    elites = get_elites(old_generation)
    new_population.extend(elites)
    """calculate the remaining space"""
    remaining_space = len(old_generation) - len(elites)
    """if there is any space left in the population, run the while loop"""
    if remaining_space <= 0:
        full = True
    else:
        full = False
    """while there is space in the population, fill it up with children"""
    while not full:
        parents = choose_parents(old_generation)
        children = create_pair_of_children(parents["ma"], parents["pa"])
        """use both children if the remaining space is even, use only one if it is odd"""
        if remaining_space % 2 == 0:
            new_population.append(children[0])
            new_population.append(children[1])
            remaining_space -= 2
        else:
            new_population.append(children[0])
            remaining_space -= 1
        """check if there is any remaining space"""
        if remaining_space <= 0:
            full = True
    """return the new population"""
    return new_population


def choose_parents(population):
    pop_list = list()
    total_fitness = 0
    """create wheel of fortune"""
    for solution in population:
        pop_list.append(solution)
        if solution[1] > 0:
            total_fitness += solution[1]
    """find parents"""
    return select_parents_from_wheel_of_fortune(total_fitness, pop_list)


def select_parents_from_wheel_of_fortune(total_fitness, pop_list):
    ma = pop_list[0]
    random_number = random.randint(1, int(total_fitness))
    """find out who the random number corresponds to"""
    for i in xrange(0, len(pop_list)):
        ma = pop_list[i]
        """only if the score is above 0 it will be check it"""
        if pop_list[i][1] > 0:
            if random_number > pop_list[i][1]:
                random_number -= pop_list[i][1]
            else:
                ma = pop_list[i]
                break
    pa = pop_list[0]
    random_number = random.randint(1, int(total_fitness))
    for i in xrange(0, len(pop_list)):
        pa = pop_list[i]
        if random_number > pop_list[i][1]:
            random_number -= pop_list[i][1]
        else:
            pa = pop_list[i]
            break
    return {"ma": ma, "pa": pa}


def create_pair_of_children(ma, pa):
    ma_list = well_first(ma[0])
    pa_list = well_first(pa[0])
    child1 = []
    child2 = []
    """find which of ma and pa is smaller"""
    if len(ma_list) < len(pa_list):
        longest_nr = len(pa_list)
        shortest_nr = len(ma_list)
        first = ma_list
        second = pa_list
        """single-point crossover (random point)"""
        point = random.randint(0, shortest_nr)
    else:
        longest_nr = len(ma_list)
        shortest_nr = len(pa_list)
        first = pa_list
        second = ma_list
        """single-point crossover (random point)"""
        point = random.randint(0, shortest_nr)
    """start adding buildings to the children"""
    gene_changer = False
    for i in range(0, longest_nr):
        if point == i:
            gene_changer = not gene_changer
        if gene_changer:
            if shortest_nr > i:
                building = copy.deepcopy(first[i])
                child1.append(building)
            building2 = copy.deepcopy(second[i])
            child2.append(building2)
        else:
            if shortest_nr > i:
                building = copy.deepcopy(first[i])
                child2.append(building)
            building2 = copy.deepcopy(second[i])
            child1.append(building2)
    return [child1, child2]


def get_elites(old_generation):
    elites = list()
    """sort so the elites are first"""
    elites_first = sorted(old_generation, key=lambda solution: solution[1], reverse=True)
    """find how many of the elites is wanted"""
    amount = int(math.ceil(ELITES_PERCENTAGE * len(old_generation)))
    """get the elites and put them in another list"""
    for i in range(0, amount):
        elites.append(elites_first[i][0])
    return elites


def well_first(parent):
    new_list = list()
    extra_list = list()
    for building in parent:
        if building.type_of_house == "well":
            new_list.append(building)
        else:
            extra_list.append(building)
    for building in extra_list:
        new_list.append(building)
    return new_list
