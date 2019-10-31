from variables.MC_LIBRARY import *
from variables.GA_VALUES import *
from src.Building import *
from src.genetic_algorithm.SharedFunctions import *


def generate_population(box_x, box_z, starting_point):
    full_pop = list()
    for i in xrange(POPULATION_SIZE):
        x = generate_solution(box_x, box_z, starting_point)
        full_pop.append(x)
    return full_pop


def generate_solution(box_x, box_z, starting_point):
    buildings_copy = copy_of_buildings()
    list_of_buildings = list()
    """Generate single solution"""
    for house_number in xrange(0, get_amount_of_houses(box_x, box_z)):
        current_house = get_random_house(buildings_copy)
        """We need a well at first"""
        if house_number == 0:
            current_house = "well"
        list_of_buildings.append(place_building(box_x, box_z, starting_point, current_house, list_of_buildings))
    return list_of_buildings


def place_building(box_x, box_z, starting_point, current_house, list_of_buildings):
    successful = False
    building = None
    while not successful:
        try_again = False
        coordinate = place_house_point_randomly(box_x, box_z, starting_point, current_house)
        building = Building(coordinate["x"], coordinate["z"], current_house)
        for building2 in list_of_buildings:
            if building.check_if_house_is_within(building2):
                try_again = True
                break
        if try_again:
            continue
        successful = True
    return building


def place_house_point_randomly(box_x, box_z, starting_point, house_name):
    if house_name in buildings:
        """pick a random coordinate"""
        allowed_max_x_area = starting_point["x"] + box_x - buildings[house_name]["xLength"]
        allowed_max_z_area = starting_point["z"] + box_z - buildings[house_name]["zWidth"]
        random_x = random.randint(starting_point["x"], allowed_max_x_area)
        random_z = random.randint(starting_point["z"], allowed_max_z_area)
        coordinate = {"x": random_x, "z": random_z}
        return coordinate
    else:
        print("You tried to place: " + house_name)
        print("place_house_randomly can't find the house's name")


def get_amount_of_houses(box_x, box_z):
    amount_of_houses = random.randint(get_minimum_amount_of_houses(box_x, box_z), get_maximum_amount_of_houses(box_x,
                                                                                                               box_z))
    return amount_of_houses
