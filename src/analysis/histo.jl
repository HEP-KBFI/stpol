module Hist

using DataFrames

import Base.+, Base.-, Base.*, Base./
immutable Histogram
    bin_entries::Vector{Float64} #n values
    bin_contents::Vector{Float64} #n values
    bin_edges::Vector{Float64} #n+1 values, lower edges of all bins + upper edge of last bin

    function Histogram(entries, contents, edges)
        @assert length(entries)==length(contents) "entries and contents vector must be of equal length"
        if (length(entries)!=length(edges)-1)
            error("must specify n+1 edges, $(length(entries))!=$(length(edges)-1)")
        end
        @assert all(entries .>= 0.0) "number of entries must be >= 0"
        new(entries, contents, edges)
    end
end

function Histogram(n::Integer, low::Number, high::Number)
    bins = linspace(low, high, n)
    unshift!(bins, -inf(Float64))
    push!(bins, inf(Float64))
    n_contents = size(bins,1)-1
    return Histogram(
        zeros(Float64, (n_contents, )),
        zeros(Float64, (n_contents, )),
        bins
    )
end

Histogram(h::Histogram) = Histogram(h.bin_entries, h.bin_contents, h.bin_edges)

function errors(h::Histogram)
    return h.bin_contents ./ sqrt(h.bin_entries)
end

function findbin(h::Histogram, v::Real)
    v < h.bin_edges[1] && return -Inf
    v >= h.bin_edges[length(h.bin_edges)] && return +Inf

    idx = searchsorted(h.bin_edges, v)
    low = idx.start-1
    return low
end

function hfill!(h::Histogram, v::Real, w::Real=1.0)
    low = findbin(h, v)
    abs(low) == Inf && error("over- or underflow for $v")

    h.bin_entries[low] += 1
    h.bin_contents[low] += w
    return sum(h.bin_contents)
end

function hfill!(h::Histogram, v::NAtype, w::Union(Real, NAtype))
    h.bin_entries[1] += 1
    h.bin_contents[1] += 1
    return sum(h.bin_contents)
end

function +(h1::Histogram, h2::Histogram)
    @assert h1.bin_edges == h2.bin_edges
    h = Histogram(h1.bin_entries + h2.bin_entries, h1.bin_contents+h2.bin_contents, h1.bin_edges)
    return h
end

-(h1::Histogram, h2::Histogram) = h1 + (-1.0 * h2)

function *{T <: Real}(h1::Histogram, x::T)
    return Histogram(h1.bin_entries, h1.bin_contents * x, h1.bin_edges)
end

function *{T <: Real}(x::T, h1::Histogram)
    return h1 * x
end


function /{T <: Real}(h1::Histogram, x::T)
    return h1 * (1.0/x)
end

function /(h1::Histogram, h2::Histogram)
    #warn("ratio plot errors are currently incorrect")
    @assert(h1.bin_edges == h2.bin_edges, "bin edges must be the same for both histograms")
    div = h1.bin_contents ./ h2.bin_contents
    #div = Float64[d >= 0.0 ? d : 0.0 for d in div]

    ent = (h1.bin_entries ./ h1.bin_contents) .^ 2 + (h2.bin_entries ./ h2.bin_contents) .^ 2
    #ent = Float64[x >= 0.0 ? x : 0.0 for x in ent]

    return Histogram(
        ent,
        div,
        h1.bin_edges
    )
end

function integral(h::Histogram)
    return sum(h.bin_contents)
end

function integral(h::Histogram, x1::Real, x2::Real)
    if !(x1 in h.bin_edges) || !(x2 in h.bin_edges)
        warn("integration will be inexact due to binning")
    end
    a = searchsorted(h.bin_edges, x1).start
    b = searchsorted(h.bin_edges, x2).start
    return sum(h.bin_contents[a:b])
end

#returns the low edges of a list of histogram edges
lowedge(arr) = arr[1:length(arr)-1];
widths(arr) = [arr[i+1]-arr[i] for i=1:length(arr)-1]

function normed{T <: Histogram}(h::T)
    i = integral(h)
    return i > 0 ? h/i : error("histogram integral was $i")
end

#conversion to dataframe
#todf(h::Histogram) = DataFrame(bin_edges=h.bin_edges, bin_contents=h.bin_contents, bin_entries=h.bin_entries)

#assumes df columns are entries, contents, edges
#length(entries) = length(contents) = length(edges) - 1, edges are lower, lower, lower, ..., upper
function fromdf(df::DataFrame; entries=:entries)
    ent = df[1].data[1:nrow(df)-1]
    cont = df[2].data[1:nrow(df)-1]
    if entries == :poissonerrors
        ent = (cont ./ ent ) .^ 2
        ent = Float64[x > 0 ? x : 0 for x in ent]
    elseif entries == :entries
        ent = ent
    else
        error("unknown value for keyword :entries=>$(entries)")
    end

    Histogram(
        ent, #entries
        cont, #contents
        df[3].data #edges
    )
end

flatten(h) = reshape(h, prod(size(h)))

export Histogram, hfill!, integral, normed, errors, findbin
export +, -, *, /
export todf, fromdf
export flatten

end #module

