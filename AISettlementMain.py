# noinspection PyUnresolvedReferences
import utilityFunctions
import GeneticAlgorithmMinecraft as GAM
import MapAnalysis as MA

"Dimensions for the different buildings."
"Dict of all the different buildings which have a dict for their dimensions"
buildings = {
    "well": {"probability": 0, "xLength": 4, "zWidth": 4},
    "normalHouse": {"probability": 0, "xLength": 5, "zWidth": 5},
    "blackSmith": {"probability": 0, "xLength": 8, "zWidth": 5},
    "inn": {"probability": 0, "xLength": 20, "zWidth": 10},
    "smallFarm": {"probability": 0, "xLength": 6, "zWidth": 9},
    "bigFarm": {"probability": 0, "xLength": 13, "zWidth": 9},
    "church": {"probability": 0, "xLength": 17, "zWidth": 22}
}

def perform(level, box, options):
    print("start")
    """Depending on the size of the box, different amount of buildings needs to be added. x-size = z-size"""
    initialize_buildings()
    heightMap = MA.create_two_dimensional_height_map(level, box)
    startingPoint = {"x": box.minx, "z": box.minz}
    gam = GAM.Genetic_Algorithm()
    gam.run_genetic_algorithm(heightMap, box.maxx - box.minx, box.maxz - box.minz, startingPoint, buildings)
    # building1 = GAM.Building(10, 10, "church")
    # building2 = GAM.Building(8, 0, "well")
    # print(gam.distance_to_well(building1, building2, buildings))
    #for key in coor.keys():
    #    print(key)
        #utilityFunctions.setBlock(level, (am.DiamondOre.ID, 0), key[0], coor[key][1], key[1])


def initialize_buildings():
    buildings["well"]["probability"] = 0
    buildings["normalHouse"]["probability"] = 30
    buildings["blackSmith"]["probability"] = 10
    buildings["inn"]["probability"] = 10
    buildings["smallFarm"]["probability"] = 10
    buildings["bigFarm"]["probability"] = 10
    buildings["church"]["probability"] = 10
