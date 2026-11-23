# Advertio Video Agent

This repository contains **independent, folder-scoped video projects**, so a change to one video never requires rebuilding every video.

## Video projects

- [Original dark-tech airplane film (`بز/`)](./%D8%A8%D8%B2/) — 15-second vertical Three.js flight film, rendered by the existing `render-tiktok.yml` workflow.
- [3D isometric parcel-to-Iran ad (`videos/parcel-to-iran-isometric/`)](./videos/parcel-to-iran-isometric/) — four-scene, 15-second Persian passenger-cargo story. Output: 1080×1920 MP4.

## Shared Persian typography

All new Persian-language video compositions must load **Vazirmatn** from the checked-in font files at `assets/fonts/`. Use `Vazirmatn-Regular.ttf` for supporting text and `Vazirmatn-Bold.ttf` for primary headlines. The font files are version-controlled and do not need to be downloaded during CI rendering. See [font usage and licensing](./assets/fonts/README.md).

The `parcel-to-iran-isometric` project uses these assets for all Persian captions and interface labels (and Latin brand/domain labels). The existing legacy `بز/` composition still has its own styling and renderer; it has not been automatically migrated.

## GitHub Actions — manual rendering

Use the **dedicated manual-only workflow**:

**[Advertio Manual Render - Folder and Preview or Final](https://github.com/abolfazl2600/video_agent/actions/workflows/render-manual.yml)**

The workflow is committed to `main` (GitHub's default branch) and also exists on `feature/restyle-soft-minimal-isometric`. Open **Actions**, select **Advertio Manual Render - Folder and Preview or Final** in the left sidebar, and then click **Run workflow** in the top-right. Select:

1. **Branch:** `main` or `feature/restyle-soft-minimal-isometric`.
2. **folder:** `parcel-to-iran-isometric` (or `custom` to select a future folder inside `videos/`).
3. **custom_folder:** required only if `folder=custom`; enter its directory name without `videos/`.
4. **mode:** `preview` (default, 10 fps / 540×960 / `preview.mp4`) or `final` (30 fps / 1080×1920 / `output.mp4`).

Click **Run workflow**. The job validates and renders only the chosen folder, then uploads its MP4 to **Artifacts**.

## GitHub Actions — automatic rendering

The separate [Advertio Auto Render - Changed Folders](https://github.com/abolfazl2600/video_agent/actions/workflows/render-video.yml) is for pushes only. It selects only changed folders inside `videos/`. For `parcel-to-iran-isometric`, pushes run **Quick Preview** (10 sample JPG frames and a contact sheet). Other compatible video folders run their default Preview. Pushes never trigger Final. Changes to `بز/**` continue to use the legacy dedicated workflow.

### Adding future videos

Create a new folder `videos/<your-video-slug>/` with at least:

```text
videos/your-video-slug/
  package.json     # scripts: lint and render
  ...              # every asset needed to render this video
```

The project's `render` command must respect `ADVERTIO_RENDER_MODE=preview|final` (defaults to preview) and produce `preview.mp4` or `output.mp4`, respectively. New projects can define their own preview/final resolutions, durations, fps and dependencies; only `parcel-to-iran-isometric` currently enforces exact 10/30 fps and 15-second duration. The existing legacy `بز/` renderer has its own workflow and has not yet been migrated to this preview/final protocol.

**Brand assets:** Never AI-generate or redraw the Advertio logo. Use the original uploaded `Advertio Logo.png` for any designs that include the logo; plain text brand mentions are permitted.

## Mother supplement campaign

The standalone `videos/mother-supplement-network/` project is included on main with a folder-scoped, Pillow-rendered Quick Preview (10 image samples plus a contact sheet) and manually selectable Preview/Final MP4 outputs. Open **Actions → Advertio Manual Render** and choose `mother-supplement-network` as the folder. Advertio connects customers with travelers; it is not the carrier. Any supplement or parcel must comply with airline, carrier, destination, and customs rules.

## Reusable content templates

- **[Image-to-Motion Storyboard v1 — Persian guide](./templates/image-to-motion-storyboard-v1/README.fa.md)**: the approved **16s, 4-scene, 9:16** Advertio motion-graphics format. Each prepared scene image is placed into a large **lower rounded viewport**, animated by slow camera pan/zoom, while independent Persian kinetic typography remains at the top. Includes scene-specific motion overlays, subtle crossfades and timeline.
- **[Copy-paste full production prompt](./templates/image-to-motion-storyboard-v1/MASTER_PROMPT.en.md)**: detailed exact timings, layout coordinates, crop/pan/zoom parameters, logo rules, GitHub Actions instructions and output-quality checks.
- **[Editable example configuration](./templates/image-to-motion-storyboard-v1/template.example.json)**: machine-readable parameters and four example scenes.

This is an **image-based 2.5D animation template**, not a full character rig and not a new video project. To use it, supply one four-panel source artwork or four scene images, plus the campaign's Persian text; create a new isolated folder under videos/. The source project's original Advertio logo must be used when the logo appears; do not generate or approximate a logo.
