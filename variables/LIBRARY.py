WELL_PROBABILITY        = 0
NORMALHOUSE_PROBABILITY = 30
BLACKSMITH_PROBABILITY  = 10
INN_PROBABILITY         = 10
SMALLFARM_PROBABILITY   = 10
BIGFARM_PROBABILITY     = 10
CHURCH_PROBABILITY      = 10


buildings = {
    "well": {"probability": WELL_PROBABILITY, "xLength": 4, "zWidth": 4, "yHeight": 4},
    "normalHouse": {"probability": NORMALHOUSE_PROBABILITY, "xLength": 5, "zWidth": 5, "yHeight": 6},
    "blackSmith": {"probability": BLACKSMITH_PROBABILITY, "xLength": 8, "zWidth": 5, "yHeight": 5},
    "inn": {"probability": INN_PROBABILITY, "xLength": 20, "zWidth": 10, "yHeight": 12},
    "smallFarm": {"probability": SMALLFARM_PROBABILITY, "xLength": 6, "zWidth": 9, "yHeight": 2},
    "bigFarm": {"probability": BIGFARM_PROBABILITY, "xLength": 13, "zWidth": 9, "yHeight": 2},
    "church": {"probability": CHURCH_PROBABILITY, "xLength": 17, "zWidth": 22, "yHeight": 18}
}



def totalprobability():
    totalprobability = 0
    for building in buildings.keys():
        if building == "well":
            continue
        totalprobability += building["probability"]
    return totalprobability