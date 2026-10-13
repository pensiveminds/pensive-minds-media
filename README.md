# Pensive Minds media

Media and build scripts for Chris's Instagram suite. Each page has its own folder; nothing is shared between them except this repo.

| Folder | Page | What's inside |
| --- | --- | --- |
| `pensive-minds/` | @pensive.minds_ | `posts/` (numbered carousels), `stories/` (prayer notes and live stories) |
| `ranks-and-reason/` | @ranksandreason | Brand bible, Reel renderer (`c001-marathon/`), Story builder (`stories/launch/`) |
| `heel-and-serpent/` | @heelandserpent | Brand bible, logo builders (`brand/`), post builder (`make_posts.py`), posts by set (`posts/<date>-<set>/`) |

## Conventions

- New content goes in its page's folder, in a dated or numbered set folder. Never at the repo root.
- Metricool fetches images from `https://raw.githubusercontent.com/pensiveminds/pensive-minds-media/main/<path>` when a post is scheduled and keeps its own copy, so moving files after scheduling does not affect posts already in the planner.
- Topics don't cross pages (see each brand bible).

## Changelog

- Oct 13, 2026: Pensive Minds content moved from `posts/` and `stories/` into `pensive-minds/`. Added `heel-and-serpent/`. Ranks & Reason unchanged.
