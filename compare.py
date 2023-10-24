import os
import re

# Define the two directories
directory1 = os.getcwd()
directory2 = f"{directory1}/Reencode/"

# List files in both directories
files1 = os.listdir(directory1)
files2 = os.listdir(directory2)

# Create a set of filenames in each directory for faster comparison
file_set1 = set(files1)
file_set2 = set(files2)

pattern = re.compile(r'S\d{2}E\d{2}')

# Create a dictionary to store the extracted formats from the secondary directory
formats_in_directory2 = {}

# Extract "SyyEzz" formats from filenames in the secondary directory
for filename2 in files2:
    match2 = pattern.search(filename2)
    if match2:
        format2 = match2.group()
        formats_in_directory2[format2] = filename2

# Loop through files in the primary directory
total_start_size = total_end_size = 0
print("Negative reduction means file grew, keep original")
for filename1 in files1:
    match1 = pattern.search(filename1)
    if match1:
        format1 = match1.group()
        if format1 in formats_in_directory2:
            file1_path = os.path.join(directory1, filename1)
            file2_path = os.path.join(directory2, formats_in_directory2[format1])

            size1 = round(os.path.getsize(file1_path)/1024/1024)
            size2 = round(os.path.getsize(file2_path)/1024/1024)
            size_char1 = size_char2 ='M'
            total_start_size += size1
            total_end_size += size2

            size_difference = size1 - size2
            percentage_difference = (size_difference / size1) * 100

            if size1 > 974: # 95% of GiB
                size1 = size1 / 1024
                size_char1 = "G"
            if size2 > 974:
                size2 = size2 / 1024
                size_char2 = "G"
            print(f"{format1} Original: {size1:.2f} {size_char1}iB, Reencoded: {size2:.2f} {size_char2}iB, reduction: {percentage_difference:.2f}%")

size_difference = total_start_size - total_end_size
percentage_difference = (size_difference / total_start_size) * 100

size_char1 = size_char2 ='M'
if total_start_size > 974:
    total_start_size = total_start_size / 1024
    size_char2 = "G"
if total_end_size > 974:
    total_end_size = total_end_size / 1024
    size_char2 = "G"
print(f"TOTAL Original: {total_start_size:.2f} {size_char1}iB, Reencoded: {total_end_size:.2f} {size_char2}iB, reduction: {percentage_difference:.2f}%")