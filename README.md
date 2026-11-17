# Video Agent — Three.js flight

انیمیشن عمودی ۱۵ ثانیه‌ای بر اساس عکس مرجع: حرکت هواپیما از فریم اول، بدون ترنزیشن و بار، حرکت دوربین از زاویهٔ مایل به مرکز باند، شتاب‌گیری، اوج‌گرفتن و جمع‌شدن چرخ‌ها.

نوشتهٔ فارسی با **B Yekan** و تأکید بزرگ و ضخیم روی «فضای خالی چمدونت»، سایهٔ برجسته و نوار مورب متحرک ساخته شده است. مدل، بازسازی سبک‌پردازی‌شدهٔ عکس است و کپی دقیق فوتورئال نیست.

[دانلود آخرین ویدیو](renders/flight-three-modern.mp4) — MP4 / H.264 · 720×1280 · 30 fps · 15 s · بدون صدا

![قاب پایانی](preview.jpg)

## اجرا و ویرایش

نیازمندی‌ها: Node.js 22+، Python 3 و FFmpeg روی PATH. برای شکل‌دهی درست متن فارسی، Pillow باید از RAQM پشتیبانی کند.

```bash
npm ci
python3 -m pip install -r requirements.txt
npm run build
npm run preview
```

`npm run preview` پروژه را در HyperFrames Studio باز می‌کند.

## ساخت MP4

```bash
npm run render
```

خروجی: `renders/flight-three-modern.mp4`. مرحلهٔ `frames` با Three.js SVGRenderer از هندسه و دوربین واقعی سه‌بعدی PNG می‌سازد؛ مرحلهٔ `encode` متن فارسی را اضافه می‌کند و با FFmpeg ویدیو می‌سازد. این مسیر به WebGL یا GPU نیاز ندارد. پیش‌نمایش HTML هم از همان صحنه و زمان‌بندی استفاده می‌کند. تغییر متن باید در `index.html` و `finish.py` هماهنگ شود.

## فایل‌های اصلی

| فایل | کاربرد |
| --- | --- |
| `scene.mjs` | مدل هواپیما، فرودگاه، دوربین و مسیر حرکت |
| `browser.mjs` | زمان‌بندی GSAP برای پیش‌نمایش |
| `index.html` | ترکیب HyperFrames و تایپوگرافی |
| `render.mjs` | رندر فریم‌های سه‌بعدی |
| `finish.py` | متن B Yekan و خروجی MP4 |
| `build.mjs` | ساخت bundle با تصادفی‌سازی seed ثابت |
| `DESIGN.md` | رنگ‌ها و جهت طراحی |
| `reference.jpg` | عکس مرجع؛ در خروجی نمایش داده نمی‌شود |

`film.js` و `gsap.min.js` برای پیش‌نمایش بدون CDN همراه پروژه‌اند. فریم‌های موقت و node_modules وارد گیت نمی‌شوند.

## بررسی‌ها

```bash
npm run lint
ffmpeg -v error -i renders/flight-three-modern.mp4 -f null -
python3 -c "from PIL import features; print(features.check('raqm'))"
```

خروجی MP4 بررسی تصویری شده و decode کامل آن موفق بوده است. رندر خروجی با مسیر SVGRenderer انجام شده؛ بررسی مرورگری HyperFrames در محیط اولیه به دلیل محدودیت اجرای Chromium قابل انجام نبود.

## منابع

- عکس مرجع: تصویر ارائه‌شده توسط صاحب پروژه.
- فونت B Yekan: https://github.com/intuxicated/css-persian/blob/master/fonts/BYekan.ttf
- Three.js: https://threejs.org/
- GSAP: https://gsap.com/

حقوق هر دارایی و کتابخانه متعلق به صاحب آن است؛ مجوز یکپارچه‌ای برای دارایی‌های شخص ثالث این مخزن تعیین نشده است.
