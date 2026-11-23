# Advertio — Mother & Supplement / Original Animated Story
An independently renderable **15-second vertical Persian advertising video** in `videos/mother-supplement-network/`.

## Creative direction
The original orange/black/white reference provided **only art direction**, not a literal layout. This implementation does **not** copy its connected chess pawns or the entire abstract network. It instead uses four distinct original, soft isometric miniature environments with off-white studio backgrounds, rounded clay geometry, restrained orange accents, gentle shadows, and prominent Persian editorial typography.

## Story & actual on-screen animation

| Time | Story / copy | Animated visual action |
| --- | --- | --- |
| 0–3.8s | «مامانت توی ایران حالش خوب نیست؟ یه مکمل خوب لازم داره؟» | A concerned daughter in Canada, an incoming video-call card with her mother, a levitating supplement jar, and subtle communication pulses |
| 3.8–7s | «مکمل رو تهیه کردی... چطور به ایران برسونیش؟» | Close-up miniature packing: the jar descends toward an isometric parcel, its lid moves, and an animated airplane travels from Canada toward Iran |
| 7–11s | «توی ادورتیو مسافر مسیر ایران رو پیدا کن!» | Large fictional Advertio listing phone: listing cards, scrolling/selection highlight, the traveler with a suitcase, and a new chat-response bubble |
| 11–15s | «بیش از ۱۱٬۰۰۰ آگهی حمل بار و مسافر در ادورتیو منتشر شده» | The mother smiles and waves, the parcel enters, a confirmation checkmark pulses, and the 11,000 figure counts up |

**Product accuracy:** Advertio is a platform for connecting users and travelers, not the carrier. Visual arrival is an illustrative outcome rather than a guarantee. Any shipment of supplements remains subject to relevant airline, carrier and customs rules. The 11,000+ claim comes from supplied campaign copy and should be verified before public posting.

## Implementation
- **`isometric.py`**: 2.5D isometric scene geometry, full-body clay characters, matte materials, simple architectural perspective, eased positional animation, scene-specific movement. Efficient Pillow renderer—no SVGRenderer polygon occlusion.
- **`finish.py`**: staggered Persian RTL typography, 11,000 count-up, 10-frame contact sheet, and FFmpeg H.264 video encoding.
- **`package.json`**: `npm run lint`, `npm run samples`, `npm run render`. No per-folder JS dependencies.
- Official shared `assets/fonts/Vazirmatn-Regular.ttf` and `Vazirmatn-Bold.ttf` are used in GitHub Actions. No generated/modified Advertio logo (plain text brand name only).

## Preview
Quick Preview is the folder-scoped **automatic action on pushes**. It generates 10 portrait JPGs, 720×1280, and a `quick-preview-contact-sheet.jpg`. Manual run: Actions → **Render Advertio Video — Select Folder and Quality** → branch `feature/mother-supplement-network-isometric` → `folder=custom` → `custom_folder=mother-supplement-network` → `mode=quick-preview`.

Preview MP4: 540×960, 10fps, 15s, silent (`ADVERTIO_RENDER_MODE=preview npm run render`); final MP4: 1080×1920, 30fps, 15s, silent (`ADVERTIO_RENDER_MODE=final npm run render`), manual only.

Dependencies: Node 22 for the workflow wrapper, Python 3.12 + Pillow 11.3.0 with libraqm shaping, and FFmpeg for MP4. Animation and RTL typography use deterministic per-frame time (no audio/voice).
