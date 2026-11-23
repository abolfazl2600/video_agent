# Shared Persian typeface — Vazirmatn

## Canonical video font assets

| Role | Source file in this repository |
| --- | --- |
| Supporting body text / UI | `assets/fonts/Vazirmatn-Regular.ttf` |
| Headlines / emphasis | `assets/fonts/Vazirmatn-Bold.ttf` |

**Font family:** Vazirmatn (وزیرمتن), by the Vazirmatn Project Authors, based on the official upstream repository: https://github.com/rastikerdar/vazirmatn

**License:** SIL Open Font License 1.1, included verbatim in [OFL.txt](./OFL.txt). These font files are original upstream TTFs, without redraws, tracing, or alterations.

**Source integrity:** Original Git blob SHA1 of Regular `64e4a8189557a17b63fd7a77794207483e592972`, Bold `efa9b095da01d299310bdcae293e24e657fe6da9`. They were copied byte-for-byte from `rastikerdar/vazirmatn/fonts/ttf/`.

## Integration pattern

Every video should reference **these shared files** rather than copying the fonts into its project folder or relying on the runner's system font. For a project at `videos/<folder>/`:

```python
from pathlib import Path
from PIL import ImageFont
ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = ROOT / "assets" / "fonts"
PERSIAN_FONT = FONT_DIR / "Vazirmatn-Regular.ttf"
PERSIAN_BOLD = FONT_DIR / "Vazirmatn-Bold.ttf"
font = ImageFont.truetype(str(PERSIAN_BOLD), 42)
# When drawing Persian, pass direction="rtl", language="fa".
```

Do not call an external font API during rendering. GitHub Actions validates both shared files and Pillow's RTL text shaping support before the render begins.

The official **Advertio logo** is a separate brand asset. Its use must always come from the original supplied `Advertio Logo.png` rather than any generated or redrawn version.
