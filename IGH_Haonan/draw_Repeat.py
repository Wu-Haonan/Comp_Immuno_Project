import os
from Bio import SeqIO
from dna_features_viewer import GraphicFeature, GraphicRecord


color_map = {"RepeatA": "#ff9999", "RepeatB": "#99ccff", "RepeatC": "#99ff99"}

repeat_map_dir = "Repeat_Map"
igdetective_dir = "IGdetective_Predict_IGHs"
output_dir = "Visualizations"
os.makedirs(output_dir, exist_ok=True)


for filename in os.listdir(repeat_map_dir):
    if not filename.endswith(".txt"):
        continue

    prefix = filename.replace(".txt", "")
    fasta_file = os.path.join(igdetective_dir, f"{prefix}.fasta")
    txt_file = os.path.join(repeat_map_dir, filename)

    record = next(SeqIO.parse(fasta_file, "fasta"))

    features = []
    min_start, max_end = float('inf'), 0

    with open(txt_file, 'r') as f:
        next(f)  
        for line in f:
            cols = line.strip().split()
            name1, start1, end1, name2, start2, end2 = cols[0], int(cols[1]), int(cols[2]), cols[3], cols[4], cols[5]

            feature_label = f"{name2} ({start2}-{end2})"
            min_start = min(min_start, start1)
            max_end = max(max_end, end1)

            features.append(GraphicFeature(start=start1, end=end1, strand=+1,
                                           label=feature_label,
                                           color=color_map.get(name2, "#cccccc")))

    adjusted_features = [
        GraphicFeature(
            start=f.start - min_start,
            end=f.end - min_start,
            strand=f.strand,
            label=f.label,
            color=f.color
        ) for f in features
    ]

    graphic_record = GraphicRecord(sequence_length=max_end - min_start,
                                   features=adjusted_features)

    ax, _ = graphic_record.plot(figure_width=12)
    ax.set_title(prefix, fontsize=14)

    output_path = os.path.join(output_dir, f"{prefix}_annotation.png")
    ax.figure.savefig(output_path, dpi=300)
    print(f"Visualization saved for {prefix}: {output_path}")
