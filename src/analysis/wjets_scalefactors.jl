#calculates cos-theta dependent scale factors for W+jets in 2J0T
#run as $julia wjets_scalefactors.jl wjets.txt
include("../analysis/base.jl");
import SingleTopBase.FitResult
include("../fraction_fit/hists.jl")

using ROOT, ROOTDataFrames

using PyCall
#pygui(:wx)
#using PyPlot

include("hplot.jl")

#fns = [
#    "/hdfs/local/joosep/stpol/skims/step3/csvt/Jul4_newsyst_newvars_metshift/iso/nominal/WJets_sherpa/4382/output.root",
#    "/hdfs/local/joosep/stpol/skims/step3/csvt/Jul4_newsyst_newvars_metshift/iso/nominal/W3Jets_exclusive/1109/output.root"
#]

#read input root files
fns = split(readall(ARGS[1]))

#create ROOT TTree
df = TreeDataFrame(fns)
df2 = TreeDataFrame(map(x->"$x.added", fns))

#create intermediate dataframe buffer
d = similar(DataFrame(
    bdt=Float64[], ct=Float64[], sample=Symbol[],
    jet_cls_1=Symbol[], jet_cls_2=Symbol[],
    weight=Float64[],
), length(df));

# t = readtable("$BASE/src/skim/hmap.csv");
# hmap[:from] = {x[2]=>x[1] for x in eachrow(t)};
# hmap[:to] = {x[1]=>x[2] for x in eachrow(t)};

#these are the samples of interest that we consider
const samps = [hmap[:to]["wjets_sherpa"], hmap[:to]["wjets"]];

include("$BASE/src/skim/jet_cls.jl")

#enable_branches(df, [
#    "sample*", "iso*", "jet_cls*", "njets*",
#    "ntags*", "jet_cls*", "cos_theta_lj*",
#    "xsweight*", "gen_weight*", "pu_weight*"])

#loop- over input TTrees
tic()
n = 0
for i=1:length(df)
    load_row(df, i)
    load_row(df2, i)

    s = df[i, :sample, true];
    isna(s) && continue
    #select events which come from the samples of interest
    s in samps || continue
    
    iso = hmap[:from][df[i, :isolation]];
    #select events which contain one isolated lepton
    iso == "iso" || continue
    
    nj, nt = df[i, :njets], df[i, :ntags]

    #select 2J, 0T
    nj == 2 || continue
    nt == 0 || continue
    
    #select events where cos theta is calculated
    isna(df[i, :cos_theta_lj]) && continue
    #((df[i, :n_signal_mu] == 1 && df2[i, :bdt_qcd] > -0.15) || (df[i, :n_signal_ele] == 1 && df2[i, :bdt_qcd] > 0.15)) || continue 
    #event successfully selected
    n += 1
    d[n, :sample] = symbol(hmap[:from][s]);
    d[n, :ct] = df[i, :cos_theta_lj]
    d[n, :jet_cls_1] = jet_cls_from_number(df[i, :jet_cls])
    d[n, :jet_cls_2] = jet_cls_heavy_light(d[n, :jet_cls_1])
    
    d[n, :weight] = df2[i, :xsweight] * df[i, :gen_weight] * df[i,:b_weight] * df[i, :pu_weight] * df[i, :lepton_weight__id] * df[i, :lepton_weight__iso] * df[i, :lepton_weight__trigger] 

    n%1000000 == 0 && println(n)
end
toc()

#trim dataframe to size
d = d[1:n, :];

#bitmask with sherpa events
const SH = d[:sample] .== :wjets_sherpa;

import SingleTopBase: makehist_1d, VARS

#store costheta histograms here
hd = Dict()
yields = Dict()

for k in jet_classifications
    hd[k] = Dict()
	yields[k] = Dict()
    c = d[:jet_cls_1] .== k

    #project sherpa cos-theta distribution
    hd[k][:sherpa] = makehist_1d(sub(d, SH & c), :ct, infb(linspace(-1, 1, 30)), r -> r[:weight]);
    
    #project madgraph cos-theta distribution
    hd[k][:madgraph] = makehist_1d(sub(d, !SH & c), :ct, infb(linspace(-1, 1, 30)), r -> r[:weight]);


	yields[k][:sherpa] = makehist_1d(sub(d, SH & c), :ct, infb(linspace(-1, 1, 1)), r -> r[:weight]);
    #project madgraph cos-theta distribution
    yields[k][:madgraph] = makehist_1d(sub(d, !SH & c), :ct, infb(linspace(-1, 1, 1)), r -> r[:weight]);
end

println("III")
println(yields[:XX][:madgraph])
println(yields[:XX][:sherpa])
ratios_sherpa = {x => yields[x][:madgraph] / yields[x][:sherpa] for x in jet_classifications};
println(ratios_sherpa[:XX])
#save ratios to csv
for (k, v) in ratios_sherpa
    p = "$BASE/results/wjets_shape_weight_feb25/sherpa_$k.csv"
    mkpath(dirname(p))
    writetable(p, htodf(v))
end
      
fig = figure(figsize=(15, 15))
n = 1
for x in jet_classifications
    ax = subplot(3, 3, n)
    eplot(ax, normed(hd[x][:sherpa]), label="sherpa", drawstyle="steps-mid")
    eplot(ax, normed(hd[x][:madgraph]), label="madgraph", drawstyle="steps-mid")
    legend()
    ax[:set_ylim](bottom=0)
    ax[:set_ylim](top=0.08)
    grid(true, which="both")
    title("$x")
    xlabel(VARS[:cos_theta_lj])
    ylabel("normalized event yield")
    n += 1
end
suptitle("W+jets angular modelling, split by jet parton flavour in 2J0T", y=0.95)
savefig("$BASE/results/wjets_shape_weight_feb25/costheta.pdf")
close()


#calculate ratios between normalized distributions (shapes)
ratios = {x => normed(hd[x][:sherpa]) / normed(hd[x][:madgraph]) for x in jet_classifications};

#save ratios to csv
for (k, v) in ratios
    p = "$BASE/results/wjets_shape_weight_feb25/$k.csv"
    mkpath(dirname(p))
    writetable(p, htodf(v))
end

fig = figure(figsize=(15, 15))
n = 1
for x in jet_classifications
    ax = subplot(3, 3, n)
    z = ratios[x]
    z = rebin(z, 2) / 2
    eplot(ax, ratios[x])
    ax[:set_ylim](bottom=0.0)
    ax[:set_ylim](top=3.0)
    grid(true, which="both")
    title("$x")
    xlabel(VARS[:cos_theta_lj])
    ylabel("ratio sherpa / madgraph")
    #legend()
    n += 1
end
savefig("$BASE/results/wjets_shape_weight_feb25/ratios.pdf")
    close()



