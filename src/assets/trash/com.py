import os
import subprocess

# Define the directory containing the .ogg files
directory = '.'

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file ends with .ogg
    if filename.endswith('.ogg'):
        # Create the new filename by replacing .ogg with .wav
        new_filename = filename[:-4] + '.wav'
        
        # Construct the full file paths
        input_path = os.path.join(directory, filename)
        output_path = os.path.join(directory, new_filename)
        
        # Run the ffmpeg command
        subprocess.run(['ffmpeg', '-i', input_path, output_path])

print("Conversion complete!")
