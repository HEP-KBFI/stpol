import os

def read_cross_sections():
    lines = [line.strip() for line in open("/".join([os.environ["STPOL_DIR"], "src", "headers", "cross_sections.txt"]))]
    cross_sections = {}
    for line in lines:
        if len(line) == 0 or "#" in line or "sample" in line:
            continue
        (name, xs) = line.split(",")
        cross_sections[name.replace("\"", "")] = float(xs)
    return cross_sections

def scale_to_lumi(lumi, xs, total_events):
      expected_events = xs * lumi
      scale_factor = float(expected_events)/total_events
      #print lumi, "xs", xs, "exp", expected_events, "total", total_events
      return scale_factor

def replace_name(name):
    x = name.replace("Mu1", "Mu")    
    x = x.replace("Mu2", "Mu")
    x = x.replace("Mu3", "Mu")
    x = x.replace("Mu_miss", "Mu")
    x = x.replace("Ele1", "Ele")
    x = x.replace("Ele2", "Ele")
    x = x.replace("Ele_miss", "Ele")
    return x

def list_to_string(mylist):
    conc = ""    
    for a in mylist:
        conc += a + " "
    return conc

def get_file_list(file_list_file):
    lines = [line.strip() for line in open(file_list_file)]
    return lines

def getEventCount(dataset):
        eventCounts = {}
        eventCounts["T_t_ToLeptons"] = 3915598
        eventCounts["Tbar_t_ToLeptons"] = 1711403
        eventCounts["T_t"] = 3651392
        eventCounts["Tbar_t"] = 1935072
        eventCounts["W1Jets_exclusive"] = 12562714 + 6467533
        eventCounts["W2Jets_exclusive"] = 7423962 + 7354689 + 5808646
        eventCounts["W3Jets_exclusive"] = 3081900 + 3174240 + 3169456 + 3070848 + 164630
        eventCounts["W4Jets_exclusive"] = 2784130 + 2961608 + 2815115 + 3119782
        eventCounts["WJets_inclusive"] = 45092454
        eventCounts["DYJets"] = 18968731
        eventCounts["TTJets_SemiLept"] = 11542049 + 10170892
        eventCounts["TTJets_FullLept"] = 10577636
        eventCounts["TTJets_MassiveBinDECAY"] = 5562714
        eventCounts["T_s"] = 259961
        eventCounts["Tbar_s"] = 139974
        eventCounts["T_tW"] = 497658
        eventCounts["Tbar_tW"] = 493460
        eventCounts["WW"] = 9298332
        eventCounts["WZ"] = 8912443
        eventCounts["ZZ"] = 9214948
        eventCounts["GJets1"] = 5021621
        eventCounts["GJets2"] = 1611963
        eventCounts["QCDMu"] = 3015550
        eventCounts["QCD_Pt_20_30_BCtoE"] = 1713354
        eventCounts["QCD_Pt_250_350_EMEnriched"] = 2822766
        eventCounts["QCD_Pt_350_BCtoE"] = 1441627
        eventCounts["QCD_Pt_80_170_EMEnriched"] = 3233144
        eventCounts["QCD_Pt_170_250_BCtoE"] = 1621439
        eventCounts["QCD_Pt_170_250_EMEnriched"] = 2979462
        eventCounts["QCD_Pt_20_30_EMEnriched"] = 3049395
        eventCounts["QCD_Pt_250_350_BCtoE"] = 1865711
        eventCounts["QCD_Pt_30_80_BCtoE"] = 2048152
        eventCounts["QCD_Pt_30_80_EMEnriched"] = 2845499
        eventCounts["QCD_Pt_350_EMEnriched"] = 3042374
        eventCounts["QCD_Pt_80_170_BCtoE"] = 1522160
        return eventCounts[dataset]

#indir = "/home/andres/single_top/stpol/filelists/Nov29_tW_etabl_CSVT_genwhgt_2fdd84/step2/"
indir = "/home/andres/single_top/stpol_pdf/filelists/Jul4/"
#indir = "/home/andres/single_top/stpol/filelists/343e0a9_Aug22/step2/"
indir_mc = indir + "iso/nominal/"
indir_mc_antiiso = indir + "antiiso/nominal/"
indir_antiiso = indir + "antiiso/"
indir_data = indir + "iso/"

if __name__ == "__main__":
    xs = read_cross_sections()
    for (name, x) in xs.items():
        print name, x

