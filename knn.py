import matplotlib.pyplot as plt
import math
import random
import numpy as np

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
        
    #def sortDistances(self, X, clusters):
     #   distances = []
     #   ind = 0
     #   for vector in X:
     #       for centroid in clusters:
     #           distances.append((euclideanDistance(vector, centroid), y[ind]))
     #           ind += 1

        #distances.sort()
        #print distances

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
        #print clusters
        for c in range(self.K):
            clusters.append({})
        #print clusters
        for movie, user_rating in self.movies.iteritems():
            min_dist = float('inf')
            for c in range(self.K):
                dist = self.calculateCentroidDist(user_rating, centroids[c])
                if dist < min_dist:
                    min_dist = dist
                    closest = c
            clusters[closest][movie] = user_rating
        #print clusters
        return clusters

    def recalculateCentroids(self, clusters, centroids):
        for ind in range(len(clusters)):
            for userid in centroids[ind]:
                distance = 0
                count = 1
                for movie in clusters[ind]:
                    #print movie
                    if userid in clusters[ind][movie]:
                        #print clusters[ind][movie][userid]
                        distance += clusters[ind][movie][userid]
                        count += 1
                    centroids[ind][userid] = distance/count
        return centroids

    def iterate(self, my_data):
        centroids = self.generateInitCentroids(my_data)
        #print "centroids"
        print centroids[0:2]
        
        #print clusters
        #new_centroids = []
        c = 0
        finished = False
        while finished == False:
            clusters = self.cluster(centroids)
            old = np.array([])
            for i in range(len(centroids)):
                for users, ratings in centroids[i].iteritems():
                    #old = np.append(old,[users, ratings])
                    old = np.append(old, ratings)
            print old
            new_centroids = self.recalculateCentroids(clusters, centroids)
            print "new centroids"
            print new_centroids[0:2]
            
            new = np.array([])

            for i in range(len(new_centroids)):
                for new_users, new_ratings in new_centroids[i].iteritems():
                    #new = np.append(new, [new_users, new_ratings])
                    new = np.append(new, new_ratings)
            print new
            compare = abs(old - new)
            print compare
            c = np.mean(compare)
            print c
            if c < 0.0001:
                finished = True
            else: 
                centroids = new_centroids
            #C = [a - b for a, b in zip(A, B)]
            #print C
            #if C < 1:
                #finished = True
            #else:
               # centroids = new_centroids
        #return centroids

def loadDataset(my_KNN, dataset="u.data", movie_file = "u.item"):
    #my_data = np.genfromtxt(dataset, delimiter=' ', skip_header=1)
    my_data = np.genfromtxt(dataset, skip_footer = 99500)
    movie_data = np.genfromtxt(movie_file, delimiter='|', skip_header=1)
    # userID   movieID     rating      timestamp
    #userID = my_data[:, 0]
    #movieID = my_data[:, 1]
    #rating = my_data[:, 2]
    #movie_names = movie_data[:, [0,1]]
    #print my_data
    for entry in my_data:
        my_KNN.addToDictionary(entry[0],entry[1],entry[2])
    return my_data

#userID, movieID, rating, movie_names, my_data = loadDataset()
myKNN = KNN(100)
my_data = loadDataset(myKNN)
#print myKNN.movies
#my_centroids = myKNN.generateInitCentroids(my_data)
#my_clusters = myKNN.cluster(my_centroids)
#update_centroids = myKNN.recalculateCentroids(my_clusters, my_centroids)
myKNN.iterate(my_data)
#print centroids
#print update_centroids
#myKNN.addDataToDictionary(userID, movieID, rating, my_data)
#myKNN.generateInitClusters()
#myKNN.calculateDistances()
#print userID



#
