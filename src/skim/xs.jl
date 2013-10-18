using DataFrames

function sample_type(fn, prefix="file:/hdfs/cms/store/user")
    r = Regex("$prefix/(.*)/(.*)/(.*)/(.*)/(.*)/output_(.*).root")
    m = match(r, fn)
   
    if m==nothing
        tag = :unknown
        syst = :unknown
        samp = :unknown
        iso = :unknown
        
        cls = data_cls(fn)
        if cls != nothing
            samp = cls[2]
            iso = cls[1]
        end
    else
        tag = m.captures[2]
        iso = m.captures[3]

        syst = m.captures[4]
        samp = m.captures[5]
    end
    return {:tag => tag, :iso => iso, :systematic => syst, :sample => samp}
end

function data_cls(fn)
    if contains(fn, "/iso/SingleMu")
        return (:iso, :SingleMu)
    elseif contains(fn, "/antiiso/SingleMu")
        return (:antiiso, :SingleMu)
    elseif contains(fn, "/iso/SingleEle")
        return (:iso, :SingleEle)
    elseif contains(fn, "/antiiso/SingleEle")
        return (:antiiso, :SingleMu)
    end 
    return nothing
end

fpath = joinpath(dirname(Base.source_path()), "cross_sections.txt")
df = readtable(fpath, allowcomments=true)
cross_sections = Dict{String, Float64}()
for i=1:nrow(df)
    cross_sections[df[i, 1]] = df[i, 2]
end
