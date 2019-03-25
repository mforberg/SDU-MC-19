# noinspection PyUnresolvedReferences
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
# noinspection PyUnresolvedReferences
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

def create_two_dimensional_height_map(level, box):
    positionDict = {}
    xReferencePoint = 200
    """Find the reference point by going down the y-axiz untill there is a block that isn't in the skipBlocks"""
    for y in range(box.maxy + dimensionCorrector, box.miny + dimensionCorrector, -1):
        currentBlock = level.blockAt(box.maxx + dimensionCorrector, y, box.maxz + dimensionCorrector)
        if currentBlock in skipBlocks:
            continue
        xReferencePoint = y
        break

    """From the reference point, start finding the heights"""
    for x in range(box.maxx + dimensionCorrector, box.minx + dimensionCorrector, -1):
        currentReferencePoint = xReferencePoint
        onlyUpdateOnce = True
        for z in range(box.maxz + dimensionCorrector, box.minz + dimensionCorrector, -1):
            currentBlock = level.blockAt(x, currentReferencePoint, z)
            """if air is found, go down until there is a non-air block"""
            if(currentBlock in skipBlocks):
                while currentBlock in skipBlocks:
                    currentReferencePoint -= 1
                    currentBlock = level.blockAt(x, currentReferencePoint, z)
                y = currentReferencePoint
                positionDict[x, z] = [y, currentBlock]
                if(onlyUpdateOnce):
                    onlyUpdateOnce = False
                    xReferencePoint = y
            else:
                """if any other block is found, go up until air is found and -1 in the y-coordinate"""
                while currentBlock not in skipBlocks:
                    currentReferencePoint += 1
                    currentBlock = level.blockAt(x, currentReferencePoint, z)
                currentReferencePoint -= 1
                currentBlock = level.blockAt(x, currentReferencePoint, z)
                y = currentReferencePoint
                positionDict[x, z] = [y, currentBlock]
                if (onlyUpdateOnce):
                    onlyUpdateOnce = False
                    xReferencePoint = y

    return positionDict