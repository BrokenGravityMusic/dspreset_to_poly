import sys
import os
import shutil
import xml.etree.ElementTree as ET
import re

# Note: This is hardcoded for the Samples From Mars sample packs. (search From Mars in the code)

# An example. Run from WSL on windows. WSL is to have access to the `find` command. 
# The script should work fine in normal windows.
#
# $ find /mnt/c/Users/bgrav/DecentSampler/out/ -wholename "*Kit*.dspreset" -exec python3 ./dspreset_to_play.py "{}" \;

OUTDIR = '/mnt/f/tmp_out/'  # Set your output directory path here

DEBUG=False

#------------------
# -- Mappings
#
# These are used to pick outpot subdirs. 
# the script will find all the first letters of the filename. That could be "BD"
# for bassdrum in my example. It then lowercases and compares to the mappings below.
# bd => kick, means that bd will go into a directory called "Kick" instead of bd.
# When no mapping is found, the output subdir would just be bd in this case.

type_dir_mapping = {
    "bd": "Kick",
    "sd": "Snare",
    "clap": "Snare",
    "handclap": "Snare",
    "hh": "HiHat",
    "ch": "HiHat",
    "oh": "HiHat",
    "perc": "Perc"
}

# I want many different types in the perc dir. This mapps everyything int the list, into the Perc dir.
perc = [
    "bell", "bongo",   "click",  "shaker",  "blip" , "cabasa",  "conga", "smack",   "tamb",
    "block", "clave",  "cowbell",  "duck",  "guiro", "laser",  "rip", "triangle", "shaker",
    "hand", "sidestick", "snap", "splat", "tabla", "udu", "wood", "woodblock", "wub", "timable", "knock", 
    "rimshot", "rim", "tambo", "clack", "bell", "burst", "klak", "klick", "tambourine", "tube", "agogo", "djembe"
    "cowb", "maraca", "cross", "toms", "tom", "timbale"

]

# Same, but for FX
fx = ["stun","echo","tone","xplo"]

#------------

for i in perc:
    type_dir_mapping[i] = "Perc"
for i in fx:
    type_dir_mapping[i] = "FX"

# define a helper function to print debug information
def debug_print(*args):
    if DEBUG:
        print("DEBUG: ", *args)


def xml_for_all_samples(dspreset_path):
    # Initialize list to hold the files to copy
    files_to_copy = []
    
    tree = ET.parse(dspreset_path)
    root = tree.getroot()
    
    # Iterate through samples in the XML
    for sample in root.findall('.//sample'):
        root_note = int(sample.get('rootNote'))
        path = sample.get('path')
        files_to_copy.append(path)
        
    return files_to_copy


def main(dspreset_path):
    try:
        # Get the list of files to copy
       
        files_to_copy = xml_for_all_samples(dspreset_path)
        
        debug_print(f"files to copy: {files_to_copy}")

        for path in files_to_copy:
            match = re.search(r'[a-zA-Z]+', path.split('/')[-1])
            if match is not None:
                type_name = match.group(0)
            else:
                type_name = "undefined"  # or any default value as per the requirement
            debug_print(f"Sample path: {path} Sample type: {type_name}")

            pack_name = "undefined"

            # grab Pack name to become the top level directory of the new output
            match = re.search(r'(\w+ From Mars)+', dspreset_path+"/"+path)
            if match is not None:
                pack_name = match.group(0)
            else:
                raise Exception("Couldnt match X From Mars") 
            debug_print(f"pack name: {pack_name}")

            # Use the type_dir_mapping to determine the correct directory.
            if type_name.lower() in type_dir_mapping:
                dir_name = type_dir_mapping[type_name.lower()]
            else:
                dir_name = type_name

            type_dir = os.path.join(OUTDIR,pack_name, dir_name)
            debug_print(f"Directory for files: {type_dir}")

            # Ensure the target directory exists
            os.makedirs(type_dir, exist_ok=True)
            #debug_print(f"Created directory {type_dir} if not exists")

            # Define source and destination paths
            src_path = os.path.join(os.path.dirname(dspreset_path), path)
            dst_path = os.path.join(type_dir, os.path.basename(path))
        
            # Copy the file to the destination
            shutil.copy(src_path, dst_path)
            print(f"Sample copied to: {dst_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_dspreset_file>")
    else:
        main(sys.argv[1])