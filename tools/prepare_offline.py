from pathlib import Path
import re
import shutil

src = Path('tools/source-v3.html').read_text(encoding='utf-8')

# The V3 game remains an ES module, but it must import Three.js from local
# Android assets rather than jsDelivr. The Android WebView serves the assets
# from the appassets virtual HTTPS origin, so native ES-module loading works
# without file:// CORS restrictions.
src, n = re.subn(
    r"import\s+\*\s+as\s+THREE\s+from\s+[\"'][^\"']+[\"'];",
    "import * as THREE from './three.module.min.js';",
    src,
    count=1,
)
if n != 1:
    raise SystemExit('Could not rewrite the V3 Three.js import')

out = Path('app/src/main/assets')
out.mkdir(parents=True, exist_ok=True)

three_module = Path('tools/three.module.min.js')
three_core = Path('tools/three.core.js')
for p in (three_module, three_core):
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f'Missing or invalid Three.js asset: {p}')
    shutil.copy2(p, out / p.name)

(out / 'index.html').write_text(src, encoding='utf-8')
print(f'Prepared {out / "index.html"} ({(out / "index.html").stat().st_size} bytes)')
print(f'Copied {three_module.name}: {three_module.stat().st_size} bytes')
print(f'Copied {three_core.name}: {three_core.stat().st_size} bytes')
