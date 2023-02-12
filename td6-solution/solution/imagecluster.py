#!/usr/bin/env python3 -W ignore

## cluster images (rescale first)

import sys
import os
import time
import math
from math import sqrt
import numpy as np
from blis.py import einsum, gemv, gemm
from PIL import Image
import glob
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import adjusted_mutual_info_score

############# configurable arguments ###############
myZero = 1e-10
image_exts = [".jpg",".gif",".png"]
thumbnailsize = (100,100)
thumbnaildepth = 3
jlleps = 0.15
jllC = 2.0

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
        print("  " + str(c+1) + ":",)
        for j in range(n):
            if clust.labels_[j] == c:
                print(filenames[j],)
        print()

# count non-empty clusters
def nonemptyclust(clust):
    nclust = len(set(list(clust.labels_)))
    clustering = {}
    for c in range(nclust):
        cluster = [j for j in range(n) if clust.labels_[j] == c]
        if len(cluster) > 0:
            clustering[c] = cluster
    return clustering

####################### MAIN #######################

## read command line
if len(sys.argv) < 3:
    print("syntax is " + sys.argv[0] + " dir nclust")
    print("  dir contains image files")
    print("  nclust is number of clusters")
    sys.exit(1)

dir = sys.argv[1]
nclust = int(sys.argv[2])
if nclust < 2:
    sys.exit('nclust must be at least 2')

if len(sys.argv) >= 4:
    m = int(sys.argv[2])
    n = int(sys.argv[3])
    thumbnailsize = (m,n)

m = thumbnailsize[0]*thumbnailsize[1]*thumbnaildepth

## read all image files in dir, scale them, put them into a data matrix
images = []
filenames = []
X = []
n = 0
print(sys.argv[0] + ": reading " + dir + " ...",)
sys.stdout.flush()
t0 = time.time()
id2fn = dict()
id = 0
for ext in image_exts:
    for filename in glob.glob(dir + '/*' + ext):
        im = Image.open(filename)
        im = im.resize(thumbnailsize)
        im = im.convert("RGB")
        images.append(im)
        filenames.append(os.path.basename(filename))
        ima = np.reshape(np.array(im), (m))
        id2fn[id] = os.path.basename(filename)
        id += 1
        X.append(ima)
        n += 1
X = np.array(X)
t1 = time.time()
print("took " + outstr(t1-t0,2) + "s")

## cluster the data matrix
print(sys.argv[0] + ": " + str(nclust) + "-means clustering ...",)
sys.stdout.flush()
t2 = time.time()
clust = KMeans(n_clusters=nclust).fit(X)
t3 = time.time()
#outclustering(clust, filenames)
print("took " + outstr(t3-t2,2) + "s")

## projecting the data matrix
print(sys.argv[0] + ": projecting data matrix ...",)
sys.stdout.flush()
t4 = time.time()
k = int(round(jllC*(1/(jlleps**2))*math.log(n)))
T = (1/sqrt(k))*normalmatrix(m,k)
multmethod = "blis.gemm"
try:
    XT = gemm(X,T)
except:
    XT = np.dot(X,T)
    multmethod = "numpy.dot"
t5 = time.time()
print("took " + outstr(t5-t4,2) + "s")
print(sys.argv[0] + ": projected from " + str(m) + " to " + str(k) + " dims")

## projected k-means clustering
print(sys.argv[0] + ": " + str(nclust) + "-means proj. clustering ...",)
sys.stdout.flush()
projclust = KMeans(n_clusters=nclust).fit(XT)
t6 = time.time()
#outclustering(projclust, filenames)
print("took " + outstr(t6-t5,2) + "s")
print(sys.argv[0] + ": used " + multmethod + " for matrix dot product")

## print clust and projclust
#print(clust.labels_)
#print(projclust.labels_)
cl = dict()
cln = dict()
prjcl = dict()
prjcln = dict()
for c in range(nclust):
    cl[c] = []
    cln[c] = []
    prjcl[c] = []
    prjcln[c] = []
for id,lb in enumerate(clust.labels_):
    cl[lb].append(id)
    cln[lb].append(id2fn[id])
for id,lb in enumerate(projclust.labels_):
    prjcl[lb].append(id)
    prjcln[lb].append(id2fn[id])
print("mapping indices->files:")
for i in id2fn:
    print("  ", i, id2fn[i])
print("org:", cl)
print("prj:", prjcl)

## output times
print(sys.argv[0] + ": clust took " + outstr(t3-t2,2) + "s; proj+clust took " + outstr(t6-t4,2) + "s")

## evaluate clustering similarity
q = adjusted_mutual_info_score(clust.labels_, projclust.labels_)
print(sys.argv[0] + ": adj mutual info = " + outstr(q,3) + " (0=different, 1=equal)")
clustering = nonemptyclust(clust)
print(sys.argv[0] + ": " + str(n) + " images clustered into " + str(len(clustering.keys())) + " non-empty clusters")

