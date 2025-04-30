#!/bin/bash

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <input_fasta> <chromosome_id> <start> <end> <output_fasta>"
    echo "Example: $0 input.fa NC_088381.1 174027159 176010037 output.fa"
    exit 1
fi

input=$1
chrom=$2
start=$3
end=$4
output=$5

echo "Looking for sequence: >$chrom in $input"

awk -v target=">$chrom" '
BEGIN { found=0; printing=0; }
/^>/ { 
    if (found && printing) { 
        printing=0; 
        exit;
    }
    if ($0 ~ target) { 
        found=1; 
        printing=1; 
        header=$0;
    } else {
        printing=0;
    }
}
printing==1 { print }
' "$input" > temp.fa

if [ ! -s temp.fa ]; then
    echo "Error: No sequence found matching >$chrom"
    exit 1
fi


header=$(head -n 1 temp.fa)
echo "Found header: $header"

tail -n +2 temp.fa | tr -d '\n\r\t ' > seq.tmp


seq_len=$(wc -c < seq.tmp)
echo "Original sequence length: $seq_len"


if [ "$start" -lt 1 ] || [ "$end" -gt "$seq_len" ]; then
    echo "Warning: Region $start-$end may be outside sequence bounds (1-$seq_len)"
fi


cut -c${start}-${end} seq.tmp > extract.tmp


echo "$header region:$start-$end" > "$output"


fold -w 60 extract.tmp >> "$output"

echo "Created FASTA file: $output"


rm temp.fa seq.tmp extract.tmp