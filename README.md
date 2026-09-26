# BARAD RUNNER — exact V3, truly offline build

This project keeps the approved V3 game source and does not redesign the game.

The online V3 page currently loads Three.js from jsDelivr. This project fetches that exact Three.js build **only at build time**, embeds it into the HTML, and ships the resulting single-file HTML inside the APK. Runtime therefore needs no internet.

## Build

The included GitHub Actions workflow builds a real Android APK with Android SDK build-tools, zipalign and apksigner. It also verifies the APK before publishing the artifact.

The final APK is `BARAD_RUNNER_OFFLINE.apk`.
