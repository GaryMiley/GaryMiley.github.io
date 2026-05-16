"""Sync files/ directory with data.json — remove deleted files, report missing ones."""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, 'data.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

expected = set(f['name'] for f in data.get('files', []))
existing = set(os.listdir(os.path.join(BASE, 'files'))) if os.path.exists(os.path.join(BASE, 'files')) else set()

# Remove files not in data.json
removed = 0
for name in existing - expected:
    os.remove(os.path.join(BASE, 'files', name))
    print(f'  deleted: {name}')
    removed += 1

# Report missing files
missing = expected - existing
if missing:
    print(f'  MISSING ({len(missing)}):')
    for name in missing:
        print(f'    {name}')

if removed:
    print(f'Cleaned up {removed} file(s).')
if not removed and not missing:
    print('Already in sync.')
if missing:
    print(f'\nDownload missing files from the export, then run: git add -A && git commit -m "update" && git push')
