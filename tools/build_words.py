"""Parse everyday-english-500.md and embed the words in index.html.

Run from the project folder:  python tools/build_words.py
The words go between the /*EVERYDAY_START*/ and /*EVERYDAY_END*/ markers.
"""
import json, re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
md = (root / 'everyday-english-500.md').read_text(encoding='utf8')

words, sec, sec_name = [], 0, ''
for line in md.splitlines():
    m = re.match(r'### (\d+)\. (.+?) \((\d+)\)\s*$', line)
    if m:
        sec, sec_name = int(m.group(1)), m.group(2)
        continue
    if not sec or not line.startswith('|') or set(line.replace('|', '').strip()) <= set('- '):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if cells[0] == 'English':
        continue
    if len(cells) == 3:
        groups = [(cells[0], cells[1], cells[2])]
    elif len(cells) == 4:
        groups = [(cells[0], cells[1], ''), (cells[2], cells[3], '')]
    else:
        raise SystemExit('Unexpected row: ' + line)
    for en, sv, ex in groups:
        if en and sv:
            words.append({'id': len(words) + 1, 'sec': sec, 'secName': sec_name, 'en': en, 'sv': sv, 'ex': ex})

data = 'const EVERYDAY = ' + json.dumps(words, ensure_ascii=False, separators=(',', ':')) + ';'
page = root / 'index.html'
h = page.read_text(encoding='utf8')
new, n = re.subn(r'/\*EVERYDAY_START\*/.*?/\*EVERYDAY_END\*/',
                 lambda _: '/*EVERYDAY_START*/ ' + data + ' /*EVERYDAY_END*/', h, flags=re.S)
if n != 1:
    raise SystemExit('Markers not found in index.html')
page.write_text(new, encoding='utf8')
print(len(words), 'words,', len({w['sec'] for w in words}), 'sections,', sum(1 for w in words if w['ex']), 'with examples')
