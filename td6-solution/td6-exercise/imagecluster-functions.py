#################### FUNCTIONS #####################

# round and output a number as part of a string
def outstr(x,d):
    return str(round(x,d))

# generate a componentwise Normal(0,1) matrix
def normalmatrix(m, n):
    return np.random.normal([0],[[1]],(m,n))

# generate a componentwise Uniform(0,1) matrix
def uniformmatrix(m, n):
    return np.random.rand(m,n)

# output a clustering on screen
def outclustering(clust, filenames):
    nclust = len(set(list(clust.labels_)))
    for c in range(nclust):
        print "  " + str(c+1) + ":",
        for j in range(n):
            if clust.labels_[j] == c:
                print filenames[j],
        print

# count non-empty clusters
def nonemptyclust(clust):
    nclust = len(set(list(clust.labels_)))
    clustering = {}
    for c in range(nclust):
        cluster = [j for j in range(n) if clust.labels_[j] == c]
        if len(cluster) > 0:
            clustering[c] = cluster
    return clustering
