desc="tmp"
i="$1"
size=${#i}
if [ $size>0 ];
then
    desc="_$1"
fi

#output="output_skip"
output="output"
mkdir -p ${output}/added${desc}
cd $output
for channel in "ele"
do
    mkdir -p added${desc}/$channel
    for dataset in "DYJets" "Tbar_tW" "W4Jets_exclusive" "ZZ" "TTJets_FullLept" "T_tW" "Tbar_t_ToLeptons" "T_t_ToLeptons" "W1Jets_exclusive" "TTJets_SemiLept" "Tbar_s" "W2Jets_exclusive" "WW" "T_s" "W3Jets_exclusive" "WZ"
    do
        hadd added${desc}/$channel/${channel}_${dataset}.root pdftest_${channel}_${dataset}_*.root
    done
    #hadd added${desc}/$channel/${channel}_T_t.root pdftest_${channel}_T_t_N*.root pdftest_${channel}_T_t_C*.root pdftest_${channel}_T_t_M*.root
done
