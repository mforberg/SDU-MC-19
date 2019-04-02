import Building
from variables.MC_LIBRARY import *
from variables.GA_VALUES import *

def generate_population(heightMap, boxWidth, boxHeigth, startingPoint):
    fullpop = list()
    for i in xrange(POPULATION_SIZE):
        x = generate_solution(heightMap, boxWidth, boxHeigth, startingPoint)
        tuple = (x, 0)
        fullpop.append(tuple)
    return fullpop


def generate_solution(heightMap, boxWidth, boxHeigth, startingPoint):
    blockedCoordinates = {}
    dictOfCoordinates = {}
    buildingsCopy = copy_of_buildings()

    """Generate single solution"""
    for houseNumber in xrange(0, GENE_SIZE):  # <-- GENE_SIZE should change depending on map size?
        currentHouse = get_random_house(buildingsCopy)
        """We need a well at first"""
        if (houseNumber == 0):
            currentHouse = "well"
        """Place the house's point at a random location, and check if the location works out"""
        while True:
            tryAgain = False
            tempBlockedCoordinates = {}
            coordintate = place_house_point_randomly(boxWidth, boxHeigth, startingPoint, currentHouse)
            for x in range(coordintate["x"], coordintate["x"] + buildingsCopy[currentHouse]["xLength"]):
                for z in range(coordintate["z"], coordintate["z"] + buildingsCopy[currentHouse]["zWidth"]):
                    convertedCoordinate = (x, z)
                    if convertedCoordinate in blockedCoordinates.keys():
                        # print("SKIPPED: " + currentHouse)
                        tryAgain = True
                        break
                    else:
                        tempBlockedCoordinates[x, z] = [currentHouse, heightMap[x, z][0]]
                        # TODO: Maybe change this ^
                if tryAgain:
                    break
            if tryAgain:
                continue
            """add the location to blocked coordinates"""
            blockedCoordinates.update(tempBlockedCoordinates)
            dictOfCoordinates[(coordintate["x"], coordintate["z"])] = currentHouse
            break
        """The probability of normal houses should not be lowered"""
        if currentHouse == "normalHouse":
            continue
        """Reduce the probability of specialty buildings"""
        buildingsCopy[currentHouse]["probability"] = buildingsCopy[currentHouse]["probability"] / 2
    listOfBuildings = []
    for key, value in dictOfCoordinates.iteritems():
        building = Building.Building(key[0], key[1], value)
        listOfBuildings.append(building)
    #returnDict = {"blockedCoordinates": blockedCoordinates, "listOfBuildings": listOfBuildings}
    # print("- - - - - - - - - -")
    # for x in listOfBuildings:
    #     print x.typeOfHouse,
    # print("")
    # print("- - - - - - - - - -")
    #return returnDict
    return listOfBuildings


def place_house_point_randomly(boxWidth, boxHeigth, startingPoint, houseName):
    if houseName in buildings:
        """pick a random coordinate"""
        allowedMaxXArea = startingPoint["x"] + boxWidth - buildings[houseName]["xLength"]
        allowedMaxZArea = startingPoint["z"] + boxHeigth - buildings[houseName]["zWidth"]
        randomX = random.randint(startingPoint["x"], allowedMaxXArea)
        randomZ = random.randint(startingPoint["z"], allowedMaxZArea)
        coordinate = {"x": randomX, "z": randomZ}
        return coordinate
    else:
        print("You tried to place: " + houseName)
        print("place_house_randomly cant find the house's name")