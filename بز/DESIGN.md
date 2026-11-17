# Advertio — Dark Tech TikTok
## Theme
Deep navy `#050B16`, midnight panels `#101E32`, electric cyan `#2AD9E6`, soft off-white `#E3FAFF`. Technical grid/flight-control HUD, scan lines, disciplined typography. Modern dark cinematic look rather than cartoon neon overload.
## Source photo and logo policy
`reference.jpg` is the **first frame**; no artificial photo recreation. Photo stays on screen before dissolving into 3D flight at 1.25–2.60 seconds. **Never generate or redraw the official Advertio logo.** This version uses a text domain and text system label, not an invented logo. If adding the logo later, use the original uploaded Advertio Logo.png asset.
## Format
15.0 s at 30 fps, 720×1280 scene master, 1080×1920 final H.264 MP4, silent. TikTok-safe visual margins, a legible Farsi headline from 7.85 seconds, website CTA from 12.85 seconds.
## Timing
0.0–1.25 source photo only (gentle zoom); 1.25–2.6 photographic-to-tech dissolve; 2.6–7.85 3D accelerating aircraft; 7.85–10.35 reveal Persian benefit; 10.35–15 hold headline and `advertio.net`.
## Automation
GitHub Actions `Render Advertio Dark Tech TikTok` automatically runs after relevant pushes and can also be manually dispatched. Only the MP4 video is uploaded as the workflow artifact; sample JPG frames are not generated or uploaded.

## Aircraft geometry — detailed airport version
- Main airliner: cabin windows and doors, cockpit glazing, fuselage seams, long stripes, flap/aileron seams and spoiler indications, winglets and port/starboard navigation beacons, nacelle intake/exhaust rings and fan details, hydraulic struts and wheel hubs, fin hinge lines.
- Four static narrow-body aircraft occupy ground apron stands on either side of the runway, with distinctive tail colors, wings, engines, cockpits, cabin windows and landing gear. Their geometry is in world space, so all camera movement, runway takeoff and the existing dark technical style remain intact.
- Taxiway and apron stand markings align the background aircraft with the terminal setting. Airport airplanes stay grounded and never animate.
- Retain exactly one GitHub Actions output: `flight-dark-tech-tiktok.mp4`.
