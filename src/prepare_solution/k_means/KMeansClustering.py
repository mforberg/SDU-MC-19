from sklearn.cluster import KMeans
" For testing "
# import numpy as np
# from numpy import linalg

# Uses the sklearn framework to run K-means Clustering for the buildings


def starting_points(amount_of_clusters, list_of_buildings):
    # Find the starting points for the houses
    list_of_starting_points = list()
    for building in list_of_buildings:
        coords_for_building = building.path_connection_point
        list_of_starting_points.append([coords_for_building[0], coords_for_building[1], coords_for_building[2]])
    list_of_centroids = k_means_clustering(amount_of_clusters, list_of_starting_points)

    return list_of_centroids

def k_means_clustering(amount_of_clusters, list_of_starting_points):
    k = amount_of_clusters  # The chosen k-value is in GA_FILTER.py
    list_of_clusters = [[] for x in xrange(k)]  # Will create k lists in a list

    " For testing purpose to use the elbow method "
    # wcss = []
    # for i in range(1, 11):
    #
    #     kmeans = KMeans(n_clusters=i, init="k-means++")
    #     kmeans = kmeans.fit(list_of_starting_points)
    #     labels = kmeans.predict(list_of_starting_points)
    #     wcss.append(kmeans.inertia_)
    #     print(kmeans.inertia_)
    # p1 = (1, wcss[0])
    # p1 = np.asarray(p1)
    # p2 = np.asarray(10, wcss[9])
    # p2 = np.asarray(p2)
    #
    # for i in range(0, 10):
    #     p3 = (i + 1, wcss[i])
    #     p3 = np.asarray(p3)
    #     #distances.append(p.distance_to_line(p1, p2))
    #     d = linalg.norm(np.cross(p2 - p1, p1 - p3)) / linalg.norm(p2 - p1)
    #     print d
    " End of testing code "

    # Generate K-means Clustering
    kmeans = KMeans(n_clusters=k, init="k-means++")
    kmeans = kmeans.fit(list_of_starting_points)
    labels = kmeans.predict(list_of_starting_points)

    # Divide the different starting points to their respectively clusters
    for i in range(len(list_of_starting_points)):
        list_of_clusters[labels[i]].append(list_of_starting_points[i])
    return list_of_clusters


def set_all_connections_points(list_of_buildings, height_map):
    for building in list_of_buildings:  # find the well
        if building.type_of_house == "well":
            well = building
            break

    for building in list_of_buildings:  # set connection points for all buildings
        if building.type_of_house == well:  # don't set connection point for well to begin with
            continue
        building.set_connection_point(well, height_map)
