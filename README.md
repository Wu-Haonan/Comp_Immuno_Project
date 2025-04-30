# Comp_Immuno_Project
Course project of Comp Immuno
Study of the Structual Variances among Macaca

## IGH 

### Immuno Loci Annotation 

We run IGdetective to obatain the annotation for Immuno locus of following genomes

[Macaca fascicularis](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_037993035.1/)

[Macaca Nemestrina hap1](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_043159975.1/)

[Macaca Nemestrina hap2](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_043161795.1/)

[Macaca Thibetiana](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_024542745.1/)

[Macaca Cyclopus](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_026956025.1/)

[Papio Papio(Baboon)](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_965153135.1/)

The results of IGH of each genome sequences are shown in `./IGH_Haonan/IGH_macacas_summary.csv`. 

We extract corresponding substrings from the abovle whole genomes and store them in the folder `./IGH_Haonan/IGdetective_Predict_IGHs/`.

### Dotplot

We run [PatchWorkPlot](https://github.com/yana-safonova/PatchWorkPlot) and generate Multiple-dotplot in `./IGH_Haonan/Multi_dotplots/`. We generate another version with keeping all the alignments greater than 20,000 in `./IGH_Haonan/Multi_dotplots_filter/`. 

### Repeat Map

1. Cut Repeat A,B and C

2. Run lastz

   ```
   lastz ./IGdetective_Predict_IGHs/Macaca_nemestrina-hap2_IGH.fasta[multiple] \
     --filter=identity:90 --filter=coverage:30 \
     ./RepeatRegion/Repeat_all.fasta \
     --format=general:name1,start1,end1,name2,start2,end2,strand2,identity,score \
     > ./Repeat_Map/MN_hap2.txt
   ```

   
