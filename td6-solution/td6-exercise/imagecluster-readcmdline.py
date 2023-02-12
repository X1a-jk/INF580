####################### MAIN #######################

## read command line
if len(sys.argv) < 3:
    print("syntax is" + sys.argv[0] + "dir nclust")
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

