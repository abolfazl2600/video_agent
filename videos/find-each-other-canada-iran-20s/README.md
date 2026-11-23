# Advertio — فقط باید همدیگه رو پیدا کنن!

**Project status:** storyboards and visual direction. This folder is intentionally **not runnable** yet. Video implementation will be added after selecting/revising the storyboard frames.

**Branch:** `feature/find-each-other-canada-iran-20s`
**Duration:** 20 seconds
**Format:** 9:16 Instagram Reels / Stories
**Style:** very small, restrained 3D isometric / miniature diorama, modeled after the user-provided deep navy canvas and yellow airplane reference.
**Video modes:** Preview 10 fps first; 30 fps Final only with explicit request.

## Five scenes

| Time | Name | Voiceover and on-screen copy | Reference frame |
|---|---|---|---|
| 0–3s | Hook: Canada sender and parcel | Narration: «این بسته باید بره ایران... ولی چه طوری بفرستم؟!» / Caption: «یه بسته، ۱۰ هزار کیلومتر فاصله!» | `01_hook_canada.png` |
| 3–7s | Surprise: airport traveler | Narration: «اون طرف، یکی همین هفته داره می‌ره ایران!» / Caption: «فقط هنوز همدیگه رو پیدا نکردن!» | `02_airport_traveler.png` |
| 7–11s | Advertio introduction | Narration: «اینجاست که ادورتیو وارد می‌شه!» / Caption: «آگهی بذار، مسافر پیدا کن.» | `03_advertio_entry.png` |
| 11–16s | The match | Passenger message: «من جمعه می‌رم تهران، می‌تونم بسته‌ات رو ببرم!» | `04_connection_message.png` |
| 16–20s | Yellow aircraft + CTA | «بار داری؟ مسافرت رو پیدا کن!» / `Advertio.net | ارسال بار مسافری` | `05_plane_cta.png` |

## Assets and import

Five 9:16 storyboard images were created for this project and delivered separately as a downloadable ZIP in the corresponding ChatGPT conversation. The generated binary frames are **not yet committed to GitHub**. After retrieving the storyboard package, place PNG assets inside `assets/storyboard_frames/` using the helper `import_storyboard_images.sh`; review the imported image files and commit them on this branch.

```bash
cd videos/find-each-other-canada-iran-20s
bash import_storyboard_images.sh /path/to/unzipped/storyboard_frames
git add assets/storyboard_frames
git commit -m "assets(video): add approved five-scene storyboard images"
```

See `storyboard.json` for timed actions and copy; `ART_DIRECTION.md` for the visual specification.

### Branding and typography

- Do **not** generate/recreate or modify the Advertio logo. If a logo is shown, use only the **original uploaded Advertio Logo.png** source asset.
- Overlay Persian text in code using shared repository `assets/fonts/Vazirmatn-Regular.ttf` and `assets/fonts/Vazirmatn-Bold.ttf`, not text rendered into AI images.
- Smartphone screens in these pictures are visual concepts, not authentic captures of the production app.
- User-provided reference is an art-direction guide; keep small 3D props, yellow aircraft, navy backdrop, low visual density and large negative space. Realistic scene details in illustrative boards should be simplified further when implementing the actual 3D video.
