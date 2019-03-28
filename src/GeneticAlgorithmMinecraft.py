import random
import math
import Building
from variables.MC_LIBRARY import *
from variables.GA_VALUES import *

class Genetic_Algorithm:

    #gene_size = GENE_SIZE
    crossover_rate = CROSSOVER_RATE
    mutation_rate = MUTATION_RATE
    population_size = POPULATION_SIZE

    def run_genetic_algorithm(self, heightMap, boxWidth, boxHeigth, startingPoint, buildingsCopy):
        tempDict = self.generate_population(heightMap, boxWidth, boxHeigth, startingPoint)
        blockedCoordinates = tempDict["blockedCoordinates"]
        listOfBuildings = tempDict["listOfBuildings"]

        fitnessPopulation = self.calculate_fitness(listOfBuildings, heightMap, buildingsCopy)

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
                coordintate = self.place_house_point_randomly(boxWidth, boxHeigth, startingPoint, currentHouse, buildingsCopy)
                for x in xrange(coordintate["x"], coordintate["x"] + buildingsCopy[currentHouse]["xLength"]):
                    for z in xrange(coordintate["z"], coordintate["z"] + buildingsCopy[currentHouse]["zWidth"]):
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
            if(buildingsCopy[currentHouse].viewkeys() == "normalHouse"):
                continue
            print("- - - - - - - - - -")
            print(currentHouse)
            print("BEFORE:")
            print(buildingsCopy[currentHouse]["probability"])
            buildingsCopy[currentHouse]["probability"] = buildingsCopy[currentHouse]["probability"] / 2
            print("AFTER:")
            print(buildingsCopy[currentHouse]["probability"])
        listOfBuildings = []
        for key, value in dictOfCoordinates.iteritems():
            building = Building.Building(key[0], key[1], value)
            listOfBuildings.append(building)
        returnDict = {"blockedCoordinates": blockedCoordinates, "listOfBuildings": listOfBuildings}
        for x in listOfBuildings:
            print x.typeOfHouse,
        return returnDict

    def place_house_point_randomly(self, boxWidth, boxHeigth, startingPoint, houseName, buildingsCopy):
        if houseName in buildingsCopy:
            """pick a random coordinate"""
            allowedMaxXArea = startingPoint["x"] + boxWidth - buildingsCopy[houseName]["xLength"]
            allowedMaxZArea = startingPoint["z"] + boxHeigth - buildingsCopy[houseName]["zWidth"]
            randomX = random.randint(startingPoint["x"], allowedMaxXArea)
            randomZ = random.randint(startingPoint["z"], allowedMaxZArea)
            coordinate = {"x": randomX, "z": randomZ}
            return coordinate
        else:
            print("You tried to place: " + houseName)
            print("place_house_randomly cant find the house's name")

    def calculate_fitness(self, population, heightMap, buildingsCopy):

        fitnessScore = 0

        #fitnessScore += distance_between()

        return fitnessScore

    def distance_between(self, house1, house2, buildingsCopy):
        distance = house1.distance_between_building(house2, buildingsCopy)
        """distance score is calculated using an quadratic equation"""
        a = float(-4) / 45
        b = float(16)/3
        c = 20
        distanceScore = a * math.pow(distance, 2) + b * distance + c
        return distanceScore