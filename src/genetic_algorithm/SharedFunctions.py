import random
import copy


def well_first(solution):
    new_list = list()
    extra_list = list()
    for building in solution:
        if building.type_of_house == "well":
            new_list.append(copy.deepcopy(building))
        else:
            extra_list.append(copy.deepcopy(building))
    for building in extra_list:
        new_list.append(building)
    return new_list


def new_randomized_order(solution):
    temp_solution = copy.deepcopy(solution)
    random.shuffle(temp_solution)
    return temp_solution
