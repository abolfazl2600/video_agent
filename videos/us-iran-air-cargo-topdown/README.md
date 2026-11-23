# Advertio | USA ⇄ Iran | Top-Down Air Cargo

15-second **1080×1920 final / 540×960 preview** film, created entirely in Python Pillow and FFmpeg. The original graphic artwork is drawn programmatically: matte crimson background, ultra-long ivory flight corridor, central red stripe, stylized overhead aircraft, animated parcel and document cards, and independently timed Persian typography. No source-reference image is reused, and **no logo is synthesized**; only the word ADVERTIO appears.

## Storyboard

| Time | On-screen copy | Visual |
| --- | --- | --- |
| 0–3.4s | «آمریکا به ایران؟ یا ایران به آمریکا؟» | Aircraft enters a pale flight corridor on a deep red field |
| 3.4–7.2s | «بار یا مدارک داری؟ مسیر هوایی رو انتخاب کن» | Parcel and document props move into view |
| 7.2–11s | «توی ادورتیو مسافر هوایی پیدا کن» | Airplane progresses along the lane, two-way labels |
| 11–15s | «حدود ۲ هفته*» / «با مسافران هوایی» / `advertio.net` | Editorial end card, subtle flight-path animation |

**Accuracy:** Advertio connects people with independent travelers; it does not guarantee shipping or act as the airline. «حدود ۲ هفته» is a campaign estimate provided for this brief, not a guaranteed delivery time. Verify operational accuracy before publishing; actual timing, permitted items, documentation, customs and airline rules depend on the route and traveler agreement.

## Commands

`npm run lint` validates the source.

`npm run samples` generates ten full-size storyboard sample JPEGs and `quick-preview-contact-sheet.jpg`.

`ADVERTIO_RENDER_MODE=preview npm run render` generates silent 15s `preview.mp4`, 540×960 at 10 fps.

`ADVERTIO_RENDER_MODE=final npm run render` generates silent 15s `output.mp4`, 1080×1920 at 30 fps.

Dependencies: Python 3.12, Pillow 11.3 (with libraqm), FFmpeg, Node 22+ to execute the npm scripts. Text uses shared original `assets/fonts/Vazirmatn` fonts checked into this repository; the local rendering fallback is only for developers without shared assets. No third-party downloads are needed at render time beyond Pillow.

## Manual GitHub Actions

Open the repository's `Actions` tab, select **Advertio Manual Render - Folder and Quick Preview / Preview / Final**, choose this branch and `folder=us-iran-air-cargo-topdown`, then choose `quick-preview`, `preview`, or `final`. The workflow renders the selected folder only. Auto-render generates a quick-preview artifact for changes in this folder.
