from pathlib import Path
import re

src = Path('tools/source-v3.html').read_text(encoding='utf-8')
# Keep the approved V3 game code exactly as-is; only make Three.js local.
src, n = re.subn(
    r"import\s+\*\s+as\s+THREE\s+from\s+[\"'][^\"']+[\"'];",
    "import * as THREE from './three.module.min.js';",
    src,
    count=1,
)
if n != 1:
    raise SystemExit('Could not rewrite the Three.js import')

out = Path('app/src/main/assets/index.html')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src, encoding='utf-8')
print(f'Wrote {out} ({out.stat().st_size} bytes)')
