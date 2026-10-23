"""Feed set Sat Oct 24 - Sat Oct 31, 2026 (weekly task, built Oct 23). One feed post a day.

    python3 posts/2026-10-24-week/build.py

Scripture: CSB, from VERSE_BANK.json (checked verbatim against BibleGateway, Oct 20, 2026). Partial verses
are marked with an ellipsis. Every verse is logged in SOURCES.md.

  Sat Oct 24, 6:55 PM  Get Back Up: Jacob, wrestled till dawn (get back up) [Bone]
  Sun Oct 25, 1:15 PM  Armor Check #2: the breastplate of righteousness (armor) [Engraved]
  Mon Oct 26, 6:45 AM  Marching Orders: 2 Timothy 1:7 (enemy) [Classic]
  Tue Oct 27, 7:15 PM  Get Back Up: the lie "your past is who you are" (enemy) [Bone]
  Wed Oct 28, 6:45 AM  Marching Orders: 1 Corinthians 16:13 (discipline) [Ledger]
  Thu Oct 29, 7:15 PM  Get Back Up: Joseph, sold, jailed, faithful (get back up) [Classic]
  Fri Oct 30, 6:45 AM  Marching Orders: Ephesians 4:32 (father) [Forge]
  Sat Oct 31, 7:15 PM  Get Back Up: John Mark, the quitter who came back (get back up) [Bone]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from make_variants import mo_look, carousel, render_looks

G, A = "Get Back Up", "Armor Check"
SET = {}
SET.update(carousel("bone", "01_sat_get_back_up_jacob", G, [
    dict(title=["HE WRESTLED", "TILL [DAWN]"], body=["Jacob. Swipe."], cover=True),
    dict(title=["He was [alone]."],
         verse_lines=["“Jacob was left alone,", "and a man wrestled with him", "until daybreak.”"], ref="Genesis 32:24, CSB"),
    dict(title=["He came away", "[wounded]."],
         verse_lines=["“…he struck Jacob’s hip socket", "as they wrestled", "and dislocated his hip.”"], ref="Genesis 32:25, CSB"),
    dict(title=["He didn’t", "let [go]."],
         verse_lines=["“…I will not let you go", "unless you bless me.”"], ref="Genesis 32:26, CSB"),
    dict(title=["He left with", "a new [name]."],
         verse_lines=["“…It will be Israel because", "you have struggled with God", "and with men and have prevailed.”"],
         ref="Genesis 32:28, CSB"),
    dict(title=["BLESSED.", "AND [LIMPING]."], body=["Get back up."], close=True),
]))
SET.update(carousel("engraved", "02_sun_armor_check_breastplate", A, [
    dict(title=["THE", "BREASTPLATE OF", "[RIGHTEOUSNESS]"], body=["Armor piece 2 of 6. Swipe."], cover=True),
    dict(title=["It covers", "the [heart]."],
         verse_lines=["“Guard your heart above all else,", "for it is the source of life.”"], ref="Proverbs 4:23, CSB"),
    dict(title=["It isn’t", "your [own]."],
         verse_lines=["“…not having a righteousness", "of my own from the law,", "but one that is through faith", "in Christ…”"],
         ref="Philippians 3:9, CSB"),
    dict(title=["It was", "[given] to you."],
         verse_lines=["“He made the one who did not know sin", "to be sin for us, so that in him", "we might become the righteousness", "of God.”"],
         ref="2 Corinthians 5:21, CSB"),
    dict(title=["Check [yours]."],
         body=["Trying to earn it?", "Hiding a crack under it?", "Wear His. Then walk clean."]),
    dict(title=["STRAP IT", "[ON]."], body=["Next Sunday: the shoes of peace."], close=True),
], ))
SET["03_mon_marching_orders_2tim1-7.jpg"] = mo_look("classic",
    ["FEAR IS NOT", "YOUR [ORDERS]."],
    ["“For God has not given us a spirit", "of fear, but one of power,", "love, and sound judgment.”"],
    "2 Timothy 1:7, CSB",
    sub=["Walk in what He gave you."])
SET.update(carousel("bone", "04_tue_get_back_up_past", G, [
    dict(title=["THE LIE:", "YOUR PAST IS", "WHO YOU [ARE]."], body=["Swipe."], cover=True),
    dict(title=["In Christ,", "the old is [gone]."],
         verse_lines=["“…if anyone is in Christ, he is", "a new creation; the old has passed away,", "and see, the new has come!”"],
         ref="2 Corinthians 5:17, CSB"),
    dict(title=["He has made", "a way [before]."],
         verse_lines=["“Look, I am about to do something new;", "even now it is coming. Do you not see it?", "Indeed, I will make a way", "in the wilderness…”"],
         ref="Isaiah 43:19, CSB"),
    dict(title=["Confess it.", "He [cleans] it."],
         verse_lines=["“If we confess our sins, he is faithful", "and righteous to forgive us our sins", "and to cleanse us", "from all unrighteousness.”"],
         ref="1 John 1:9, CSB"),
    dict(title=["He isn’t done", "with [you]."],
         verse_lines=["“…he who started a good work in you", "will carry it on to completion", "until the day of Christ Jesus.”"],
         ref="Philippians 1:6, CSB"),
    dict(title=["YOUR PAST", "ISN’T YOUR", "[NAME]."], body=["Get back up."], close=True),
]))
SET["05_wed_marching_orders_1cor16-13_ledger.jpg"] = mo_look("ledger",
    ["STAND", "[FIRM]."],
    ["“Be alert, stand firm in the faith,", "be courageous, be strong.”"],
    "1 Corinthians 16:13, CSB",
    sub=["Then do it all in love."])
SET.update(carousel("classic", "06_thu_get_back_up_joseph", G, [
    dict(title=["SOLD. JAILED.", "[FAITHFUL]."], body=["Joseph. Swipe."], cover=True),
    dict(title=["His own brothers", "[sold] him."],
         verse_lines=["“…his brothers pulled Joseph out of the pit", "and sold him for twenty pieces of silver", "to the Ishmaelites…”"],
         ref="Genesis 37:28, CSB"),
    dict(title=["Then prison,", "for a wrong he", "didn’t [do]."],
         verse_lines=["“…So Joseph was there in prison.”"], ref="Genesis 39:20, CSB"),
    dict(title=["God never", "[left]."],
         verse_lines=["“But the LORD was with Joseph", "and extended kindness to him…”"], ref="Genesis 39:21, CSB"),
    dict(title=["Years later,", "he [forgave]."],
         verse_lines=["“You planned evil against me;", "God planned it for good…”"], ref="Genesis 50:20, CSB"),
    dict(title=["WRONGED", "IS NOT", "[FINISHED]."], body=["Get back up."], close=True),
]))
SET["07_fri_marching_orders_eph4-32_forge.jpg"] = mo_look("forge",
    ["FORGIVE", "[FIRST]."],
    ["“And be kind and compassionate", "to one another, forgiving one another,", "just as God also forgave you in Christ.”"],
    "Ephesians 4:32, CSB",
    sub=["Start at home."])
SET.update(carousel("bone", "08_sat_get_back_up_john_mark", G, [
    dict(title=["THE QUITTER", "WHO CAME", "[BACK]"], body=["John Mark. Swipe."], cover=True),
    dict(title=["He [quit]."],
         verse_lines=["“…this man who had deserted them", "in Pamphylia and had not gone on", "with them to the work.”"],
         ref="Acts 15:38, CSB"),
    dict(title=["One brother", "didn’t give", "up on [him]."],
         verse_lines=["“…Barnabas took Mark with him", "and sailed off to Cyprus.”"], ref="Acts 15:39, CSB"),
    dict(title=["Years [later]."],
         verse_lines=["“…Bring Mark with you,", "for he is useful to me", "in the ministry.”"], ref="2 Timothy 4:11, CSB"),
    dict(title=["Quitting once", "isn’t your [story]."],
         body=["Come back.", "And be the brother who goes and gets him."]),
    dict(title=["COME", "[BACK]."], body=["Get back up."], close=True),
]))

if __name__ == "__main__":
    print("\n".join(render_looks(SET, HERE)))
