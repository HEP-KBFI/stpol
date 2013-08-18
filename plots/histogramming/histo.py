#!/usr/bin/env python
"""
A simple script to create one or several fully reweighed analysis histograms using tree.py
"""
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import tree
#tree.logger.setLevel(logging.DEBUG)
from plots.common.cuts import Cuts, Weights
import networkx as nx
import argparse


def analysis_tree_all_reweighed(cuts, infiles, outfile, **kwargs):
    out = tree.ObjectSaver(outfile)
    graph = nx.DiGraph()

    #top = tree.Node(graph, "top", [], [])
    snodes = [tree.SampleNode(out, graph, inf, [], []) for inf in infiles]

    logger.info("Done constructing sample nodes: %d" % len(snodes))

    cutnodes = []
    for cut_name, cut in cuts:
        cutnodes.append(
            tree.CutNode(cut, graph, cut_name, snodes, [])
        )

    from histo_descs import create_plots
    create_plots(graph, cutnodes, **kwargs)

    try:
        nx.write_dot(graph, outfile.replace(".root", "_gviz.dot"))
    except Exception as e:
        logger.warning("Couldn't write .dot file for visual representation of analysis: %s" % str(e))
    
    return snodes, out


if __name__=="__main__":

    parser = argparse.ArgumentParser(
        description='Produces a hierarchy of histograms corresponding to cuts and weights.'
    )

    parser.add_argument('outfile', action='store',
        help="The output file name."
    )

    parser.add_argument('infiles', nargs='+',
        help="The input file names"
    )

    args = parser.parse_args()

    cuts = [
        # ("2j0t", Cuts.mt_mu()*Cuts.n_jets(2)*Cuts.n_tags(0)*Cuts.lepton("mu")*Cuts.hlt("mu")),
        # ("2j1t", Cuts.mt_mu()*Cuts.n_jets(2)*Cuts.n_tags(1)*Cuts.lepton("mu")*Cuts.hlt("mu")),
        ("final_cb_2j1t", Cuts.lepton("mu")*Cuts.hlt("mu")*Cuts.final(2,1))
    ]

    #Construct the analysis chain
    snodes, out = analysis_tree_all_reweighed(
        cuts, args.infiles,
        args.outfile,
        filter_funcs=[
            #lambda x: "mva" not in x
        ]
    )

    print "Recursing down"
    for sn in snodes:
        sn.recurseDown()
    out.tfile.close()