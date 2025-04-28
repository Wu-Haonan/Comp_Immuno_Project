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

# 提取匹配的染色体序列（包括头行）
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

# 检查是否找到序列
if [ ! -s temp.fa ]; then
    echo "Error: No sequence found matching >$chrom"
    exit 1
fi

# 获取原始头信息
header=$(head -n 1 temp.fa)
echo "Found header: $header"

# 提取序列（删除头行，并将序列连接成一行）
tail -n +2 temp.fa | tr -d '\n\r\t ' > seq.tmp

# 检查序列长度
seq_len=$(wc -c < seq.tmp)
echo "Original sequence length: $seq_len"

# 验证起始和结束位置
if [ "$start" -lt 1 ] || [ "$end" -gt "$seq_len" ]; then
    echo "Warning: Region $start-$end may be outside sequence bounds (1-$seq_len)"
fi

# 提取指定区域
cut -c${start}-${end} seq.tmp > extract.tmp

# 新的头行：原始头行 + 区域信息
echo "$header region:$start-$end" > "$output"

# 将序列按60个碱基每行格式化
fold -w 60 extract.tmp >> "$output"

echo "Created FASTA file: $output"

# 清理临时文件
rm temp.fa seq.tmp extract.tmp