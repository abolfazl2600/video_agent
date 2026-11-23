# Advertio Video Agent

This repository contains **independent, folder-scoped video projects**, so a change to one video never requires rebuilding every video.

## Video projects

- [Original dark-tech airplane film (`بز/`)](./%D8%A8%D8%B2/) — 15-second vertical Three.js flight film, rendered by the existing `render-tiktok.yml` workflow.
- [3D isometric parcel-to-Iran ad (`videos/parcel-to-iran-isometric/`)](./videos/parcel-to-iran-isometric/) — four-scene, 15-second Persian passenger-cargo story. Output: 1080×1920 MP4.

## Folder-based GitHub Actions

Open **Actions → Render Advertio Video by Folder → Run workflow**. In the `folder` input enter a video project name **without `videos/`**, e.g. `parcel-to-iran-isometric`. The action validates the folder, installs dependencies only there, runs its `npm run lint` and `npm run render`, verifies `output.mp4`, and uploads **only that project's video**.

When code in `videos/<folder>/**` is pushed, the workflow detects the changed folder(s) and renders **only those folder(s)** as separate matrix jobs. Jobs are isolated, including their dependencies, video output, artifact names and concurrency groups. Changes to the original `بز/**` continue to use its existing dedicated workflow.

### Adding future videos

Create a new folder `videos/<your-video-slug>/` with at least:

```text
videos/your-video-slug/
  package.json     # scripts: lint and render
  ...              # every asset needed to render this video
```

The project's `render` command must produce `videos/<your-video-slug>/output.mp4`. Each project may choose its own video duration, aspect ratio, resolution, scenes and dependencies. The workflow checks that the resulting MP4 is readable and nonempty. Changing one folder will not trigger a rebuild of the rest.

**Brand assets:** Never AI-generate or redraw the Advertio logo. Use the original uploaded `Advertio Logo.png` for any designs that include the logo; plain text brand mentions are permitted.
