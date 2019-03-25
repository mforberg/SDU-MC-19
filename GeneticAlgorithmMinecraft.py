import random

def generate_population(heightMap, boxWidth, boxHeigth, startingPoint, buildingsCopy):
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
        avaiableHouse = list()
        for building in buildingsCopy.keys():
            if building == "well":
                continue
            avaiableHouse.append(building)
        """calculate total probability"""
        totalProbablility = 0
        for building in buildingsCopy:
            if building == "well":
                continue
            totalProbablility += buildingsCopy[building]["probability"]
        """pick a random number between 0 and the total probability"""
        randomPickedNumber = random.randint(0, totalProbablility)
        """Find which house it corresponds to"""
        currentHouse = avaiableHouse[0]
        for i in range(0, len(avaiableHouse)):
            currentHouse = avaiableHouse[i]
            if randomPickedNumber > buildingsCopy[currentHouse]["probability"]:
                randomPickedNumber -= buildingsCopy[currentHouse]["probability"]
            else:
                currentHouse = avaiableHouse[i]
                break

        # currentHouse = random.choice(avaiableHouse)
        """We need a well at first"""
        if (houseNumber == 0):
            currentHouse = "well"
        """Place the house's point at a random location, and check if the location works out"""
        while True:
            tryAgain = False
            tempBlockedCoordinates = {}
            coordintate = place_house_point_randomly(boxWidth, boxHeigth, startingPoint, currentHouse, buildingsCopy)
            for x in range(coordintate["x"],
                           coordintate["x"] + buildingsCopy[currentHouse]["xLength"]):
                for z in range(coordintate["z"],
                               coordintate["z"] + buildingsCopy[currentHouse]["zWidth"]):
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
        """decrement the building probability from the dict"""
        buildingsCopy[currentHouse]["probability"] = buildingsCopy[currentHouse]["probability"] / 2

    """Don't do this, only for testing"""
    print(dictOfCoordinates)
    return blockedCoordinates



def place_house_point_randomly(boxWidth, boxHeigth, startingPoint, houseName, buildingsCopy):
    print(houseName)
    #print(buildingsCopy.keys())
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
