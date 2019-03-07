import utilityFunctions
import numpy as np
import random
import datetime
from multiprocessing import Process
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

am = alphaMaterials

# naturally occuring materials
blocks = [
    am.Grass.ID,
    am.Dirt.ID,
    am.Stone.ID,
    am.Bedrock.ID,
    am.Sand.ID,
    am.Gravel.ID,
    am.GoldOre.ID,
    am.IronOre.ID,
    am.CoalOre.ID,
    am.LapisLazuliOre.ID,
    am.DiamondOre.ID,
    am.RedstoneOre.ID,
    am.RedstoneOreGlowing.ID,
    am.Netherrack.ID,
    am.SoulSand.ID,
    am.Clay.ID,
    am.Glowstone.ID,
    am.Water.ID
]

skipBlocks = [
    am.Air.ID,
    am.Wood.ID,
    am.Leaves.ID
]


#zero indexed coordinates in the box
dimensionCorrector = -1

"Dimensions for the different buildings."
"Dict of all the different buildings which have a dict for their dimensions"
buildings = {
    'well': {'xLength': 4, 'zWidth': 4},
    'normalHouse': {'xLength': 5, 'zWidth': 5},
    'blackSmith': {'xLength': 8, 'zWidth': 5},
    'inn': {'xLength': 20, 'zWidth': 10},
    'smallFarm': {'xLength': 6, 'zWidth': 9},
    'bigFarm': {'xLength': 13, 'zWidth': 9},
    'church': {'xLength': 17, 'zWidth': 22}
}

def perform(level, box, options):
    """
    procs = []
    amountOfProcesses = 4
    lengthOfChunk = (box.maxx - box.minx) / amountOfProcesses
    currentStartingPoint = box.minx

    # instantiating process with arguments
    for process in range(0, amountOfProcesses):
        currentEndingPoint = currentStartingPoint + lengthOfChunk
        if process == amountOfProcesses - 1:
            currentEndingPoint = box.maxx
        proc = Process(target=create_two_dimensional_height_map(level, box, currentStartingPoint, currentEndingPoint))

        procs.append(proc)
        proc.start()
        print("HERERERERERERE123")
        print(proc.pid)
        currentStartingPoint = currentEndingPoint + 1

    # complete the processes
    for proc in procs:
        proc.join()
    """

    #start = datetime.datetime.now()
    #print(am.Grass.ID)
    heightMap = create_two_dimensional_height_map(level, box, options)
    startingPoint = {"x": box.minx, "z": box.minz}
    #print(datetime.datetime.now() - start)
    coor = skidaddle_skidoodle_perform_genetic_algorithm_you_noodle(heightMap, box.maxx - box.minx, box.maxz - box.minz,
                                                             startingPoint, buildings)
    for key in coor.keys():
        utilityFunctions.setBlock(level, (am.DiamondOre.ID, 0), key[0], coor[key][1], key[1])


def create_two_dimensional_height_map(level, box, options):
    positionDict = {}
    xReferencePoint = 200
    """Find the reference point by going down the y-axiz untill there is a block that isn't in the skipBlocks"""
    for y in range(box.maxy + dimensionCorrector, box.miny + dimensionCorrector, -1):
        currentBlock = level.blockAt(box.maxx + dimensionCorrector, y, box.maxz + dimensionCorrector)
        if currentBlock in skipBlocks:
            continue
        print(y)
        xReferencePoint = y
        #utilityFunctions.setBlock(level, (am.DiamondOre.ID, 0), box.maxx + dimensionCorrector, y, box.maxz + dimensionCorrector)
        break

    """From the reference point, start finding the heights"""
    for x in range(box.maxx + dimensionCorrector, box.minx + dimensionCorrector, -1):
        currentReferencePoint = xReferencePoint
        onlyUpdateOnce = True
        for z in range(box.maxz + dimensionCorrector, box.minz + dimensionCorrector, -1):
            currentBlock = level.blockAt(x, currentReferencePoint, z)
            """if air is found, go down until there is a non-air block"""
            if(currentBlock == am.Air.ID):
                while currentBlock == am.Air.ID:
                    currentReferencePoint -= 1
                    currentBlock = level.blockAt(x, currentReferencePoint, z)
                y = currentReferencePoint
                print(str(y) + "going down")
                positionDict[x, z] = [y, currentBlock]
                if(onlyUpdateOnce):
                    onlyUpdateOnce = False
                    xReferencePoint = y
            else:
                """if any other block is found, go up until air is found and -1 in the y-coordinate"""
                while currentBlock != am.Air.ID:
                    currentReferencePoint += 1
                    currentBlock = level.blockAt(x, currentReferencePoint, z)
                currentReferencePoint -= 1
                currentBlock = level.blockAt(x, currentReferencePoint, z)
                y = currentReferencePoint
               # print(str(y) + "going up")
                positionDict[x, z] = [y, currentBlock]
                if (onlyUpdateOnce):
                    onlyUpdateOnce = False
                    xReferencePoint = y

    "Create two lists which will contain the x and z coordinates which are present in the Dict"
    xvalues = []
    zvalues = []
    for key in positionDict:
        xvalues.append(key[0])
        zvalues.append(key[1])

    "First check if the area is big enough to build a well as of now, and the places it in the corner of the selected area"
    # if abs(max(xvalues)-min(xvalues) + 1) > buildings['well']['xLength'] - 1 and \
    #         abs(max(zvalues) - min(zvalues) + 1) > buildings['well']['zWidth'] - 1:
    #     for x in range(min(xvalues), min(xvalues) + buildings['well']['xLength']):
    #         utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, box.miny + 5, min(zvalues),
    #                                           box.miny)
    #         utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), x, box.miny + 5, min(zvalues)
    #                                           + buildings['well']['zWidth'] - 1, box.miny)
    #     for z in range (min(zvalues), min(zvalues) + buildings['well']['zWidth']):
    #         utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), min(xvalues) +
    #                                           buildings['well']['xLength'] - 1, box.miny + 5, z, box.miny)
    #         utilityFunctions.setBlockToGround(level, (am.Wood.ID, 0), min(xvalues), box.miny + 5, z,
    #                                           box.miny)

    return positionDict


dummyData = {}


def skidaddle_skidoodle_perform_genetic_algorithm_you_noodle(heightMap, boxWidth, boxHeigth, startingPoint, buildingsCopy):
    blockedCoordinates = {}

    """Pick a number between ~10 to ~20 if the size is 250*250"""
    minimumAmountOfHouses = round((boxHeigth * boxWidth) / 6200)
    maximumAmountOfHouses = round((boxHeigth * boxWidth) / 3100)
    amountOfHouses = random.randint(minimumAmountOfHouses, maximumAmountOfHouses + 1)
    print(amountOfHouses)
    """randomly place them"""
    for houseNumber in range(0, amountOfHouses):
        """Pick random house"""
        currentHouse = random.choice(list(buildingsCopy.keys()))
        """We need a well at first"""
        if(houseNumber == 0):
            currentHouse = "well"
        """Place the house's point at a random location, and check if the location works out"""
        while True:
            tryAgain = False
            tempBlockedCoordinates = {}
            coordintate = place_house_point_randomly(boxWidth, boxHeigth, startingPoint, currentHouse, buildingsCopy)
            for x in range(coordintate["x"], coordintate["x"] + buildingsCopy[currentHouse]["xLength"]):
                for z in range(coordintate["z"], coordintate["z"] + buildingsCopy[currentHouse]["zWidth"]):
                    tempBlockedCoordinates[x, z] = [currentHouse, heightMap[x, z][0]]
                    if coordintate in blockedCoordinates.keys():
                        tryAgain = True
            if tryAgain:
                continue
            """add the location to blocked coordinates"""
            blockedCoordinates.update(tempBlockedCoordinates)
            break
        """delete the building from the dict"""
        print(currentHouse)
        del buildingsCopy[currentHouse]

    """Don't do this, only 4 testing"""
    return blockedCoordinates



    #create_population()
    #calculate_fitness()
    #choose_parents()
    #mate_those_bastards()
    #add_some_mutation()
    #check_those_children()


def place_house_point_randomly(boxWidth, boxHeigth, startingPoint, houseName, buildingsCopy):
    if houseName in buildingsCopy:
        """pick a random coordinate"""
        allowedMaxXArea = startingPoint["x"] + boxWidth - buildings[houseName]["xLength"]
        allowedMaxZArea = startingPoint["z"] + boxHeigth - buildings[houseName]["zWidth"]
        randomX = random.randint(startingPoint["x"], allowedMaxXArea + 1)
        randomZ = random.randint(startingPoint["z"], allowedMaxZArea + 1)
        coordinate = {"x": randomX, "z": randomZ}
        return coordinate


