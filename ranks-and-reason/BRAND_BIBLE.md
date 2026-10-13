# Ranks & Reason: Brand Bible and Setup

Oct 12, 2026 · @Chris · Instagram: @ranksandreason

Short, narrated, animated explainers on military history, history and philosophy. One idea, one battle or one thinker per Reel. Secular: no faith content (that lives on Pensive Minds).

## Identity

- **Name field:** Ranks & Reason | History in 40s
- **Bio:** War, history & philosophy in under a minute. / One campaign at a time. ⚔️ / AI-narrated
- **Profile picture:** brass chevrons over an R&R monogram on charcoal (avatar_A_chevrons).
- **Series:** every Reel is a numbered "Campaign No. N". Multi-part stories run as Part 1, Part 2.
- **Metricool:** brand "Ranks & Reason", blogId 7390927, Instagram @ranksandreason, time zone America/Chicago (connected Oct 13, 2026).
- **AI disclosure:** the narration is a synthetic voice, so Instagram's AI-generated label is ON for every Reel, and the profile's AI label is on.

## Format (single Reels, not carousels)

- 30 to 50 seconds, 1080x1920, 30 fps, narrated, captions burned in (most people watch muted).
- **Structure:** hook in the first 2 seconds (a date, a number, a stake) → three or four beats → a hard payoff number or line → cliffhanger or follow prompt.
- **Visual language:** charcoal background with film grain and vignette; brass (#C49242) for highlights; bone (#E9E4D8) for friendly forces and text; red (#B23428) for the enemy; sea #16262C. DM Serif Display for big text and captions, DM Sans Bold for labels. Animated top-down maps with unit blocks, arrows, distance brackets, camera push-ins and impact shakes; big counters for casualty or army figures. Gemini stills or clips may be used for scene-setting.
- **Header on every frame:** "CAMPAIGN No. N" (brass) / "TOPIC · DATE" (muted) / "RANKS & REASON" (top right).
- **Captions:** two lines max per beat, one brass highlight word, inside the safe zone (y ≈ 1250 to 1450).
- **Sound:** narration first; synthesized drum score underneath (tom hits on beats, accelerating drums into a charge, a boom on the decisive moment), ducked under the voice. Target about -16 dB mean, peaks under -1 dB.

## Voice

- Pilot used a free open-source voice (Piper LibriTTS #432, CC BY 4.0). Rejected Oct 12 as not good enough.
- **Plan:** a paid studio-quality voice service (ElevenLabs Starter at $5/month to begin, with a commercial license; Creator at $22/month for daily posting). One consistent voice: deep, measured, documentary narrator.
- Chris signs in himself; scripts are generated in his account, then the MP3 is attached to the chat or pulled from his computer.

## Accuracy rules

- Every number, quote and claim traces to a named source (primary where possible: Herodotus, Thucydides, Caesar, Clausewitz, Sun Tzu in a named translation, etc.), with modern scholarship noted where the ancient figure is doubted ("per Herodotus").
- Keep a Sources log: Reel, claim, source.
- Separate legend from record (example: the Marathon-to-Athens run is a later legend; Herodotus records the run to Sparta).
- No invented quotes. Paraphrase unless the translation is public domain.

## Guardrails

- Educational, not glorifying: no gore, no graphic imagery, no celebration of killing.
- HOLD anything about current wars, living politicians or ongoing conflicts.
- No real living people named in a promotional way; no brands.
- The narrator is an AI voice and never claims to have served or to have been there.

## Pillars

1. **Battles that turned on one decision** (Marathon, Cannae, Agincourt, Midway).
2. **Commanders and their choices** (historical figures only).
3. **Ideas that shaped war and life** (Sun Tzu, Clausewitz, the Stoics, Machiavelli).
4. **Myth vs record** (what really happened vs the legend).

## Cadence

Start at 3 Reels a week at fixed times (adjust after the first month of data). Part 2s post within 48 hours of Part 1.

## Commands (for the Ranks & Reason Project)

| Command | Action |
| --- | --- |
| **Deploy** [topic] | Research, script, narrate, animate and publish one Reel now (AI label on). HOLD if it touches current events. |
| **Recon** | Report the latest Metricool numbers for @ranksandreason. |
| **Resupply** [notes] | Build and schedule next week's three Reels. |
| **Stand down** | Move all scheduled posts to draft. "Stand down off" restores them. |

## Pipeline (code)

The pilot's renderer and script live in the media repo under ranks-and-reason/: render.py (animation, captions, drum score, mux), beats.json (script beats with captions and highlight words). Fonts: DM Serif Display, DM Sans. Voice files are generated per beat, then laid on a timeline with 0.4 s gaps.

## Pilot status

- Campaign No. 1: Marathon (490 BC). 48 s. Rendered with the free voice; to be re-voiced with the paid voice before posting.
- Caption draft: "Ten thousand Athenians. The largest empire on Earth. And a general who did the unthinkable. At Marathon in 490 BC, Miltiades thinned his own center, stacked his wings and charged at a run. Herodotus counts 6,400 Persian dead to 192 Athenian. The run everyone remembers isn't the one that mattered. Part 2 next. Source: Herodotus, Histories, Book 6. #history #militaryhistory #ancientgreece #battleofmarathon #ancienthistory"
- Part 2 topic: Pheidippides' run to Sparta (about 150 miles in two days, per Herodotus) and the Spartans' answer (they waited for the full moon).

Sources for the pilot: Herodotus, Histories 6.105–117; Livius, "Marathon (490 BCE)".
