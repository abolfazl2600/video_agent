# Advertio | USA ⇄ Iran | Reference-style editorial 2.5D (v3)

18-second vertical video **coded from scratch** to closely follow the four approved still-image references. The supplied images are **visual references only**, never embedded in the video. Each shape, light/shadow layer, airplane, parcel, passport, interface card and calendar is constructed with Python/Pillow geometry. The design uses an original matte Burgundy/Ivory palette, stylized overhead airliner, layered soft-shadow cards, alternating light/dark scenes and generous negative space.

## Six original scenes

| Time | Art direction | On-screen story |
| --- | --- | --- |
| 00:00–00:03 | Deep-burgundy background, long ivory flight corridor, prominent overhead airplane, parcel and passport on opposite sides | «از آمریکا به ایران؟ یا برعکس؟» |
| 00:03–00:06 | Warm-ivory background, two deep physical-style product cards and close-up soft-shadow miniature parcel / documents | «بار، بسته یا مدارک؟» |
| 00:06–00:09 | Wide, ivory circular dashed air-route diagram with moving aircraft and USA/IRAN pins | «بین دو کشور، دوطرفه» |
| 00:09–00:12 | Dark-burgundy scene with oversized Advertio listing smartphone and independently animated floating cards | «مسافر مسیرت رو پیدا کن» |
| 00:12–00:15 | Thick raised cream calendar with burgundy header and two rows of highlighted days | «زمان ارسال، حدود ۲ هفته» |
| 00:15–00:18 | Minimal burgundy overhead route end-card with airplane and prominently placed website | `advertio.net` |

## Source, font and original brand asset

All Persian text loads the **original existing** `بز/BYekan.ttf` from the repository. Do not replace or regenerate this binary. The renderer requires Pillow with libraqm for correct RTL shaping. `ADVERTIO_FONT_OVERRIDE` is only a developer test option: the GitHub Actions production renderer does not set it and uses the original BYekan.

The **original Advertio Logo.png** is the only permitted image logo. This particular film uses *only ordinary text* `ADVERTIO` and `advertio.net`; there is no generated, traced or approximate logo.

The complete, editable `film-reference-v3.py` source is stored losslessly as `reference-v3-source.bz2.b64` for GitHub connector file transport. `run_reference_v3.py` verifies a SHA256 before executing and can unpack the **readable original Python source** with `npm run unpack`. The older `film.py` remains for historical comparison; the active renderer is the new v3 runner.

## Run in selected folder only

```bash
cd videos/us-iran-air-cargo-topdown
npm run unpack            # materialize editable film-reference-v3.py
npm run lint              # checks source integrity and Python AST
npm run samples           # quick-preview: 10 JPG frames, 720x1280 + contact sheet
ADVERTIO_RENDER_MODE=preview npm run render   # 540x960, 10 fps, 18-second MP4
ADVERTIO_RENDER_MODE=final npm run render     # 1080x1920, 30 fps, 18-second MP4
```

Needs Python 3.12, Pillow 11.3 + libraqm, FFmpeg, and Node 22 for npm script launch. No third-party pre-rendered artwork, Blender, internet image service, or font download is required. Video is silent by default.

In GitHub Actions open **Advertio Manual Render**, choose branch `feature/us-iran-air-cargo-topdown`, folder `us-iran-air-cargo-topdown`, and quality `quick-preview`, `preview`, or `final`. The auto pipeline targets only the changed video folder and runs preview; other video projects are unaffected.

## Publishing accuracy
Advertio connects senders with independent travelers; it does not directly operate flights or guarantee cargo delivery. `حدود ۲ هفته` is an **estimate**, not a contractual deadline; timing depends on the traveler, route, airline, customs and permitted items. Validate the timing before publishing.
