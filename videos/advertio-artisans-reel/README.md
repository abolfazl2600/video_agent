# Advertio Cargo — Artisans / Global Market Reel

Six original Persian campaign slides, animated without new text, illustrations, logos, music, or visual overlays.

## Final specification
1080 x 1920, 30 fps, 47 seconds, H.264, yuv420p, silent. Six camera moves with cosine easing (maximum zoom 1.04x) and five 0.6-second cross-dissolves. Scene durations before overlap: 7, 9, 7, 8, 9, 10 seconds.

## Upload status
The actual final MP4 was rendered and decoded successfully in the authoring environment. The GitHub connector could not transfer the local binary assets or the final MP4 into this repository. This commit contains the renderer and instructions, not the media. Do not treat it as a published final video.

Upload the supplied project archive's six source files to assets/slide-01.png through assets/slide-06.png. The rendered final.mp4 from the archive can also be uploaded directly to renders/final.mp4; alternatively, reproduce it using Python 3 and FFmpeg 7:

```sh
cd videos/advertio-artisans-reel
python3 render.py
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,pix_fmt -of json renders/final.mp4
```

This folder is intentionally not registered with the existing auto-render workflow until all six original images are present, avoiding a failed render or changes to unrelated projects.
