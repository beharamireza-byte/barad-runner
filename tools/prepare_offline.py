from pathlib import Path
import re
import subprocess

src = Path("tools/source-v3.html").read_text(encoding="utf-8")
src, n = re.subn(
    r"import\s+\*\s+as\s+THREE\s+from\s+[\"'][^\"']+[\"'];",
    "import * as THREE from './three.module.min.js';",
    src, count=1,
)
if n != 1:
    raise SystemExit('Could not rewrite the Three.js import')

m = re.search(r'<script\s+type=["\']module["\']>([\s\S]*?)</script>', src, re.I)
if not m:
    raise SystemExit('Could not find the V3 module script')

entry = Path('tools/v3-entry.js')
entry.write_text(m.group(1).strip() + '\n', encoding='utf-8')
bundle = Path('tools/v3-bundle.js')
subprocess.run([
    'npx', '--yes', 'esbuild@0.25.9', str(entry),
    '--bundle', '--format=iife', '--outfile=' + str(bundle), '--minify',
], check=True)

compiled = bundle.read_text(encoding='utf-8')
out_html = src[:m.start()] + '<script>\n' + compiled + '\n</script>' + src[m.end():]
out = Path('app/src/main/assets/index.html')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(out_html, encoding='utf-8')
print(f'Wrote {out} ({out.stat().st_size} bytes)')
