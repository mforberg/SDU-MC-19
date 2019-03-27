import random
import math
import Building

class Genetic_Algorithm:

    def __init__(self, gene_size, crossover_rate, mutation_rate, population_size):
        self.gene_size = gene_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population_size = population_size

    def run_genetic_algorithm(self, heightMap, boxWidth, boxHeigth, startingPoint, buildingsCopy):
        tempDict = self.generate_population(heightMap, boxWidth, boxHeigth, startingPoint, buildingsCopy)
        blockedCoordinates = tempDict["blockedCoordinates"]
        listOfBuildings = tempDict["listOfBuildings"]

        fitnessPopulation = self.calculate_fitness(listOfBuildings, heightMap, buildingsCopy)

        # choose_parents()
        # mate_those_bastards()
        # add_some_mutation()
        # check_those_children()

    def generate_population(self, heightMap, boxWidth, boxHeigth, startingPoint, buildingsCopy):
        blockedCoordinates = {}
        """Pick a number between ~10 to ~20 if the size is 250*250"""
        # minimumAmountOfHouses = round((boxHeigth * boxWidth) / 6200)
        # maximumAmountOfHouses = round((boxHeigth * boxWidth) / 3100)
        minimumAmountOfHouses = 10
        maximumAmountOfHouses = 20
        amountOfHouses = random.randint(minimumAmountOfHouses, maximumAmountOfHouses)
        dictOfCoordinates = {}
        """randomly place them"""
        for houseNumber in range(0, amountOfHouses):
            availableHouse = list()
            for building in buildingsCopy.keys():
                if building == "well":
                    continue
                availableHouse.append(building)
            """calculate total probability"""
            totalProbablility = 0
            for possibleBuilding in buildingsCopy:
                if possibleBuilding == "well":
                    continue
                totalProbablility += buildingsCopy[possibleBuilding]["probability"]
            """pick a random number between 0 and the total probability"""
            randomPickedNumber = random.randint(0, totalProbablility)
            """Find which house it corresponds to"""
            currentHouse = availableHouse[0]
            for i in range(0, len(availableHouse)):
                currentHouse = availableHouse[i]
                if randomPickedNumber > buildingsCopy[currentHouse]["probability"]:
                    randomPickedNumber -= buildingsCopy[currentHouse]["probability"]
                else:
                    currentHouse = availableHouse[i]
                    break

            # currentHouse = random.choice(availableHouse)

            """We need a well at first"""
            if (houseNumber == 0):
                currentHouse = "well"
            """Place the house's point at a random location, and check if the location works out"""
            while True:
                tryAgain = False
                tempBlockedCoordinates = {}
                coordintate = self.place_house_point_randomly(boxWidth, boxHeigth, startingPoint, currentHouse,
                                                              buildingsCopy)
                for x in range(coordintate["x"], coordintate["x"] + buildingsCopy[currentHouse]["xLength"]):
                    for z in range(coordintate["z"], coordintate["z"] + buildingsCopy[currentHouse]["zWidth"]):
                        convertedCoordinate = (x, z)
                        if convertedCoordinate in blockedCoordinates.keys():
                            print("SKIPPY")
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
            if buildingsCopy[currentHouse] == "normalHouse":
                continue
            buildingsCopy[currentHouse]["probability"] = buildingsCopy[currentHouse]["probability"] / 2
        listOfBuildings = []
        for key, value in dictOfCoordinates.iteritems():
            building = Building.Building(key[0], key[1], value)
            listOfBuildings.append(building)
        returnDict = {"blockedCoordinates": blockedCoordinates, "listOfBuildings": listOfBuildings}
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

    def modified_blocks(self, house, buildingsCopy, heightMap):
        