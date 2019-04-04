import random
from variables.GA_VALUES import *


def create_new_population_from_old_one(oldGeneration):
    newPopulation = list()
    """Find the elites"""
    elites = get_elites(oldGeneration)
    """calculate the remaining space"""
    remainingSpace = POPULATION_SIZE - len(elites)
    """if there is any space left in the population, run the while loop"""
    if remainingSpace <= 0:
        full = True
    else:
        full = False
    """while there is space in the population, fill it up with children"""
    while not full:
        parents = choose_parents(oldGeneration)
        children = it_is_baby_time(parents[0]["ma"], parents[0]["pa"])
        """use both children if the remaining space is even, use only one if it is odd"""
        if remainingSpace % 2 == 0:
            newPopulation.append(children[0])
            newPopulation.append(children[1])
            remainingSpace -= 2
        else:
            newPopulation.append(children[0])
            remainingSpace -= 1
        """check if there is any remaining space"""
        if remainingSpace <= 0:
            full = True
    """return the new population"""
    return newPopulation


def choose_parents(population):
    popList = list()
    totalFitness = 0
    """create wheel of fortune"""
    for solution in population:
        popList.append(solution)
        totalFitness += solution[1]

    """find parents pair"""
    parents = list()
    for i in range(0, POPULATION_SIZE / 2):
        parents.append(find_ma_and_pa(totalFitness, popList))
    return parents


def find_ma_and_pa(totalFitness, popList):
    ma = popList[0]
    randomNumber = random.randint(0, int(totalFitness))
    for i in xrange(0, POPULATION_SIZE):
        ma = popList[i]
        if randomNumber > popList[i][1]:
            randomNumber -= popList[i][1]
        else:
            ma = popList[i]
            break
    pa = popList[0]
    randomNumber = random.randint(0, int(totalFitness))
    for i in xrange(0, POPULATION_SIZE):
        pa = popList[i]
        if randomNumber > popList[i][1]:
            randomNumber -= popList[i][1]
        else:
            pa = popList[i]
            break
    return {"ma": ma, "pa": pa}


def it_is_baby_time(ma, pa):
    maList = ma[0]
    paList = pa[0]

    child1 = []
    child2 = []

    """single-point crossover (random point)"""
    point = random.randint(0, len(maList))
    geneChanger = False
    for i in range(0, len(maList)):
        if point == i:
            geneChanger = not geneChanger
        if geneChanger:
            child1.append(maList[i])
            child2.append(paList[i])
        else:
            child2.append(maList[i])
            child1.append(paList[i])
    return [child1, child2]


def get_elites(oldGeneration):
    elites = list()
    """sort so the elites are first"""
    elitesFirst = sorted(oldGeneration, key=lambda solution: solution[1], reverse=True)
    """find how many of the elites is wanted"""
    amount = int(round(ELITES_PERCENTAGE * POPULATION_SIZE))
    """get the elites and put them in another list"""
    for i in range(0, amount):
        elites.append(elitesFirst[i])
    return elites
