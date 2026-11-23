# Advertio / Traveler Dollar Income — independent video project

A 23-second, six-scene, 9:16 Persian short-form advertising video based on the **Image-to-Motion** production pattern. New design relative to earlier Advertio parcel videos. The story uses the originally generated airport illustrations and independent 3D Persian typography stickers; source files are in `assets/scenes` and `assets/typography`.

## Story / 23 seconds

| Time | Visual | Typography / message |
|---|---|---|
| 00:00–03:30 | Traveler at airport, open suitcase, highlighted empty space | اگر مسافری و فضای خالی داری |
| 03:30–07:00 | Traveler considers dollar earnings | می‌تونی درآمد دلاری داشته باشی |
| 07:00–11:00 | Traveler packs documents and personal belongings | به شرط این که مدارک و وسایل شخصی دیگران رو حمل کنی |
| 11:00–15:00 | Advertio app visual matching travelers and senders | ما در ادورتیو مسافران و ارسال‌کنندگان رو بهم وصل می‌کنیم |
| 15:00–19:00 | Two participants communicate directly through app messaging | می‌تونید رایگان مستقیم با هم ارتباط بگیرید |
| 19:00–23:00 | 11,000+ proof and call-to-action | بیش از ۱۱ هزار آگهی اینجا منتشر شده؛ فرصت رو از دست نده |

## Assets and visual identity

- `assets/scenes/scene-01.webp` ... `scene-06.webp`: six losslessly organized, quality-90 WebP derivatives of original generated 941×1672 illustrations. Original large PNGs remain in the downloadable local production bundle.
- `assets/typography/*.webp`: all five generated 3D typography designs plus two separately cropped overlays for the connection/direct-contact scenes. Crops preserve transparency.
- `assets/Advertio Logo.png`: unmodified uploaded original logo, never recreated by AI. The illustration source derivatives also have AI-drawn logo pictograms concealed and replaced with the approved original mark.
- `render.py`: source, timing, easing, image viewport, text animation, scene-specific accent animation and MP4 encoding. Uses 30 *original* rendered frames/second in Preview, no duplicated upsampled frames.
- `renders/preview.mp4`: encoded portrait MP4 preview, 720×1280, 30 FPS, 23 sec, silent.
- `renders/quick-preview-contact-sheet.jpg`: thumbnail grid.

**Source accuracy:** The sample UI in the illustrated phone is conceptual, not a live screenshot or verified listing. “Over 11,000 ads” is supplied advertising copy and should be verified before publication. Advertio connects users directly; it does not itself guarantee transport. Traveling with documents/other people's belongings must comply with customs, airline and carrier regulations; always verify the contents and never transport unknown or prohibited items.

## Render

Install Python 3.12, Pillow with libraqm, and FFmpeg.

```bash
npm run lint
npm run samples
ADVERTIO_RENDER_MODE=preview npm run render
# opt-in 1080x1920 60 FPS Final:
ADVERTIO_RENDER_MODE=final npm run render
```

**Scope:** GitHub Actions should select only `videos/advertio-traveler-dollar-income-23s`, never run every project. Automatic folder change runs preview. A local archive can also be used to obtain the uncompressed original generated PNGs.