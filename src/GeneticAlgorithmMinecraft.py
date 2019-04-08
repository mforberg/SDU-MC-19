import Generation
import Fitness
import Crossover
import Mutation
import time


class Genetic_Algorithm:

    def run_genetic_algorithm(self, heightMap, boxWidth, boxHeigth, startingPoint):
        initGeneration = Generation.generate_population(heightMap, boxWidth, boxHeigth, startingPoint)
        currentGeneration = initGeneration
        """start of for-loop"""
        #for x in range(0, GENERATIONS):
        generationWithFitness = Fitness.population_fitness(currentGeneration, heightMap)
        """properly skip mutation and new generation on last"""
        newGenerationWithoutFitness = Crossover.create_new_population_from_old_one(generationWithFitness)
        Mutation.mutate_population(newGenerationWithoutFitness)

        #currentGeneration = newGenerationWithoutFitness

        """end of for-loop"""

        """
        Runtimes for sections
        InitGeneration: 9.985
        FITNESS: 2.163
        MINMAXAVG: 0.0
        MUTATE: 0.007
        """
        """
        11.05799 initGen
        2.2326 Fitness
        3.1375 Crossover
        0.022988 Mutation
        """
        """ time testing in future: time.time() - time.time() = x seconds"""
        return newGenerationWithoutFitness

    def min_max_avg(self, data):
        maximum = data[0]
        minimum = data[0]
        average = 0

        for item in data:
            if item[1] > maximum[1]:
                maximum = item
            if item[1] < minimum[1]:
                minimum = item
            average += item[1]
        average = average/len(data)
        return "MIN: {0}\tMAX: {1}\tAVG: {2}".format(round(minimum[1], 8), round(maximum[1], 8), round(average, 8))
