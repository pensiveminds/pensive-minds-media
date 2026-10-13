# Heel & Serpent

Faith-driven motivation for men who get back up. Brand rules live in `BRAND_BIBLE.md`.

## Layout

- `brand/shapes.py` palette and geometry helpers
- `brand/logos.py` the marks in code (Cross & Serpent, Seal, Monogram); run it for a contact sheet
- `brand/export_logos.py` writes the finished logo files to `brand/logos/`
- `make_posts.py` templates: `marching_orders()`, `slide()` (carousels), `story()`; the launch set is defined at the bottom
- `posts/<date>-<set>/` rendered posts plus `CAPTIONS.md`
- `SOURCES.md` every verse used, by post
- `posts/_template/build.py` copy this to start a new set
- `PROJECT_SETUP.md` how to set up a dedicated claude.ai Project
- `fonts/` EB Garamond and Inter (SIL Open Font License)

## Rendering

```
pip install cairosvg pillow numpy
mkdir -p ~/.fonts && cp fonts/*.ttf ~/.fonts/ && fc-cache -f   # SVG text needs the fonts installed
python3 brand/export_logos.py
python3 make_posts.py            # renders the launch set into posts/2026-10-13-launch/
```

Mark one word per line for ember with brackets: `"GET [UP]."`
