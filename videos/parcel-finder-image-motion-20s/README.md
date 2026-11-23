# Advertio — «فقط باید همدیگه رو پیدا کنن!»

A 20-second, five-scene 9:16 image-to-motion campaign based on the reusable `templates/image-to-motion-storyboard-v1` pattern.

## Storyboard

| Timing | Visual | Narration / copy |
|---|---|---|
| 00–03 | Young woman in Canada, parcel closeup, quick digital push-in | «این بسته باید بره ایران… ولی چه‌طوری بفرستم؟!» / «یه بسته، ۱۰ هزار کیلومتر فاصله!» |
| 03–07 | Traveler closing suitcase at airport, split reveal of the two strangers | «اون طرف، یکی همین هفته داره می‌ره ایران!» / «فقط هنوز همدیگه رو پیدا نکردن!» |
| 07–11 | Large Advertio listing phone; original official logo; scroll and incoming notification | «اینجاست که ادورتیو وارد می‌شه!» / «آگهی بذار، مسافر پیدا کن.» |
| 11–16 | Blue animated connection, separate sender / traveler images, incoming chat card | «من جمعه می‌رم تهران، می‌تونم بسته‌ات رو ببرم!» |
| 16–20 | Canada–Iran flight route and animated app CTA | «بار داری؟ مسافرت رو پیدا کن!» / Advertio.net |

## Outputs

- `preview.mp4`: 720×1280, H.264, 15 fps, 20 seconds, silent preview.
- `quick-preview-contact-sheet.jpg`: key frames from all five scenes.
- `assets/scene-01.jpg` through `assets/scene-05.jpg`: five **separate** creative scene artworks, not a single scrolling poster.
- `assets/Advertio Logo.png`: original user-supplied brand file, unchanged.
- `render.py`: source of the pan/zoom camera, independent graphic overlays, Persian typography and FFmpeg rendering.

## Run locally

Install Python 3.11+, Pillow and NumPy, plus FFmpeg, then `python render.py --samples` or `python render.py` in this folder. Source scene images are pre-rendered and included; no image-generation service is needed to render the MP4. For production in GitHub Actions, use the repository-shared original Vazirmatn fonts by setting `ADVERTIO_FONT_BOLD` and `ADVERTIO_FONT_REGULAR` to the respective checked-in font paths; the standalone preview falls back to installed Noto Sans Arabic when Vazirmatn is unavailable.

**Brand safety:** Never recreate the logo; this project only composites the supplied original logo. The app screen is an illustration/mockup, not the real production UI.

**Business accuracy:** Advertio connects senders and travelers. Cargo transfer must be agreed directly between them and is subject to airline, carrier and customs rules. «۱۰ هزار کیلومتر» is illustrative campaign language, not a verified distance for every Canada-to-Iran route.

**Audio:** This deliverable contains scene narration text for a future professionally recorded voiceover, but no recorded human narration track is included. The MP4 is silent.