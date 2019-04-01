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

        fullButthole = self.generate_population(heightMap, boxWidth, boxHeigth, startingPoint)
        withFitness = self.population_fitness(fullButthole, heightMap)


        #blockedCoordinates = tempDict["blockedCoordinates"]


        # choose_parents()
        # mate_those_bastards()
        # add_some_mutation()
        # check_those_children()

    def generate_population(self, heightMap, boxWidth, boxHeigth, startingPoint):
        fullpop = {}
        for i in xrange(POPULATION_SIZE):
            x = self.generate_solution(heightMap, boxWidth, boxHeigth, startingPoint)
            fullpop[x] = 0
        return fullpop

    def generate_solution(self, heightMap, boxWidth, boxHeigth, startingPoint):
        blockedCoordinates = {}
        dictOfCoordinates = {}
        buildingsCopy = copy_of_buildings()

        """Generate single solution"""
        for houseNumber in xrange(0, GENE_SIZE): # <-- GENE_SIZE should change depending on map size?
            currentHouse = get_random_house(buildingsCopy)
            """We need a well at first"""
            if (houseNumber == 0):
                currentHouse = "well"
            """Place the house's point at a random location, and check if the location works out"""
            while True:
                tryAgain = False
                tempBlockedCoordinates = {}
                coordintate = self.place_house_point_randomly(boxWidth, boxHeigth, startingPoint, currentHouse)
                for x in range(coordintate["x"], coordintate["x"] + buildingsCopy[currentHouse]["xLength"]):
                    for z in range(coordintate["z"], coordintate["z"] + buildingsCopy[currentHouse]["zWidth"]):
                        convertedCoordinate = (x, z)
                        if convertedCoordinate in blockedCoordinates.keys():
                            #print("SKIPPED: " + currentHouse)
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
        returnDict = {"blockedCoordinates": blockedCoordinates, "listOfBuildings": listOfBuildings}
        # print("- - - - - - - - - -")
        # for x in listOfBuildings:
        #     print x.typeOfHouse,
        # print("")
        # print("- - - - - - - - - -")
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

    def population_fitness(self, population, heightMap):
        for solution in population.keys:
            listOfBuildings = solution["listOfBuildings"]
            fitness = self.calculate_fitness(listOfBuildings, heightMap)
            population[solution] = fitness
        return population

    def calculate_fitness(self, population, heightMap):
        fitnessScore = 0
        alreadyCalculated = list()
        for building in population:
            fitnessScore += self.check_area(building, heightMap)
            if building.typeOfHouse == "well":
                continue
            for building2 in population:
                if building == building2 or building2 in alreadyCalculated:
                    continue
                elif building2.typeOfHouse == "well":
                    fitnessScore += 2 * (self.distance_between(building, building2))
                else:
                    fitnessScore += self.distance_between(building, building2)
            alreadyCalculated.append(building)
        return fitnessScore

    def distance_between(self, house1, house2):
        distance = house1.distance_between_building(house2)
        """distance score is calculated using an quadratic equation"""
        a = float(-4) / 45
        b = float(16)/3
        c = 0
        distanceScore = a * math.pow(distance, 2) + b * distance + c
        """we dont want score under zero"""
        if distanceScore < 0:
            distanceScore = 0
        elif distanceScore > 50:
            distanceScore = 100
        return distanceScore

    def check_area(self, building, heightMap):
        totalArea = buildings[building.typeOfHouse]["xLength"] * buildings[building.typeOfHouse]["zWidth"]
        listOfHeights = []
        unique = set()
        amount = 0
        amountOfWater = 0
        for x in xrange(building.x, building.x + buildings[building.typeOfHouse]["xLength"]):
            for z in xrange(building.z, building.z + buildings[building.typeOfHouse]["zWidth"]):
                """check for water"""
                if heightMap[x, z][1] == 9:
                    amountOfWater += 1
                amount += heightMap[x, z][0]
                listOfHeights.append(heightMap[x, z][0])
                unique.add(heightMap[x, z][0])
        average = int(round(amount / float(totalArea)))
        blocksModified = 0
        for number in unique:
            blocksModified += listOfHeights.count(number) * abs(average - number)
        """the score is calculated here. Maximum score is 100"""
        score = 100 - int(round(blocksModified/10))
        """subtract extra for water"""
        score -= amountOfWater * 6
        """we dont want score under zero"""
        if score < 0:
            score = 0
        return score

    def choose_parents(self, population):
        popList = list()
        totalFitness = 0
        """create wheel of fortune"""
        for solution in population:
            popList.append(solution)
            totalFitness += solution[1]

        """find parents pair"""
        parents = list()
        for i in range(0, self.population_size/2):
            parents.append(self.find_ma_and_pa(totalFitness, popList))
        return parents

    def find_ma_and_pa(self, totalFitness, popList):
        ma = popList[0]
        randomNumber = random.randint(0, totalFitness)
        for i in xrange(0, self.population_size):
            ma = popList[i]
            if randomNumber > popList[i][1]:
                randomNumber -= popList[i][1]
            else:
                ma = popList[i]
                break
        pa = popList[0]
        randomNumber = random.randint(0, totalFitness)
        for i in xrange(0, self.population_size):
            pa = popList[i]
            if randomNumber > popList[i][1]:
                randomNumber -= popList[i][1]
            else:
                pa = popList[i]
                break
        return {"ma": ma, "pa": pa}
