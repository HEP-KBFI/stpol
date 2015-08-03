from FitGroup import *

"""if len(extra) > 0:
            table += " & & & %s: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & \\\\ \n" % (temp.replace("_","-"), sf, delta_sf, nonqcd_yield, yield_var, nonqcd_yield_cut, yield_var_cut)
        else:
            table += " & & %s: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & \\\\ \n" % (temp.replace("_","-"), sf, delta_sf, nonqcd_yield, yield_var, nonqcd_yield_cut, yield_var_cut)

if not extra is None and len(extra) > 0:
        table = "%s & %s & %s & %s & QCD: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & $%.1f$ \\\\ \n" % (display_var, channel, region, extra_string, qcd_result[0], abs(qcd_result[1]), qcd_yield, yield_var, qcd_yield_cut, yield_var_cut, chi2)
    else:
        table = "%s & %s & %s & QCD: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & $%.1f$ \\\\ \n" % (display_var, channel, region, qcd_result[0], abs(qcd_result[1]), qcd_yield, yield_var, qcd_yield_cut, yield_var_cut, chi2)
"""




def make_results_tables(results, groups):
    tables = ""
    for group in groups:
        table = ""
        table += make_header(groupings[group])
        table += make_table(results, groupings[group])
        table += make_footer(groupings[group])
        tables += table + "\n"
    print tables

def make_header(group):
    table = "\\begin{table}[h]\n"
    table += "\\begin{center}\n"
    table += "\\begin{tabular}{ %s } \n" % group.columns
    table += "\\hline\n"
    table += group.header
    table += "\\hline\n"
    return table

def make_footer(group):
    table = "\\end{tabular}\n"
    table += "\\caption{%s}\n" % group.caption
    table += "\\end{center}\n"
    table += "\\end{table}\n"
    return table


def make_table(results, group):
    name = group.name
    if name == "nominal":
        return make_table_nominal(results, group)
    elif name == "nocut":
        return make_table_nominal(results, group, cut = "nocut")
    elif name == "qcdcut":
        return make_table_nominal(results, group, cut = "qcdcut")
    elif name == "isovar":
        return make_table_extra(results, group, extra="isovar")
    elif name == "varMC":
        return make_table_extra(results, group, extra="varMC")
    elif name == "metmtw":
        return make_table_metmtw(results, group)
    elif name == "metmtw_qcdcut":
        return make_table_metmtw(results, group, cut="qcdcut")
    elif name in ["qcd_mva_nomet", "bdt_qcd_dphis_nomet", "bdt_qcd_dphis_withmet"]:
        return make_table_nominal(results, group, cut = "nocut", var = name)
    elif name in ["qcd_mva_nomet_qcdcut", "bdt_qcd_dphis_nomet_qcdcut", "bdt_qcd_dphis_withmet_qcdcut"]:
        return make_table_nominal(results, group, cut = "qcdcut", var = name.replace("_qcdcut",""))

def make_table_nominal(results, group, cut = "reversecut", var = "qcd_mva"):
    table = ""
    for jt in jt_order:
        for channel in channel_order:
            fit = results[jt+channel+var+cut]
            print fit.result["QCD"]
            print fit.chi2
            table += "%s & %s & QCD: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & $%.1f$ \\\\ \n" % (jt, channel, fit.result["QCD"]["sf"], fit.result["QCD"]["delta_sf"], fit.result["QCD"]["yield"], fit.result["QCD"]["delta_yield"], fit.result["QCD"]["yield_cut"], fit.result["QCD"]["delta_yield_cut"], fit.chi2)
            for comp in fit.result.keys():
                if comp == "QCD": continue
                table += " & & %s: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & \\\\ \n" % (comp.replace("_","-"), fit.result[comp]["sf"], fit.result[comp]["delta_sf"], fit.result[comp]["yield"], fit.result[comp]["delta_yield"], fit.result[comp]["yield_cut"], fit.result[comp]["delta_yield_cut"])
            table += "\\hline\n"
    return table
            
def make_table_extra(results, group, extra="isovar", cut="reversecut"):
    table = ""
    for jt in jt_order:
        for channel in channel_order:
            for variation in ["up", "down"]:
                fit = results[jt+channel+"qcd_mva"+cut+extra+variation]
                table += "%s & %s & %s & QCD: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & $%.1f$ \\\\ \n" % (jt, channel, variation, fit.result["QCD"]["sf"], fit.result["QCD"]["delta_sf"], fit.result["QCD"]["yield"], fit.result["QCD"]["delta_yield"], fit.result["QCD"]["yield_cut"], fit.result["QCD"]["delta_yield_cut"], fit.chi2)
                for comp in fit.result.keys():
                    if comp == "QCD": continue
                    table += " & & & %s: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & \\\\ \n" % (comp.replace("_","-"), fit.result[comp]["sf"], fit.result[comp]["delta_sf"], fit.result[comp]["yield"], fit.result[comp]["delta_yield"], fit.result[comp]["yield_cut"], fit.result[comp]["delta_yield_cut"])
                table += "\\hline\n"
    return table

def make_table_metmtw(results, group, cut="reversecut"):
    table = ""
    for jt in jt_order:
        for channel in channel_order:
            var = "mtw"
            if channel == "ele":
                var = "met"
            for var in ["met", "mtw"]:
                #for v in [1]:
                fit = results[jt+channel+var+cut]
                table += "%s & %s & %s & QCD: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & $%.1f$ \\\\ \n" % (jt, channel, var, fit.result["QCD"]["sf"], fit.result["QCD"]["delta_sf"], fit.result["QCD"]["yield"], fit.result["QCD"]["delta_yield"], fit.result["QCD"]["yield_cut"], fit.result["QCD"]["delta_yield_cut"], fit.chi2)
                for comp in fit.result.keys():
                    if comp == "QCD": continue
                    table += " & & & %s: $%.3f \\pm %.3f$ & $%.0f \\pm %.0f$ & $%.1f \\pm %.1f$ & \\\\ \n" % (comp.replace("_","-"), fit.result[comp]["sf"], fit.result[comp]["delta_sf"], fit.result[comp]["yield"], fit.result[comp]["delta_yield"], fit.result[comp]["yield_cut"], fit.result[comp]["delta_yield_cut"])
                table += "\\hline\n"
    return table






def make_footer_old(channel, jt, extra=""):
    #table = "\\hline\n"
    table = "\\end{tabular}\n"
    if len(extra) > 0:
        table += "\\caption{QCD fit results, %s channel, %s, %s}\n" % (channel, jt, extra)
    else:
        table += "\\caption{QCD fit results, %s channel, %s}\n" % (channel, jt)
    table += "\\end{center}\n"
    table += "\\end{table}\n"
    return table

def make_footer_grouped(extra=""):
    #table = "\\hline\n"
    table = "\\end{tabular}\n"
    if len(extra) > 0:
        table += "\\caption{QCD fit results, %s}\n" % (extra)
    else:
        table += "\\caption{QCD fit results}\n" % (channel, jt)
    table += "\\end{center}\n"
    table += "\\end{table}\n"
    return table

def make_results_tables_old(texs, channels, jettags, fitvars, cuts, extras=[" "]):
    for jt in jettags:
        for channel in channels:
            table = make_header_old()
            for cuttype in cuts:
                for var in fitvars:
                    if channel == "ele" and var == "mtw": continue
                    #for varmc in [" ", "varMC_up", "varMC_down"]:
                    if len(extras) > 0:                    
                        for varmc in extras:    
                            table += texs[channel+jt+var+cuttype+varmc]
                    else:
                        table += texs[channel+jt+var+cuttype]
                    table += "\\hline \n"
            table += make_footer_old(channel, jt)
            print table
            print

def make_results_tables_grouped(texs, channels, jettags, fitvars, cuts, extras=[" "]):
    table = make_header_grouped()
    for jt in jettags:
        for channel in channels:
            for cuttype in cuts:
                for var in fitvars:
                    if channel == "ele" and var == "mtw": continue
                    #for varmc in [" ", "varMC_up", "varMC_down"]:
                    if len(extras) > 0:                    
                        for varmc in extras:    
                            table += texs[channel+jt+var+cuttype+varmc]
                    else:
                        table += texs[channel+jt+var+cuttype]
                    table += "\\hline \n"
    table += make_footer_grouped()
    print table
    print 


def make_results_tables_old(texs, channels, jettags, fitvars, cuts, extras=[]):
    print "extras", extras
    #print texs
    for jt in jettags:
        for channel in channels:
            table = make_header_old()
            for cuttype in cuts:
                for var in fitvars:
                    #if channel == "ele" and jt == "2j0t" and cuttype == "reversecut" and var == "mtw": continue
                    #if channel == "ele" and var == "mtw": continue
                    #for varmc in [" ", "varMC_up", "varMC_down"]:
                    if len(extras) > 0:                    
                        #for varmc in extras:    
                        #    table += texs[channel+jt+var+cuttype+varmc]
                        for ext in extras:
                            table += texs[channel+jt+var+cuttype+ext+"down"]
                            table += texs[channel+jt+var+cuttype+ext+"up"]
                    #else:
                    #print channel, jt, var, cuttype, texs[channel+jt+var+cuttype]
                    #print channel+jt+var+cuttype, 'mu2j1tqcd_mvareversecut', channel+jt+var+cuttype == 'mu2j1tqcd_mvareversecut'
                    #print texs.keys(), 'mu2j1tqcd_mvareversecut' in texs
                    table += texs[channel+jt+var+cuttype]
                    table += "\\hline \n"
            table += make_footer_old(channel, jt)
            print table
            print 

  

