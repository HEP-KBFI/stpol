include("../histo.jl")
using Hist
using Base.Test

h = Histogram([1],[1],[0,1])
@test integral(h)==1

hs=h+h
@test hs==Histogram([2],[2],[0,1])

hs=sum([h,h])
@test hs==h+h

hs=sum([h])
@test hs==h

#show(h)
#df = todf(h)
#show(df)
#h1 = fromdf(df)
#show(h1)

@test fromdf(todf(h)) == h