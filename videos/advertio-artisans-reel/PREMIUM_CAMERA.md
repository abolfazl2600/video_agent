# Premium Camera Edition

Original six slides, unchanged. Previous renders preserved. Output: renders/premium-camera-final.mp4 (52 seconds, Full HD 1080x1920, 60 fps, 3120 individually generated frames, no audio).

Six individually art-directed camera paths use fractional affine transforms and monotone cubic interpolation. Wide reading views flow into detail shots of the actual artwork and return to full framing. Five spatial camera-travel transitions use a short simulated shutter exposure, without overlapping text. No new typography, logo, or artwork. Close views intentionally crop portions of the poster briefly.

Run python render_premium_camera.py with Python 3.12, numpy, opencv-python-headless and FFmpeg. Dedicated Actions workflow verifies frame count, duration, codec and full decode before publishing.
