# Advertio Video Agent — Dark Tech TikTok
Current composition lives in [بز](./%D8%A8%D8%B2/). It's a 15-second vertical aircraft video with a source-image opening, 3D runway motion, a cinematic dark technical HUD and readable Persian kinetic text.
- Format: **1080×1920**, 30fps, H.264, 9:16, silent.
- The repository already contains the original photo **بز/reference.jpg**. The video starts on that exact photo (cropped to 9:16) before transitioning to Three.js.
- No synthetic replacement for the official Advertio logo is used.
## Automated render
Open **Actions → Render Advertio Dark Tech TikTok → Run workflow**. A push changing `بز/**` or the workflow also triggers the render. Download `advertio-dark-tech-tiktok` from the completed run's Artifacts section.
## Local render
```bash
cd بز
npm install
python3 -m pip install Pillow==11.3.0
npm run build
npm run render
```
Requires Node 22+, Python 3.12, FFmpeg. Video appears at `بز/flight-dark-tech-tiktok.mp4`. For a browser preview run `npx hyperframes preview`; the Python finishing stage produces the final video overlay, so HTML previews are a design/timing reference, not pixel-for-pixel identical.
See [DESIGN.md](./%D8%A8%D8%B2/DESIGN.md) for style/timing details.
