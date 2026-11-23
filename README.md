# Advertio Video Agent

This repository contains **independent, folder-scoped video projects**, so a change to one video never requires rebuilding every video.

## Video projects

- [Original dark-tech airplane film (`بز/`)](./%D8%A8%D8%B2/) — 15-second vertical Three.js flight film, rendered by the existing `render-tiktok.yml` workflow.
- [3D isometric parcel-to-Iran ad (`videos/parcel-to-iran-isometric/`)](./videos/parcel-to-iran-isometric/) — four-scene, 15-second Persian passenger-cargo story. Output: 1080×1920 MP4.

## Folder-based GitHub Actions

Open **Actions → Render Advertio Video by Folder → Run workflow**. In `folder` enter the project slug **without `videos/`** (e.g. `parcel-to-iran-isometric`). **Mode defaults to Preview**. Final must be manually chosen only when a full-quality video is explicitly requested.

- **Preview (default):** 10 fps at 540×960 for this isometric project; produces `preview.mp4`. Every push affecting a `videos/<folder>/**` project runs Preview only.
- **Final (manual only):** 30 fps at 1080×1920 for this isometric project; produces `output.mp4`.
- Actions check the selected output and upload one video artifact for that folder and mode. Neither an unrelated video change nor a workflow-only change triggers a full-quality render.

When code in `videos/<folder>/**` is pushed, the workflow detects the changed folder(s) and renders **only those folder(s)** as separate matrix jobs. Jobs are isolated, including their dependencies, video output, artifact names and concurrency groups. Changes to the original `بز/**` continue to use its existing dedicated workflow.

### Adding future videos

Create a new folder `videos/<your-video-slug>/` with at least:

```text
videos/your-video-slug/
  package.json     # scripts: lint and render
  ...              # every asset needed to render this video
```

The project's `render` command must respect `ADVERTIO_RENDER_MODE=preview|final` (defaults to preview) and produce `preview.mp4` or `output.mp4`, respectively. New projects can define their own preview/final resolutions, durations, fps and dependencies; only `parcel-to-iran-isometric` currently enforces exact 10/30 fps and 15-second duration. The existing legacy `بز/` renderer has its own workflow and has not yet been migrated to this preview/final protocol.

**Brand assets:** Never AI-generate or redraw the Advertio logo. Use the original uploaded `Advertio Logo.png` for any designs that include the logo; plain text brand mentions are permitted.
