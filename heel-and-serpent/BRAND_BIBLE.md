# Heel & Serpent: Brand Bible and Setup

Oct 13, 2026 · @Chris · Instagram: @heelandserpent

Faith-driven motivation for men of every age who've been knocked down and want to rise again. Gritty, disciplined, integrity-first father energy: strong enough to fight, choosing peace. The through-line: with God behind you, the war is already won.

## Where it sits in the suite

- **Ranks & Reason:** secular military history and philosophy. No faith content.
- **Pensive Minds:** reflective faith content.
- **Heel & Serpent:** faith as a fight. Motivation, discipline, getting back up, spiritual warfare.

Topics don't cross over. A story that fits two pages goes to the one it fits best.

## The promise behind the name

- Genesis 3:15: "He will strike your head, and you will strike his heel." (CSB) The man gets wounded, and still wins.
- Romans 16:20: "The God of peace will soon crush Satan under your feet." (CSB) Peace and victory in one verse.
- Romans 8:31: "If God is for us, who is against us?" (CSB)

These are the anchors, not a slogan. No single quote is repeated across posts, and no post asks followers to recite or answer back. Each post earns its own line from Scripture and from life. The idea that a man can't lose with God behind him should come through in the variety, not in repetition.

**Tagline (merch and bio, used sparingly):** "Bruised, not beaten." Alternates for merch: "Heel down." / "Crush the head."

## Identity

- **Name field:** Heel & Serpent | Rise Again
- **Bio:** Knocked down. Not out. / Faith, discipline & fatherhood for men who get back up. / Bruised, not beaten.
- **Feel:** quiet luxury with a warrior's spine. Built for combat, finished like a fine watch. Restraint over noise.
- **Logo system (locked Oct 13, 2026; the earlier boot mark is retired):**
  - **Monogram (profile picture):** "H & S" in EB Garamond capitals; the S is drawn as a serpent with an ember tongue; ampersand in ember italic; a thin rule beneath. File: hs_profile_monogram_1080.png.
  - **Seal (merch, launch post, watermark):** engraved double ring reading HEEL & SERPENT (top) and GENESIS III · XV (bottom, ash), two ember dots at three and nine o'clock, Cross & Serpent at the center. Files: hs_seal_bone / hs_seal_ember (.svg, .png).
  - **Cross & Serpent (header mark, small uses):** a slender cross with a sword point driven onto the head of a coiled serpent. It reads Genesis 3:15 as fulfilled at the cross. File: hs_cross_serpent_bone (.svg, .png).
  - Ember appears sparingly: the serpent's tongue, plus the ampersand on the monogram and the dots on the seal.
  - Logo scripts: heel-and-serpent/brand/logos.py and export_logos.py render every mark from code; finished files in brand/logos/.
- **Metricool:** brand "Heel & Serpent", blogId 7400959, Instagram @heelandserpent, time zone America/Chicago (connected Oct 13, 2026; first link mistakenly pointed at @pensive.minds_ and was corrected the same morning, so check the handle before any bulk scheduling).

## Voice

- Short sentences. Second person. Direct, like a father who's been through it talking to a son or a brother.
- Grit with grace: hard on excuses, never hard on the man. No shaming the fallen.
- Confident, not preachy. Commands, not lectures ("Get up. Make the bed. Open the Book.").
- Humor allowed, dry and rare. Never mocking.
- Never claims a personal testimony that didn't happen. The page speaks as a voice, not as a specific man with an invented past.

### Reels: daily cadence and pacing (Oct 14, 2026)

Day-1 data: the two Reels reached 106 and 71 people while feed posts reached 2-3 (3 followers), but average watch time was about 4 s of 16. Chris approved a daily Strike Reel, about 3:30 PM CT, starting Oct 14. Pacing rules: the hook line is fully on screen at frame 0 (no fade-in), 1.5-1.8 s per line, the verse lands by about 5 s, 10-12 s total, fade 0.25 s. Chris prefers efficiency and autonomy: daily Reels are built, previewed to him with at least an hour's lead, and go out on schedule unless he pulls them.

### What's landing (Chris's feedback; read before writing, add to it after)

The voice keeps evolving with Chris's reactions and the numbers from Watch. Log what he likes or pushes back on here, with the date, and let it shape the next set.

- Oct 13, 2026: liked the intro carousel ("Why Heel & Serpent"). What it did: opened with the promise, not with us; let Scripture carry the weight; short lines; named the wound before the win ("The heel gets bruised. The head gets crushed."); closed on "Bruised, not beaten." Keep that shape.
- Oct 13, 2026: called Strike #1 (Micah 7:8 Reel) "incredible." What it did: three short blows before the verse (YOU'RE DOWN. / HE THINKS IT'S OVER. / IT ISN'T.), the enemy named, then the full verse, then GET BACK UP on the seal; the score turns from minor to major on the seal. Liked the generated instrumental over a trending sound.
- Oct 13, 2026 (end of launch day): "I can relate to this, it gives something to hold onto and is a responsible reminder to obey God." Keep both halves: something a man can hold onto when he's down, and a clear call to obedience. Grace and command together, never one without the other.

## Visual language

- **Feed:** 1080x1350 (4:5) stills and carousels. **Stories:** 1080x1920.
- **Palette:** iron #1A1A1A background, bone #ECE6DA for text, ember #C8501E for the single highlight word, ash #8A8580 for labels and references.
- **Type:** EB Garamond capitals, widely letter-spaced, for the big line (matches the logos); EB Garamond italic for Scripture; Inter Bold for small labels. Bebas Neue only for the occasional hard-hitting command line, if at all.
- **Finish:** fine grain, soft vignette, thin hairline rules, generous margins. One idea per frame.
- **Imagery (optional):** moody stills like boots on a trail, a forge, a man at dawn, an empty chapel, a father's hands. Stylized serpent only, never gore.
- **Header on every frame:** series name in ember (top left), Cross & Serpent mark (top right).
- **Scripture reference always shown** under any verse, in ash (e.g. "Romans 8:31, CSB").

### Looks (rotation set by Chris, Oct 13, 2026)

Five looks, same words, palette, type and marks. Built by heel-and-serpent/make_variants.py: mo_look() for Marching Orders, carousel() for carousels (a carousel keeps one look on every slide), render_looks() to render.

- **Classic:** centred on iron. The anchor look.
- **Bone:** iron type on a bone ground (marks swapped to iron). Breaks the grid into light and dark.
- **Ledger:** left-aligned and larger, with an ember rule down the left margin. Suits discipline posts.
- **Engraved:** inset double frame, the seal faint behind the type, three ember dots as the divider. Suits Sundays and Armor Check.
- **Forge:** low ember glow from below; on stills, covers and closing slides the ember word is set huge and cropped behind the command. Strongest lines only, about once or twice a week.

**Visual variety (Chris, Oct 14, 2026):** the brand palette stays; he respects it. But he wants the grid and the Story line-up to stay visually pleasing, not monotonous, so be deliberate about variety within the looks above. A one-off palette is allowed only when Chris asks for one, and it keeps the type, marks and layout so it still reads as Heel & Serpent. Available: "dawn" (deep slate ground, bone type, muted gold highlight, low warm glow), via make_reel.use_palette("dawn"); first used for the "First light" Story, Oct 14.

Rules: no two posts in a row share a look (count Reels as their own look); Classic and Bone carry most of the week; Armor Check runs in Engraved; Forge stays rare. Non-classic files carry a _<look> suffix. When rebuilding a scheduled post in a new look, use new file names and update the Metricool post's media.

## Formats and cadence

About 14 feed posts a week plus daily Stories, all templated. Fixed times; adjust after the first month of data.

| Series | When | Format |
| --- | --- | --- |
| **Marching Orders** | Daily, morning | One still: a verse plus one command for the day |
| **Get Back Up** | Daily, evening | 5–7 slide carousel: a man who fell and rose, or a lie men believe and the truth that answers it |
| **Armor Check** | Sundays | Carousel on one piece of the armor of God (Ephesians 6), rotating weekly |
| **Stories** | Daily | Poll, question box, behind-the-post, or a repost of the day's feed post |

## Pillars

1. **Get back up:** men who fell and rose (David, Peter, Samson, Jonah, Paul).
2. **Discipline as worship:** body, mind, money, mornings, habits.
3. **The warrior father:** protecting, leading, staying gentle at home.
4. **Know your enemy:** temptation, pride, despair, anger and the lies men believe.
5. **Armor of God:** Ephesians 6, one piece at a time.

Rotate so the same pillar doesn't run twice in a row.

## Scripture and accuracy rules

- **Translation: CSB (Christian Standard Bible)**, chosen by Chris Oct 13, 2026. Quote it verbatim; mark partial verses with an ellipsis; check the wording against a published CSB source, never from memory.
- **CSB license:** up to 1,000 verses without written permission, under 50% of any work, never a complete book. Track the running count in heel-and-serpent/SOURCES.md and ask Holman Bible Publishers before it nears 1,000.
- **Credit line on every caption that quotes Scripture:** "Scripture quotations marked CSB have been taken from the Christian Standard Bible®, Copyright © 2017 by Holman Bible Publishers. Used by permission. Christian Standard Bible® and CSB® are federally registered trademarks of Holman Bible Publishers." The graphic itself shows the reference with ", CSB".
- Every verse shows its reference. Read the surrounding passage first; no verse used to mean something its context doesn't support.
- Quotes from historical Christians (Spurgeon, Augustine, Luther, etc.) must trace to a named work. No viral misattributions.
- Keep a Sources log (heel-and-serpent/SOURCES.md in the media repo): post, verse, context read, verse count.

## Guardrails

- **The fight is spiritual** (Ephesians 6:12, "not against flesh and blood"). No hostility toward people, groups, denominations or other faiths.
- No glorifying real violence, no weapons-as-lifestyle content, no gore.
- No politics, living politicians, current wars or culture-war bait. HOLD anything tied to current events.
- No prosperity promises. "You can't lose" means eternal victory and God's faithfulness, not guaranteed money, health or outcomes.
- Grace for addiction, divorce, failure and doubt. When a post touches despair or self-harm, it points to real help (a pastor, a counselor, or the 988 Suicide & Crisis Lifeline in the US) and never treats it lightly.
- No real living people named in a promotional way; no brands.

## Merch (design started Oct 14, 2026; no sales yet)

- Emblems: the Seal (primary) and the Monogram. Lines: "Bruised, not beaten." "Heel down." "Crush the head."
- Chris chose to start design work slowly on Oct 14, 2026 (hat, shirt, hoodie, socks). Nothing goes on sale until the trademark knockout ("Heel & Serpent" and the tagline lines) and the domain check have cleared.
- **Principle:** small marks, tonal thread, heavy blanks. Ember once per piece, as a hidden detail. Colorways: iron first, bone second.
- **Hat:** low-profile unstructured cap. Cross & Serpent front (tonal on iron; iron thread on bone, ember tongue kept); GENESIS III · XV in ash on the back. Alternate: debossed leather Seal patch.
- **Tee:** heavyweight. Monogram at the left chest. Iron tee carries the Seal large on the back (the one statement piece); bone tee has "BRUISED, NOT BEATEN." at the nape.
- **Hoodie:** heavy fleece. Tonal Monogram at the chest, "HEEL DOWN." down the left sleeve, Seal on the back optional. Ember only at the drawcord tips and a stitch inside the hood.
- **Socks:** "the ember heel": iron crew with an ember heel cup (the bruised heel, Genesis 3:15), knit Cross & Serpent at the ankle, "CRUSH THE HEAD." on the footbed. Bone pair: ember heel, iron toe and cuff stripe.
- **Rule:** no verse text on anything worn underfoot; phrases and marks only.
- Thread prep: thicken the cross and serpent tail for embroidery; the Seal's ring text only holds on leather or large prints, never small in thread.
- Files: merch/marks.py recolors the locked logos for garments (tonal, contrast, leather, knit grid) into merch/marks/. Mockups: "H&S Merch Line" design canvas on claude.ai.
- Knockout search (Oct 14, 2026, USPTO Trademark Search, exact phrase searches; not legal clearance): no filings for HEEL & SERPENT / HEEL AND SERPENT, HEEL DOWN, CRUSH THE HEAD or BRUISED NOT BEATEN. Nearest marks: BEATEN NOT BROKEN, live and registered in class 25 (t-shirts, socks, hats; reg. 5540638), close in wording to "Bruised, not beaten", so have an attorney weigh in before putting that line on product; HEELS DOWN in class 25 (shoes) is dead, CHIN UP, HEELS DOWN is live but for jewelry and watches; live class 25 SERPENT marks (DECAL SERPENT, SERPENT SKIN CAMO) are not close. Design marks (cross, serpent imagery) were not searched.
- Domain (Oct 14, 2026, Verisign RDAP): heelandserpent.com and heelserpent.com unregistered. Not bought.
- Embroidered option (Chris, Oct 14; mocked up alongside the print version): every mark stitched, softer fabric. Tee in a drapier cotton-modal or fine garment-dyed jersey (not the thinnest jersey, which puckers); hoodie in midweight French terry. Lighter stitch density, soft mesh backing. The large back Seal becomes a small stitched Seal (about 4 in) between the shoulders or below the hood, or nothing.
- On hold (Chris, Oct 14, 2026): no domain purchase, attorney or merch spending yet. Revisit in about a month (mid-November 2026) once momentum is clearer.
- When resumed: attorney review (especially "Bruised, not beaten"), register the domain, embroidery-ready and knit-ready mark files, print-on-demand samples to test fit before any small batch.

## Commands (for Heel & Serpent)

| Command | Action |
| --- | --- |
| **Rise** [optional topic] | Make one feed post (Marching Orders still or Get Back Up carousel, whichever is next) and schedule it about 2 minutes out via Metricool. No topic: pick by pillar rotation. Scripture rules and guardrails apply; HOLD if it touches current events. |
| **Arm** [notes] | Build and schedule next week's 14 feed posts plus Armor Check. |
| **Strike** [optional topic] | Make one short Reel (9:16, 12–18 s) with heel-and-serpent/make_reel.py: moving type over the iron ground, a verse with its reference, the seal to close, and an original score built into the video (drone in D minor, heartbeat pulse, impacts on the cuts, resolving to D major on the seal). Show Chris and wait for his OK, then schedule about 2 minutes out via Metricool as a REEL. Use it between the morning and evening posts. No topic: pick by pillar rotation. Sets go in heel-and-serpent/reels/<date>-<topic>/. |
| **Watch** | Report the latest Metricool numbers for the page. |
| **Sheathe** | Move all scheduled posts to draft. "Sheathe off" restores them. |

**Music policy (Chris, Oct 13, 2026; he prefers efficiency and autonomy):** feed posts stay on automatic publishing; Chris adds the paired song to feed posts himself. Reels carry their own original score built into the video (or a song attached, if Metricool ever can: needs a Facebook Page linked). Stories: music preferred but optional; default is to build Story frames as short videos with the original score baked in so they carry sound with no extra step for Chris. For Stories the score should be motivational and dramatic, not dark and moody (Chris, Oct 13): use make_reel.score_drive (D major, driving pulse, lifts into each cut, big resolve). Reels keep make_reel.score (minor to major).

**One score per Story (Chris, Oct 14, 2026):** Story frames post as separate clips, so a score built per frame restarts on every tap and sounds repetitive. A multi-frame Story gets ONE continuous score across all its frames: build it with make_reel.build_story_set({frame: scenes, ...}, out_dir), which writes the score once for the whole set (one intro, lifts on each cut, one resolve on the last frame) and slices it so each frame picks up where the last left off. Schedule the frames back to back, in order, a minute apart, with nothing else between them. Never call build_reel per frame for a Story set.

Every post, Reel and Story set comes with one gospel or worship song pairing for Chris to add in the Instagram app (standing request, Oct 13, 2026). Log each in heel-and-serpent/SONGS.md with the post, song, artist and why it fits. Titles and artists only, never lyrics.

## Pipeline

- Media repo: pensiveminds/pensive-minds-media, folder heel-and-serpent/ (reorganized Oct 13, 2026: each page has its own folder; Pensive Minds moved to pensive-minds/, Ranks & Reason unchanged).
- Builder: heel-and-serpent/make_posts.py. Templates: marching_orders(), slide() for carousels (cover, body, close with the Seal), story(). Bracket one word for ember, e.g. "GET [UP]." Text is measured and auto-shrinks to fit; content centres between the header and footer rules. Slides go in heel-and-serpent/posts/<date>-<set>/ with a CAPTIONS.md, and are pushed to main so Metricool can fetch them; a copy goes in a Heelandserpent Desktop folder.

## Working session (start here in any new Project or chat)

Everything needed lives in the media repo; nothing depends on earlier chats.

1. **Attach the repo:** pensiveminds/pensive-minds-media (push access). Work only inside heel-and-serpent/; don't touch pensive-minds/ or ranks-and-reason/.
2. **Read** heel-and-serpent/BRAND_BIBLE.md (this file), SOURCES.md, and the latest posts/<date>-<set>/CAPTIONS.md.
3. **Set up rendering:** `pip install --break-system-packages cairosvg pillow numpy`, then `mkdir -p ~/.fonts && cp heel-and-serpent/fonts/*.ttf ~/.fonts/ && fc-cache -f` (SVG text needs the fonts installed).
4. **Build a set:** copy posts/_template/ to posts/<YYYY-MM-DD>-<set>/, fill SET in build.py, run it, look at every image, write CAPTIONS.md (CSB credit line on every caption that quotes Scripture), add each verse to SOURCES.md. To check CSB wording, open the passages on BibleGateway (version=CSB, several references separated by semicolons) in the built-in browser and read the page text; the web fetcher only returns short snippets and the shell can't reach the site. If an ember word loses the space before it (seen after "WAY"), use an en space (\u2002) before the bracket.
5. **Publish:** commit and push to main; images are then at https://raw.githubusercontent.com/pensiveminds/pensive-minds-media/main/heel-and-serpent/posts/<set>/<file>. Before scheduling, run Metricool getBrandSettings and confirm blogId 7400959 shows instagramData "heelandserpent". Schedule with createScheduledPost (Story: no text; feed: caption plus alt text per image; isAiGenerated false).
6. **Record** what was scheduled (date, time, Metricool post id) in Setup status below, in the repo copy and the Project copy of this bible.

## Setup status

- Name locked: Heel & Serpent (Oct 13, 2026).
- Done: Instagram account @heelandserpent created; Metricool connected; logo system locked (Monogram, Seal, Cross & Serpent) (Oct 13).
- Done: post templates and a draft launch set (welcome Story, Marching Orders on Proverbs 24:16, Get Back Up carousel on Peter) (Oct 13).
- Launch set scheduled Oct 13, 2026 (Metricool): welcome Story Tue Oct 13, 9:30 AM CT (post 394994572); Marching Orders #1 Wed Oct 14, 6:45 AM CT (394994656); Get Back Up #1, Peter, Wed Oct 14, 7:15 PM CT (394994778). Working cadence: Marching Orders 6:45 AM, Get Back Up 7:15 PM.
- Intro carousel "Why Heel & Serpent" (Start Here, Genesis 3:15 and Romans 16:20) published Oct 13, 2026, 9:57 AM CT: https://www.instagram.com/p/DecE5YZDT3a/ (Metricool 395032100). Meant to stay pinned at the top of the profile. Set: posts/2026-10-13-intro/.
- Week 1 (Arm) scheduled Oct 13, 2026, set posts/2026-10-15-week1/ (38 verses). Armor Check runs Sundays 1:15 PM CT. Rebuilt in the rotating looks the same afternoon (Metricool ids changed on update; uuids did not). Metricool post ids, look in brackets:
  - Thu Oct 15: Marching Orders, 1 Cor 9:27, 6:45 AM (395318385) [Ledger]; Get Back Up, David, 7:15 PM (395318548) [Bone]
  - Fri Oct 16: Marching Orders, Eph 6:4 (395008539) [Classic]; Get Back Up, lie "too far gone" (395318688) [Engraved]
  - Sat Oct 17: Marching Orders, Ps 5:3 (395318742) [Bone]; Get Back Up, Jonah (395009231) [Classic]
  - Sun Oct 18: Marching Orders, 1 Cor 10:13 (395318798) [Bone]; Armor Check #1, belt of truth, 1:15 PM (395318899) [Engraved]; Get Back Up, lie "strong men don't apologize" (395009536) [Classic]
  - Mon Oct 19: Marching Orders, Col 3:23 (395318964) [Ledger]; Get Back Up, Samson (395319087) [Bone]
  - Tue Oct 20: Marching Orders, Josh 24:15 (395009927) [Classic]; Get Back Up, lie "it's just my temper" (395319232) [Ledger]
  - Wed Oct 21: Marching Orders, Rom 12:2 (395319273) [Forge]; Get Back Up, Paul (395319380) [Bone]
- Wed Oct 14: Marching Orders #1, Prov 24:16, rebuilt in Forge (395318152, posts/2026-10-13-launch/build_forge.py); Get Back Up #1, Peter, stays Classic (394994778).
- Tue Oct 13 evening (first posts in the new looks, set posts/2026-10-13-evening/): Marching Orders, Deut 6:7, 5:45 PM [Bone] (395317735); Get Back Up, lie "you're the only one" (Elijah), 8:30 PM [Ledger] (395318012).
- Next week (Arm) starts Thu Oct 22; Armor Check #2 is the breastplate of righteousness. Stories for week 1 are not built yet (feed only).
- Story burst "Before you sleep" (6 frames, 8:16–8:26 PM Oct 13, leading into the 8:30 Elijah post; Lamentations 3:22–23). Stories are built with make_variants.story_look() in the five looks, type kept inside y 300–1500. Polls, question boxes and link stickers can't go through Metricool; add them in the app. Set: stories/2026-10-13-before-you-sleep/.
- Stories "Tomorrow starts tonight" (3 Story videos with score_drive, 10:15–10:19 PM Oct 13; Isaiah 40:31). Set: stories/2026-10-13-tomorrow-starts-tonight/.
- Story "First light" (one-off dawn palette, 4 frames, one continuous score_drive score across all four; Mark 1:35) scheduled Wed Oct 14, 2026, 4:35–4:38 AM CT: Metricool 395698359, 395698387, 395698420, 395698448. Set: stories/2026-10-14-first-light/. Song: 10,000 Reasons (Bless the Lord), Matt Redman.
- Strike #3 (Proverbs 22:6, "Your kids are watching", first Reel on the new pacing, 11 s) scheduled Wed Oct 14, 2026, 3:30 PM CT (Metricool 396190107). Set: reels/2026-10-14-prov22-6/.
- Strike #2 (Psalm 4:8 night Reel, "Rest. Then rise.") published Oct 13, 2026, 8:44 PM CT: https://www.instagram.com/reel/DedO3WYE8Z7/ (Metricool 395475633). Set: reels/2026-10-13-psalm4-8/. Reel type width narrowed to 740 px the same night so lines clear Instagram's side buttons.
- Strike #1 (Micah 7:8 Reel) published Oct 13, 2026, 3:28 PM CT: https://www.instagram.com/reel/DecqtXAoNuJ/ (Metricool 395304172). Set: reels/2026-10-13-micah7-8/.
- Reels (Strike) added Oct 13, 2026. Instagram sounds can't be attached through Metricool: @heelandserpent is a Business account with no Facebook Page linked. Chris chose the original generated score instead (Oct 13); he can still add a trending sound in the app.
- On hold (Chris, Oct 13, 2026): comment and DM auto-replies via Metricool Flows. If revisited: narrow keyword triggers only, every reply says a real person reads the inbox, crisis messages point to 988, never an auto-reply on every comment.
- Oct 14, 2026: trademark knockout and domain check done (results under Merch). Domain, attorney and merch spending on hold until about mid-November 2026 (Chris).
