# Heel & Serpent: Status

What is running right now. Update this file whenever the plan, the queue, the task or the bank changes; put the dated history in LOG.md. Rules live in BRAND_BIBLE.md.

Last updated: Nov 1, 2026, 7:50 PM CT.

## Current plan (set Nov 1, 2026; frozen until Dec 1, 2026)

- One Strike Reel every other day at 3:30 PM CT. Posting days are an even number of days after Wed Oct 28, 2026 (Nov 1, 3, 5 … 29, Dec 1 …): `(date - 2026-10-28).days % 2 == 0`.
- Reels only. No feed posts, no Stories. Feed posts reached 1–6 people each; every non-follower reach came from Reels.
- Pace: slow for every new Reel. The pacing test ended Nov 1 (slow averaged 88 reach per Reel and 17% watched past 3 s; fast 47 and 15%). Reels already built on fast stay as built.
- No cadence, time or format change before Dec 1 unless Chris says so. Between Oct 13 and Oct 28 the cadence changed four times, each on two to five days of data, and no test finished. One month of clean data first.
- Review: Dec 1, 2026. Run Watch against the gauge below, then decide: continue (and daily vs every other day, on per-Reel reach) or Sheathe.
- Chris, Nov 1, 2026 (evening): posting never waits on him; no trending-sound step. He takes the commenting and engagement. Keep usage low (his main usage goes to another project); he trusts the gauge below. No instant growth needed, but the spend must not be waste.
- Spend: the only recurring cost is the scheduled task, twice a month (Nov 15 and Dec 1). No live build sessions, no hook-redesign session, no Stories or feed posts unless Chris asks. Hook improvement rides free inside the task prompt (open on a specific, ordinary weight a man recognizes).
- **Gauge, Dec 1, 2026 (Chris says Watch):** continue only if the November Reels average more than 100 reach each (October: 70) and the account adds 30 or more followers in November (count read in the Instagram app). If either misses, Sheathe: the task stops and the spend stops; decide then whether to redesign or retire the page.

## Queue (Metricool, blogId 7400959, America/Chicago)

All at 3:30 PM CT, type REEL, autoPublish, cover jpg set, set reels/<date>-<slug>/. Times confirmed after the Nov 1 clock change.

| Day | Verse | Pace | Score | Metricool id |
| --- | --- | --- | --- | --- |
| Tue Nov 3 | John 16:33 | slow | pulse G 126 | 413031310 |
| Thu Nov 5 | Ephesians 5:25 (partial) | fast | hymn G 69 | 413031326 |
| Sat Nov 7 | Matthew 26:41 | slow | dawn F 77 | 413031341 |
| Mon Nov 9 | Galatians 6:2 | fast | anthem F 94 | 413031356 |
| Wed Nov 11 | Psalm 40:2 (988 line in caption) | slow | nocturne C 65 | 413031737 |
| Fri Nov 13 | Ephesians 6:16 | fast | march Bb 100 | 413031754 |
| Sun Nov 15 | 1 Peter 2:11 | slow | pulse Bb 121 | 413031768 |
| Tue Nov 17 | John 15:13 | fast | hymn D 70 | 413031781 |

Next uncovered posting days: Nov 19, 21, 23, 25, 27, 29, Dec 1. The Nov 15 task run fills through Dec 2.

**Built but unpublished** (Metricool drafts dated in the past). Chris decides in a live session: use them (move the date to an open posting day and untick draft) or delete them and un-mark their verses in VERSE_BANK.json and SOURCES.md. The scheduled task leaves drafts alone. Their verses are already marked used.

- Reel Romans 8:37, fast, dawn F 80 (409454697), reels/2026-10-29-rom8-37/
- Reel Psalm 27:1, fast, nocturne A 68 (409454721), reels/2026-10-31-ps27-1/
- Get Back Up carousel, Joseph [Classic] (409454708), posts/2026-10-24-week/
- Get Back Up carousel, John Mark [Bone] (409454729), posts/2026-10-24-week/

## Scheduled task

- **"Heel & Serpent Arm (every-other-day Reels)"**, id trig_013uukPqcVyA7iA2e8nRZuJ7. Runs the 1st and 15th at 9:48 AM CT in the cloud with automatic approval, model Opus 5.5. Fills every posting day from the run (if its 3:30 PM slot is at least 3 hours away) through 17 days out with one Reel each; never duplicates a day that already has a non-draft REEL; builds only from REEL_QUEUE.json and VERSE_BANK.json; pushes to main; schedules via Metricool; records the run; reports to Chris by push and email.
- Stops if heel-and-serpent/PAUSED exists (Sheathe).
- Last run: Nov 1, 2026, 9:48 AM CT, succeeded (scheduled Nov 1–17). Next run: Nov 15, 2026.
- The only scheduled task for this page. The earlier daily and weekly tasks were this same task, renamed.
- Prompt current as of Nov 1, 2026, 7:50 PM CT (slow only; reads STATUS.md; records in STATUS.md and LOG.md). The text is kept in TASK_PROMPT.md; change both together.

## Verse bank

- VERSE_BANK.json: 109 CSB verses plus 7 story passages, verified byte for byte against BibleGateway (CSB). After the Nov 1 run: 73 unused verses; 3 unused story passages (Moses, Thomas, the prodigal son). Ephesians 6:14 is marked used (its first clause ran Oct 18), so breastplate posts quote other verses.
- Refill in a live session (built-in browser, BibleGateway, CSB) when fewer than 20 unused remain; the task flags it.
- Running total of verses on posts: 112 (SOURCES.md). CSB license cap: 1,000.

## Numbers to date

Reels, Oct 13–30 (14 published; the Nov 1 Reel is not in yet):

- Reach 12–147 each, average 70, no upward trend. Average watch time 1.6–4.4 s on 10–16 s videos. 8–24% watched past 3 s. 51 likes, 9 saves, 3 shares (all on the Psalm 4:8 night Reel), 0 comments.
- Best: Psalm 4:8 "You carried it all day" (Oct 13, 8:44 PM: reach 147, 24% past 3 s, 3 shares); Micah 7:8 (114); 2 Tim 4:7 (105); Neh 4:14 (103); 1 Pet 5:8 (102); Prov 27:17 (100). Worst: James 4:7 (12), Prov 22:6 (16), 2 Cor 12:9 (16), Josh 1:9 (36).
- Slow vs fast: slow 8 Reels, average reach 88 (74 without launch day), 17% past 3 s; fast 6 Reels, average reach 47, 15% past 3 s.
- Feed: 29 posts, reach 1–6 each, 0 follows attributed, 1 share (the intro carousel). Stories: 13, Oct 13–14 only.
- Reach by audience: non-followers almost entirely from Reels (10–180 a day); followers 1–3 a day.
- Followers: Metricool's follower series is unreliable for this brand (it showed 14, 35, 43, 44, then 175 on consecutive days in late October). Read the count in the Instagram app. Metricool's "gained" column showed +3, +1, +4 on Oct 28–30.

## Metricool notes

- Brand "Heel & Serpent", blogId 7400959, Instagram @heelandserpent, time zone America/Chicago. Before any bulk scheduling, getBrandSettings must show instagramData "heelandserpent".
- Clock changes: a post set for 7:00–7:59 PM CT on the night Madrid (the account's join zone) changes its clocks saved an hour off (Oct 24, 2026). Check publicationDate in every create result around US and EU clock changes.
- Instagram sounds can't be attached through Metricool (Business account, no Facebook Page linked). Polls, question boxes and link stickers can't go through Metricool either; add them in the app.
- Metricool Flows (comment and DM auto-replies): on hold (Chris, Oct 13, 2026). If revisited: narrow keyword triggers only, every reply says a real person reads the inbox, crisis messages point to 988, never an auto-reply on every comment.

## Growth levers only Chris can pull

- 10 minutes a day of real comments from @heelandserpent on larger Christian men's and fatherhood pages.
- A trending sound added to each Reel in the app.
- Sharing a Reel from his personal account.

Suggested Oct 20 and again Nov 1, 2026. His call.
