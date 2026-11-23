# Advertio / «فقط باید همدیگه رو پیدا کنن!» — 20s motion ad

A self-contained short-form 9:16 advertising video project using five isometric scene keyframes and **nine transparent Persian WEBP typography assets**.

## Repository assets

- `assets/storyboard_frames/` — 5 optimized 540×960 WEBP scene backdrops (derived from the supplied original scene images).
- `assets/typography/` — 9 WEBP caption plates with transparency, kept independent so each can be animated.
- `render.py` — deterministic FFmpeg motion renderer, zoom + separate fade-in/out for each typography layer.
- `package.json` — folder-scoped `lint`, `render` and `samples` targets for GitHub Actions.
- The official Advertio logo is **not regenerated or traced**. There is no generated logo in this project. If one is introduced later, the only permitted asset is the original `Advertio Logo.png` uploaded by the owner.

## Timing (20 seconds)

| Sec | Action | Foreground typography |
| --- | --- | --- |
| 0–3 | Girl in Canada + parcel, slow push toward parcel | «این بسته باید بره ایران... ولی چه طوری بفرستم؟!» / «یه بسته، ۱۰ هزار کیلومتر فاصله!» |
| 3–7 | Passenger packing suitcase in airport | «اون طرف، یکی همین هفته داره می‌ره ایران!» / «فقط هنوز همدیگه رو پیدا نکردن!» |
| 7–11 | Advertio illustrated mockup, Canada and Iran connected | «اینجاست که ادورتیو وارد می‌شه!» / «آگهی بذار، مسافر پیدا کن.» |
| 11–16 | Matching + passenger chat message | «من جمعه می‌رم تهران، می‌تونم بسته‌ات رو ببرم!» |
| 16–20 | Yellow airplane with phone, CTA | «بار داری؟ مسافرت رو پیدا کن!» / `Advertio.net | ارسال بار مسافری` |

The visuals are **stylized keyframes with animated camera/caption effects**, not yet rigged or fully reconstructed 3D characters. This preview has no audio voiceover; the narration is represented by readable animated text.

## Render modes

```bash
# Run inside this folder, not the repository root.
python3 -m pip install Pillow==11.3.0  # FFmpeg must already be installed
npm run lint
ADVERTIO_RENDER_MODE=quick-preview npm run render  # 20s, 540x960, 10fps; quick-preview.mp4
ADVERTIO_RENDER_MODE=preview npm run render        # 20s, 540x960, 15fps; preview.mp4
ADVERTIO_RENDER_MODE=final npm run render          # 20s, 1080x1920, 30fps; output.mp4
ADVERTIO_RENDER_MODE=quick-preview npm run samples # 10 JPGs + contact sheet
```

Final merely upscales preview-resolution imagery and is **not approved for high-resolution publication** until higher-resolution image assets are committed. The final mode must be launched only by an explicit manual request.

## GitHub Actions

On pushes to this directory, the branch-local `render-video.yml` workflow automatically runs this folder's **quick-preview MP4** only and uploads it as a GitHub Actions artifact. Other video folders are isolated. The branch-local `render-manual.yml` can also select this folder using the `custom` option and entering `find-each-other-canada-iran-20s`, then selecting `quick-preview`, `preview`, or `final`.

This project inherits `storyboard.json` and `ART_DIRECTION.md` from its parent storyboard branch; actual render code and optimized assets are fully committed alongside this README.
