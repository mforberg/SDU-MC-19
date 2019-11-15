import random
import copy


def get_minimum_amount_of_houses(box_x, box_z):
    minimum_amount_of_houses = round((box_z * box_x) / 6200)
    return minimum_amount_of_houses


def get_maximum_amount_of_houses(box_x, box_z):
    maximum_amount_of_houses = round((box_z * box_x) / 3100)
    return maximum_amount_of_houses


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
    return solution
