import Building
from variables.MC_LIBRARY import *
from variables.GA_VALUES import *


def generate_population(box_x, box_z, starting_point):
    full_pop = list()
    for i in xrange(POPULATION_SIZE):
        x = generate_solution(box_x, box_z, starting_point)
        full_pop.append(x)
    return full_pop


def generate_solution(box_x, box_z, starting_point):
    dict_of_coordinates = place_houses(box_x, box_z, starting_point)
    list_of_buildings = list()
    for key, value in dict_of_coordinates.iteritems():
        building = Building.Building(key[0], key[1], value)
        list_of_buildings.append(building)
    return list_of_buildings


def place_houses(box_x, box_z, starting_point):
    dict_of_coordinates = {}
    buildings_copy = copy_of_buildings()
    blocked_coordinates = {}
    """Generate single solution"""
    for house_number in xrange(0, get_amount_of_houses(box_x, box_z)):
        current_house = get_random_house(buildings_copy)
        """We need a well at first"""
        if house_number == 0:
            current_house = "well"
        """Place the house's point at a random location, and check if the location works out"""
        successful = False
        while not successful:
            try_again = False
            temp_blocked_coordinates = {}
            coordinate = place_house_point_randomly(box_x, box_z, starting_point, current_house)
            for x in range(coordinate["x"], coordinate["x"] + buildings_copy[current_house]["xLength"]):
                for z in range(coordinate["z"], coordinate["z"] + buildings_copy[current_house]["zWidth"]):
                    converted_coordinate = (x, z)
                    if converted_coordinate in blocked_coordinates.keys():
                        try_again = True
                        break
                    else:
                        temp_blocked_coordinates[x, z] = [current_house]
                if try_again:
                    break
            if try_again:
                continue
            """add the location to blocked coordinates"""
            blocked_coordinates.update(temp_blocked_coordinates)
            dict_of_coordinates[(coordinate["x"], coordinate["z"])] = current_house
            successful = True
        """The probability of normal houses should not be lowered"""
        if current_house == "normalHouse":
            continue
        """Reduce the probability of specialty buildings"""
        buildings_copy[current_house]["probability"] = buildings_copy[current_house]["probability"] / 2
    return dict_of_coordinates


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
    """Pick a number between ~10 to ~20 if the size is 250*250"""
    minimumAmountOfHouses = round((box_z * box_x) / 6200)
    maximumAmountOfHouses = round((box_z * box_x) / 3100)
    amountOfHouses = random.randint(minimumAmountOfHouses, maximumAmountOfHouses)
    return amountOfHouses
