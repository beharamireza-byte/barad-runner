from pathlib import Path
import re

src = Path("tools/source-v3.html").read_text(encoding="utf-8")
three = Path("tools/three.global.js").read_text(encoding="utf-8")

# The approved V3 source imports Three.js from jsDelivr. Replace that import
# with the global Three.js object produced at build time, then inline the
# bundled runtime into the same HTML file so the Android app needs no network.
src, n = re.subn(
    r"import\s+\*\s+as\s+THREE\s+from\s+[\"\'][^\"\']+[\"\'];",
    "const THREE = window.THREE;",
    src,
    count=1,
)
if n != 1:
    raise SystemExit("Could not replace the V3 Three.js import")

src, n = re.subn(r"<script\s+type=[\"\']module[\"\']>", "<script>", src, count=1)
if n != 1:
    raise SystemExit("Could not convert the V3 game script tag")

needle = "<script>\nconst THREE = window.THREE;"
if needle not in src:
    raise SystemExit("Expected V3 Three.js bootstrap marker not found")

# esbuild's global-name output creates a classic global named THREE. Expose it
# on window explicitly so the game's existing code can keep using window.THREE.
bootstrap = "<script>\n" + three + "\nwindow.THREE = THREE;\n</script>\n<script>\nconst THREE = window.THREE;"
src = src.replace(needle, bootstrap, 1)

out = Path("app/src/main/assets/index.html")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src, encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size} bytes)")
