include("../analysis/base.jl")
using SingleTopBase, ROOT, ROOTHistograms

s = convert(ASCIIString, ARGS[1])
yn = convert(ASCIIString, ARGS[2])
#hd_mu = load_hists_from_file("$s/mu/cos_theta_lj.root") |> remove_prefix;
#hd_ele = load_hists_from_file("$s/ele/cos_theta_lj.root") |> remove_prefix;
hd_combined = load_hists_from_file("$s/mu/cos_theta_lj.root") |> remove_prefix;
hd_top = load_hists_from_file("$s/../../../Jun22_final_top/merged/0.45000/mu/cos_theta_lj.root") |> remove_prefix;
hd_antitop = load_hists_from_file("$s/../../../Jun22_final_antitop/merged/0.45000/mu/cos_theta_lj.root") |> remove_prefix;

for (k,v) in hd_combined
    println("prescale: ", k, " ", sum(entries(v)), " ", sum(contents(v))) 
end

#hd_mu = reweight_hists_to_fitres(FITRESULTS[:mu], hd_mu)
#hd_ele = reweight_hists_to_fitres(FITRESULTS[:ele], hd_ele)
hd_combined = reweight_hists_to_fitres(FITRESULTS[:combined], hd_combined)
hd_top = reweight_hists_to_fitres(FITRESULTS[:top], hd_top)
hd_antitop = reweight_hists_to_fitres(FITRESULTS[:antitop], hd_antitop)

function yield_table(hd, fr)
    println("aha")
    println(fr)
    ret = Dict()
    ret["data"] = [integral(hd["DATA"]), sqrt(integral(hd["DATA"])), 0, 0]
    for k in ["tchan", "ttjets", "wjets", "schan", "twchan", "dyjets", "diboson", "qcd"]
        println(k)
        if k == "wjets"
            total = integral(hd["wjets_light"])+integral(hd["wjets_charm"])+integral(hd["wjets_heavy"])
            total_entries = sum(entries(hd["wjets_light"])) + sum(entries(hd["wjets_charm"])) + sum(entries(hd["wjets_heavy"]))
            ret[k] = [total, total * 1.0/sqrt(total_entries), 0]
        else        
            println(k, " ", sum(entries(hd[k])), " ", sum(contents(hd[k]))) 
            if haskey(hd, k)
                ret[k] = [integral(hd[k]), integral(hd[k]) * 1.0/sqrt(sum(entries(hd[k]))), 0]
            else
                ret[k] = [0,0,0]
            end
        end
        ret[k][isnan(ret[k])] = 0.0
    end
    x = fr.means[indexof(fr, :beta_signal)]
    err = fr.sigmas[indexof(fr, :beta_signal)]
    ret["tchan"][3] = err/x *  ret["tchan"][1]
    
    x = fr.means[indexof(fr, :wzjets)]
    err = fr.sigmas[indexof(fr, :wzjets)]
    ret["wjets"][3] = err/x *  ret["wjets"][1]
    ret["diboson"][3] = err/x *  ret["diboson"][1]
    ret["dyjets"][3] = err/x *  ret["dyjets"][1]

    x = fr.means[indexof(fr, :ttjets)]
    err = fr.sigmas[indexof(fr, :ttjets)]
    ret["ttjets"][3] = err/x *  ret["ttjets"][1]
    ret["twchan"][3] = err/x *  ret["twchan"][1]
    ret["schan"][3] = err/x *  ret["schan"][1]
    
    ret["qcd"][3] = 0.5 * ret["qcd"][1]
    order = ["tchan", "ttjets", "twchan", "schan", "wjets", "diboson", "dyjets", "qcd"]
    
    df = DataFrame(names=order, yields=[ret[o][1] for o in order], stat=[ret[o][2] for o in order], fit=[ret[o][3] for o in order])
    push!(df, ["total_mc", sum(df[:yields]), df[:stat].^2|>sum|>sqrt, df[:fit].^2|>sum|>sqrt ])
    push!(df, ["data", ret["data"][1], ret["data"][2], ret["data"][3]])
    df[:total] = sqrt(Float64[a for a in df[:stat].^2 + df[:fit].^2])
    #df = DataFrame(names=order, yields=[ret[o][1] for o in order], stat=[ret[o][2] for o in order], fit=[ret[o][3] for o in order])
    return df
end 

function getorder(col, arr...)
    Int64[findfirst(col, a) for a in arr]
end

function print_tables(ytop, yantitop, ycombined)
    ns = ["ttjets", "twchan", "schan", "wjets", "dyjets", "diboson", "qcd", "tchan", "total_mc", "data"]
    ord = getorder(ycombined[1], ns...)
    println(ord) 
    _names = ["\$\\ttbar\$", "tW-channel", "s-channel", "\$\\wjets\$", "DY-jets", "Diboson", "QCD", "t-channel", "Total Expected", "Data"]
    j = 0 
    for i in ord
        j += 1
        println(_names[j], " & ",
            round(ytop[i, 2], 0)|>int, " \$\\pm\$ ", round(ytop[i, 5], 0)|>int, " & ",
            round(yantitop[i, 2], 0)|>int, " \$\\pm\$ ", round(yantitop[i, 5], 0)|>int, " & ",
            round(ycombined[i, 2], 0)|>int, " \$\\pm\$ ", round(ycombined[i, 5], 0)|>int, " \\\\"
        )
    end
end

#yt_mu = yield_table(hd_mu, FITRESULTS[:mu])
#print(yt_mu)
#writetable("$BASE/results/tables/$(yn)_mu.csv", yt_mu)

#yt_ele = yield_table(hd_ele, FITRESULTS[:ele])
#print(yt_ele)
#writetable("$BASE/results/tables/$(yn)_ele.csv", yt_ele)

yt_top = yield_table(hd_top, FITRESULTS[:top])
print(yt_top)
writetable("$BASE/results/tables/$(yn)_top.csv", yt_top)

yt_antitop = yield_table(hd_antitop, FITRESULTS[:antitop])
print(yt_antitop)
writetable("$BASE/results/tables/$(yn)_antitop.csv", yt_antitop)

yt_combined = yield_table(hd_combined, FITRESULTS[:combined])
print(yt_combined)
writetable("$BASE/results/tables/$(yn)_combined.csv", yt_combined)

print_tables(yt_top, yt_antitop, yt_combined)
