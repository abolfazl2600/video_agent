# Advertio / USA ⇄ Iran / Creative Top-Down Film

An independent **18-second six-scene vertical** (9:16) motion graphic, entirely programmatically drawn with Pillow. Film uses original reference **style** (cinematic crimson, overhead product/aircraft, cream materials, strong negative space) but no pixels or logos were copied or recreated.

## Creative storyboard

| Time | Shot | Persian message |
| --- | --- | --- |
| 0–3s | Opposing USA / Iran labels; camera looks straight down on a long pale flight corridor as a miniature aircraft travels | آمریکا / ایران / بارت رو می‌خوای بفرستی؟ |
| 3–6s | New cream close-up shot, physical isometric package, passport and documents in separate cards | بار یا مدارک؟ هر دو، با مسافر هوایی |
| 6–9s | Cinematic burgundy abstract route globe, two route pins and curved aircraft flight | یک مسیر، دو جهت / USA ⇄ IRAN |
| 9–12s | Mock Advertio passenger listings on an oversized phone; cards appear in succession; message bubble animates | مسافر مسیرت رو توی ادورتیو پیدا کن |
| 12–15s | Top-down kinetic 14-day calendar with animated progress squares | حدود ۲ هفته* |
| 15–18s | Final dark editorial flight lane, moving white airplane and website CTA | بار و مدارکت با مسافر هوایی / advertio.net |

**Accuracy:** Advertio provides listings and connects senders with independent travelers. It is not an airline, carrier or guaranteed-delivery service. The approximate two-week line is campaign copy, subject to route, travel, customs, airline requirements and agreement with the traveler. The 14-day motif should not be interpreted as a guaranteed delivery deadline.

## Required typography (original uploaded asset)

**All Persian copy uses the original `بز/BYekan.ttf` already in this repository**, loaded from the existing original binary file (relative path `../../بز/BYekan.ttf` from repo root resolution; actual code derives the repo root robustly). The font is never recreated, downloaded, or replaced when running in GitHub Actions. English metadata uses the shared `assets/fonts/Vazirmatn-Bold.ttf`. Font shaping uses Pillow with libraqm.

`ADVERTIO_FONT_OVERRIDE` exists solely for developers testing without the repository's original font; do **not** set it in the publishing workflow. Production renders fail if original BYekan is missing.

## Render isolated folder

```bash
cd videos/us-iran-air-cargo-topdown
npm run lint
npm run samples                                     # 10 x 720×1280 JPG + montage
ADVERTIO_RENDER_MODE=preview npm run render         # 540×960, 10 fps, 18s MP4
ADVERTIO_RENDER_MODE=final npm run render           # 1080×1920, 30 fps, 18s MP4
```

Requires Python 3.12, Pillow 11.3 with libraqm, ffmpeg, Node 22 for npm scripts. No third-party 3D engine, browser or external rendered asset required. Video is silent by design: narration/music can be added after approval. Only the original uploaded `Advertio Logo.png` is approved for any future logo insert; **this film uses wordmark text only and never generates a logo**.

## GitHub Actions

Select the `feature/us-iran-air-cargo-topdown` branch and folder `us-iran-air-cargo-topdown` using the *Advertio Manual Render* workflow. Choose quick-preview (10 stills), preview (MP4) or final (MP4). Pushes to this folder automatically generate the isolated preview MP4; no unrelated project is rendered.

### Render validation

GitHub Actions renders the preview with the repository's original `بز/BYekan.ttf`; no `ADVERTIO_FONT_OVERRIDE` is configured in CI. The 18-second run is validated against 540×960 at 10 fps, while manual Final uses 1080×1920 at 30 fps.
