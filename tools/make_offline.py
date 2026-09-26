from pathlib import Path
import re
src = Path('tools/source-v3.html').read_text(encoding='utf-8')
three = Path('tools/three.module.min.js').read_text(encoding='utf-8')
# Convert the standalone ESM build into a classic script by turning its final export list into window.THREE.
m = re.search(r'export\s*\{([\s\S]*?)\};?\s*$', three)
if not m:
    raise SystemExit('Could not find Three.js export block')
exports = m.group(1).strip()
pairs=[]
for part in exports.split(','):
    part=part.strip()
    if not part: continue
    if ' as ' in part:
        a,b = [x.strip() for x in part.split(' as ')]
        pairs.append(f'{b}:{a}')
    else:
        pairs.append(f'{part}:{part}')
classic_three = three[:m.start()] + 'window.THREE={' + ','.join(pairs) + '};\n'
src = re.sub(r"import\s+\*\s+as\s+THREE\s+from\s+['\"][^'\"]+['\"];", 'const THREE = window.THREE;', src, count=1)
# Put Three first, then the game's existing module code becomes classic JS.
# It contains no remaining imports after the replacement.
src = src.replace('<script type="module">\nconst THREE = window.THREE;', '<script>\n' + classic_three + '\nconst THREE = window.THREE;', 1)
Path('app/src/main/assets/index.html').write_text(src, encoding='utf-8')
