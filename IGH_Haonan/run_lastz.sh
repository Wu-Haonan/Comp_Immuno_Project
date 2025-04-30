#!/bin/bash

SAMPLES=("Macaca_nemestrina-hap2" "Macaca_nemestrina-hap1" "Macaca_thibetana" "Macaca_fascicularis" Papio_papio)

for SAMPLE in "${SAMPLES[@]}"; do
    echo "Running LASTZ for $SAMPLE..."

    lastz ./IGdetective_Predict_IGHs/${SAMPLE}_IGH.fasta[multiple] \
        --filter=identity:90 --filter=coverage:30 \
        ./RepeatRegion/Repeat_all.fasta \
        --format=general:name1,start1,end1,name2,start2,end2,strand2,identity,score \
        > ./Repeat_Map/${SAMPLE}_IGH.txt
done



