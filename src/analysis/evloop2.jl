using JSON
using ROOT, Histograms

const VERBOSE = bool(int(get(ENV, "VERBOSE", 0)))
const outfile = ARGS[1]
const PARS = JSON.parse(readall(ARGS[2]))

infiles = map(x->convert(ASCIIString, x), ARGS[5:end])

#how to cut on QCD?
const QCD_CUT_TYPE = symbol(PARS["qcd_cut"])
const DO_LJET_RMS = PARS["do_ljet_rms"]

#FIXME: currently this is different for TCHPT and CSVT
const B_WEIGHT_NOMINAL = symbol(PARS["b_weight_nominal"])

const BDT_VAR = symbol(PARS["bdt_var"])
#const BDT_CUTS = [-0.2:0.1:0.9]
#const BDT_CUTS = [-0.2, 0.0, 0.06, 0.13, 0.2, 0.4, 0.6,]
#const BDT_CUTS = [-0.2, -0.10, 0.0, 0.06, 0.10, 0.13, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.50, 0.55, 0.6, 0.65, 0.70, 0.75, 0.80]
const BDT_CUTS = [-0.2, 0.45]
#const BDT_REVERSE_CUTS = [-0.2, -0.10, 0.0, 0.06, 0.10, 0.13, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.50, 0.55, 0.6, 0.65, 0.70, 0.75, 0.80]
const BDT_REVERSE_CUTS = [0.0]
const VARS_TO_USE = symbol(PARS["vars_to_use"])


import ROOT.to_root
function to_root_z(h::NHistogram, name="hist")
    length(size(h))==2 || error("to_root not defined for nd=$(length(size(h)))")

    nbins_x = nbins(h, 1)
    nbins_y = nbins(h, 2)

    conts, errs = contents(h), errors(h)

    #remove overflow bins
    e1 = convert(Vector{Float64}, h.edges[1][2:end-1])
    e2 = convert(Vector{Float64}, h.edges[2][2:end-1])

    hi = TH2D(name, name, int32(nbins_x - 3), pointer(e1), int32(nbins_y - 3), pointer(e2))
    for i=0:nbins_x-1
        for j=0:nbins_y-1
            SetBinContent(hi, int32(i), int32(j), conts[i + 1, j + 1])
            SetBinError(hi, int32(i), int32(j), errs[i + 1, j + 1])
        end
    end
    SetEntries(hi, sum(entries(h)))
    return hi
end

function to_root_z(h::Histogram, name="hist")
    edges = copy(h.bin_edges)

    #remove underflow low and overflow high
    edges = h.bin_edges[2:end-1]
    hi = TH1D(name, name, int32(nbins(h) - 3), pointer(edges))
    for i=0:GetNbinsX(hi)+1
        SetBinContent(hi, int32(i), contents(h)[i + 1])
        SetBinError(hi, int32(i), errors(h)[i + 1])
    end
    SetEntries(hi, sum(entries(h)))

    # println(h)
    # Print(hi, "ALL")
    conts, errs, ents, edges = get_hist_bins_z(hi)

    if !all(conts .==  contents(h))
        warn("mismatch in contents: \n", hcat(conts, contents(h))|>string, "\n")
    end
    if !all(errs .==  errors(h))
        warn("mismatch in errors: \n", hcat(errs, errors(h))|>string, "\n")
    end
    # if !all(ents .==  entries(h))
    #     warn("mismatch in entries: \n", hcat(ents, entries(h))|>string, "\n")
    # end
    if !all(edges .==  h.bin_edges)
        warn("mismatch in edges: \n", hcat(edges, h.bin_edges)|>string, "\n")
    end
    return hi
end

function get_hist_bins_z(h::Union(TH1D, TH1A, TH1); error_type=:contents)
    nb = int64(GetNbinsX(h))
    nb>0 || error("nbins = $nb")

    #+3 = underflow, overflow, superfluous extra bin
    conts = zeros(Float64, nb+3)
    errs = zeros(Float64, nb+3)
    ents = zeros(Float64, nb+3)

    #underflow low, overflow low, overflow high
    edges = zeros(Float64, nb+3)
    for n=0:nb+1
        conts[n+1] = GetBinContent(h, int32(n))
        errs[n+1] = GetBinError(h, int32(n))
        #entries[n+1] = GetEntries(h) * conts[n+1]
        edges[n+1] = GetBinLowEdge(h, int32(n))
    end

    #this work for histograms for which the bin errors have been manually set
    #to non-Poisson, GetEntries is meaningless
    if error_type == :errors
        ents = (conts ./ errs).^2
        ents[isnan(ents)] = 0
        ents[ents .== Inf] = 1
        #println(hcat(conts, errs, ents, conts./sqrt(ents)))
    end
    #this works for Poisson bin errors
    if error_type == :contents
        ents = conts ./ sum(conts) .* GetEntries(h)
        ents[isnan(ents)] = 0
    end
    #ents = int(round(ents))
    edges[1] = -Inf
    edges[nb+2] = edges[nb+1] + GetBinWidth(h, int32(nb))
    edges[nb+3] = Inf

    if error_type != :errors
        if GetEntries(h)>0 && Integral(h)>0
            @assert abs(sum(ents) - GetEntries(h))/sum(ents)<0.0001 string("entries unequal ", sum(ents), "!=", GetEntries(h))
        end
    end
    if Integral(h)>0
        @assert abs(sum(conts) - Integral(h, int32(0), int32(nb+1)))/sum(conts)<0.0001 string("contents unequal ", sum(conts), "!=", Integral(h, int32(0), int32(nb+1)))
    end
    # if (abs(sum(conts) - Integral(h)) > 100000 * eps(Float64))
    #     warn(
    #         GetName(h)|>bytestring,
    #         " integral mismatch: $(sum(conts)) != $(Integral(h))"
    #     )
    # end
    return conts, errs, ents, edges
end

function load_with_errors(f::TDirectoryA, k::ASCIIString; kwargs...)
    th = root_cast(TH1, Get(f, k))
    #println(th)
    conts, errs, ents, edgs = get_hist_bins(th; kwargs...)
    h = Histogram(ents, conts, edgs)
    return h
end

const IS_TOP = false
const IS_ANTITOP = false

const IS_CT_BIN = false
const WHICH_BIN = 6

#const BDT_CUTS = [0.0, 0.06, 0.13, 0.2, 0.4, 0.6, 0.8, 0.9]

#PAS
#const BDT_CUTS = [0.06, 0.13]

const sp = dirname(Base.source_path())
require("$sp/base.jl")

using ROOT, ROOTDataFrames
using ROOTHistograms

_infiles = Any[]
for inf in infiles
    try
        df = TreeDataFrame(inf)
        if nrow(df)<=0
            error("empty dataframe")
        end
        push!(_infiles, inf)
    catch err
        warn("$err: skipping file")
    end
end
infiles = _infiles

println("loading dataframe:$infiles");

#Load the main event TTree
const df_base = TreeDataFrame(infiles)
df_base.tt == C_NULL && (warn("empty TTree for $infiles, exiting");exit(0))
nrow(df_base)>0 || (warn("$infiles was emtpy, exiting");exit(0))

#load the TTree with the QCD values, xs weights
const df_added = TreeDataFrame(map(x->"$x.added", infiles))

#create a combined view of both ttrees
df = MultiColumnDataFrame(TreeDataFrame[df_base, df_added])

#ARGS[3] = number of events to skip from the beginning
const FIRST_EVENT = int(ARGS[3]) + 1
#ARGS[4] = number of events to process
nevents = int(ARGS[4])
if nevents<0
    nevents = nrow(df)
end
LAST_EVENT = min(FIRST_EVENT + nevents - 1, nrow(df))

#eventids = open("eventids_$(FIRST_EVENT)_$(LAST_EVENT).txt", "w")

require("$sp/histogram_defaults.jl")

const BDT_SYMBOLS = {bdt=>symbol(@sprintf("%.5f", bdt)) for bdt in BDT_CUTS}
const BDT_REVERSE_SYMBOLS = {bdt=>symbol(@sprintf("LESSTHAN_%.5f", bdt)) for bdt in BDT_REVERSE_CUTS}
const LEPTON_SYMBOLS = {13=>:mu, 11=>:ele, -13=>:mu, -11=>:ele, 15=>:tau, -15=>:tau, NA=>NA}

const DO_TRANSFER_MATRIX = true
const HISTS_NOMINAL_ONLY = false
const TM_NOMINAL_ONLY = false
const JET_TAGS = [(2, 0), (2, 2), (2, 1), (3, 0), (3, 1), (3, 2), (3, 3)]
#const JET_TAGS = [(2,1)]

const wjets_weights = {
    :heavy => {:up=>2.0, :down=>0.5},
    :light => {:up=> 1.2, :down=>0.8},
    :wc => {:up=> 1.2, :down=>0.8}
}

lepton_iso_limits = {
    :mu => {
        :up => (0.22, 0.5),
        :down => (0.2, 0.45),
    },
    :ele => {
        :up => (0.165, 0.5),
        :down => (0.15, 0.45),
    }
}

crosscheck_vars = Any[]

##Variables to plot
if VARS_TO_USE == :all_crosscheck
    crosscheck_vars = [
        :bdt_sig_bg,
        :bdt_sig_bg_old,
        :bdt_qcd,
        :bdt_sig_bg_top_13_001,

#        (:abs_ljet_eta, row::DataFrameRow -> abs(row[:ljet_eta])),
#        (:abs_ljet_eta_16, row::DataFrameRow -> abs(row[:ljet_eta])),
#        (:abs_bjet_eta, row::DataFrameRow -> abs(row[:bjet_eta])),
        :C, :shat, :ht,
        (:C_signalregion, row->row[:C]),
        (:top_mass_signalregion, row->row[:top_mass]),

#        :lepton_pt, :lepton_iso, :lepton_eta,
#        (:abs_lepton_eta, r->abs(r[:lepton_eta])),
#        :met_phi,
        :met, :mtw,
        :bjet_pt, :ljet_pt,
        :ljet_eta, :bjet_eta,
        :bjet_mass, :ljet_mass,
        :ljet_dr, :bjet_dr,
        (:abs_ljet_eta, row::DataFrameRow -> abs(row[:ljet_eta])),

        :top_mass,
#       :top_pt,

#       :n_good_vertices,
        :cos_theta_lj,
#        :cos_theta_bl,
#        :cos_theta_lj_gen, :cos_theta_bl_gen,
#        :nu_soltype,
        :njets,
        :ntags,
    ]
elseif VARS_TO_USE == :analysis
    crosscheck_vars = [
        :bdt_sig_bg,
        :bdt_sig_bg_old,
        :bdt_sig_bg_top_13_001,
        :cos_theta_lj,
        :C,
        :bjet_bd_b,
        :ljet_bd_b,
        :lepton_met_dphi,
        :jet1_met_dphi,
        :bdt_qcd,
        #:bdt_qcd_dphis_nomet,
        #:bdt_qcd_dphis_withmet,
        #:bdt_sig_bg_dr_nomet_nolpt,
        #:bdt_sig_bg_dr_nomet_lpt,
        #:bdt_sig_bg_dr_met_nolpt,
        #:bdt_sig_bg_dr_met_lpt,
#        :ljet_eta,
        (:abs_ljet_eta, row::DataFrameRow -> abs(row[:ljet_eta])),
        (:abs_ljet_eta_16, row::DataFrameRow -> abs(row[:ljet_eta])),
        :top_mass
    ]
else
    error("Unknown VARS_TO_USE=$VARS_TO_USE")
end

const SOLTYPE = symbol(PARS["soltype"])

#default transfer matrix shortcut
const TM = defaults[:transfer_matrix]

#vector of transfer matrix dimensions
const TM_hsize = tuple([length(ed) for ed in TM.edges]...)

include("$BASE/src/skim/jet_cls.jl")

#returns the object corresponding to key x from the dictionary ret
#if ret[x] does not exist, it is created according to defaults_func[k](),
#where k is a key specifying the description of the object to create
function getr{K <: Any, V <: Any}(ret::Dict{K, V}, x::HistKey, k::Symbol)
    if !haskey(ret, x)
        ret[x] = defaults_func[k]()::V
    end
    return ret[x]::Union(Histogram, NHistogram)
end

function print_ev(row)
    println("hlt=", row[:hlt], " Nj=", row[:njets], " Nt=", row[:ntags], " nsigmu=", row[:n_signal_mu], " nsigele=", row[:n_signal_ele],
        " nvetomu=", row[:n_veto_mu], " nvetoele=", row[:n_veto_ele], " bdt_qcd=", row[:bdt_qcd], " bdt_sig_bg=", row[:bdt_sig_bg],
        " ljet_dr=", row[:ljet_dr], " bjet_dr=", row[:bjet_dr],
    )
end

function fill_histogram(
    nw::Float64, #nominal weight value
    row::DataFrameRow, #present data row
    isdata::Bool, #data or MC?
    hname::Symbol, #name of the histogram
    hex::Function, #function row->Real used to fill the histogram
    ret::Dict, #the reference to the dict of all the histograms

    sample::Symbol,
    iso::Symbol,
    systematic::Symbol,
    selection_major::Symbol,
    selection_minor::Symbol,
    lepton::Symbol,
    njets::Int64,
    ntags::Int64,

    )

    #value to be filled to histogram
    const x = hex(row)

    #get the index of the bin to be filled.
    #this is the same regardless of the systematic scenario or weight
    const bin = findbin(defaults[hname]::Histogram, x)::Int64

    #loop over all the systematic scenarios
    for (scname, scenario::Scenario) in scenarios
        #println(scname)
        if (iso == :antiiso && (scname == (:qscale_me_weight__up,:tchan) || scname == (:qscale_me_weight__down,:tchan) || scname == (:qscale_me_weight__up,:ttjets) || scname == (:qscale_me_weight__down,:ttjets) || scname == (:qscale_me_weight__up,:wjets) || scname == (:qscale_me_weight__down,:wjets)))
            #println(scname)
            #not there in antiiso
            continue
        end
        #get the type of weighting to be applied
        const w_scenario = scenario.weight_scenario

        #scenario not defined for this sample
        if !((sample == scenario.sample) || get_process(sample)::Symbol==scenario.sample::Symbol)
            VERBOSE && println("skipping sample=$sample scenario.sample=$(scenario.sample) process=$(get_process(sample))")
            continue
        end

        #scenario not defined for this systematic processing
        if systematic != scenario.systematic
            VERBOSE && println("skipping systematic=$systematic scenario.systematic=$(scenario.systematic)")
            continue
        end

        if HISTS_NOMINAL_ONLY && !(
                w_scenario==:nominal || w_scenario==:unweighted
            )
            VERBOSE && println("skipping nominal_only=$w_scenario")
            continue
        end

        if haskey(SingleTopBase.SYSTEMATICS_TABLE, w_scenario)
            const wname = SingleTopBase.SYSTEMATICS_TABLE[w_scenario]
        else
            const wname = w_scenario
        end

        if !((sample == scenario.sample) || get_process(sample)::Symbol==scenario.sample::Symbol)
            VERBOSE && println("skipping sample=$sample scenario.sample=$(scenario.sample) process=$(get_process(sample))")
            continue
        end
        
        const kk = HistKey(
            hname,
            sample,
            iso,
            systematic,
            wname,
            selection_major,
            selection_minor,
            lepton,
            njets,
            ntags,
        )
        VERBOSE && println("passing=$kk")

        #get the histogram for this sample, systematic scenario
        h = getr(ret, kk, hname)::Histogram

        const w = scenario.weight(nw, row)::Union(NAtype, Float64)
        (isnan(w) || isna(w)) && error("$kk: w=$w $(df[row.row, :])")

        #fill the histogram
        h.bin_contents[bin] += w
        h.bin_entries[bin] += 1

        #fill W+jets jet flavours separately as well
        if get_process(sample) == :wjets || get_process(sample) == :dyjets || get_process(sample) == :wjets_fsim
            for cls in jet_classifications
                const ev_cls = row[:jet_cls] |> jet_cls_from_number
                ev_cls == cls || continue

                ev_cls = jet_cls_bcl(ev_cls)
                #println(symbol("$(sample)_$(ev_cls)"))
                const kk = HistKey(
                    hname,
                    symbol("$(sample)_$(ev_cls)"),
                    iso,
                    systematic,
                    wname,
                    selection_major,
                    selection_minor,
                    lepton,
                    njets,
                    ntags,
                )

                h = getr(ret, kk, hname)::Histogram

                const w = scenario.weight(nw, row)::Union(NAtype, Float64)

                (isnan(w) || isna(w)) && error("$kk: w=$w $(df[row.row, :])")
                #fill the histogram
                h.bin_contents[bin] += w
                h.bin_entries[bin] += 1
            end
        end
    end

    if get_process(sample) == :wjets || get_process(sample) == :dyjets
        for cls in jet_classifications
            const ev_cls = row[:jet_cls] |> jet_cls_from_number
            ev_cls == cls || continue

            ev_cls = jet_cls_bcl(ev_cls)

            #W+jets heavy/light flavour reweighting
            for wdir in [:up, :down]
                const kk = HistKey(
                    hname,
                    symbol("$(sample)_$(ev_cls)"),
                    iso,
                    systematic,
                    symbol("wjets_flavour_$(ev_cls)__$(wdir)"),
                    selection_major,
                    selection_minor,
                    lepton,
                    njets,
                    ntags,
                )

                h = getr(ret, kk, hname)::Histogram
                const w = nw * wjets_weights[ev_cls][wdir]

                h.bin_contents[bin] += w
                h.bin_entries[bin] += 1
            end
        end
    end

    #fill QCD anti-iso range variation systematic
    if iso == :antiiso
        liso = row[:lepton_iso]
        for wdir in [:up, :down]
            if (liso >= lepton_iso_limits[lepton][wdir][1] && liso <= lepton_iso_limits[lepton][wdir][2])
                const kk = HistKey(
                    hname,
                    sample,
                    iso,
                    systematic,
                    symbol("qcd_antiiso__$(wdir)"),
                    selection_major,
                    selection_minor,
                    lepton,
                    njets,
                    ntags,
                )
                h = getr(ret, kk, hname)::Histogram
                h.bin_contents[bin] += nw
                h.bin_entries[bin] += 1
            end
        end

    end
end

#selection function
sel(row::DataFrameRow, nj=2, nt=1) = (Cuts.njets(row, nj) & Cuts.ntags(row, nt) & Cuts.dr(row))::Bool

fails = {:qcd=>0, :jet_tag=>0}

function process_df(rows::AbstractVector{Int64})
    const t0 = time()
    tprev = time()

    println("mapping across $(length(rows)) rows")

    nproc = 0

    nfsel = 0

    const ret = Dict{HistKey, Any}()

    for cur_row::Int64 in rows
        #println("row=$cur_row")
        #get entries corresponding to current row in TTrees
        for sdf in df.dfs
            #CMSSW.getentry!(sdf.tree, cur_row)
            load_row(sdf, cur_row)
        end

        const row = DataFrameRow(df, cur_row)
        nproc += 1
        if nproc % 10000==0
            dt = time() - tprev
            println("N $nproc $dt $nfsel")
            tprev = time()
        end
        is_any_na(row, :sample, :systematic, :isolation)::Bool &&
            warn("sample, systematic or isolation were NA")

        const sample = hmap_symb_from[row[:sample]::Int64]
        const subsample = hmap_symb_from[row[:subsample]::Int64]
        if hmap_symb_from[row[:systematic]::Int64] == :nominal_scaleweight_fixed
            const systematic = :nominal
        else
            const systematic = hmap_symb_from[row[:systematic]::Int64]
        end
        const iso = hmap_symb_from[row[:isolation]::Int64]
    
        true_lep = sample==:tchan ? row[:gen_lepton_id] : int64(0)
        if isna(true_lep) || true_lep==0
            true_lep = row[:lepton_id]
        end
        #VERBOSE && println("row $cur_row $sample $subsample $systematic $iso genlep=$true_lep")
        # println("row $cur_row $sample $subsample $systematic $iso genlep=$true_lep")

        const isdata = ((sample == :data_mu) || (sample == :data_ele))
        if !isdata && HISTS_NOMINAL_ONLY
            if !((systematic==:nominal)||(systematic==:unknown))
                continue
            end
        end

        ###
        ### transfer matrices
        ###
        const transfer_matrix_reco = {
            :mu=>{k=>false for k in BDT_CUTS},
            :ele=>{k=>false for k in BDT_CUTS}
        }

        #cache nominal weight
        const nw = nominal_weight(row)::Float64

        if DO_TRANSFER_MATRIX && sample==:tchan && iso==:iso

           const x = row[:cos_theta_lj_gen]::Union(Float32, NAtype)
           const y = row[:cos_theta_lj]::Union(Float32, NAtype)
           #println("X & Y ", x, " ", y)
           const ny_ = searchsortedfirst(TM.edges[2], y)

           #can get gen-level index here
           const nx = (isna(x)||isnan(x)) ? 1 : searchsortedfirst(TM.edges[1], x)-1

           const nw = nominal_weight(row)::Float64

           for reco_lep in Symbol[:ele, :mu]

               #did event pass reconstruction ?
               #need to reinitialize for each new cut-tree "branch"
               local reco = true
               reco = reco && !is_any_na(row, :njets, :ntags, :bdt_sig_bg, :n_signal_mu, :n_signal_ele, :n_veto_mu, :n_veto_ele)::Bool
               reco = reco && sel(row)
               reco = reco && Cuts.is_reco_lepton(row, reco_lep)
               reco = reco && Cuts.qcd_cut(row, QCD_CUT_TYPE, reco_lep)
               reco = reco && Cuts.nu_soltype(row, SOLTYPE)
               if IS_TOP
                   reco = reco && Cuts.is_top(row)
               elseif IS_ANTITOP
                   reco = reco && Cuts.is_antitop(row)
               end
               if IS_CT_BIN
                    reco = reco && Cuts.cos_theta_bin(row, WHICH_BIN)                    
               end            
               if DO_LJET_RMS
                   reco = reco && Cuts.ljet_rms(row)
               end
               VERBOSE && println("$reco $x $y")
               #println("RECO $reco $x $y $reco_lep")
               
               const lep_symb = symbol("gen_$(get(LEPTON_SYMBOLS, true_lep, NA))__reco_$(reco_lep)")
               
               for (scen_name::(Symbol, Symbol), scen::Scenario) in scens_gr[systematic]
                   #println(scen_name, " ", scen.weight(nw, row)::Float64)
                   
                   (TM_NOMINAL_ONLY && scen_name[1]!=:nominal) && continue
                   const w = scen.weight(nw, row)::Float64
                   (isnan(w) || isna(w)) && error("$k2: w=$w $(df[row.row, :])")

                   const _prebdtcut_reco = reco
                   #println("RECO1 ", reco)
                   #assumes BDT cut points are sorted ascending
                   for bdt_cut::Float64 in BDT_CUTS::Vector{Float64}
                       const _reco = reco &&
                           Cuts.bdt(row, bdt_cut, BDT_VAR)

                       #if scen_name[1] == :nominal
                       #    transfer_matrix_reco[reco_lep][bdt_cut] = reco
                       #end
                       #println("siin! ",reco," ", _reco, " ", BDT_VAR, " ",Cuts.bdt(row, bdt_cut, BDT_VAR))
                       
                       #need to get the reco-axis index here, it will depend on passing the BDT cut
                       #unreconstructed events are put to underflow bin
                       const ny = (isna(y)||isnan(y)||!_reco) ? 1 : ny_ - 1

                       #get transfer matrix linear index from 2D index
                       const linind = sub2ind(TM_hsize, nx, ny)

                       (linind>=1 && linind<=length(TM.baseh.bin_contents)) ||
                           error("incorrect index $linind for $nx,$ny $x,$y")

                       const k2 = HistKey(
                           :transfer_matrix,
                           subsample,
                           iso,
                           systematic,
                           scen_name[1],
                           :bdt,
                           BDT_SYMBOLS[bdt_cut],
                           lep_symb,
                           2, 1
                       )

                       const h = getr(ret, k2, :transfer_matrix)::NHistogram
                       h.baseh.bin_contents[linind] += w
                       h.baseh.bin_entries[linind] += 1.0
                       
                       # println("Adding $nx,$ny $x,$y $scen_name $w $bdt_cut")
                       # println("$cur_row ", sum(entries(h.baseh)), " ", integral(h.baseh))
                       
                   end
                   
                   reco = _prebdtcut_reco
                   #println("RECO2 ", reco)
                   
                   #cut-based selection
                   for (cut_major, cut_minor, cutfn) in {
                           (:cutbased, :etajprime_topmass_default, Cuts.cutbased_etajprime),
                           (:cutbased, :topmass, Cuts.cutbased_topmass)
                       }
                       const _reco = reco && cutfn(row)
                       const ny = (isna(y)||isnan(y)||!_reco) ? 1 : ny_ - 1
                       const linind = sub2ind(TM_hsize, nx, ny)

                       (linind>=1 && linind<=length(TM.baseh.bin_contents)) ||
                           error("incorrect index $linind for $nx,$ny $x,$y")

                       const k2 = HistKey(
                           :transfer_matrix,
                           subsample,
                           iso,
                           systematic,
                           scen_name[1],
                           cut_major,
                           cut_minor,
                           lep_symb,
                           2, 1
                       )

                       const h = getr(ret, k2, :transfer_matrix)::NHistogram

                       h.baseh.bin_contents[linind] += w
                       h.baseh.bin_entries[linind] += 1.0
                   end
                   #println("RECO3 ", reco)
                   
               end
           end
        end

        ###
        ### lepton reco
        ###
        if is_any_na(row, :n_signal_mu, :n_signal_ele, :n_veto_mu, :n_veto_ele)
            continue
        end

        if Cuts.is_reco_lepton(row, :mu)
            const lepton = :mu
        elseif Cuts.is_reco_lepton(row, :ele)
            const lepton = :ele
        else
            continue
        end

        ###
        ### pre-bdt
        ###
        is_any_na(row, :njets, :ntags, :cos_theta_lj, :bdt_sig_bg) && continue

        #required to cut away mismodeled high-eta region
        (abs(row[:ljet_eta]) < 4.5 && abs(row[:bjet_eta]) < 4.5) || continue
        
        if IS_TOP
            Cuts.is_top(row) || continue
        elseif IS_ANTITOP
            Cuts.is_antitop(row) || continue
        end
        if IS_CT_BIN
            Cuts.cos_theta_bin(row, WHICH_BIN) || continue
            
        end   
        
       #pre-qcd plots
       for (nj, nt) in JET_TAGS
           #pre-bdt selection
           const _reco = sel(row, nj, nt)::Bool
           _reco || continue
           for var in [
               :bdt_qcd,
               :mtw, :met,
               :bdt_sig_bg
          #     :met_phi
           ]
               fill_histogram(
                   nw,
                   row, isdata,
                   var,
                   row->row[var],
                   ret,

                   subsample,
                   iso,
                   systematic,
                   :preqcd,
                   :nothing,
                   lepton,
                   nj, nt
               )
               
           end
       end
       
        if DO_LJET_RMS
            Cuts.ljet_rms(row) || continue
        end
        ###
        ### QCD rejection
        ###
        const reco = Cuts.qcd_cut(row, QCD_CUT_TYPE, lepton)
        if !reco
            fails[:qcd] += 1
            continue
        end
        
        
       ###
       ### project BDT templates and input variables with full systematics
       ###
       for (nj, nt) in JET_TAGS
           #pre-bdt selection
           const _reco = reco && sel(row, nj, nt)::Bool && Cuts.nu_soltype(row, SOLTYPE)
           if !_reco
               fails[:jet_tag] += 1
               continue
           end

           for var in crosscheck_vars

               #if a 2-tuple is specified, 2. arg is the function to apply
               #otherwise, identity
               if isa(var, Tuple)
                   var, f = var
               else
                   var, f = var, (row::DataFrameRow -> row[var])
               end

               fill_histogram(
                   nw,
                   row, isdata,
                   var,
                   row -> f(row),
                   ret,
                   subsample,
                   iso,
                   systematic,
                   :preselection,
                   :nothing,
                   lepton,
                   nj, nt
               )
           end
       end
       

       ###
       ### project BDT templates and input variables with full systematics, reverse BDT cut for fit
       ###
       for (nj, nt) in JET_TAGS
           #pre-bdt selection
           for bdt_cut in BDT_REVERSE_CUTS
               const _reco = reco && sel(row, nj, nt)::Bool && Cuts.nu_soltype(row, SOLTYPE) && Cuts.bdt_reverse(row, bdt_cut, BDT_VAR)
               if !_reco
                   fails[:jet_tag] += 1
                   continue
               end

               for var in crosscheck_vars

                   #if a 2-tuple is specified, 2. arg is the function to apply
                   #otherwise, identity
                   if isa(var, Tuple)
                       var, f = var
                   else
                       var, f = var, (row::DataFrameRow -> row[var])
                   end

                   fill_histogram(
                       nw,
                       row, isdata,
                       var,
                       row -> f(row),
                       ret,
                       subsample,
                       iso,
                       systematic,
                       :preselection,
                       BDT_REVERSE_SYMBOLS[bdt_cut],
                       lepton,
                       nj, nt
                   )
               end
            end
       end

       ###
       ### cut-based cross-check, 2J1T
       ###
       for (nj, nt) in JET_TAGS
           if (reco &&
               Cuts.cutbased_etajprime(row) &&
               sel(row, nj, nt)::Bool &&
               Cuts.nu_soltype(row, SOLTYPE)
           )
               for var in crosscheck_vars

                   #if a 2-tuple is specified, 2. arg is the function to apply
                   #otherwise, identity
                   if isa(var, Tuple)
                       var, f = var
                   else
                       var, f = var, (row::DataFrameRow -> row[var])
                   end

                   fill_histogram(
                       nw,
                       row, isdata,
                       var,
                       f,
                       ret,
                       subsample,
                       iso,
                       systematic,
                       :cutbased,
                       :etajprime_topmass_default,
                       lepton,
                       nj, nt
                   )
               end
           end
       end

        #final selection by BDT
        for (nj, nt) in JET_TAGS
            for bdt_cut in BDT_CUTS

                if (reco &&
                    Cuts.bdt(row, bdt_cut, BDT_VAR) &&
                    sel(row, nj, nt)::Bool &&
                    Cuts.nu_soltype(row, SOLTYPE)
                )
###                    if ((nj==2) && (nt == 1) && (bdt_cut==0.6) && (lepton==:mu))
###                        write(eventids, "$(row[:event]):$(row[:run]):$(row[:lumi]):$(row[:lepton_weight__id]):$(row[:lepton_weight__iso]):$(row[:lepton_weight__trigger]):$(row[:xsweight]):$(row[:pu_weight]):$(row[:top_weight]):$(row[:b_weight]):$(row[:wjets_ct_shape_weight]):$nw\n")
###                    end
                    for var in crosscheck_vars
                        #if a 2-tuple is specified, 2. arg is the function to apply
                        #otherwise, identity
                        if isa(var, Tuple)
                            var, f = var
                        else
                            var, f = var, (row::DataFrameRow -> row[var])
                        end

                        nfsel += 1

                        fill_histogram(
                            nw,
                            row, isdata,
                            var,
                            f,
                            ret,
                            subsample,
                            iso,
                            systematic,
                            :bdt,
                            BDT_SYMBOLS[bdt_cut],
                            lepton,
                            nj, nt
                        )
                    end
                else
                    continue
                end
            end
        end
    end #event loop

    const t1 = time()
    println(
        "processing ", first(rows), ":", last(rows),
        " (N=$(length(rows))) took $(t1-t0) seconds, nfsel=$nfsel"
    )

    return ret

end #function


###
### Process the events
###
tic()
ret = process_df(FIRST_EVENT:LAST_EVENT)
q = toc()

###
### OUTPUT
###
tic()
tempf = mktemp()[1]
rfile = string(splitext(outfile)[1], ".root")
println("saving to $rfile, temp file $tempf")
mkpath(dirname(rfile))
tf = TFile(convert(ASCIIString, tempf), "RECREATE")
Cd(tf, "")
for (k, v) in ret
    typeof(k) <: HistKey || continue
#    dn = "$(k.object)/$(k.iso)/$(k.lepton)/$(k.selection_major)/$(k.selection_minor)/$(k.njets)/$(k.ntags)/$(k.systematic)/$(k.scenario)/$(get_process(k.sample))"
#    mkpath(tf, dn)
    #println(
    #    k, " sument=$(sum(entries(v))) ",
    #    @sprintf(" int=%.2f", integral(v)),
    #    @sprintf(" sumerr=%.2f", sum(errors(v)))
    #)
    #isa(v, Histogram) && println(v)

    hi = to_root_z(v, tostr(k))
    #hi = to_root(v, string(k.sample))
end

println("projected $(length(ret)) objects in $q seconds")
print("writing...");Write(tf);q=toq();println("done in $q seconds")

#skipping TFile::Close
Close(tf)

for i=1:5
    try
        println("cleaning $rfile...");isfile(rfile) && rm(rfile)
        mkpath(dirname(rfile))
        println("copying...");cp(tempf, rfile)
        s = stat(rfile)
        #run(`sync`)
        s.size == 0 && error("file corrupted")
        break
    catch err
        println("$err: retrying")
        sleep(5)
    end
end

println(fails)
println("cleaning $tempf...");rm(tempf)

#gROOT.process_line("gROOT->GetListOfFiles()->Remove((TFile*)$(uint64(tf.p)));");
