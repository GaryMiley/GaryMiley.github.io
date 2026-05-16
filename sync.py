"""Sync: scan new files into data.json, remove deleted files from files/."""
import json, os, time, random, string

BASE = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE, 'files')

os.makedirs(FILES_DIR, exist_ok=True)

with open(os.path.join(BASE, 'data.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)
if 'files' not in data: data['files'] = []
if 'folders' not in data: data['folders'] = []

# 1. Scan files/ — register new files in data.json
existing_names = {f['name'] for f in data['files']}
added = 0

for name in os.listdir(FILES_DIR):
    path = os.path.join(FILES_DIR, name)
    if not os.path.isfile(path):
        continue
    size = os.path.getsize(path)
    ext = name.rsplit('.', 1)[-1].lower() if '.' in name else ''

    existing = next((f for f in data['files'] if f['name'] == name), None)
    if existing:
        if existing.get('size') != size:
            existing['size'] = size
            print(f'  updated: {name}')
    else:
        uid = 'fl_' + hex(int(time.time() * 1000))[2:] + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        data['files'].append({
            'id': uid,
            'folderId': None,
            'name': name,
            'type': ext,
            'size': size,
            'createdAt': int(time.time() * 1000)
        })
        added += 1
        print(f'  added: {name}')

# 2. Remove files in files/ that aren't in data.json
expected = set(f['name'] for f in data['files'])
existing = set(os.listdir(FILES_DIR))
removed = 0

for name in existing - expected:
    p = os.path.join(FILES_DIR, name)
    if os.path.isfile(p):
        os.remove(p)
        print(f'  deleted: {name}')
        removed += 1

# Save
with open(os.path.join(BASE, 'data.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Report
missing = expected - set(os.listdir(FILES_DIR))
if added:   print(f'Added {added} file(s).')
if removed: print(f'Cleaned up {removed} file(s).')
if not added and not removed and not missing:
    print('Already in sync.')

print(f'Total: {len(data["files"])} file(s) in data.json')
if missing:
    print(f'\nMISSING {len(missing)} file(s) — download from web export:')
    for n in missing:
        print(f'  {n}')
    print(f'\nThen re-run: python sync.py')

if not missing:
    print('\nReady to push:')
    print('  git add -A && git commit -m "update" && git push')
