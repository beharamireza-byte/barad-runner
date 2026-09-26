from pathlib import Path
import re

src = Path("tools/source-v3.html").read_text(encoding="utf-8")
three = Path("tools/three.min.js").read_text(encoding="utf-8")

# The V3 game was written as an ES module. Replace its remote import with
# the global THREE object exposed by the classic Three.js build, then inline
# that build into the same HTML file. This avoids file:// module/CORS issues
# inside Android WebView and keeps runtime fully offline.
src, n = re.subn(
    r"import\s+\*\s+as\s+THREE\s+from\s+[\"\'][^\"\']+[\"\'];",
    "const THREE = window.THREE;",
    src,
    count=1,
)
if n != 1:
    raise SystemExit("Could not replace the V3 Three.js import")

# Change only the game script tag. The source has a module script directly
# containing the game code; after the import is removed it can run as classic JS.
src, n = re.subn(r"<script\s+type=\"module\">", "<script>", src, count=1)
if n != 1:
    raise SystemExit("Could not convert the V3 game script tag")

# Prepend the self-contained classic Three.js build before the game's script.
needle = "<script>\nconst THREE = window.THREE;"
if needle not in src:
    raise SystemExit("Expected V3 Three.js bootstrap marker not found")
src = src.replace(needle, "<script>\n" + three + "\nconst THREE = window.THREE;", 1)

# The Android app loads this exact single asset.
out = Path("app/src/main/assets/index.html")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(src, encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size} bytes)")
