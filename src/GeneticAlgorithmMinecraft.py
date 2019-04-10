import Generation
import Fitness
import Crossover
import Mutation
import time
import CheckCriterias
from variables.GA_VALUES import *



class Genetic_Algorithm:
    def run_genetic_algorithm(self, height_map, box_x, box_z, starting_point):
        init_generation = Generation.generate_population(box_x, box_z, starting_point)
        current_generation = init_generation
        """start of for-loop"""
        for x in range(0, GENERATIONS):
            print "- - - - - - - - - - - -"
            print "CURRENT GEN: ", x
            generation_with_fitness = Fitness.population_fitness(current_generation, height_map)
            print self.min_max_avg(generation_with_fitness)
            """properly skip mutation and new generation on last"""
            if x < GENERATIONS - 1:
                new_generation_without_fitness = Crossover.create_new_population_from_old_one(generation_with_fitness)
                Mutation.mutate_population(new_generation_without_fitness)
                start = time.time()
                current_generation = CheckCriterias.check_population(new_generation_without_fitness, box_x, box_z, starting_point)
                end = time.time()
                print end-start, "<-- Time"
            else:
                final_generation = self.find_best_solution(generation_with_fitness)
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
        """
        avg time for fitness:
        0.631109833717
        crossover:
        0.03
        mutation:
        0.006
        checkcriterias with no commented out code:
        3.52894238063
        with comment:
        same
        
        
        """
        """ time testing in future: time.time() - time.time() = x seconds"""
        return final_generation

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
        return "MIN: {0}\tMAX: {1}\tAVG: {2}".format(round(minimum[1], 3), round(maximum[1], 3), round(average, 3))

    def find_best_solution(self, fitness_generation):
        current_top = 0
        for solution in fitness_generation:
            if solution[1] > current_top:
                current_top = solution[1]
                current_best = solution[0]
        return current_best
