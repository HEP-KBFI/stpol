include ../analysis/Makefile.options

#INDIR=../../results/hists/Aug26_tchpt/bdt_scan/hists/
INDIR=output_plots/bdt_scan/hists/
OUTDIR=../../results/hists/raw_Jul11_plots/merged

all: merge merge2 merge3 merge4
clean:
	rm -Rf $(OUTDIR)


test:
	julia evloop2.jl test.txt infile.json 0 10000 /hdfs/local/joosep/stpol/skims/step3_v2/Jul4_newsyst_newvars_metshift/iso/nominal/T_t_ToLeptons/837/output.root

merge:
	@for lep in mu ele; do \
	  for var in $(INDIR)/preselection/2j_1t/$$lep/*.root; do \
		fn=`basename $${var} .root` ; \
		if [ "$$fn" = "bdt_sig_bg" ]; then \
			python regroup.py $$var $(OUTDIR)/preselection/2j_1t/$$lep/merged/$${fn}__nopdf.root $$lep 2j1t fit ; \
		else \
			python regroup.py $$var $(OUTDIR)/preselection/2j_1t/$$lep/merged/$${fn}.root $$lep 2j1t fit ; \
		fi ; \
        #python regroup.py $$var $(OUTDIR)/reverseBDT/2j_1t/$$lep/merged/$$fn $$lep 2j1t fit ; \
	  done ; \
	  for var in $(INDIR)/preselection/3j_2t/$$lep/*.root; do \
		fn=`basename $${var} .root` ; \
		if [ "$$fn" = "bdt_sig_bg" ]; then \
			python regroup.py $$var $(OUTDIR)/preselection/3j_2t/$$lep/merged/$${fn}__nopdf.root $$lep 3j2t fit ; \
		else \
			python regroup.py $$var $(OUTDIR)/preselection/3j_2t/$$lep/merged/$${fn}.root $$lep 3j2t fit ; \
		fi ; \
        #python regroup.py $$var $(OUTDIR)/reverseBDT/3j_2t/$$lep/merged/$$fn $$lep 3j2t fit ; \
	  done ; \
	  for var in $(INDIR)/preselection/2j_0t/$$lep/*.root; do \
		fn=`basename $${var} .root` ; \
		if [ "$$fn" = "bdt_sig_bg" ]; then \
			python regroup.py $$var $(OUTDIR)/preselection/2j_0t/$$lep/merged/$${fn}__nopdf.root $$lep 2j0t fit ; \
		else \
			python regroup.py $$var $(OUTDIR)/preselection/2j_0t/$$lep/merged/$${fn}.root $$lep 2j0t fit ; \
		fi ; \
        #python regroup.py $$var $(OUTDIR)/reverseBDT/3j_2t/$$lep/merged/$$fn $$lep 3j2t fit ; \
	  done ; \
	done

	hadd -f $(OUTDIR)/preselection/2j_1t/mu/merged/bdt_sig_bg.root $(OUTDIR)/preselection/2j_1t/mu/merged/bdt_sig_bg__nopdf.root ../../results/hists/pdf_histos_final/mu_bdt_sig_bg_2j1t_pdf.root
	hadd -f $(OUTDIR)/preselection/3j_2t/mu/merged/bdt_sig_bg.root $(OUTDIR)/preselection/3j_2t/mu/merged/bdt_sig_bg__nopdf.root ../../results/hists/pdf_histos_final/mu_bdt_sig_bg_3j2t_pdf.root
	hadd -f $(OUTDIR)/preselection/2j_1t/ele/merged/bdt_sig_bg.root $(OUTDIR)/preselection/2j_1t/ele/merged/bdt_sig_bg__nopdf.root
	hadd -f $(OUTDIR)/preselection/3j_2t/ele/merged/bdt_sig_bg.root $(OUTDIR)/preselection/3j_2t/ele/merged/bdt_sig_bg__nopdf.root
	hadd -f $(OUTDIR)/preselection/2j_0t/mu/merged/bdt_sig_bg.root $(OUTDIR)/preselection/2j_0t/mu/merged/bdt_sig_bg__nopdf.root
	hadd -f $(OUTDIR)/preselection/2j_0t/ele/merged/bdt_sig_bg.root $(OUTDIR)/preselection/2j_0t/ele/merged/bdt_sig_bg__nopdf.root
	hadd -f $(OUTDIR)/preselection/2j_1t/combined/merged/bdt_sig_bg.root $(OUTDIR)/preselection/2j_1t/mu/merged/bdt_sig_bg.root $(OUTDIR)/preselection/2j_1t/ele/merged/bdt_sig_bg.root
	hadd -f $(OUTDIR)/preselection/3j_2t/combined/merged/bdt_sig_bg.root $(OUTDIR)/preselection/3j_2t/mu/merged/bdt_sig_bg.root $(OUTDIR)/preselection/3j_2t/ele/merged/bdt_sig_bg.root

merge2:
	@for lep in mu ele; do \
	  for var in $(INDIR)/reverseBDT/0.00000/2j_1t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/reverseBDT/0.00000/2j_1t/$$lep/$$fn $$lep 2j1t plot ; \
	  done ; \
	  for var in $(INDIR)/reverseBDT/0.00000/3j_1t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/reverseBDT/0.00000/3j_1t/$$lep/$$fn $$lep 3j1t plot ; \
	  done ; \
	  for var in $(INDIR)/reverseBDT/0.00000/3j_2t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/reverseBDT/0.00000/3j_2t/$$lep/$$fn $$lep 3j2t plot ; \
	  done ; \
	  for var in $(INDIR)/reverseBDT/0.00000/2j_0t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/reverseBDT/0.00000/2j_0t/$$lep/$$fn $$lep 2j0t plot ; \
	  done ; \
	done

    #python regroup.py $(INDIR)/preselection/2j_1t/mu/bdt_sig_bg.root $(OUTDIR)/preselection/2j_1t/mu/merged/bdt_sig_bg__nopdf.root mu 2j1t fit
	#python regroup.py $(INDIR)/preselection/3j_2t/mu/bdt_sig_bg.root $(OUTDIR)/preselection/3j_2t/mu/merged/bdt_sig_bg__nopdf.root mu 3j2t fit
	#python regroup.py $(INDIR)/preselection/2j_1t/ele/bdt_sig_bg.root $(OUTDIR)/preselection/2j_1t/ele/merged/bdt_sig_bg__nopdf.root ele 2j1t fit
	#python regroup.py $(INDIR)/preselection/3j_2t/ele/bdt_sig_bg.root $(OUTDIR)/preselection/3j_2t/ele/merged/bdt_sig_bg__nopdf.root ele 3j2t fit
	for bdt in 0.00000; do \
        python regroup.py $(INDIR)/reverseBDT/$$bdt/2j_1t/mu/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/2j_1t/mu/merged/bdt_sig_bg__nopdf.root mu 2j1t fit ; \
	    python regroup.py $(INDIR)/reverseBDT/$$bdt/3j_2t/mu/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/3j_2t/mu/merged/bdt_sig_bg__nopdf.root mu 3j2t fit ; \
	    python regroup.py $(INDIR)/reverseBDT/$$bdt/2j_1t/ele/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/2j_1t/ele/merged/bdt_sig_bg__nopdf.root ele 2j1t fit ; \
	    python regroup.py $(INDIR)/reverseBDT/$$bdt/3j_2t/ele/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/3j_2t/ele/merged/bdt_sig_bg__nopdf.root ele 3j2t fit ; \
	done ; \

	
	for bdt in 0.00000; do \
		hadd -f $(OUTDIR)/reverseBDT/$$bdt/2j_1t/mu/merged/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/2j_1t/mu/merged/bdt_sig_bg__nopdf.root ; \
		#../../results/hists/pdf_histos_Mar10/mu_bdt_sig_bg_2j1t_pdf.root ; \
	    hadd -f $(OUTDIR)/reverseBDT/$$bdt/3j_2t/mu/merged/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/3j_2t/mu/merged/bdt_sig_bg__nopdf.root ; \
		#../../results/hists/pdf_histos_Mar10/mu_bdt_sig_bg_3j2t_pdf.root ; \
	    hadd -f $(OUTDIR)/reverseBDT/$$bdt/2j_1t/ele/merged/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/2j_1t/ele/merged/bdt_sig_bg__nopdf.root ; \
		#../../results/hists/pdf_histos_Mar10/ele_bdt_sig_bg_2j1t_pdf.root ; \
	    hadd -f $(OUTDIR)/reverseBDT/$$bdt/3j_2t/ele/merged/bdt_sig_bg.root $(OUTDIR)/reverseBDT/$$bdt/3j_2t/ele/merged/bdt_sig_bg__nopdf.root ; \
		#../../results/hists/pdf_histos_Mar10/ele_bdt_sig_bg_3j2t_pdf.root ; \
	done ; \

	@for lep in mu ele; do \
	  for var in $(INDIR)/preselection/2j_1t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preselection/2j_1t/$$lep/$$fn $$lep 2j1t plot ; \
	  done ; \
	  for var in $(INDIR)/preselection/3j_1t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preselection/3j_1t/$$lep/$$fn $$lep 3j1t plot ; \
	  done ; \
	  for var in $(INDIR)/preselection/3j_2t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preselection/3j_2t/$$lep/$$fn $$lep 3j2t plot ; \
	  done ; \
	  for var in $(INDIR)/preselection/2j_0t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preselection/2j_0t/$$lep/$$fn $$lep 2j0t plot ; \
	  done ; \
	done
	
	@for lep in mu ele; do \
	  for var in $(INDIR)/preqcd/2j_1t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preqcd/2j_1t/$$lep/$$fn $$lep 2j1t plot ; \
	  done ; \
	  for var in $(INDIR)/preqcd/3j_1t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preqcd/3j_1t/$$lep/$$fn $$lep 3j1t plot ; \
	  done ; \
	  for var in $(INDIR)/preqcd/3j_2t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preqcd/3j_2t/$$lep/$$fn $$lep 3j2t plot ; \
	  done ; \
	  for var in $(INDIR)/preqcd/2j_0t/$$lep/*.root; do \
		fn=`basename $$var` ; \
		python regroup.py $$var $(OUTDIR)/preqcd/2j_0t/$$lep/$$fn $$lep 2j0t plot ; \
	  done ; \
	done


merge3:
	for bdt in 0.45000; do \
		mkdir -p $(OUTDIR)/$$bdt/mu ; \
		mkdir -p $(OUTDIR)/$$bdt/ele ; \
		mybdt=$$bdt ; \
		cp $(INDIR)/$$bdt/mu/tmatrix*.root $(OUTDIR)/$$bdt/mu/ ; \
		cp $(INDIR)/$$bdt/ele/tmatrix*.root $(OUTDIR)/$$bdt/ele/ ; \
		python regroup.py $(INDIR)/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/$$bdt/mu/merged/cos_theta_lj__nopdf.root mu  2j1t fit ; \
		python regroup.py $(INDIR)/$$bdt/ele/cos_theta_lj.root $(OUTDIR)/$$bdt/ele/merged/cos_theta_lj__nopdf.root ele 2j1t fit ; \
		hadd -f $(OUTDIR)/$$bdt/mu/merged/cos_theta_lj.root $(OUTDIR)/$$bdt/mu/merged/cos_theta_lj__nopdf.root ../../results/hists/pdf_histos_final/mu_cos_theta_2j1t_$${bdt}_pdf.root ; \
		hadd -f $(OUTDIR)/$$bdt/ele/merged/cos_theta_lj.root $(OUTDIR)/$$bdt/ele/merged/cos_theta_lj__nopdf.root ; \
		echo "" ; \
		python regroup.py $(INDIR)/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/$$bdt/mu/cos_theta_lj.root mu  2j1t plot ; \
		python regroup.py $(INDIR)/$$bdt/ele/cos_theta_lj.root $(OUTDIR)/$$bdt/ele/cos_theta_lj.root ele 2j1t plot ; \
		#python regroup.py $(INDIR)/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/$$bdt/mu/merged/cos_theta_lj.root mu  2j1t fit ; \
		#python regroup.py $(INDIR)/$$bdt/ele/cos_theta_lj.root $(OUTDIR)/$$bdt/ele/merged/cos_theta_lj.root ele 2j1t fit ; \
		python regroup.py $(INDIR)/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/$$bdt/mu/cos_theta_lj.root mu  2j1t plot ; \
		python regroup.py $(INDIR)/$$bdt/ele/cos_theta_lj.root $(OUTDIR)/$$bdt/ele/cos_theta_lj.root ele 2j1t plot ; \
		python regroup.py $(INDIR)/2j_0t/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/2j_0t/$$bdt/mu/cos_theta_lj.root mu  2j0t plot ; \
		python regroup.py $(INDIR)/2j_0t/$$bdt/ele/cos_theta_lj.root $(OUTDIR)/2j_0t/$$bdt/ele/cos_theta_lj.root ele 2j0t plot ; \
		python regroup.py $(INDIR)/3j_1t/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/3j_1t/$$bdt/mu/cos_theta_lj.root mu  3j1t plot ; \
		python regroup.py $(INDIR)/3j_1t/$$bdt/ele/cos_theta_lj.root $(OUTDIR)/3j_1t/$$bdt/ele/cos_theta_lj.root ele 3j1t plot ; \
		python regroup.py $(INDIR)/3j_2t/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/3j_2t/$$bdt/mu/cos_theta_lj.root mu  3j2t plot ; \
		python regroup.py $(INDIR)/3j_2t/$$bdt/ele/cos_theta_lj.root $(OUTDIR)/3j_2t/$$bdt/ele/cos_theta_lj.root ele 3j2t plot ; \
		mkdir -p $(OUTDIR)/$$bdt/combined/merged ; \
		hadd -f $(OUTDIR)/$$bdt/combined/merged/cos_theta_lj.root $(OUTDIR)/$$bdt/mu/merged/cos_theta_lj.root $(OUTDIR)/$$bdt/ele/merged/cos_theta_lj.root ; \
		hadd -f $(OUTDIR)/$$bdt/combined/cos_theta_lj.root $(OUTDIR)/$$bdt/mu/cos_theta_lj.root $(OUTDIR)/$$bdt/ele/cos_theta_lj.root ; \
		hadd -f $(OUTDIR)/$$bdt/combined/tmatrix_nocharge__gen_ele.root $(OUTDIR)/$$bdt/mu/tmatrix_nocharge__gen_ele.root $(OUTDIR)/$$bdt/ele/tmatrix_nocharge__gen_ele.root ; \
		hadd -f $(OUTDIR)/$$bdt/combined/tmatrix_nocharge__gen_mu.root $(OUTDIR)/$$bdt/mu/tmatrix_nocharge__gen_mu.root $(OUTDIR)/$$bdt/ele/tmatrix_nocharge__gen_mu.root ; \
		hadd -f $(OUTDIR)/$$bdt/combined/tmatrix_nocharge__gen_tau.root $(OUTDIR)/$$bdt/mu/tmatrix_nocharge__gen_tau.root $(OUTDIR)/$$bdt/ele/tmatrix_nocharge__gen_tau.root ; \
	done

merge4:
	mkdir -p $(OUTDIR)/etajprime_topmass_default/mu
	mkdir -p $(OUTDIR)/etajprime_topmass_default/ele
	cp $(INDIR)/etajprime_topmass_default/mu/tmatrix*.root $(OUTDIR)/etajprime_topmass_default/mu/
	cp $(INDIR)/etajprime_topmass_default/ele/tmatrix*.root $(OUTDIR)/etajprime_topmass_default/ele/
	python regroup.py $(INDIR)/etajprime_topmass_default/mu/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/mu/merged/cos_theta_lj.root mu  2j1t fit
	python regroup.py $(INDIR)/etajprime_topmass_default/ele/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/ele/merged/cos_theta_lj.root ele 2j1t fit
	
	python regroup.py $(INDIR)/etajprime_topmass_default/mu/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/mu/cos_theta_lj.root mu  2j1t plot
	python regroup.py $(INDIR)/etajprime_topmass_default/ele/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/ele/cos_theta_lj.root ele 2j1t plot
	
	python regroup.py $(INDIR)/etajprime_topmass_default/mu/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/mu/merged/cos_theta_lj.root mu  2j1t fit
	python regroup.py $(INDIR)/etajprime_topmass_default/ele/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/ele/merged/cos_theta_lj.root ele 2j1t fit
	
	python regroup.py $(INDIR)/etajprime_topmass_default/mu/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/mu/cos_theta_lj.root mu  2j1t plot
	python regroup.py $(INDIR)/etajprime_topmass_default/ele/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/ele/cos_theta_lj.root ele 2j1t plot
	
	mkdir -p $(OUTDIR)/etajprime_topmass_default/combined/merged
	hadd -f $(OUTDIR)/etajprime_topmass_default/combined/merged/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/mu/merged/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/ele/merged/cos_theta_lj.root
	hadd -f $(OUTDIR)/etajprime_topmass_default/combined/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/mu/cos_theta_lj.root $(OUTDIR)/etajprime_topmass_default/ele/cos_theta_lj.root
	hadd -f $(OUTDIR)/etajprime_topmass_default/combined/tmatrix_nocharge__gen_ele.root $(OUTDIR)/etajprime_topmass_default/mu/tmatrix_nocharge__gen_ele.root $(OUTDIR)/etajprime_topmass_default/ele/tmatrix_nocharge__gen_ele.root
	hadd -f $(OUTDIR)/etajprime_topmass_default/combined/tmatrix_nocharge__gen_mu.root $(OUTDIR)/etajprime_topmass_default/mu/tmatrix_nocharge__gen_mu.root $(OUTDIR)/etajprime_topmass_default/ele/tmatrix_nocharge__gen_mu.root
	hadd -f $(OUTDIR)/etajprime_topmass_default/combined/tmatrix_nocharge__gen_tau.root $(OUTDIR)/etajprime_topmass_default/mu/tmatrix_nocharge__gen_tau.root $(OUTDIR)/etajprime_topmass_default/ele/tmatrix_nocharge__gen_tau.root

.PHONY: test
