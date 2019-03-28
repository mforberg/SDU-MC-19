import math
import Building
from variables.MC_LIBRARY import *
from variables.GA_VALUES import *

class Genetic_Algorithm:

    #gene_size = GENE_SIZE
    crossover_rate = CROSSOVER_RATE
    mutation_rate = MUTATION_RATE
    population_size = POPULATION_SIZE

    def run_genetic_algorithm(self, heightMap, boxWidth, boxHeigth, startingPoint):
        tempDict = self.generate_population(heightMap, boxWidth, boxHeigth, startingPoint)
        blockedCoordinates = tempDict["blockedCoordinates"]
        listOfBuildings = tempDict["listOfBuildings"]
        building = listOfBuildings[0]
        self.modified_blocks(building, heightMap)

        fitnessPopulation = self.calculate_fitness(listOfBuildings, heightMap)

        # choose_parents()
        # mate_those_bastards()
        # add_some_mutation()
        # check_those_children()

    def generate_population(self, heightMap, boxWidth, boxHeigth, startingPoint):
        blockedCoordinates = {}
        dictOfCoordinates = {}
        buildingsCopy = copy_of_buildings()

        """Generate single solution"""
        for houseNumber in xrange(0, GENE_SIZE): # <-- GENE_SIZE should change depending on map size?
            currentHouse = get_random_house()
            """We need a well at first"""
            if (houseNumber == 0):
                currentHouse = "well"
            """Place the house's point at a random location, and check if the location works out"""
            while True:
                tryAgain = False
                tempBlockedCoordinates = {}
                coordintate = self.place_house_point_randomly(boxWidth, boxHeigth, startingPoint, currentHouse)
                for x in range(coordintate["x"], coordintate["x"] + buildings[currentHouse]["xLength"]):
                    for z in range(coordintate["z"], coordintate["z"] + buildings[currentHouse]["zWidth"]):
                        convertedCoordinate = (x, z)
                        if convertedCoordinate in blockedCoordinates.keys():
                            print("SKIPPED: " + currentHouse)
                            tryAgain = True
                            break
                        else:
                            tempBlockedCoordinates[x, z] = [currentHouse, heightMap[x, z][0]]
                    if tryAgain:
                        break
                if tryAgain:
                    continue
                """add the location to blocked coordinates"""
                blockedCoordinates.update(tempBlockedCoordinates)
                dictOfCoordinates[(coordintate["x"], coordintate["z"])] = currentHouse
                break
            """decrement the building probability from the dict, unless it is a normal house"""
            if currentHouse == "normalHouse":
                continue
            buildingsCopy[currentHouse]["probability"] = buildingsCopy[currentHouse]["probability"] / 2
        listOfBuildings = []
        for key, value in dictOfCoordinates.iteritems():
            building = Building.Building(key[0], key[1], value)
            listOfBuildings.append(building)
        returnDict = {"blockedCoordinates": blockedCoordinates, "listOfBuildings": listOfBuildings}
        for x in listOfBuildings:
            print x.typeOfHouse,
        return returnDict

    def place_house_point_randomly(self, boxWidth, boxHeigth, startingPoint, houseName):
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

    def calculate_fitness(self, population, heightMap):
        fitnessScore = 0

        #fitnessScore += distance_between()

        return fitnessScore

    def distance_between(self, house1, house2):
        distance = house1.distance_between_building(house2, buildings)
        """distance score is calculated using an quadratic equation"""
        a = float(-4) / 45
        b = float(16)/3
        c = 20
        distanceScore = a * math.pow(distance, 2) + b * distance + c
        return distanceScore

    def modified_blocks(self, building, heightMap):
        totalArea = buildings[building.typeOfHouse]["xLength"] * buildings[building.typeOfHouse]["zWidth"]
        listOfHeights = []
        unique = set()
        amount = 0
        for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
                amount += heightMap[x, z][0]
                listOfHeights.append(heightMap[x, z][0])
                unique.add(heightMap[x, z][0])
        average = int(round(amount / float(totalArea)))
        blocksModified = 0
        for number in unique:
            blocksModified += listOfHeights.count(number) * abs(average - number)
        return blocksModified
