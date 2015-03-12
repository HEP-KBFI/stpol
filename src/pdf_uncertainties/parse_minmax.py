
f = open('minmax', 'r')
maxstuff = {}
minstuff = {}
maxstuff["x"] = 0.
minstuff["x"] = 0.
maxstuff["id"] = 0
minstuff["id"] = 0
maxstuff["scale"] = 170.
minstuff["scale"] = 170.
for line in f:
    stuff = line.split(" ")
    maxscale = float(stuff[1])
    minscale = float(stuff[2])
    maxid = int(stuff[3])
    minid = int(stuff[4])
    maxx = float(stuff[5])
    minx = float(stuff[6])
    maxstuff["scale"] = max(maxstuff["scale"], maxscale)
    minstuff["scale"] = min(minstuff["scale"], minscale)
    maxstuff["id"] = max(maxstuff["id"], maxid)
    minstuff["id"] = min(minstuff["id"], minid)
    maxstuff["x"] = max(maxstuff["x"], maxx)
    minstuff["x"] = min(minstuff["x"], minx)
    print minstuff["id"], minid, min(minstuff["id"], minid)
print "max", maxstuff
print "min", minstuff
