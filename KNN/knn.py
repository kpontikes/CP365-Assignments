import matplotlib.pyplot as plt
import math
import random
import numpy as np
import csv

np.set_printoptions(threshold=50)
np.random.seed(42)

def euclideanDistance(x, y):
    s = 0.0
    for i in range(len(x)):
        s += (x[i] - y[i]) ** 2
    return math.sqrt(s)

class KNN:

    def __init__(self, K):
        self.K = K
        self.movies = {}

    def addToDictionary(self, userid, movie, rating):
        # userID   movieID     rating      timestamp
        if movie in self.movies:
            self.movies[movie][userid] = rating
        else:
            self.movies[movie] = {userid : rating}

    def generateInitCentroids(self, my_data):
        #generate random list of centroids with userid and corresponding ratings
        centroids = []
        for c in range(self.K):
            #centroids.append({})
            centroid = {}
            for entry in my_data:
                #centroids[c] = {entry[0] : random.randint(0,5)}
                centroid[entry[0]] = random.randint(0,5)
                centroids.append(centroid)
                #centroids[entry[1]][entry[0]] = rating
                #centroid[1] = {entry[0] : entry[2]}
                #centroid[c][entry[0]] = random.randint(0,5)
                #centroid[entry[0]] = random.randint(0,5)
                #centroids.append(centroid)
        #print centroids
        #print len(centroids)
        return centroids

    def calculateCentroidDist(self, p1, p2):
        distance = 0
        #print p1
        for userid, rating in p1.iteritems():
            if userid in p2:
                distance += (p2[userid] - rating)**2
        return math.sqrt(distance)

    def closestCentroid(self, vector, centroids):
        min_dist = float('inf')
        #closest = centroids[0]
        for centroid in centroids:
            vec_dist = self.calculateCentroidDist(vector, centroid)
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
                dist = self.calculateCentroidDist(user_rating, centroids[c])
                if dist < min_dist:
                    min_dist = dist
                    closest = c
            clusters[closest][movie] = user_rating
        return clusters

    def recalculateCentroids(self, clusters, centroids):
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

    def iterate(self, my_data):
        centroids = self.generateInitCentroids(my_data)
        #print centroids[0:2]
        finished = False
        while finished == False:
            clusters = self.cluster(centroids)
            old = np.array([])
            for i in range(len(centroids)):
                for users, ratings in centroids[i].iteritems():
                    old = np.append(old,[users, ratings])
                    #old = np.append(old, ratings)
            #print old
            new_centroids = self.recalculateCentroids(clusters, centroids)
            #print "new centroids"
            #print new_centroids[0:2]
            new = np.array([])
            for i in range(len(new_centroids)):
                for new_users, new_ratings in new_centroids[i].iteritems():
                    new = np.append(new, [new_users, new_ratings])
                    #new = np.append(new, new_ratings)
            #print new
            compare = abs(old - new)
            #print compare
            c = np.mean(compare)
            #print c
            if c < 0.0001:
                finished = True
            else: 
                centroids = new_centroids
        return clusters

def movieKey(movie_names, clusters):
    movie_key = {}
    for entry in movie_names:
        movie_key[float(entry[0])] = entry[1]
    #print movie_key
    #for i in range(len(clusters)):
    for cluster in clusters:
        print "CLUSTER"
        for movie in cluster:
            #movie_dict = {k:movie_key[k] for k in cluster if k in movie_key}
            #print movie
            print movie_key[movie]

def loadDataset(my_KNN, dataset="u.data", item_file = "u.item"):
    my_data = np.genfromtxt(dataset, skip_footer = 99000)
    #movie_names = np.genfromtxt(item_file, delimiter='|')
    movie_names = []
    with open(item_file, 'rb') as f:
        titlereader = csv.reader(f, delimiter='|')
        for entry in titlereader:
            movie_names.append([entry[0], entry[1]])
    # userID   movieID     rating      timestamp
    for entry in my_data:
        my_KNN.addToDictionary(entry[0], entry[1], entry[2])
    return my_data, movie_names

myKNN = KNN(10)
my_data, movie_names = loadDataset(myKNN)
#print myKNN.movies
#my_centroids = myKNN.generateInitCentroids(my_data)
#my_clusters = myKNN.cluster(my_centroids)
#update_centroids = myKNN.recalculateCentroids(my_clusters, my_centroids)
clusters = myKNN.iterate(my_data)
#print clusters
movieKey(movie_names, clusters)




#
