# Flight — modern Three.js continuation

15 seconds, 720×1280, 30 fps, silent MP4.

Three.js geometry and PerspectiveCamera animate immediate forward motion from the photo-matched rear-quarter view, a centerline orbit, acceleration, nose-up climb and landing-gear retraction. The model is a stylized reconstruction inspired by the supplied photo, without external luggage. The B Yekan focal phrase is split into two oversized bold lines, with dimensional offset, a skewed teal banner and an animated underline. No photo transition is used. The model is a stylized reconstruction, not an exact photographic replica.

## Preview
Run `npx hyperframes preview` in this folder. `index.html` is the HyperFrames source; `film.js` is a bundled browser build that requires no external CDN.

## Rebuild
`npm install`
`node render.mjs`
`python3 finish.py`

Python needs Pillow built with RAQM for Persian shaping. FFmpeg must be on PATH. Three.js SVGRenderer renders the actual 3D meshes and camera without a GPU. PNG frames are generated in `frames/` and combined with the reference and Persian typography by `finish.py`.

To rebuild the browser bundle after changing `scene.mjs` or `browser.mjs`, use esbuild and replace Math.random with a seeded filmRandom function as in the included bundle header.

The delivered MP4 was rendered with this offline Three.js workflow and visually reviewed. HyperFrames Chromium rendering is blocked by the environment's browser socket restriction, so browser layout/contrast checks could not be completed here.

B Yekan source: https://github.com/intuxicated/css-persian/blob/master/fonts/BYekan.ttf
