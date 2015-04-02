module Reweight

    using JSON, DataFrames
    import SingleTopBase: BASE, fromdf
    import DataFrames: isna, DataFrameRow
    import Histograms: findbin

    const _lumis = JSON.parse(readall("$BASE/metadata/lumis.json"))
    include("$BASE/src/skim/jet_cls.jl")

    const lumis = {symbol(k)=>v for (k,v) in _lumis}
    const lumis_id = {:13 => lumis[:mu], :11 => lumis[:ele]}

    include("selection.jl")

    function reweight(indata, inds)

        indata["totweight"] = 1.0
        indata["fitweight"] = 1.0
        
        indata[inds[:data], :pu_weight] = 1.0
        indata[:totweight] = indata[:totweight].*indata[:pu_weight].*indata[:b_weight]
        
        #Sherpa reweight to madgraph yield
        #indata[indata["sample"].==int(hash("wjets_sherpa")), :xsweight] = 0.04471345 .* indata[sample_is("wjets_sherpa"), :xsweight]
        
        #remove events with incorrect weights
        indata[isna(indata[:totweight]), :totweight] = 0.0
        
        ##########
        #  LUMI  #
        ##########  
        for c in [:mu, :ele]
            tic()
            println("xs reweighting: $c")
            indata[inds[c], :xsweight] *= lumis[c]
            toc()
        end
        
        indata[inds[:data], :xsweight] = 1.0
    end

    const wjets_ratio_hists = {
        k => fromdf(readtable("$BASE/results/wjets_shape_weight_mar24/$k.csv"))
        for k in jet_classifications
    }

    function wjets_shape_weight(row::DataFrameRow)
        cls = jet_cls_from_number(row[:jet_cls])

        const ct = row[:cos_theta_lj]

        if !isna(ct)
            const h = wjets_ratio_hists[cls]
            const w = h.bin_contents[findbin(h, ct)]
        else
            const w = 1
        end

        #nominal, half, double
        return w, (1.0 - 0.5 * (1.0 - w)), (1.0 - 2.0 * (1.0 - w))
    end

    const sherpa_flavor_ratio_hists = {
        k => fromdf(readtable("$BASE/results/wjets_shape_weight_mar24/sherpa_$k.csv"))
        for k in jet_classifications
    }

    function sherpa_flavor_weight(row::DataFrameRow)
        cls = jet_cls_from_number(row[:jet_cls])

        const ct = row[:cos_theta_lj]

        if !isna(ct)
            const h = sherpa_flavor_ratio_hists[cls]
            const w = h.bin_contents[findbin(h, ct)]
        else
            const w = 1
        end

        #nominal, half, double
        return w
    end

    const wjets_pt_ratio_hists = {
        k => fromdf(readtable("$BASE/results/wjets_pt_weight/weights_$k.csv"))
        for k in [:mu, :ele]
    }

    function wjets_pt_weight(row::DataFrameRow)
        if Cuts.is_reco_lepton(row, :mu)
            const lepton = :mu
        elseif Cuts.is_reco_lepton(row, :ele)
            const lepton = :ele
        else
            #println(row[:lepton_type], row[:n_signal_mu], row[:n_signal_ele], row[:n_veto_mu], row[:n_veto_ele], row[:hlt_mu], row[:hlt_ele])
            return 1.0,1.0,1.0        
        end

        const w_pt = row[:w_pt]
        const h = wjets_pt_ratio_hists[lepton]
        const w = h.bin_contents[findbin(h, w_pt)]
        const bin = findbin(h, w_pt)
        #nominal, no weight
        return w, 1.0, 1.0
    end

    export reweight, wjets_shape_weight, sherpa_flavor_weight, wjets_pt_weight

end
