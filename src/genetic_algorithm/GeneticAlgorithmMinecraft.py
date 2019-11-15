from src.genetic_algorithm import CheckCriterias, Crossover, Fitness, Generation, Mutation, InfeasibleFitness
from variables.GA_VALUES import *
import copy, time


class GeneticAlgorithm:
    def __init__(self):
        pass

    def run_genetic_algorithm(self, height_map, box_x, box_z, starting_point):
        min_list = list()
        avg_list = list()
        max_list = list()
        infeasible_len = list()
        infeasible_population = list()
        overall_best_solution = None
        init_generation = Generation.generate_population(box_x, box_z, starting_point)
        current_generation = init_generation
        highest_fitness = 0
        """save the overall best"""
        for x in range(0, GENERATIONS):
            start = time.time()
            print "- - - - - - - - - - - -"
            print "CURRENT GEN: ", x + 1
            generation_with_fitness = Fitness.population_fitness(current_generation, height_map, box_x, box_z)
            # """used for creating graphs"""
            score = self.min_max_avg(generation_with_fitness)
            if score != "empty":
                min_list.append(score[0])
                avg_list.append(score[1])
                max_list.append(score[2])
            """if there is any feasible solutions"""
            if len(generation_with_fitness) > 0:
                current_best_solution = self.find_best_solution(generation_with_fitness)
                """save the best solution"""
                if current_best_solution[1] > highest_fitness:
                    highest_fitness = current_best_solution[1]
                    overall_best_solution = copy.deepcopy(current_best_solution[0])
                    print "------NEW MAX------"
                    print "       ", x + 1
                    print "-------------------"
            """FI2POP"""
            if USE_FI2POP:
                extra_with_fitness = InfeasibleFitness.population_fitness(infeasible_population, box_x, box_z,
                                                                          starting_point)
                new_extra_without_fitness = Crossover.create_new_population_from_old_one(extra_with_fitness)
                Mutation.mutate_population(new_extra_without_fitness, box_x, box_z, starting_point)
                infeasible_population = new_extra_without_fitness

            """skip mutation and new generation on last"""
            if x < GENERATIONS - 1:
                new_generation_without_fitness = Crossover.create_new_population_from_old_one(generation_with_fitness)
                Mutation.mutate_population(new_generation_without_fitness, box_x, box_z, starting_point)
                if USE_FI2POP:
                    result = CheckCriterias.fi2pop_check(new_generation_without_fitness, box_x, box_z, starting_point,
                                                         infeasible_population)
                    current_generation = result["feasible"]
                    infeasible_population = result["infeasible"]
                else:
                    current_generation = CheckCriterias.check_population(new_generation_without_fitness, box_x, box_z,
                                                                         starting_point)
            infeasible_len.append(len(infeasible_population))
            end = time.time()
            print end - start, "<-- Time"
            print "Overall Best: ", highest_fitness, ",   Size: ", len(overall_best_solution)

        dump = open(r"C:\Users\zaczt\Documents\ScientificMethods\uctest5.txt", "w+")
        for value in min_list:
            dump.write("\n" + str(round(value)))
        dump.write("\n")
        dump.write("\n")
        for value in avg_list:
            dump.write("\n" + str(round(value)))
        dump.write("\n")
        dump.write("\n")
        for value in max_list:
            dump.write("\n" + str(round(value)))
        dump.write("\n")
        dump.write("\n")
        # for value in feasible_len:
        #     dump.write("\n" + str(round(value)))
        # dump.write("\n")
        # dump.write("\n")
        for value in infeasible_len:
            dump.write("\n" + str(round(value)))
        dump.close()
        print len(overall_best_solution)
        return overall_best_solution

    @staticmethod
    def min_max_avg(data):
        if len(data) == 0:
            return "empty"
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
        ok = [minimum[1], average, maximum[1]]
        return ok
        # return "{0}\t{1}\t{2}".format(round(minimum[1], 3), round(maximum[1], 3), round(average, 3))

    @staticmethod
    def find_best_solution(fitness_generation):
        current_top = 0
        current_best = None
        for solution in fitness_generation:
            if solution[1] > current_top:
                current_top = solution[1]
                current_best = solution
        return current_best

    @staticmethod
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
