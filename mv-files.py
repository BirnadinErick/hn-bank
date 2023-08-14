import sys
import os
import re

# Get params from cmdline args
MANIFEST = sys.argv[1]
DESTINATION = sys.argv[2] or "files"

def parse_img_links(c, r, s):
    """
    * Takes MD content `c` and substitutes patterns matching `r` with `s`
    param c: str; content of MD file to be parsed
    param r: rstr; regex pattern to be substituted
    param s: str; substitute pattern
    """
    result = re.sub(r, s, c, 0, re.MULTILINE)
    return result

# Create the "files" directory if it doesn't exist
os.makedirs(DESTINATION, exist_ok=True)

# Get the filenames to be moved
with open(MANIFEST, "r") as m:
    files_to_move = [f.replace("\n", "").rstrip().lstrip() for f in m.read().split(",")]

REGEX = r"!\[([\d\w\s]*)\]\(([\d\w:\/.*-]*)\s[\w\"=]*\)"
SUBSTITUTE = r"![\1](\2)"

# Create map of files
files = dict()
for f in files_to_move:
    with open(f, "r") as h_f:
        files[f] = h_f.read()

# Parse the contents
files = {k: parse_img_links(v, REGEX, SUBSTITUTE) for k, v in files.items()}

# Write it to the destination
for f, c in files.items():
    with open(os.path.join(DESTINATION, f), "x") as h_f:
        h_f.write(c)
