# Advertio — Supplement Delivery Network (15-second 3D Isometric)
A dedicated folder-scoped vertical campaign. **New branch:** `feature/mother-supplement-network-isometric`.

## Storyboard
| Time | Visual beat | Persian copy |
|---|---|---|
| 00:00–00:04 | Mother in Iran and package node appear; network's orange first line lights up. | «مامانت توی ایرانه و حالش خوب نیست؟ یه مکمل لازم داره؟» |
| 00:04–00:07 | Package connects to traveler node across branching paths. | «می‌خوای از خارج کشور به ایران برسونیش؟ مسافر مسیر ایران رو پیدا کن.» |
| 00:07–00:11 | Isometric Advertio phone connects the sender, traveler and mother. | «توی ادورتیو آگهی بذار؛ به مسافرها وصل شو؛ مستقیم گفت‌وگو کن.» |
| 00:11–00:15 | Network expands around phone and destination; numerical proof and CTA dominate. | «بیش از ۱۱٬۰۰۰ آگهی حمل بار و مسافر در ادورتیو منتشر شده» / advertio.net |

## Visual direction
Orthographic-looking miniature-3D arrangement on ivory background: black/white pawn-like human markers, extruded bright orange branching connectors, tactile black/white square stations, matte bottle and packet nodes, soft neutral shadows, tiny orange and black diagram accents, high-contrast oversized editorial Persian typography. Inspired by the attached conceptual reference; reference image pixels and its copyrighted headline are **not reused**. The original low-poly isometric aesthetic is now drawn with deterministic layered raster geometry in Pillow, avoiding the large SVGRenderer floor polygons that hid connections.

## Render choices
- `npm run samples`: **Quick Preview**, 10 representative 720×1280 JPGs and `quick-preview-contact-sheet.jpg`; no MP4. Default for folder changes.
- `npm run render`: **Preview MP4**, 540×960, 10 fps, 15 s.
- `ADVERTIO_RENDER_MODE=final npm run render`: **Final MP4**, 1080×1920, 30 fps, 15 s, only on explicit selection.
- `npm run lint`: validates both Python render and finishing scripts.
- Node 22+, Python 3.12, Pillow 11.3 (with libraqm for Persian RTL), FFmpeg for MP4.
- Shared original Vazirmatn font files: `../../assets/fonts`.
- No generated logo. If an official Advertio logo is ever included, only the original supplied file may be used.
- Video is silent; voice/narration is currently represented by on-screen Persian copy.

## Manual GitHub Actions
Actions → **Render Advertio Video — Select Folder and Quality** → Run workflow → choose this branch → `folder=custom`, `custom_folder=mother-supplement-network`, `mode=quick-preview` (or `preview`/`final`). Folder-scoped push renders Quick Preview automatically; all outputs remain in this folder's job/artifact.

**Important:** Advertio connects users with travelers; it is not itself the carrier or provider of supplements. Any supplement must be permitted by airline, customs and carrier policies. «۱۱٬۰۰۰+» is marketing copy supplied for this campaign and should be verified against live platform data before publication.

### Execution trigger
A change to this folder launches the GitHub Actions folder-scoped **Quick Preview** and uploads a contact sheet plus ten sample JPGs; the workflow change and the story have both been committed on this branch.

## Fix: background visibility and render stability
The first prototype obscured the isometric scene with a near-opaque footer panel starting at y=895, and used oversized SVGRenderer floor polygons that could partially cover small models. The rendering pipeline now uses a deterministic Pillow isometric scene with correctly depth-ordered extruded paths and figures, no occluding floor, and reserves y=430–1080 for graphics. The full branched network is visible and animated highlights travel along the routes. Quick Preview requires no Node 3D dependencies and runs just the 10 chosen frames.
