import random
from variables.GA_VALUES import *


def create_new_population_from_old_one(oldGeneration):
    newPopulation = list()
    for x in range(0, POPULATION_SIZE/2):
        parents = choose_parents(oldGeneration)
        children = it_is_baby_time(parents[0]["ma"], parents[0]["pa"])
        newPopulation.append(children[0])
        newPopulation.append(children[1])
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
