import utilityFunctions
import numpy as np
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
    am.Glowstone.ID
]


dimensionCorrector = -1


def perform(level, box, options):
    print(create_two_dimensional_height_map(level, box))


def create_two_dimensional_height_map(level, box):
    positionDict = {}
    for x in range(box.maxx + dimensionCorrector, box.minx + dimensionCorrector, -1):
        for z in range(box.maxz + dimensionCorrector, box.minz + dimensionCorrector, -1):
            for y in range(box.maxy + dimensionCorrector, box.miny + dimensionCorrector, -1):
                currentBlock = level.blockAt(x, y, z)
                if currentBlock in blocks:
                    positionDict[x, z] = y
                    break
                else:
                    utilityFunctions.setBlock(level, (0, 0), x, y, z)
    return positionDict