
const nb_reco = 20

const binnings = {
    :cos_theta_lj => {
        :gen => infb(linspace(-1, 1, int(nb_reco/2) + 1)),
        :reco => infb(linspace(-1, 1, int(nb_reco) + 1)),
    },
    :bdt => infb(linspace(-1, 1, 21)),
}

#functions to make default histograms
#these are called when a necessary histogram was not found in the database
const defaults_func = {

    :ljet_pt => () -> Histogram(infb(linspace(40, 310, 31))),
    :bjet_pt => () -> Histogram(infb(linspace(40, 310, 31))),

    :cos_theta_lj_tm => () -> Histogram(binnings[:cos_theta_lj][:reco]),
    :cos_theta_lj_tm_gen => () -> Histogram(binnings[:cos_theta_lj][:gen]),
    :cos_theta_lj => () -> Histogram(infb(linspace(-1, 1, int(nb_reco*2) + 1))),
    :cos_theta_bl => () -> Histogram(binnings[:cos_theta_lj][:reco]),
    :cos_theta_lj_gen => () -> Histogram(infb(linspace(-1, 1, int(nb_reco) + 1))),
    :cos_theta_bl_gen => () -> Histogram(binnings[:cos_theta_lj][:gen]),
    :bdt_sig_bg => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_dr_nomet_nolpt => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_dr_nomet_lpt => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_dr_met_lpt => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_dr_met_nolpt => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_mixed => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_before_reproc => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_old => () -> Histogram(binnings[:bdt]),
    :bdt_sig_bg_top_13_001 => () -> Histogram(infb(linspace(-1, 1, 21))),
    :bdt_qcd => () -> Histogram(infb(linspace(-1, 1.0, 21))),
    :bdt_qcd_dphis_nomet => () -> Histogram(infb(linspace(-1, 1.0, 21))),
    :bdt_qcd_dphis_withmet => () -> Histogram(infb(linspace(-1, 1.0, 21))),
    :bdt_qcd_mixed => () -> Histogram(infb(linspace(-1, 1.0, 21))),
    :bdt_qcd_before_reproc => () -> Histogram(infb(linspace(-1, 1.0, 21))),
    :bdt_qcd2 => () -> Histogram(infb(linspace(-1, 1.0, 21))),

    :lepton_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :jet1_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),


    :C => () -> Histogram(infb(linspace(0, 1, 31))),
    :C_21 => () -> Histogram(infb(linspace(0, 1, 21))),
    :C_signalregion => () -> Histogram(infb(linspace(0, 0.3, 31))),

    :shat => () -> Histogram(infb(linspace(150, 1200, 31))),
    :ht => () -> Histogram(infb(linspace(80, 400, 31))),

    :met_phi => () -> Histogram(infb(linspace(-3.2, 3.2, 31))),

    :transfer_matrix => () -> NHistogram({
        binnings[:cos_theta_lj][:gen],
        binnings[:cos_theta_lj][:reco]
    }),
    :abs_ljet_eta => () -> Histogram(infb(linspace(0, 5, 31))),
    :abs_ljet_eta_16 => () -> Histogram(infb(linspace(0, 4.5, 16))),
    :abs_bjet_eta => () -> Histogram(infb(linspace(0, 5, 31))),

    :ljet_eta => () -> Histogram(infb(linspace(-5, 5, 31))),
    :bjet_eta => () -> Histogram(infb(linspace(-5, 5, 31))),

    :lepton_iso => () -> Histogram(infb(linspace(0, 0.3, 60))),

    :lepton_eta => () -> Histogram(infb(linspace(-3, 3, 60))),

    :ljet_dr => () -> Histogram(infb(linspace(0, 2, 31))),
    :bjet_dr => () -> Histogram(infb(linspace(0, 2, 31))),

    :ljet_met_dr => () -> Histogram(infb(linspace(0, 6, 61))),
    :bjet_met_dr => () -> Histogram(infb(linspace(0, 6, 61))),
    :sjet1_met_dr => () -> Histogram(infb(linspace(0, 6, 61))),
    :sjet2_met_dr => () -> Histogram(infb(linspace(0, 6, 61))),
    :jet1_met_dr => () -> Histogram(infb(linspace(0, 6, 61))),
    :jet2_met_dr => () -> Histogram(infb(linspace(0, 6, 61))),
    :lepton_met_dr => () -> Histogram(infb(linspace(0, 6, 61))),
    
    :ljet_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :bjet_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :jet1_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :jet2_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),

    :ljet_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :bjet_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :sjet1_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :sjet2_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :jet1_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :jet2_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    :lepton_met_dphi => () -> Histogram(infb(linspace(-4, 4, 41))),
    
    :mtw => () -> Histogram(infb(linspace(0, 200, 31))),

    :lepton_pt => () -> Histogram(infb(linspace(25, 200, 31))),
    :lepton_eta => () -> Histogram(infb(linspace(-5, 5, 31))),
    :abs_lepton_eta => () -> Histogram(infb(linspace(0, 5, 31))),

    :bjet_pt => () -> Histogram(infb(linspace(40, 310, 31))),
    :bjet_mass => () -> Histogram(infb(linspace(40, 150, 31))),
    :ljet_mass => () -> Histogram(infb(linspace(40, 150, 31))),

    :top_mass => () -> Histogram(infb(linspace(70, 400, 31))),
    :top_mass_signalregion => () -> Histogram(infb(linspace(120, 230, 31))),

    :top_pt => () -> Histogram(infb(linspace(0, 400, 31))),
    :n_good_vertices => () -> Histogram(infb(linspace(0, 50, 51))),
    :met => () -> Histogram(infb(linspace(0, 200, 31))),

    :nu_soltype => () -> Histogram(infb([-1, 0, 1])),
    :njets => () -> Histogram(infb([-1, 0, 1, 2, 3, 4, 5, 6])),
    :ntags => () -> Histogram(infb([-1, 0, 1, 2, 3, 4, 5, 6])),

    :lepton_charge => () -> Histogram(infb([-2, 0, 2])),

    :bjet_bd_b => () -> Histogram(infb(linspace(0, 1.0, 21))),
    :ljet_bd_b => () -> Histogram(infb(linspace(0, 1.0, 21))),
}

#default histograms
const defaults = Dict{Symbol, Any}()
for (k, v) in defaults_func
    defaults[k] = v()
end

include("histkey.jl")
