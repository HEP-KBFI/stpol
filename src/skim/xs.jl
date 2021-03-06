using DataFrames

#returns a dict with :tag, :iso, :systematic, :sample classifying the sample based on the file path
function sample_type(fn, prefix="file:/hdfs/cms/store/user")
#function sample_type(fn, prefix="/home/andres/single_top/stpol_pdf/src/step3/output")
    #MC match
    r = Regex("$prefix/(.*)/(.*)/(.*)/(.*)/(.*)/output(.*).root")
    #r = Regex("$prefix/(.*)/(.*)/(.*)/(.*)/output(.*).root")
    m = match(r, fn)
    
    if m==nothing
        tag = :unknown
        syst = :unknown
        samp = :unknown
        iso = :unknown
       
        #MC did not match, try data
        cls = data_cls(prefix, fn)
        #cls = data_cls("/hdfs/local/joosep/stpol", fn)
        if cls != nothing
            tag, iso, samp = cls
            syst = ""
        end
    else
        tag = m.captures[2]
        iso = m.captures[3]

        syst = replace(m.captures[4], "nominal_scaleweight_fixed", "nominal")
        samp = replace(m.captures[5], "T_t_ToLeptons_scaledown_v2", "T_t_ToLeptons_scaledown")
    end
    #TToBMuNu_anomWtb-unphys_t-channel

    while true #hack to have 'break' to match only once
    if syst == "SYST"
        ss = string(samp)
        m = match(r".*_(mass(166_5|169_5|175_5|178_5)).*", ss)
        if m != nothing
            syst = m.captures[1]
            break
        end
        
        m = match(r".*_(scale(up|down)).*", ss)
        if m != nothing
            syst = m.captures[1]
            break
        end
        
        m = match(r".*_(matching(up|down)).*", ss)
        if m != nothing
            syst = m.captures[1]
            break
        end

        m = match(r".*TToB.*Nu_(.*)", ss)
        if m != nothing
            if m.captures[1] == "t-channel"
                syst = "signal_comphep__nominal"
            else
                syst = string("signal_comphep__", m.captures[1])
            end
            break
        end

        m = match(r".*TToLeptons_tchannel_aMCatNLO", ss)
        if m != nothing
            syst = "signal_aMCatNLO__nominal"
            println(syst)
            break
        end

        m = match(r".*TToLeptons_t-channel_aMCatNLO", ss)
        if m != nothing
            syst = "signal_aMCatNLO__nominal"
            println(syst)
            break
        end

        m = match(r".*TToLeptons_tchannel_aMCatNLO_(.*)", ss)
        if m != nothing
            syst = string("signal_aMCatNLO_", m.captures[1])
            println(syst)
            break
        end

        m = match(r".*TToLeptons_t-channel_aMCatNLO_(.*)", ss)
        if m != nothing
            syst = string("signal_aMCatNLO_", m.captures[1])
            println(syst)
            break
        end
        
        m = match(r"exclusive_FSIM", ss)
        if m != nothing
            syst = "wjets_fsim_nominal"
            break
        end

        #m = match(r"W*JetsToLNu2", ss)
        #if m != nothing
        #    syst = "wjets_fsim_nominal"
        #    break
        #end
    end
    break #in case of no match, we also want to break
    end #while

    return {:tag => string(tag), :iso => string(iso), :systematic => string(syst), :sample => string(samp)}
end

function data_cls(prefix, fn)
    #temp for current location
    #println("prefix")
    #println(prefix," ",fn)    
    r = Regex("$prefix/.*/(.*)/(.*)/(.*)/output_.*.root")
    #r = Regex("$prefix/.*/(.*)/(.*)/output_.*.root")
    m = match(r, fn)
    if m!=nothing
        #println(m.captures)
        tag = m.captures[1]
        #tag = "s2_1101_data"
        iso = m.captures[2]
        sample = m.captures[3]
        #sample = m.captures[1]
        return (tag, iso, sample)
    else
        return nothing
    end
    return
end

fpath = joinpath(
    BASE, "metadata", "cross_sections.csv"
)
println("loading cross-sections from $fpath")

df = readtable(fpath, allowcomments=true)
cross_sections = Dict{String, Float64}()
for i=1:nrow(df)
    cross_sections[df[i, 1]] = df[i, 2]
end

function xsweight(flist)
    out = Dict()
    for fi in flist
        df = readtable(fi)
        for n=1:nrow(df)
            cls = sample_type(df[n, :files])
            generated = df[n, :total_processed]
            if !haskey(out, cls)
                out[cls] = 0
            end
            out[cls] += generated
        end
    end

    ret = Dict()
    for (k, v) in out
        x = cross_sections[k[:sample]]/v
        ret[k[:sample]] = x
    end
    return ret
end

#process ->[sample1, sample2, ...]
const merges = {
    "tchan"=>
        ["T_t_ToLeptons", "Tbar_t_ToLeptons",
        "TToBENu_anomWtb-unphys_t-channel", "TToBENu_anomWtb-0100_t-channel", "TToBENu_t-channel",
        "TToBMuNu_anomWtb-unphys_t-channel", "TToBMuNu_anomWtb-0100_t-channel", "TToBMuNu_t-channel",
        "TToBTauNu_anomWtb-unphys_t-channel", "TToBTauNu_anomWtb-0100_t-channel", "TToBTauNu_t-channel",
        
        "TToBENu_anomWtb-unphys_LVLT",
        "TToBENu_anomWtb-Lv1Rt3_LVRT",
        "TToBENu_anomWtb-Lv2Rt2_LVRT",
        "TToBENu_anomWtb-Lv3Rt1_LVRT",
        "TToBENu_anomWtb-Rt4_LVRT",
        "TToBMuNu_anomWtb-unphys_LVLT",
        "TToBMuNu_anomWtb-Lv1Rt3_LVRT",
        "TToBMuNu_anomWtb-Lv2Rt2_LVRT",
        "TToBMuNu_anomWtb-Lv3Rt1_LVRT",
        "TToBMuNu_anomWtb-Rt4_LVRT",
        "TToBTauNu_anomWtb-unphys_LVLT",
        "TToBTauNu_anomWtb-Lv1Rt3_LVRT",
        "TToBTauNu_anomWtb-Lv2Rt2_LVRT",
        "TToBTauNu_anomWtb-Lv3Rt1_LVRT",
        "TToBTauNu_anomWtb-Rt4_LVRT",
        
        "TToBENu_anomWtb-0010_LVLT",
        "TToBMuNu_anomWtb-0010_LVLT",
        "TToBTauNu_anomWtb-0010_LVLT",

        "TToLeptons_tchannel_aMCatNLO",
        "TToLeptons_tchannel_aMCatNLO_scaledown",
        "TToLeptons_tchannel_aMCatNLO_scaleup", 
        "TToLeptons_t-channel_aMCatNLO",
        "TToLeptons_t-channel_aMCatNLO_scaledown",
        "TToLeptons_t-channel_aMCatNLO_scaleup", 

        "T_t_ToLeptons_mass166_5", 
        "T_t_ToLeptons_mass169_5", 
        "Tbar_t_ToLeptons_mass166_5", 
        "Tbar_t_ToLeptons_mass169_5", 
        
        "T_t_ToLeptons_mass175_5", 
        "T_t_ToLeptons_mass178_5", 
        "Tbar_t_ToLeptons_mass175_5", 
        "Tbar_t_ToLeptons_mass178_5",
    
        "T_t_ToLeptons_mass169_5",
        "T_t_ToLeptons_mass175_5",
        
        "T_t_ToLeptons_scaleup", 
        "T_t_ToLeptons_scaledown", 
        "T_t_ToLeptons_scaledown_v2", 
        "T_t_ToLeptons_scaledown_split",
        "Tbar_t_ToLeptons_scaleup", 
        "Tbar_t_ToLeptons_scaledown", 
    ],

    "tchan_inc"=>["T_t", "T_t_v2", "Tbar_t"],
    "wjets"=>[
        "W1Jets_exclusive", "W2Jets_exclusive", "W3Jets_exclusive", "W4Jets_exclusive",
        #"W1JetsToLNu",
        "W1JetsToLNu_matchingdown",
        "W1JetsToLNu_matchingup",
        "W1JetsToLNu_scaleup",
        "W1JetsToLNu_scaledown",
        #"W2JetsToLNu2",
        "W2JetsToLNu_matchingdown",
        "W2JetsToLNu_matchingup",
        "W2JetsToLNu_scaleup",
        "W2JetsToLNu_scaledown",
        #"W3JetsToLNu2",
        "W3JetsToLNu_matchingdown",
        "W3JetsToLNu_matchingup",
        "W3JetsToLNu_scaleup",
        "W3JetsToLNu_scaledown",
        #"W4JetsToLNu2",
        "W4JetsToLNu_matchingdown",
        "W4JetsToLNu_matchingup",
        "W4JetsToLNu_scaleup",
        "W4JetsToLNu_scaledown",
    ],
    "wjets_inc"=>["WJets_inclusive"],
    "wjets_sherpa"=>["WJets_sherpa"],
    "wjets_fsim"=>["W1Jets_exclusive_FSIM", "W2Jets_exclusive_FSIM", "W3Jets_exclusive_FSIM", "W4Jets_exclusive_FSIM"],

    "ttjets"=>[
        "TTJets_FullLept", "TTJets_SemiLept",
        "TTJets_matchingdown",
        "TTJets_matchingup",
        "TTJets_scaledown",
        "TTJets_scaleup",

        "TTJets_mass166_5",
        "TTJets_mass169_5",
        "TTJets_mass175_5",
        "TTJets_mass178_5",
        "TTJets_MSDecays",
        "TTJets_MSDecays_scaleup",
        "TTJets_MSDecays_scaledown",
        "TTJets_MSDecays_matchingup",
        "TTJets_MSDecays_matchingdown",
        "TTJets_MSDecays_matchingdown_v1",
        "TTJets_MSDecays_matchingdown_v2",
        "TTJets_MSDecays_mass166_5",
        "TTJets_MSDecays_mass169_5",
        "TTJets_MSDecays_mass175_5",
        "TTJets_MSDecays_mass178_5",
        "TTJets_MS",
        "TTJets_MS_scaleup",
        "TTJets_MS_scaledown",
        "TTJets_MS_matchingup",
        "TTJets_MS_matchingdown",
        "TTJets_MS_matchingdown_v1",
        "TTJets_MS_matchingdown_v2",
        "TTJets_MS_mass166_5",
        "TTJets_MS_mass169_5",
        "TTJets_MS_mass175_5",
        "TTJets_MS_mass178_5",
    ],

    "ttjets_inc"=>["TTJets_MassiveBinDECAY"],
    "twchan"=>["T_tW", "Tbar_tW"],
    "schan"=>["T_s", "Tbar_s"],
    "diboson"=>["WW", "WZ", "ZZ"],
    "dyjets"=>["DYJets"],
    "gjets"=>["GJets1", "GJets2"],
    "data_mu"=>["SingleMuon", "SingleMu", "SingleMu1", "SingleMu2", "SingleMu3", "SingleMu_miss"],
    "data_ele"=>["SingleElectron", "SingleEle", "SingleEle1", "SingleEle2", "SingleEle3", "SingleEle_miss"],
    "qcd_mc_mu"=>["QCDMu"],
    "qcd_mc_ele"=>[
        "QCD_Pt_170_250_BCtoE",
        "QCD_Pt_170_250_EMEnriched",
        "QCD_Pt_20_30_BCtoE",
        "QCD_Pt_20_30_EMEnriched",
        "QCD_Pt_250_350_BCtoE",
        "QCD_Pt_250_350_EMEnriched",
        "QCD_Pt_30_80_BCtoE",
        "QCD_Pt_30_80_EMEnriched",
        "QCD_Pt_350_BCtoE",
        "QCD_Pt_350_EMEnriched",
        "QCD_Pt_80_170_BCtoE",
        "QCD_Pt_80_170_EMEnriched",
    ],
}

function get_process(sample)
    sample = string(sample)
    for (proc, samps) in merges
        sample in samps && return symbol(proc)
    end
    return :unknown
end

function test_cls(inf)
    flist = split(readall(inf))
    for f in flist
        st = sample_type(f)
        samp = string(st[:sample])
        proc = SingleTopBase.get_process(samp)
        xs = samp in keys(SingleTopBase.cross_sections) ? SingleTopBase.cross_sections[samp] : -1.0
        println("$f $st $proc $xs")
    end
end

#create a hash-map for strings
hmap = {:to=>Dict(), :from=>Dict()}

#list of all hashmappable strings
const tomap = ASCIIString[
    "", #for data
    "s2_Oct22",
    "antiiso",
    "data_ele",
    "data_mu",
    "diboson",
    "DYJets",
    "dyjets",
    "EnDown",
    "EnUp",
    "gjets",
    "GJets1",
    "GJets2",
    "iso",
    "mass166_5",
    "mass169_5",
    "mass175_5",
    "mass178_5",
    "matchingdown",
    "matchingup",
    "nominal",
    "nominal_scaleweight_fixed",
    "qcd_mc_ele",
    "qcd_mc_mu",
    "QCD_Pt_170_250_BCtoE",
    "QCD_Pt_170_250_EMEnriched",
    "QCD_Pt_20_30_BCtoE",
    "QCD_Pt_20_30_EMEnriched",
    "QCD_Pt_250_350_BCtoE",
    "QCD_Pt_250_350_EMEnriched",
    "QCD_Pt_30_80_BCtoE",
    "QCD_Pt_30_80_EMEnriched",
    "QCD_Pt_350_BCtoE",
    "QCD_Pt_350_EMEnriched",
    "QCD_Pt_80_170_BCtoE",
    "QCD_Pt_80_170_EMEnriched",
    "QCDMu",
    "ResDown",
    "ResUp",
    "scaledown",
    "scaleup",
    "schan",
    "signal_comphep__anomWtb-0100_t-channel",
    "signal_comphep__anomWtb-0010_LVLT",
    "signal_comphep__anomWtb-Lv1Rt3_LVRT",
    "signal_comphep__anomWtb-Lv2Rt2_LVRT",
    "signal_comphep__anomWtb-Lv3Rt1_LVRT",
    "signal_comphep__anomWtb-Rt4_LVRT",
    "signal_comphep__anomWtb-unphys_LVLT",
    "signal_comphep__anomWtb-unphys_t-channel",
    "signal_comphep__nominal",
    "signal_comphep__nominal_t-channel",
    "signal_comphep__anomWtb-0010_LVLT_t-channel",
    "signal_comphep__anomWtb-Lv1Rt3_LVRT_t-channel",
    "signal_comphep__anomWtb-Lv2Rt2_LVRT_t-channel",
    "signal_comphep__anomWtb-Lv3Rt1_LVRT_t-channel",
    "signal_comphep__anomWtb-Rt4_LVRT_t-channel",
    "signal_comphep__anomWtb-unphys_LVLT_t-channel",
    "signal_aMCatNLO__nominal",
    "signal_aMCatNLO__scaledown",
    "signal_aMCatNLO__scaleup",
    "SingleElectron",
    "SingleEle",
    "SingleElectron",
    "SingleEle1",
    "SingleEle2",
    "SingleEle3",
    "SingleEle_miss",
    "SingleMuon",
    "SingleMu",
    "SingleMu1",
    "SingleMu2",
    "SingleMu3",
    "SingleMu_miss",
    "T_s",
    "T_t",
    "T_t_v2",
    "T_t_ToLeptons",
    "T_t_ToLeptons_mass166_5",
    "T_t_ToLeptons_mass169_5",
    "T_t_ToLeptons_mass175_5",
    "T_t_ToLeptons_mass178_5",
    "T_t_ToLeptons_scaledown",
    "T_t_ToLeptons_scaledown_v2",
    "T_t_ToLeptons_scaledown_split",
    "T_t_ToLeptons_scaleup",
    "T_tW",
    "Tbar_s",
    "Tbar_t",
    "Tbar_t_ToLeptons",
    "Tbar_t_ToLeptons_mass166_5",
    "Tbar_t_ToLeptons_mass169_5",
    "Tbar_t_ToLeptons_mass175_5",
    "Tbar_t_ToLeptons_mass178_5",
    "Tbar_t_ToLeptons_scaledown",
    "Tbar_t_ToLeptons_scaleup",
    "Tbar_tW",
    "tchan", 
    "tchan_inc",
    "ttjets",
    "TTJets_FullLept",
    "ttjets_inc",
    "TTJets_mass166_5",
    "TTJets_mass169_5",
    "TTJets_mass175_5",
    "TTJets_mass178_5",
    "TTJets_MassiveBinDECAY",
    "TTJets_matchingdown",
    "TTJets_matchingup",
    "TTJets_scaledown",
    "TTJets_scaleup",
    "TTJets_SemiLept",
    "TToBENu_anomWtb-0100_t-channel",
    "TToBENu_anomWtb-unphys_t-channel",
    "TToBENu_t-channel",
    "TToBMuNu_anomWtb-0100_t-channel",
    "TToBMuNu_anomWtb-unphys_t-channel",
    "TToBMuNu_t-channel",
    "TToBTauNu_anomWtb-0100_t-channel",
    "TToBTauNu_anomWtb-unphys_t-channel",
    "TToBTauNu_t-channel",
    "TToBENu_anomWtb-unphys_LVLT",
    "TToBENu_anomWtb-Lv1Rt3_LVRT",
    "TToBENu_anomWtb-Lv2Rt2_LVRT",
    "TToBENu_anomWtb-Lv3Rt1_LVRT",
    "TToBENu_anomWtb-Rt4_LVRT",
    "TToBMuNu_anomWtb-unphys_LVLT",
    "TToBMuNu_anomWtb-Lv1Rt3_LVRT",
    "TToBMuNu_anomWtb-Lv2Rt2_LVRT",
    "TToBMuNu_anomWtb-Lv3Rt1_LVRT",
    "TToBMuNu_anomWtb-Rt4_LVRT",
    "TToBTauNu_anomWtb-unphys_LVLT",
    "TToBTauNu_anomWtb-Lv1Rt3_LVRT",
    "TToBTauNu_anomWtb-Lv2Rt2_LVRT",
    "TToBTauNu_anomWtb-Lv3Rt1_LVRT",
    "TToBTauNu_anomWtb-Rt4_LVRT",
    
    "TToBENu_anomWtb-0010_LVLT_t-channel",
    "TToBMuNu_anomWtb-0010_LVLT_t-channel",
    "TToBTauNu_anomWtb-0010_LVLT_t-channel",
    "TToBENu_anomWtb-unphys_LVLT_t-channel",
    "TToBENu_anomWtb-Lv1Rt3_LVRT_t-channel",
    "TToBENu_anomWtb-Lv2Rt2_LVRT_t-channel",
    "TToBENu_anomWtb-Lv3Rt1_LVRT_t-channel",
    "TToBENu_anomWtb-Rt4_LVRT_t-channel",
    "TToBMuNu_anomWtb-unphys_LVLT_t-channel",
    "TToBMuNu_anomWtb-Lv1Rt3_LVRT_t-channel",
    "TToBMuNu_anomWtb-Lv2Rt2_LVRT_t-channel",
    "TToBMuNu_anomWtb-Lv3Rt1_LVRT_t-channel",
    "TToBMuNu_anomWtb-Rt4_LVRT_t-channel",
    "TToBTauNu_anomWtb-unphys_LVLT_t-channel",
    "TToBTauNu_anomWtb-Lv1Rt3_LVRT_t-channel",
    "TToBTauNu_anomWtb-Lv2Rt2_LVRT_t-channel",
    "TToBTauNu_anomWtb-Lv3Rt1_LVRT_t-channel",
    "TToBTauNu_anomWtb-Rt4_LVRT_t-channel",
    
    "TToBENu_anomWtb-0010_LVLT_t-channel",
    "TToBMuNu_anomWtb-0010_LVLT_t-channel",
    "TToBTauNu_anomWtb-0010_LVLT_t-channel",

    "TToLeptons_tchannel_aMCatNLO",
    "TToLeptons_tchannel_aMCatNLO_scaledown",
    "TToLeptons_tchannel_aMCatNLO_scaleup", 
    "TToLeptons_t-channel_aMCatNLO",
    "TToLeptons_t-channel_aMCatNLO_scaledown",
    "TToLeptons_t-channel_aMCatNLO_scaleup",
    "twchan",
    "UnclusteredEnDown",
    "UnclusteredEnUp",
    "unknown",
    "WJetsToLNu_scaleup",
    "WJetsToLNu_scaledown",
    "WJetsToLNu_matchingup",
    "WJetsToLNu_matchingdown",
    "W1Jets_exclusive",
    "W1JetsToLNu",
    "W1JetsToLNu2",
    "W1JetsToLNu_matchingdown",
    "W1JetsToLNu_matchingup",
    "W1JetsToLNu_scaledown",
    "W1JetsToLNu_scaleup",
    "W2Jets_exclusive",
    "W2JetsToLNu",
    "W2JetsToLNu2",
    "W2JetsToLNu_matchingdown",
    "W2JetsToLNu_matchingup",
    "W2JetsToLNu_scaledown",
    "W2JetsToLNu_scaleup",
    "W3Jets_exclusive",
    "W3JetsToLNu",
    "W3JetsToLNu2",
    "W3JetsToLNu_matchingdown",
    "W3JetsToLNu_matchingup",
    "W3JetsToLNu_scaledown",
    "W3JetsToLNu_scaleup",
    "W4Jets_exclusive",
    "W4JetsToLNu",
    "W4JetsToLNu2",
    "W4JetsToLNu_matchingdown",
    "W4JetsToLNu_matchingup",
    "W4JetsToLNu_scaledown",
    "W4JetsToLNu_scaleup",
    "W1Jets_exclusive_FSIM",
    "W2Jets_exclusive_FSIM",
    "W3Jets_exclusive_FSIM",
    "W4Jets_exclusive_FSIM",
    "wjets",
    "wjets_fsim_nominal",
    "wjets_fsim",
    "wjets_inc",
    "WJets_inclusive",
    "WJets_sherpa",
    "wjets_sherpa",
    "WJets_scaleup",
    "WJets_scaledown",
    "WJets_matchingup",
    "WJets_matchingdown",
    "WW",
    "WZ",
    "ZZ",
    "Dec6_anom_42ccfd",
    "Mar13",
    "Nov29_tW_etabl_CSVT_genwhgt_2fdd84",
    "signal_costheta_systb",
    "343e0a9_Aug22",
    "May1_metphi_on",
    "Jul4_newsyst_newvars_metshift",
    "Aug8_tchpt",
    "Oct28_reproc",
    "Oct28_reproc_small",
    "Dec17_wjets",
    "wjets_nominals_clear",
    "s2_0801_deltaRChange",
    "s2_1101_data",
    "s2_1101_deltaRChange",
    "Jan11_deltaR",
    "Jan22_fullData",
    "Jan27_fullData",
    "Apr21_btags",
    "May30_deltaRs",
    "fullData",
    "fullData_fixpub_slurm",
    "fullData_fixmeweight",
    "fullData_fixmeweight2",
    "btag_effs",
    "deltars_27_05",
    "deltars_30_05",
    "TTJets_MSDecays",
    "TTJets_MSDecays_scaleup",
    "TTJets_MSDecays_scaledown",
    "TTJets_MSDecays_matchingup",
    "TTJets_MSDecays_matchingdown",
    "TTJets_MSDecays_matchingdown_v1",
    "TTJets_MSDecays_matchingdown_v2",
    "TTJets_MSDecays_mass166_5",
    "TTJets_MSDecays_mass169_5",
    "TTJets_MSDecays_mass175_5",
    "TTJets_MSDecays_mass178_5",
    "TTJets_MS",
    "TTJets_MS_scaleup",
    "TTJets_MS_scaledown",
    "TTJets_MS_matchingup",
    "TTJets_MS_matchingdown",
    "TTJets_MS_matchingdown_v1",
    "TTJets_MS_matchingdown_v2",
    "TTJets_MS_mass166_5",
    "TTJets_MS_mass169_5",
    "TTJets_MS_mass175_5",
    "TTJets_MS_mass178_5",
    "SYST"
]

#convert all strings to hash, create a two-way dict
for tm in tomap
    hmap[:to][tm] = int(hash(tm))
    hmap[:from][int(hash(tm))] = tm
end

#_hmap_symb_to = Dict()
#for k in hmap[:to]|>keys
#    _hmap_symb_to[symbol(k)] = hmap[:to][k]
#end
#_hmap_symb_from= Dict()
#for k in hmap[:from]|>keys
#    _hmap_symb_from[k] = hmap[:from][k]|>symbol
#end
#const hmap_symb_to = deepcopy(_hmap_symb_to)
#const hmap_symb_from = deepcopy(_hmap_symb_from)

#write out the hashmap as a CSV
function write_hmap(fname)
    cv = collect(hmap[:to])

    writetable(fname,
        DataFrame(
            name=ASCIIString[x[1] for x in cv],
            hash=Int64[x[2] for x in cv]
        )
    )
end

export cross_sections, hmap_symb_from, hmap_symb_to, get_process, sample_type, write_hmap
