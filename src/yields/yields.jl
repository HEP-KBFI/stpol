using ROOT, ROOTDataFrames, DataFrames
include("../analysis/df_extensions.jl");
include("../analysis/base.jl");
include("../fraction_fit/hists.jl");
using SingleTopBase
import SingleTopBase: FitResult, VARS

const SAMPLE = symbol(ARGS[1])
njets = 2;
ntags = 1;

files = ARGS[2:end]
println("opening $files")
chd1 = TreeDataFrame(files);
chd2 = TreeDataFrame(map(postfix_added, files));
chd = MultiColumnDataFrame(AbstractDataFrame[chd1, chd2]);
println("opened $(nrow(chd)) events")

X = chd1[[:hlt_mu, :hlt_ele, :n_signal_mu, :n_veto_mu, :n_signal_ele, :n_veto_ele, :njets, :ntags, :met, :mtw, :ljet_rms, :ljet_dr, :bjet_dr, :ljet_eta, :bjet_eta, :cos_theta_lj, :lepton_charge]];

qcdkey = :bdt_qcd
if :bdt_qcd_before_reproc in names(chd2)
    qcdkey = :bdt_qcd_before_reproc
end
Y = chd2[[:bdt_sig_bg, :bdt_sig_bg_top_13_001, qcdkey, :xsweight]];
X = hcat(X,Y);

mu = (X[:hlt_mu].==1) .* (X[:n_signal_mu].==1) .* (X[:n_signal_ele].==0) .* (X[:n_veto_mu].==0) .* (X[:n_veto_ele].==0);
nona!(mu);

ele = (X[:hlt_ele].==1) .* (X[:n_signal_ele].==1) .* (X[:n_signal_mu].==0) .* (X[:n_veto_mu].==0) .* (X[:n_veto_ele].==0);
nona!(ele);

totw = chd1[[:lepton_weight__id, :lepton_weight__trigger, :lepton_weight__iso, :b_weight, :top_weight, :pu_weight]];
totw[:wjets_ct_shape_weight] = chd2[:wjets_ct_shape_weight]
totw[:wjets_fl_yield_weight] = chd2[:wjets_fl_yield_weight]


for x in [
    :lepton_weight__iso, :top_weight,:lepton_weight__trigger, :lepton_weight__id, :pu_weight, :b_weight, :wjets_ct_shape_weight, :wjets_fl_yield_weight
    
    ]
    totw[x][isna(totw[x])] = 1.0
    totw[x][isnan(totw[x])] = 1.0
end

totw[:w_new] = totw[:lepton_weight__id] .* totw[:lepton_weight__iso] .* totw[:lepton_weight__trigger] .* totw[:pu_weight] .* totw[:top_weight] .* totw[:b_weight] .* totw[:wjets_ct_shape_weight] .* totw[:wjets_fl_yield_weight];

jet = X[:njets].==njets
nona!(jet)

tag = X[:ntags].==ntags
nona!(tag)
#
#rms = X[:ljet_rms] .< 0.025
#nona!(rms)
#
#dr = (X[:ljet_dr] .> 0.3) .* (X[:bjet_dr] .> 0.3);
#nona!(dr)
#
met = X[:met].>45
nona!(met)
mtw = X[:mtw].>50
nona!(met)

qcd_015 = X[qcdkey] .> -0.15
nona!(qcd_015)

qcd015 = X[qcdkey] .> 0.15
nona!(qcd015)

bdt = X[:bdt_sig_bg].>0.45
nona!(bdt)

bdt0 = X[:bdt_sig_bg].>0.
nona!(bdt0)

bdt06 = X[:bdt_sig_bg].>0.6
nona!(bdt06)
#
jet_eta = (abs(X[:ljet_eta]) .< 4.5) .* (abs(X[:bjet_eta]) .< 4.5)
nona!(jet_eta)
#
bdtold_mu = X[:bdt_sig_bg_top_13_001].>0.06
nona!(bdtold_mu)

bdtold_ele = X[:bdt_sig_bg_top_13_001].>0.13
nona!(bdtold_ele)

is_top = X[:lepton_charge] .== int32(1)
is_antitop = X[:lepton_charge] .== int32(-1)

cuts = {
    :mu=>{
        #:old => {dr, mu, jet, rms, tag, mtw, jet_eta, bdtold_mu},
        #:new => {mu, mu, jet, jet, tag, qcd_015, jet_eta, bdt},
        #:new => {mu, jet, tag, qcd_015, bdt0, bdt, bdt06},
        :new => {mu, jet, tag, qcd_015, bdt},
    },
    :ele=>{
        #:old => {dr, ele, jet, rms, tag, met, jet_eta, bdtold_ele},
        #:new => {ele, ele, jet, jet, tag, qcd015, jet_eta, bdt},
        #:new => {ele, jet, tag, qcd015, bdt0, bdt, bdt06},
        :new => {ele, jet, tag, qcd015, bdt},
    }
};

cuts = {
    :combined => {mu, mu, jet, tag, qcd_015, bdt},
    :top => {mu, is_top, jet, tag, qcd_015, bdt},
    :antitop => {mu, is_antitop, jet, tag, qcd_015, bdt}
}

x = X[ mu .* qcd_015 .* jet .* tag .* jet_eta .* bdt, :cos_theta_lj]
println("selected ", length(x), " cos_theta calculated for ", sum(!isna(x)))

function cutflow(A, weighted, weight)
    sel = first(A)
    v = Any[]
    w = Any[]
    for a in A
        sel = sel .* a
        nona!(sel)
        push!(v, sum(sel))
        push!(w, sum(
            X[sel, :xsweight] .*
            totw[sel, weight]
        ))
    end
    return {v,w}
end

function cutflow_data(A)
    sel = first(A)
    v = Int64[]
    for a in A
        sel = sel .* a
        sel[isna(sel)] = false
        push!(v, sum(sel))
    end
    return {v, v}
end


if SAMPLE==:data_mu || SAMPLE==:data_ele
    d = {
        #:mu=>{:new=>cutflow_data(cuts[:mu][:new]), :old=>cutflow_data(cuts[:mu][:old])},
        #:ele=>{:new=>cutflow_data(cuts[:ele][:new]), :old=>cutflow_data(cuts[:ele][:old])}
        #:mu=>{:new=>cutflow_data(cuts[:mu][:new])},
        #:ele=>{:new=>cutflow_data(cuts[:ele][:new])}
        :combined=>{:new=>cutflow_data(cuts[:combined])},
        :top=>{:new=>cutflow_data(cuts[:top])},
        :antitop=>{:new=>cutflow_data(cuts[:antitop])}
    }
else
    d = {
        #:mu=>{:new=>cutflow(cuts[:mu][:new], true, :w_new), :old=>cutflow(cuts[:mu][:old], true, :w_new)},
        #:ele=>{:new=>cutflow(cuts[:ele][:new], true, :w_new), :old=>cutflow(cuts[:ele][:old], true, :w_new)}
        #:mu=>{:new=>cutflow(cuts[:mu][:new], true, :w_new)},
        #:ele=>{:new=>cutflow(cuts[:ele][:new], true, :w_new)}
        :combined=>{:new=>cutflow(cuts[:combined], true, :w_new)},
        :top=>{:new=>cutflow(cuts[:top], true, :w_new)},
        :antitop=>{:new=>cutflow(cuts[:antitop], true, :w_new)}
    }
end
println(d)

df = similar(
    DataFrame(
        flavour=Symbol[],
        sample=Symbol[],
        #dr=Int64[],
        lepton=Int64[],
        charge=Int64[],
        jet=Int64[],
        #rms=Int64[],
        tag=Int64[],
        qcd=Int64[],
        #jet_eta=Int64[],
        #bdt=Int64[],
        #bdt_w0=Int64[],
        bdt_w=Int64[],
        #bdt_w06=Int64[],
        fit=Int64[],
    ), 3#4
);

j = 0
for lep in [:combined, :top, :antitop]
    #for cut in [:old, :new]
    for cut in [:new]
        println("J ",j)
        j += 1
        df[j, :flavour] = lep
        df[j, :sample] = SAMPLE
        if SAMPLE in [:data_mu, :data_ele]
            l = 1.0
        else
            #l = Reweight.lumis[lep]
            l = Reweight.lumis[:mu]
        end
        for i=1:6
            println(i)
            df[j, i + 2] = int(round(l * float(d[lep][cut][2][i])) )
        end
        #df[j, :bdt_w] = int(round(l * float(d[lep][cut][2][6])))
        #df[j, :bdt_w] = int(round(l * float(d[lep][cut][2][5])))
        if SAMPLE == :tchan
            sf = FITRESULTS[lep][:beta_signal]
        elseif SAMPLE in [:wjets, :gjets, :dyjets, :diboson]
            sf = FITRESULTS[lep][:wzjets]
        elseif SAMPLE in [:schan, :twchan, :ttjets]
            sf = FITRESULTS[lep][:ttjets]
        else
            sf = 1.0
        end
        println("FFF")
        df[j, :fit] = round(l * float(d[lep][cut][2][6]) * sf)|>int
        println("III")
        #df[j, 7] = round(df[j, 6] * sf)|>int
    end
end

writetable("../../results/yields/$(SAMPLE)_$(njets)j_$(ntags)t.csv", df)
println(df)
