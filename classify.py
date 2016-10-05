#! /usr/bin/env python3
import sys
from pathlib import Path
from subprocess import call, check_output

assert len(sys.argv) >= 2

def is_binary(file):
    return 'charset=binary' in check_output(['file', '-ib', str(file.absolute())]).decode('utf-8')

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

    if is_binary(file):
        call(['file', '-b', str(file.absolute())])
    else:
        call(['less', str(file.absolute())])

    action = input('(k)eep, (d)elete, (r)ename or (m)ove? ').strip().lower().lstrip('q')
    if action == 'k':
        pass
    elif action == 'd':
        file.unlink()
    elif action == 'r':
        new_name = input('New name: ').strip()
        if new_name:
            call(['mv', str(file), str(file.with_name(new_name))])
        else:
            print('No new name provided, skipping file.')
    elif action == 'm':
        destination = input('Destination: ').strip()
        if destination:
            call(['mv', str(file), destination])
        else:
            print('No destination provided, skipping file.')
