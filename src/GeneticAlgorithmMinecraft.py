import math
import Building
from variables.MC_LIBRARY import *
from variables.GA_VALUES import *
import random
import datetime

class Genetic_Algorithm:

    #gene_size = GENE_SIZE
    crossover_rate = CROSSOVER_RATE
    mutation_rate = MUTATION_RATE
    population_size = POPULATION_SIZE

    def run_genetic_algorithm(self, heightMap, boxWidth, boxHeigth, startingPoint):

        fullButthole = self.generate_population(heightMap, boxWidth, boxHeigth, startingPoint)
        withFitness = self.population_fitness(fullButthole, heightMap)
        print self.min_max_avg(withFitness)
        postMutation = self.mutate_population(withFitness)
        print self.min_max_avg(postMutation)


        #blockedCoordinates = tempDict["blockedCoordinates"]


        # choose_parents()
        # mate_those_bastards()
        # add_some_mutation()
        # check_those_children()

        """
        Runtimes for sections
        FULLBUTTHOLE: 9.985
        FITNESS: 2.163
        MINMAXAVG: 0.0
        MUTATE: 0.007
        """


    def generate_population(self, heightMap, boxWidth, boxHeigth, startingPoint):
        fullpop = list()
        for i in xrange(POPULATION_SIZE):
            i = self.generate_solution(heightMap, boxWidth, boxHeigth, startingPoint)
            tuple = (i,0)
            fullpop.append(tuple)
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

    def min_max_avg(self, data):
        maximum = data[0]
        minimum = data[0]
        average = 0

        for item in data:
            if item[1] > maximum[1]:
                maximum = item
            if item[1] < minimum[1]:
                minimum = item
            average += item[1]
        average = average/len(data)
        return "MIN: {0}\tMAX: {1}\tAVG: {2}".format(round(minimum[1], 8), round(maximum[1], 8), round(average, 8))


    def population_fitness(self, population, heightMap):
        fullpop_with_fitness = list()
        for solution in population:
            dict = solution[0]

            fitness = self.solution_fitness(dict["listOfBuildings"], heightMap)
            tuple = (dict, fitness)
            fullpop_with_fitness.append(tuple)
            del solution
        return fullpop_with_fitness


    def solution_fitness(self, solution, heightMap):
        fitnessScore = 0

        """ GLOBAL WEIGHTS """
        variance_weight = 1.0
        variance_max_score = 1000
        """ END OF WEIGHTS """

        alreadyCalculated = list()
        unique_buildings = set()
        for building in solution:
            fitnessScore += self.check_area(building, heightMap)
            if building.typeOfHouse == "well":
                continue
            for building2 in solution:
                if building == building2 or building2 in alreadyCalculated:
                    continue
                elif building2.typeOfHouse == "well":
                    fitnessScore += 2 * (self.distance_between(building, building2))
                else:
                    fitnessScore += self.distance_between(building, building2)
            alreadyCalculated.append(building)

            """" FITNESS FOR BUILDING VARIANCE """
            unique_buildings.add(building.typeOfHouse)
        float_length = len(unique_buildings)
        percent_of_max_possible = float(float_length) / len(get_placeable_buildings())
        fitnessScore += variance_weight*(variance_max_score*math.pow(percent_of_max_possible, 2))

        """ END OF VARIANCE FITNESS """
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

    def mutate_population(self, population):

        mutation_count = 0

        for item in population:
            dict = item[0]
            buildinglist = dict["listOfBuildings"]

            mutation_trigger = int(MUTATION_RATE * 100)
            print(mutation_trigger)

            for i in buildinglist:
                randomnumber = random.randint(1, 100)
                if randomnumber == mutation_trigger:
                    mutation_count += 1

                    x_or_z_decider = random.randint(1, 100)
                    add_or_subtract_decider = random.randint(1, 100)

                    if x_or_z_decider <= 50:
                        if add_or_subtract_decider >= 50:
                            i.x = i.x + 1
                        else:
                            i.x = i.x - 1
                    else:
                        if add_or_subtract_decider >= 50:
                            i.z = i.z + 1
                        else:
                            i.z = i.z - 1
        number = float(mutation_count)/((POPULATION_SIZE*GENE_SIZE))*100
        percent = round(number, 3)
        print "MUTATION TRIGGERED {0}/{1} TIMES ({2}%)".format(mutation_count, POPULATION_SIZE*GENE_SIZE, percent)
        return population