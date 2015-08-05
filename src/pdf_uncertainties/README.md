Running the PDF histogram creation

# 1. Make event lists passing selection (pre-QCD cut, pre signal BDT cut, final selection)
submit_eventlists.py submits the jobs
Code is contained in save_events.py, step3 output specified in parse_input.py is used

# 2a. Make histograms in the regular way - applies to CT10 and MSTW PDF-sets
submit_jobs.py submits the jobs
Code in pdf_eventloop.py

# 2b. special treatment for NNPDF
    1) submit_weightlists2.py
    2) submit_cutoffs.py

# 3 Add ouput together
hadd.sh

# 4. Make histograms
make_histograms.py

# 5. Add histograms together
hadd_histos.py 
