import copy
import random

WELL_PROBABILITY        = 0
NORMALHOUSE_PROBABILITY = 30
BLACKSMITH_PROBABILITY  = 10
INN_PROBABILITY         = 10
SMALLFARM_PROBABILITY   = 10
BIGFARM_PROBABILITY     = 10
CHURCH_PROBABILITY      = 10


buildings = {
    "well": {"probability": WELL_PROBABILITY, "xLength": 4, "zWidth": 4, "yHeight": 4, "floorAndRoof": False},
    "normalHouse": {"probability": NORMALHOUSE_PROBABILITY, "xLength": 7, "zWidth": 7, "yHeight": 6, "floorAndRoof": True},
    "blackSmith": {"probability": BLACKSMITH_PROBABILITY, "xLength": 9, "zWidth": 7, "yHeight": 5, "floorAndRoof": True},
    "inn": {"probability": INN_PROBABILITY, "xLength": 20, "zWidth": 10, "yHeight": 12, "floorAndRoof": True},
    "smallFarm": {"probability": SMALLFARM_PROBABILITY, "xLength": 6, "zWidth": 8, "yHeight": 2, "floorAndRoof": False},
    "bigFarm": {"probability": BIGFARM_PROBABILITY, "xLength": 13, "zWidth": 9, "yHeight": 2, "floorAndRoof": False},
    "church": {"probability": CHURCH_PROBABILITY, "xLength": 17, "zWidth": 22, "yHeight": 18, "floorAndRoof": True}
}


def copy_of_buildings():
    return copy.deepcopy(buildings) #buildings.copy() returns the same object


def total_probability():
    tp = 0
    for b in buildings:
        if b == "well":
            continue
        tp += buildings[b]["probability"]
    return tp


def get_placeable_buildings():
    availableList = list()
    for building in buildings.keys():
        if building == "well":
            continue
        availableList.append(building)
    return availableList


def get_random_house(buildingscopy):
    randomnumber = random.randint(0, total_probability())
    availableHouse = get_placeable_buildings()
    currentHouse = availableHouse[0]
    for i in xrange(0, len(availableHouse)):
        currentHouse = availableHouse[i]
        if randomnumber > buildingscopy[currentHouse]["probability"]:
            randomnumber -= buildingscopy[currentHouse]["probability"]
        else:
            currentHouse = availableHouse[i]
            break
    return currentHouse

