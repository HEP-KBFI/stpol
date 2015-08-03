        #!/bin/sh
if [ "x$1" != "x" ]; then fl=`ls -d $1`; else fl=`ls -d WD*|grep -v lumi`; fi
selist="kbfi"
for i in $fl; do 
	echo "Starting: $i"
	if [ -f nobabysit ]; then
			echo "Babysit killer found"
			exit 1
	fi

	# get current status
	#crab -c $i -status > bs.out 2>&1
    crab -c $i -USER.xml_report RReport.xml -status > bs.out 2>&1
	# check if any jobs are in Done state, if so download them and recheck status
	DN=`grep "Done" bs.out | wc|awk '{print $1}'`
	if [ $DN -gt 0 ]; then 
	  echo -n "$DN jobs done, downloading..."
	  crab -c $i -get all >/dev/null 2>&1; 
	  echo "done: "$?
	  crab -c $i -status > bs.out 2>&1
	fi
    TOTALJOBS=`cat bs.out | grep "Total Jobs" | cut -d' ' -f4`
    SUCCESSJOBS=`cat bs.out | grep "Jobs with Wrapper Exit Code : 0" | cut -d' ' -f3`
    echo "Total: "$TOTALJOBS" Exit0: "$SUCCESSJOBS
	ERRLIST=`cat bs.out|grep -A 1 "Exit Code : [1-9]"|grep "List of jobs:"|awk '{print $4}'|xargs echo -n|sed 's+\ +,+g'`
	ABORTLIST=`cat bs.out|grep -A 2 "Aborted"|grep "List of jobs:"|awk '{print $4}'`
	CANCELLED=`cat bs.out|grep -A 1 "jobs Cancelled"|grep "List of jobs"|awk '{print $7}'`
	RESUBMIT=`echo "$ERRLIST,$ABORTLIST,$CANCELLED"|sed 's+,,+,+g'|sed 's+,,+,+g'|sed 's+^,++g;s+,$++g'`
	if [ "x$RESUBMIT" != "x" ]; then
		echo "Resubmit list: $RESUBMIT"
		crab -c $i -forceResubmit $RESUBMIT > bs.out 2&>1
        echo "Resubmit status: "$?
        echo "Resubmit: "`grep "jobs submitted" bs.out`
	fi
	crab -c $i -status > bs.out 2>&1
	CR=`grep "Created" bs.out|wc|awk '{print $1}'`
	if [ $CR -ne 0 ]; then
		crab -c $i -submit 500
		crab -c $i -submit 500
    fi
done

#if [ `ps -efa|grep $i|grep -v grep|grep -v babysit|wc -l` != "0" ]; then
#	echo "|`ps -efa|grep $i|grep -v grep|wc -l`|"
#	ps -efa|grep $i|grep -v grep |wc -l
#	echo "Already processing"
#	continue
#fi
