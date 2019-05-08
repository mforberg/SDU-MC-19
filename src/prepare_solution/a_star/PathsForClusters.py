import AStar
import PrepareAStar

def distance_for_cluster(list_of_clusters):
    goal = find_goal_in_cluster(list_of_clusters)
    for cluster in list_of_clusters:
        for building in cluster:


def find_goal_in_cluster(list_of_clusters):
    for cluster in list_of_clusters:
        for building in cluster:
            if building.type_of_house == "well":
                goal = building
                return goal
