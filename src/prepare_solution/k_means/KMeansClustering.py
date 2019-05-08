from sklearn.cluster import KMeans


def starting_points(amount_of_clusters, list_of_buildings):
    list_of_starting_points = list()
    for building in list_of_buildings:
        coords_for_building = building.path_connection_point

        list_of_starting_points.append([coords_for_building[0], coords_for_building[1], coords_for_building[2]])
    list_of_centroids = k_means_clustering(amount_of_clusters, list_of_starting_points)
    return list_of_centroids

def k_means_clustering(amount_of_clusters, list_of_starting_points):
    list_of_centroids = list()
    k = amount_of_clusters
    list_of_clusters = [[] for x in xrange(k)] #Will create k lists in a list
    kmeans = KMeans(n_clusters=k, init="k-means++")
    kmeans = kmeans.fit(list_of_starting_points)
    labels = kmeans.predict(list_of_starting_points)
    # centroids = kmeans.cluster_centers_
    # for centroid in centroids:
    #     list_of_centroids.append([int(i) for i in centroid])
    #     #print centroids
    for i in range(len(list_of_starting_points)):
        list_of_clusters[labels[i]].append(list_of_starting_points[i])
    return list_of_clusters


def points_to_buildings(list_of_clusters, list_of_buildings):

    building_clusters = [[] for x in xrange(len(list_of_clusters))]  # Will create k lists in a list

    for cluster in xrange(0, len(list_of_clusters)):
        for point in list_of_clusters[cluster]:
            point_tuple = (point[0], point[1], point[2])
            for building in list_of_buildings:
                if point_tuple == building.path_connection_point:
                    building_clusters[cluster].append(building)
                    break

    return goal, building_clusters
