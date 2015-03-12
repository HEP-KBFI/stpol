def get_varlist(channel):
    varlist = ["met", "C", "top_mass", "top_eta",
        "D", "aplanarity", "isotropy", "thrust", 
        #"bjet_dr", 
        #"bjet_eta", 
        "bjet_mass", 
        #"bjet_phi", 
        "bjet_pt",
        #"ljet_dr", 
        "ljet_eta", 
        "ljet_mass", 
        #"ljet_phi", 
        "ljet_pt",
        #channel+"_pt",
        #channel+"_eta", 
        #channel+"_phi",
        ]
    if channel == "mu":
        varlist.append("mtw")        
    return varlist

def get_varlist_removed(channel):
    """if channel == "mu":
        varlist = ["met", "top_mass", "top_eta",
        "isotropy",
        "ljet_pt",
        ]
        varlist.append(channel+"_mtw")  
    if channel == "ele":
        varlist = ["met", "top_mass", "top_eta",
        "isotropy", "bjet_pt", "ljet_mass"
        ]      
    return varlist"""
    return get_varlist(channel)

def get_checkvars(channel):
    fixed = get_fixed(channel)
    all = get_varlist(channel)
    for f in fixed:
        all.remove(f)
    return all

def get_checkvars_remove(channel):
    removed = get_removed(channel)
    all = get_varlist_removed(channel)
    for f in removed:
        all.remove(f)
    return all

def get_fixed(channel):
    fixed = []
    if channel == "mu":
        #fixed = #["mu_mtw", "met", "isotropy", "c", "ljet_pt", "bjet_pt"]#, "top_mass", "ljet_pt", "ljet_mass"]#, "bjet_mass"] new 0.4
        #fixed = ["mu_mtw", "met", "isotropy", "bjet_pt", "ljet_pt", "aplanarity"]  #new 0.7, cut signal deltar
        #fixed = ["mu_mtw", "met", "isotropy", "bjet_pt", "ljet_pt", "aplanarity"]  #new 0.7, nocut signal deltar
        #fixed = ["mu_mtw", "met", "isotropy", "top_mass", "ljet_pt"]#, "ljet_mass", "bjet_mass"] #old
        fixed = ["mtw", "met", "isotropy", "top_mass", "ljet_pt"]#, "ljet_mass", "bjet_mass"] #old
    if channel == "ele":
        #fixed = ["met", "top_mass", "bjet_pt", "isotropy", "ljet_pt", "ljet_mass", "bjet_mass"]#, "top_eta"] new 0.55
        #fixed = ["met", "top_mass", "bjet_pt", "ljet_mass", "top_eta", "isotropy", "c", "bjet_mass"]  #new 0.5, cut signal deltar
        #fixed = ["met", "top_mass", "bjet_pt", "ljet_mass", "top_eta", "isotropy"]  #new 0.5, nocut signal deltar
        fixed = ["ele_mtw", "met", "top_mass", "bjet_pt", "isotropy", "top_eta"] #old
        fixed = ["met", "top_mass", "bjet_pt", "isotropy", "top_eta"] #old
    """
    if channel == "mu":
        fixed = ["lepton_eta",  
            "bjet_pt", "bjet_eta", "bjet_mass", 
            "ljet_pt", "ljet_eta", "ljet_mass",
            "met", "mtw", "circularity", "isotropy", "thrust",
            "top_mass", "top_pt", "top_eta", "w_mass", "w_pt", "w_eta", 
            #"hadronic_pt", "hadronic_mass",
            "shat_pt", "shat_eta", "shat_phi", "shat_mass"#, "shat", "ht"        
        ]
    if channel == "ele":
        fixed = ["lepton_eta",  
            "bjet_pt", "bjet_eta", "bjet_mass",
            "ljet_pt", "ljet_eta", "ljet_mass",
            "met", "mtw", "C", "circularity", "sphericity", "isotropy", "thrust", "C_with_nu",
            "top_mass", "top_pt", "top_eta", "w_pt", "w_eta", 
            "w_mass", 
            #"hadronic_pt", "hadronic_eta", "hadronic_mass",
            "shat_pt", "shat_eta", "shat_phi", "shat_mass"#, "shat", "ht"        
        ]"""

    return fixed

def get_removed(channel):
    removed = []
    if channel == "mu":
        #removed = ["mu_mtw", "met", "top_mass", "isotropy", "ljet_pt"] old
        #removed = ["mu_mtw", "met", "ljet_pt", "top_mass", "bjet_pt", "c", "aplanarity", "isotropy", "bjet_mass", "thrust"] new 0.7
        #removed = ["mu_mtw", "met", "ljet_pt", "c", "isotropy", "aplanarity", "top_mass", "bjet_pt"]    new 0.4
        removed = ["mu_mtw", "met", "ljet_pt", "top_mass", "bjet_pt", "c"]
    if channel == "ele":
        #removed = ["met", "top_mass", "isotropy", "top_eta"] old
        #removed = ["met", "top_mass", "c", "ljet_pt", "D", "bjet_pt", "top_eta", "isotropy", "aplanarity", "thrust", "bjet_mass"] new 0.55
        #removed = ["met", "top_mass", "thrust", "bjet_pt", "ljet_pt", "top_eta", "isotropy", "c", "aplanarity"]  new 0.4
        removed = ["met", "top_mass", "c", "ljet_pt", "D", "bjet_pt", "top_eta" "isotropy"]
    return removed


def get_extra_vars(channel):
    varlist = varlist = [#"bjet_dr", 
        #"bjet_eta", 
        #"bjet_phi", 
        #"ljet_dr", 
        "ljet_eta", 
        #"ljet_phi", 
        channel+"_pt",
        #channel+"_mtw",
        channel+"_eta", 
        channel+"_phi",
        "iso",
        "cos_theta",
        "cos_theta_bl",
        "qcd_mva"
        ]
    if channel == "ele":
        varlist.append(channel+"_mtw")        
    
    return varlist
