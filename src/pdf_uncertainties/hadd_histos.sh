desc="tmp"
i="$1"
size=${#i}
if [ $size>0 ];
then
    desc="$1"
fi


mkdir -p merged_histos/${desc}
for channel in "mu" "ele"
do
    for jt in "2j1t" "2j0t" "3j1t" "3j2t"
    do
        for var in "bdt_sig_bg"
        do
            hadd merged_histos/${desc}/${channel}_${var}_${jt}_pdf.root histos/${channel}/${jt}*${var}_pdf.root
        done
        for var in "cos_theta"
        do
            for bdt in "-0.20000" "-0.10000" "0.00000" "0.06000" "0.10000" "0.13000" "0.20000" "0.25000" "0.30000" "0.35000" "0.40000" "0.45000" "0.50000" "0.55000" "0.60000" "0.65000" "0.70000" "0.75000" "0.80000"
            do
                hadd merged_histos/${desc}/${channel}_${var}_${jt}_${bdt}_pdf.root histos/${channel}/${jt}*${var}_cut_${bdt}_pdf.root
            done
        done
    done
done
