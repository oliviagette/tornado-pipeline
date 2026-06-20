# this script converts all .csv.gz files in the 'data_gz' directory to .csv files in the 'data' directory
# the script uses the overall structure of the 'data_gz' and 'data' folders containing 'details', 'fatalities', 
# and 'locations' subfolders to determine where to place the converted files

# imports
import gzip
from pathlib import Path

# setting source and output directories
source = Path('data_gz')
output = Path('data')
subfolders = ['details', 'fatalities', 'locations'] # expected subfolders to help determine output paths

output.mkdir(parents=True, exist_ok=True) # ensure the output directory exists

converted_count = 0 # keep track of how many files are converted

# iterate through all .csv.gz files in the source directory and its subdirectories
for gz_file_path in source.rglob('*.csv.gz'):
    if not gz_file_path.is_file():
        continue

    relative_parent = gz_file_path.parent.relative_to(source)
    output_subfolder = output / relative_parent

    if relative_parent == Path('.') or relative_parent.parts[0] not in subfolders:
        # fallback to keyword matching in the filename
        name_lower = gz_file_path.name.lower()
        matched_folder = next((sub for sub in subfolders if sub in name_lower), None)
        if matched_folder:
            output_subfolder = output / matched_folder
        else:
            output_subfolder = output

    output_subfolder.mkdir(parents=True, exist_ok=True)
    output_path = output_subfolder / gz_file_path.with_suffix('').name

    with gzip.open(gz_file_path, 'rt') as gz_file:
        with open(output_path, 'w', newline='') as csv_file:
            csv_file.write(gz_file.read())

    converted_count += 1

# print number of files converted and where they were written to confirm successful conversion
print(f"Conversion successful! {converted_count} file(s) written under '{output}'.")