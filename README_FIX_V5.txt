BARAD RUNNER V5 Android fix

This version keeps the approved V3 gameplay/UI and changes only the Android packaging:
- Three.js 0.186.1 stays a local asset, imported as an ES module through an HTTPS-like local asset host.
- No runtime internet access or remote Three.js dependency.
- Native Android launcher icon added.
- Hardware-accelerated WebView explicitly enabled.
- Version bumped to 1.1.0 / versionCode 2.
