import matplotlib.pyplot as plt
import math
import random
import numpy as np
import csv

np.set_printoptions(threshold=50)
np.random.seed(42)

class KNN:

    def __init__(self, K):
        self.K = K
        self.movies = {}

    def addToDictionary(self, userid, movie, rating):
        if movie in self.movies:
            self.movies[movie][userid] = rating
        else:
            self.movies[movie] = {userid : rating}

    def generateInitCentroids(self, my_data):
        '''Generate random list of centroids with userid and corresponding ratings'''
        centroids = []
        for c in range(self.K):
            centroid = {}
            for entry in my_data:
                centroid[entry[0]] = random.randint(0,5)
                centroids.append(centroid)
        return centroids

    def calculateDist(self, p1, p2):
        distance = 0
        for userid, rating in p1.iteritems():
            if userid in p2:
                distance += (p2[userid] - rating)**2
        return math.sqrt(distance)

    def closestCentroid(self, vector, centroids):
        '''Find closest centroid to data point'''
        min_dist = float('inf')
        for centroid in centroids:
            vec_dist = self.calculateDist(vector, centroid)
            if vec_dist < min_dist:
                min_dist = vec_dist
                closest = centroid
        return closest

    def cluster(self, centroids):
        clusters = []
        for c in range(self.K):
            clusters.append({})
        for movie, user_rating in self.movies.iteritems():
            min_dist = float('inf')
            for c in range(self.K):
                dist = self.calculateDist(user_rating, centroids[c])
                if dist < min_dist:
                    min_dist = dist
                    closest = c
            clusters[closest][movie] = user_rating
        return clusters

    def recalculateCentroids(self, clusters, centroids):
        '''Recalculate centroid locations based on new movie clusters'''
        for ind in range(len(clusters)):
            for userid in centroids[ind]:
                distance = 0
                count = 1
                for movie in clusters[ind]:
                    if userid in clusters[ind][movie]:
                        distance += clusters[ind][movie][userid]
                        count += 1
                    centroids[ind][userid] = distance/count
        return centroids

    def compareCentroids(self, _old, _new):
        '''Get change in centroid versions'''
        #dtype = dict(names = names, formats=formats)
        for i in range(len(_old)):
            for users, ratings in _old[i].iteritems():
                old = np.append(_old,[users, ratings])
                print float(float(i)/len(_old))
            #old = np.fromiter(_old[i].iteritems(), dtype = dtype, count=len(_old))
        #old = np.array([_old.iteritems()])
        #for i in range(len(_old)):
            #for users, ratings in _old[i].iteritems():
        #new = np.array([_new.iteritems()])
        #for i in range(len(_new)):
            for new_users, new_ratings in _new[i].iteritems():
                new = np.append(_new,[new_users, new_ratings])
                print float(float(i)/len(_old))
        print old
        print new
        compare = abs(old - new)
        print compare
        c = np.mean(compare)
        print c
        return c

    def iterate(self, my_data):
        '''Generate initial centroids, then continue reclustering and recalculating centroids until there is
        little to no further change in centroids'''
        centroids = self.generateInitCentroids(my_data)
        # update cluster content and centroid locations
        finished = False
        while finished == False:
            clusters = self.cluster(centroids)
            print "New cluster"
            print clusters[0]
            new_centroids = self.recalculateCentroids(clusters, centroids)
            print "New centroid"
            print new_centroids[0]
            # compare old centroids to recalculated centroids to see if they are still changing
            c = self.compareCentroids(centroids, new_centroids)
            "Compare value"
            print c
            if c < 0.0001:
               finished = True
            else: 
                centroids = new_centroids
        return clusters

def movieKey(movie_names, clusters):
    '''Match movie keys in each cluster to respective movie titles'''
    movie_key = {}
    for entry in movie_names:
        movie_key[float(entry[0])] = entry[1]
    for cluster in clusters:
        print "------CLUSTER-------"
        for movie in cluster:
            print movie_key[movie]

def loadDataset(my_KNN, dataset="u.data", item_file = "u.item"):
    my_data = np.genfromtxt(dataset, skip_footer = 99500)
    movie_names = []
    with open(item_file, 'rb') as f:
        titlereader = csv.reader(f, delimiter='|')
        for entry in titlereader:
            movie_names.append([entry[0], entry[1]])
    # Format of input data:
    # userID   movieID     rating      timestamp
    for entry in my_data:
        my_KNN.addToDictionary(entry[0], entry[1], entry[2])
    return my_data, movie_names

myKNN = KNN(6)
my_data, movie_names = loadDataset(myKNN)
clusters = myKNN.iterate(my_data)
movieKey(movie_names, clusters)




#
