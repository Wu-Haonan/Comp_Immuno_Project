import os
import glob
import sys

def filter_alignments_by_length(input_file, min_length=20000):
    """
    Read a TSV file containing alignment data, filter records by length, 
    and write the filtered results back to the same file.
    
    Args:
        input_file (str): Path to the input/output TSV file
        min_length (int): Minimum alignment length to keep (default: 20000)
    
    Returns:
        int: Number of records kept after filtering
    """
    # Read all lines from the file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Parse and filter the lines
    filtered_lines = []
    kept_count = 0
    
    for line in lines:
        # Skip empty lines
        if line.strip() == "":
            continue
            
        # Split the line by tabs
        fields = line.strip().split('\t')
        
        # Check if this is a header line (doesn't contain length info)
        # If it doesn't have enough fields to contain length info, keep it
        if len(fields) < 10:
            filtered_lines.append(line)
            continue
            
        try:
            # Try to extract length values
            # Based on the format, length1 is at index 4 and length2 is at index 9
            length1 = int(fields[4])
            length2 = int(fields[9])
            
            # Keep the record if either length is greater than the minimum
            if length1 > min_length or length2 > min_length:
                filtered_lines.append(line)
                kept_count += 1
        except (ValueError, IndexError):
            # If we can't extract or convert length values, keep the line
            # (it might be a header or differently formatted line)
            filtered_lines.append(line)
    
    # Write the filtered lines back to the file
    with open(input_file, 'w') as f:
        f.writelines(filtered_lines)
    
    return kept_count

def process_directory(directory, min_length=20000):
    """
    Process all TSV files in the given directory, filtering each one.
    
    Args:
        directory (str): Path to the directory containing TSV files
        min_length (int): Minimum alignment length to keep
    """
    # Get all TSV files in the directory
    tsv_files = glob.glob(os.path.join(directory, "*.tsv"))
    
    if not tsv_files:
        print(f"No TSV files found in directory: {directory}")
        return
    
    print(f"Found {len(tsv_files)} TSV files in {directory}")
    
    total_processed = 0
    total_kept = 0
    
    # Process each TSV file
    for tsv_file in tsv_files:
        print(f"Processing {tsv_file}...")
        kept_count = filter_alignments_by_length(tsv_file, min_length)
        total_kept += kept_count
        total_processed += 1
        print(f"  - Kept {kept_count} records with alignment length > {min_length}")
    
    print(f"\nSummary:")
    print(f"- Total TSV files processed: {total_processed}")
    print(f"- Total records kept: {total_kept}")
    print(f"- Filtering criteria: alignment length > {min_length}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        min_length = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
        process_directory(directory, min_length)
    else:
        print("Usage: python filter_alignments_dir.py <directory> [min_length]")
        print("Example: python filter_alignments_dir.py ./data 20000")