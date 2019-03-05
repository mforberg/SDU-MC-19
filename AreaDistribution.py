import utilityFunctions
import numpy as np
import random
import datetime
from multiprocessing import Process
from pymclevel import alphaMaterials

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
    am.Air.ID#,
    #am.Wood.ID,
    #am.Leaves.ID
]

#zero indexed coordinates in the box
dimensionCorrector = -1


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
    start = datetime.datetime.now()
    create_two_dimensional_height_map(level, box)
    print(datetime.datetime.now() - start)
    #skidaddle_skidoodle_perform_genetic_algorithm_you_noodle()


def create_two_dimensional_height_map(level, box):
    positionDict = {}
    xReferencePoint = 200
    """Find the reference point by going down the y-axiz untill there is a block that isn't in the skipBlocks"""
    for y in range(box.maxy + dimensionCorrector, box.miny + dimensionCorrector, -1):
        currentBlock = level.blockAt(box.maxx + dimensionCorrector, y, box.maxz + dimensionCorrector)
        if currentBlock in skipBlocks:
            continue
        print(y)
        xReferencePoint = y + 1
        #utilityFunctions.setBlock(level, (am.DiamondOre.ID, 0), box.maxx + dimensionCorrector, y, box.maxz + dimensionCorrector)
        break

    """From the reference point, start finding the hights"""
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
                y = currentReferencePoint + 1
                positionDict[x, z] = [y, currentBlock]
                if(onlyUpdateOnce):
                    onlyUpdateOnce = False
                    xReferencePoint = y
            else:
                """if any other block is found, go up until air is found and -1 in the y-coordinate"""
                while currentBlock != am.Air.ID:
                    currentReferencePoint += 1
                    currentBlock = level.blockAt(x, currentReferencePoint, z)
                currentBlock = level.blockAt(x, currentReferencePoint - 1, z)
                y = currentReferencePoint + 1
                positionDict[x, z] = [y, currentBlock]
                if (onlyUpdateOnce):
                    onlyUpdateOnce = False
                    xReferencePoint = y
    return positionDict


dummyData = {}
#(1, 1): 1, (1, 2): 1, (1, 3): 2, (1, 4): 2, (1, 5): 3, (1, 6): 2, (1, 7): 2, (1, 8): 2,
#(2, 1): 1, (2, 2): 1, (2, 3): 2, (2, 4): 2, (2, 5): 3, (2, 6): 2, (2, 7): 2, (2, 8): 2,
#(3, 1): 2, (3, 2): 2, (3, 3): 2, (3, 4): 3, (3, 5): 3, (3, 6): 3, (3, 7): 2, (3, 8): 2,
#(4, 1): 2, (4, 2): 2, (4, 3): 2, (4, 4): 3, (4, 5): 3, (4, 6): 3, (4, 7): 3, (4, 8): 3,
#(5, 1): 2, (5, 2): 2, (5, 3): 2, (5, 4): 3, (5, 5): 3, (5, 6): 3, (5, 7): 4, (5, 8): 3,
#(6, 1): 2, (6, 2): 2, (6, 3): 3, (6, 4): 3, (6, 5): 4, (6, 6): 3, (6, 7): 5, (6, 8): 4,
#(7, 1): 2, (7, 2): 2, (7, 3): 3, (7, 4): 3, (7, 5): 4, (7, 6): 4, (7, 7): 5, (7, 8): 4,
#(8, 1): 2, (8, 2): 3, (8, 3): 3, (8, 4): 3, (8, 5): 4, (8, 6): 5, (8, 7): 5, (8, 8): 5


def skidaddle_skidoodle_perform_genetic_algorithm_you_noodle():
    amountOfHouses = 4
    size = 4
    for x in range(1, 11):
        for z in range(1, 11):
            if random.randint(1, 11) > 7:
                dummyData[x, z] = 4
            else:
                dummyData[x, z] = 3
    #print(dummyData)

    #create_population()
    populationList = {}
    #for i in range (1, 1001):
        #location = {}
        #for j in range (1, amountOfHouses + 1):
            #place houses at random location (no overlapping)
            #houses[j] =
        #populationList[i] = location



    #calculate_fitness()
    #choose_parents()
    #mate_those_bastards()
    #add_some_mutation()
    #check_those_children()


class BuildingSpot:
    def __init__(self, xStart, zStart, xEnd, zEnd):
        self.xStart = xStart
        self.zStart = zStart
        self.xEnd = xEnd
        self.zEnd = zEnd