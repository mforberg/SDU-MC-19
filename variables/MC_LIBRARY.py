import copy
import random

WELL_PROBABILITY = 0
NORMAL_HOUSE_PROBABILITY = 40
BLACKSMITH_PROBABILITY = 10
INN_PROBABILITY = 10
SMALL_FARM_PROBABILITY = 20
BIG_FARM_PROBABILITY = 10
CHURCH_PROBABILITY = 10
BUFFER = 1
MAX_HEIGHT = 255


buildings = {
    "well": {"probability": WELL_PROBABILITY, "xLength": 5 + (BUFFER * 2), "zWidth": 5 + (BUFFER * 2),
             "yHeight": 2, "floorAndRoof": False, "mutationNumber": 0},
    "normalHouse": {"probability": NORMAL_HOUSE_PROBABILITY, "xLength": 7 + (BUFFER * 2), "zWidth": 7 + (BUFFER * 2),
                    "yHeight": 6, "floorAndRoof": True, "mutationNumber": 2},
    "blackSmith": {"probability": BLACKSMITH_PROBABILITY, "xLength": 9 + (BUFFER * 2), "zWidth": 7 + (BUFFER * 2),
                   "yHeight": 5, "floorAndRoof": True, "mutationNumber": 3},
    "inn": {"probability": INN_PROBABILITY, "xLength": 20 + (BUFFER * 2), "zWidth": 10 + (BUFFER * 2),
            "yHeight": 12, "floorAndRoof": True, "mutationNumber": 5},
    "smallFarm": {"probability": SMALL_FARM_PROBABILITY, "xLength": 6 + (BUFFER * 2), "zWidth": 8 + (BUFFER * 2),
                  "yHeight": 2, "floorAndRoof": False, "mutationNumber": 1},
    "bigFarm": {"probability": BIG_FARM_PROBABILITY, "xLength": 13 + (BUFFER * 2), "zWidth": 9 + (BUFFER * 2),
                "yHeight": 2, "floorAndRoof": False, "mutationNumber": 4},
    "church": {"probability": CHURCH_PROBABILITY, "xLength": 17 + (BUFFER * 2), "zWidth": 22 + (BUFFER * 2),
               "yHeight": 18, "floorAndRoof": True, "mutationNumber": 6}
}


def copy_of_buildings():
    return copy.deepcopy(buildings)  # buildings.copy() returns the same object


def total_probability():
    tp = 0
    for b in buildings:
        if b == "well":
            continue
        tp += buildings[b]["probability"]
    return tp


def get_available_buildings():
    available_list = list()
    for building in buildings.keys():
        if building == "well":
            continue
        available_list.append(building)
    return available_list


def get_random_house(buildings_copy):
    random_number = random.randint(0, total_probability())
    available_house = get_available_buildings()
    current_house = available_house[0]
    for i in xrange(0, len(available_house)):
        current_house = available_house[i]
        if random_number > buildings_copy[current_house]["probability"]:
            random_number -= buildings_copy[current_house]["probability"]
        else:
            current_house = available_house[i]
            break
    return current_house
