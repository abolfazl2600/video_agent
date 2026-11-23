# Advertio — Isometric Parcel to Iran

A standalone 15-second, vertical, **real 3D isometric** short-form ad for Advertio passenger cargo listings. All scene geometry is built with Three.js and rendered with `SVGRenderer` using an orthographic camera, then Persian titles and interface elements are composited with Pillow. The video is **silent**, with the spoken lines represented by legible animated Persian dialogue cards; no voice recording is currently included.

## Storyboard — 9:16 / 15 seconds

| Time | Action | Exact Persian dialogue / CTA |
| --- | --- | --- |
| 00:00–00:04 | A girl in Canada holds a parcel and speaks to her friend. | «کاش یکی بود این بسته رو برام ببره ایران!» |
| 00:04–00:07 | Her friend shows her a phone. | «چرا تو ادورتیو آگهی نمی‌ذاری؟» |
| 00:07–00:11 | She creates a passenger cargo listing; a traveler replies. | «من هفته دیگه می‌رم ایران، می‌تونم ببرمش!» |
| 00:11–00:15 | She is happy; the app and CTA are shown. | «مسافرت رو پیدا کن، بارتو ارسال کن!» / Advertio.net |

## Output

- `output.mp4` — H.264, 1080×1920, 30 fps, exactly 15 seconds; no audio track.
- Characters, buildings, trees, parcels, phones and the surrounding stage are authored in 3D.
- The on-phone screen is **an illustrated mockup**, not a screenshot of production Advertio.
- No AI-made brand logo is used. If a logo is later added, only the original uploaded `Advertio Logo.png` may be used; never generate, trace or approximate a replacement.

## Render independently

From **this directory only** (Node.js 22+, Python 3.12 with Pillow 11.3.0, and FFmpeg required):

```bash
sudo apt-get update -qq && sudo apt-get install -y ffmpeg
npm install
python3 -m pip install Pillow==11.3.0
npm run lint
npm run render
```

Optional representative frame previews: `npm run samples`. The final video renderer runs without building other projects in this repository. A Linux environment with the system DejaVu fonts is expected.

## GitHub Actions

**Actions → Render Advertio Video by Folder → Run workflow** and enter `parcel-to-iran-isometric` as the folder. GitHub automatically renders this video on commits changing `videos/parcel-to-iran-isometric/**`; edits to other video folders do not rebuild it. Download `advertio-parcel-to-iran-isometric-<run number>` from Artifacts.

### CI reliability
The workflow installs FFmpeg and FFprobe **before** 3D frame rendering, so encoding dependencies are validated early instead of failing after the 450-frame render. The initial run failed during encoding because FFmpeg was missing; this project update triggers the corrected folder-only workflow automatically.
