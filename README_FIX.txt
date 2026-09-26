BARAD RUNNER V3 — GitHub Actions build fix

این بسته فقط فایل‌های لازم برای اصلاح build را دارد.

مراحل:
1) فایل‌های این پوشه را داخل پوشه محلی barad-runner کپی کن و Replace را بزن.
2) GitHub Desktop باید 2 فایل modified نشان بدهد.
3) Commit to main و بعد Push origin.
4) GitHub Actions یک Build جدید اجرا می‌کند.

این نسخه از Three.js دقیقاً 0.186.1 را از npm می‌گیرد و با esbuild به یک اسکریپت کلاسیک تبدیل می‌کند؛ بنابراین V3 تغییر نمی‌کند و APK در زمان اجرا اینترنت لازم ندارد.
