BARAD RUNNER V7 build fix

The previous build downloaded Three.js into app/src/main/assets while the esbuild entry imports it from tools/. This version downloads the exact Three.js module into tools/three.module.min.js so the bundle step can resolve it. The V3 game source remains unchanged.
