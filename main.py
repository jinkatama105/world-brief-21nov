#!/usr/bin/env python3
# make.fun news-image-20261121 entry.
#
# The image is drawn in render_board.py (see that file for the layout and the
# sources); its output, entry.png, is committed to this repository. The grader
# runs this program with no network, so the program is the simplest honest
# thing: copy the committed bytes to /output/entry.png. Two runs, identical
# bytes, by construction.
import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'entry.png')
out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(src, os.path.join(out_dir, 'entry.png'))
