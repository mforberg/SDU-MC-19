from BuildingsMetrics import BuildingsMetrics


class Well(BuildingsMetrics):

    def __init__(self, name, probability, length, width, height):
        self.name = name
        self.probability = probability
        self.length = length
        self.width = width
        self.height = height
