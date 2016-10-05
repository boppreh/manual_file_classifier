#! /usr/bin/env python3
import sys
from pathlib import Path
from subprocess import call

assert len(sys.argv) >= 2

if len(sys.argv) == 2:
    path = Path(sys.argv[1])
    if path.is_dir():
        files = list(path.iterdir())
    else:
        files = [path]
else:
    files = [Path(p) for p in sys.argv[1:]]

for i, file in enumerate(files):
    if file.is_dir():
        print("Skipping {} because it's a directory".format(file))
        continue
    else:
        print("Classifying {} ({}/{})".format(file, i+1, len(files)))

    call(['less', str(file.absolute())])
    action = input('(k)eep, (d)elete, (r)ename or (m)ove? ').strip().lower()
    if action == 'k':
        pass
    elif action == 'd':
        file.unlink()
    elif action in 'mr':
        destination = input('Destination: ').strip()
        if destination:
            call(['mv', str(file), destination])
        else:
            print('No destination provided, skipping file.')
