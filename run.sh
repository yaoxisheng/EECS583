inputs=("libquantum.part.seq" "mcf.part.seq" "sjeng.part.seq" "wrf.part.seq")
windowSizes=(500)
occurenceThresholds=(3)
for windowSize in "${windowSizes[@]}"
do
	for occurenceThreshold in "${occurenceThresholds[@]}"
	do
	    for input in "${inputs[@]}"
        do
		    ./a.out $input $windowSize $occurenceThreshold > $input"_"$windowSize"_"$occurenceThreshold
		done		
	done		
done	

