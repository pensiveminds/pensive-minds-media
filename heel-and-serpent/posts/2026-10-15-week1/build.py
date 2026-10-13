"""Week 1: Thu Oct 15 - Wed Oct 21, 2026. 7 Marching Orders, 7 Get Back Up, 1 Armor Check.

    python3 posts/2026-10-15-week1/build.py

Scripture: CSB, checked verbatim against BibleGateway (CSB) on Oct 13, 2026. Partial verses marked
with an ellipsis. Every verse is logged in SOURCES.md.

Pillar rotation (no pillar twice in a row):
  Thu MO discipline · GBU get back up (David)
  Fri MO father     · GBU enemy (lie: too far gone)
  Sat MO discipline · GBU get back up (Jonah)
  Sun MO enemy      · Armor Check (belt of truth) · GBU father (lie: strong men don't apologize)
  Mon MO discipline · GBU get back up (Samson)
  Tue MO father     · GBU enemy (lie: it's just my temper)
  Wed MO discipline · GBU get back up (Paul)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_posts import marching_orders, slide, story, render_set

G, A = "Get Back Up", "Armor Check"

def gbu(prefix, slides, series=G):
    """slides: list of slide() kwargs; returns {filename: svg}."""
    n = len(slides)
    return {f"{prefix}_{i+1}.jpg": slide(series, f"{i+1} / {n}", **kw) for i, kw in enumerate(slides)}

SET = {}

# ---------------------------------------------------------------- Thu Oct 15
SET["01_thu_marching_orders_1cor9-27.jpg"] = marching_orders(
    ["MASTER", "YOUR [BODY]."],
    ["“…I discipline my body and bring it", "under strict control…”"],
    "1 Corinthians 9:27, CSB",
    sub=["Move before you scroll. Sweat before you sit."])

SET.update(gbu("02_thu_get_back_up_david", [
    dict(title=["A KING AT", "HIS [WORST]"], body=["David. Swipe."], cover=True),
    dict(title=["He stayed home", "from the war."],
         verse_lines=["“In the spring when kings march out", "to war… David remained in Jerusalem.”"],
         ref="2 Samuel 11:1, CSB"),
    dict(title=["Idle hands found", "another man’s wife."],
         body=["Then he had her husband killed to hide it."],
         verse_lines=["Nathan replied to David,", "“You are the man!…”"], ref="2 Samuel 12:7, CSB"),
    dict(title=["No excuses.", "He [owned] it."],
         verse_lines=["David responded to Nathan,", "“I have sinned against the LORD.”…"],
         ref="2 Samuel 12:13, CSB"),
    dict(title=["Then he asked", "for a new [heart]."],
         body=["The consequences were real. So was the mercy."],
         verse_lines=["“God, create a clean heart for me", "and renew a steadfast spirit within me.”"],
         ref="Psalm 51:10, CSB"),
    dict(title=["CONFESSION", "IS WHERE KINGS", "[RISE]."], body=["Own it. Get back up."], close=True),
]))

# ---------------------------------------------------------------- Fri Oct 16
SET["03_fri_marching_orders_eph6-4.jpg"] = marching_orders(
    ["STRONG HANDS.", "[GENTLE] VOICE."],
    ["“Fathers, don’t stir up anger in your children,", "but bring them up in the training",
     "and instruction of the Lord.”"],
    "Ephesians 6:4, CSB",
    sub=["Tonight, ask your kid one real question."])

SET.update(gbu("04_fri_get_back_up_too_far", [
    dict(title=["THE LIE:", "YOU’VE GONE", "TOO [FAR]."], body=["Swipe for the truth."], cover=True),
    dict(title=["That voice is", "a [liar]."], body=["It’s the only thing he’s good at."],
         verse_lines=["“…When he tells a lie, he speaks", "from his own nature, because he is",
                      "a liar and the father of lies.”"], ref="John 8:44, CSB"),
    dict(title=["He says the stain", "is [permanent]."],
         verse_lines=["“Come, let’s settle this,” says the LORD.", "“Though your sins are scarlet,",
                      "they will be as white as snow…”"], ref="Isaiah 1:18, CSB"),
    dict(title=["He says you’re", "too far [gone]."],
         verse_lines=["“As far as the east is from the west,", "so far has he removed",
                      "our transgressions from us.”"], ref="Psalm 103:12, CSB"),
    dict(title=["He says you’re", "[condemned]."],
         verse_lines=["“Therefore, there is now no condemnation", "for those in Christ Jesus…”"],
         ref="Romans 8:1, CSB"),
    dict(title=["NOT TOO FAR.", "NOT TOO LATE.", "COME [HOME]."], body=["Get back up."], close=True),
]))

# ---------------------------------------------------------------- Sat Oct 17
SET["05_sat_marching_orders_ps5-3.jpg"] = marching_orders(
    ["WIN THE", "FIRST [HOUR]."],
    ["“In the morning, LORD, you hear my voice;", "in the morning I plead my case to you",
     "and watch expectantly.”"],
    "Psalm 5:3, CSB",
    sub=["Phone down. Book open. Knees on the floor."])

SET.update(gbu("06_sat_get_back_up_jonah", [
    dict(title=["THE MAN WHO", "RAN THE", "OTHER [WAY]"], body=["Jonah. Swipe."], cover=True),
    dict(title=["God said go.", "He bought a [ticket]", "the other way."],
         verse_lines=["“Jonah got up to flee to Tarshish", "from the LORD’s presence…”"], ref="Jonah 1:3, CSB"),
    dict(title=["He hit bottom.", "[Literally]."],
         verse_lines=["“The LORD appointed a great fish", "to swallow Jonah…”"], ref="Jonah 1:17, CSB"),
    dict(title=["From the bottom,", "he [prayed]."],
         verse_lines=["“I called to the LORD in my distress,", "and he answered me…”"], ref="Jonah 2:2, CSB"),
    dict(title=["God gave him", "the same orders", "[again]."],
         verse_lines=["“The word of the LORD came", "to Jonah a second time…”"], ref="Jonah 3:1, CSB"),
    dict(title=["THE CALL", "DIDN’T", "[EXPIRE]."], body=["Turn around. Get back up."], close=True),
]))

# ---------------------------------------------------------------- Sun Oct 18
SET["07_sun_marching_orders_1cor10-13.jpg"] = marching_orders(
    ["TAKE THE", "WAY\u2002[OUT]."],
    ["“…God is faithful; he will not allow you", "to be tempted beyond what you are able,",
     "but with the temptation he will also", "provide the way out…”"],
    "1 Corinthians 10:13, CSB",
    sub=["There’s always a door. Walk through it."])

SET.update(gbu("08_sun_armor_check_belt", [
    dict(title=["THE BELT", "OF [TRUTH]"], body=["Armor piece 1 of 6. Swipe."], cover=True),
    dict(title=["Know who you’re", "really [fighting]."],
         verse_lines=["“For our struggle is not", "against flesh and blood…”"], ref="Ephesians 6:12, CSB"),
    dict(title=["The first piece", "goes on at the [waist]."],
         verse_lines=["“Stand, therefore, with truth", "like a belt around your waist…”"],
         ref="Ephesians 6:14, CSB"),
    dict(title=["The belt holds", "everything else", "in [place]."],
         body=["Lose the truth and the rest comes loose."],
         verse_lines=["“You will know the truth,", "and the truth will set you free.”"], ref="John 8:32, CSB"),
    dict(title=["Check [yours]."],
         body=["Where are you lying to yourself?", "To your wife? To God?", "Name it. Then tell the truth."]),
    dict(title=["BUCKLE IT", "[TIGHT]."], body=["Next Sunday: the breastplate."], close=True),
], series=A))

SET.update(gbu("09_sun_get_back_up_apologize", [
    dict(title=["THE LIE:", "STRONG MEN DON’T", "[APOLOGIZE]."], body=["Swipe."], cover=True),
    dict(title=["Pride calls it", "[strength]."],
         verse_lines=["“Pride comes before destruction,", "and an arrogant spirit before a fall.”"],
         ref="Proverbs 16:18, CSB"),
    dict(title=["Your kids learn what", "a man is from [you]."],
         verse_lines=["“A righteous person acts with integrity;", "his children who come after him",
                      "will be happy.”"], ref="Proverbs 20:7, CSB"),
    dict(title=["Owning it takes", "more [spine] than", "hiding it."],
         verse_lines=["“Therefore, confess your sins to one another", "and pray for one another,",
                      "so that you may be healed…”"], ref="James 5:16, CSB"),
    dict(title=["Get down to", "eye [level]."], body=["“I was wrong. I’m sorry. I love you.”"],
         verse_lines=["“Fathers, do not exasperate your children,", "so that they won’t become discouraged.”"],
         ref="Colossians 3:21, CSB"),
    dict(title=["THE STRONGEST", "MAN IN THE HOUSE", "[KNEELS] FIRST."], body=["Go make it right tonight."],
         close=True),
]))

# ---------------------------------------------------------------- Mon Oct 19
SET["10_mon_marching_orders_col3-23.jpg"] = marching_orders(
    ["DO IT", "FOR [HIM]."],
    ["“Whatever you do, do it from the heart,", "as something done for the Lord", "and not for people…”"],
    "Colossians 3:23, CSB",
    sub=["Clock in like it’s worship. Because it is."])

SET.update(gbu("11_mon_get_back_up_samson", [
    dict(title=["THE STRONGEST", "MAN WHO", "[FELL]"], body=["Samson. Swipe."], cover=True),
    dict(title=["He had a gift.", "He [played] with it."], body=["One compromise after another."],
         verse_lines=["“…But he did not know", "that the LORD had left him.”"], ref="Judges 16:20, CSB"),
    dict(title=["Blind. Chained.", "Grinding grain", "in [prison]."], body=["Most men would call it over."]),
    dict(title=["But something", "started [growing]."],
         verse_lines=["“But his hair began to grow back", "after it had been shaved.”"], ref="Judges 16:22, CSB"),
    dict(title=["God still named him", "among the [faithful]."],
         body=["Hebrews 11 lists Samson with Gideon and David."],
         verse_lines=["“…gained strength in weakness…”"], ref="Hebrews 11:34, CSB"),
    dict(title=["YOUR STRENGTH", "IS GROWING", "[BACK]."], body=["Get back up."], close=True),
]))

# ---------------------------------------------------------------- Tue Oct 20
SET["12_tue_marching_orders_josh24-15.jpg"] = marching_orders(
    ["LEAD YOUR", "[HOUSE]."],
    ["“…As for me and my family,", "we will worship the LORD.”"],
    "Joshua 24:15, CSB",
    sub=["Pray over them before they sleep."])

SET.update(gbu("13_tue_get_back_up_temper", [
    dict(title=["THE LIE:", "IT’S JUST", "MY [TEMPER]."], body=["Swipe."], cover=True),
    dict(title=["Anger isn’t the sin.", "Letting it [rule] is."],
         verse_lines=["“Be angry and do not sin.", "Don’t let the sun go down on your anger…”"],
         ref="Ephesians 4:26, CSB"),
    dict(title=["The strong man", "holds his [fire]."],
         verse_lines=["“Patience is better than power,", "and controlling one’s emotions,",
                      "than capturing a city.”"], ref="Proverbs 16:32, CSB"),
    dict(title=["Slow is a", "[choice]."],
         verse_lines=["“…Everyone should be quick to listen,", "slow to speak, and slow to anger…”"],
         ref="James 1:19, CSB"),
    dict(title=["Lower your", "[voice]."], body=["Walk it off. Come back calm. Then talk."],
         verse_lines=["“A gentle answer turns away anger,", "but a harsh word stirs up wrath.”"],
         ref="Proverbs 15:1, CSB"),
    dict(title=["STRONG ENOUGH", "TO FIGHT.", "CHOOSING [PEACE]."], body=["Get back up."], close=True),
]))

# ---------------------------------------------------------------- Wed Oct 21
SET["14_wed_marching_orders_rom12-2.jpg"] = marching_orders(
    ["RENEW YOUR", "[MIND]."],
    ["“Do not be conformed to this age,", "but be transformed", "by the renewing of your mind…”"],
    "Romans 12:2, CSB",
    sub=["Cut one thing that’s poisoning it."])

SET.update(gbu("15_wed_get_back_up_paul", [
    dict(title=["THE MAN WHO", "HUNTED", "[CHRISTIANS]"], body=["Paul. Swipe."], cover=True),
    dict(title=["He dragged", "believers to [prison]."],
         verse_lines=["“Saul, however, was ravaging the church.", "He would enter house after house,",
                      "drag off men and women,", "and put them in prison.”"], ref="Acts 8:3, CSB"),
    dict(title=["Then God knocked", "him [down]."],
         verse_lines=["Falling to the ground, he heard a voice", "saying to him, “Saul, Saul,",
                      "why are you persecuting me?”"], ref="Acts 9:4, CSB"),
    dict(title=["He called himself", "the [worst]."],
         verse_lines=["…“Christ Jesus came into the world", "to save sinners”—and I am the worst of them."],
         ref="1 Timothy 1:15, CSB"),
    dict(title=["He didn’t stay", "[down]."],
         verse_lines=["“…Forgetting what is behind and reaching", "forward to what is ahead, I pursue as my goal",
                      "the prize promised by God’s heavenly call", "in Christ Jesus.”"],
         ref="Philippians 3:13–14, CSB"),
    dict(title=["YOUR PAST", "ISN’T YOUR", "[ORDERS]."], body=["Get back up."], close=True),
]))

if __name__ == "__main__":
    print("\n".join(render_set(SET, HERE)))
