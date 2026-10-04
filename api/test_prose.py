"""
The prose scrubber — the sentences a reader meets with references off must
carry no book, author, chapter or page, and must still read as sentences.

Run:  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python test_prose.py
"""
import re

import prose

CASES = [
    # Bṛhat Jātaka templates
    ("Bṛhat Jātaka reads a native with the Sun in Aries as renowned, clever, much-travelled, and a \"bearer of arms\" (glossed: a martial vocation) — and, as the dated text states, of little wealth.",
     "A native with the Sun in Aries is renowned, clever, much-travelled, and a \"bearer of arms\" (glossed: a martial vocation) — and of little wealth."),
    ("Bṛhat Jātaka (18.1) reads the Sun-in-Taurus native as earning a livelihood through trade in scents and clothing. Presented as the text's ~550 CE stated reading, not as fate.",
     "The Sun-in-Taurus native is earning a livelihood through trade in scents and clothing."),
    ("Bṛhat Jātaka states that the Sun in Gemini makes the native educated and learned.",
     "The Sun in Gemini makes the native educated and learned."),
    ("Bṛhat Jātaka assigns the native honour from those in authority, a wandering life.",
     "The native is assigned honour from those in authority, a wandering life."),
    ("The text reads the native as deferential in close partnership, ungrateful in friendship.",
     "The native is deferential in close partnership, ungrateful in friendship."),
    # Charak asides
    ("Favour from those in authority (the text: royal favours), professional elevation, gain in wealth.",
     "Favour from those in authority, professional elevation, gain in wealth."),
    ("Generally favourable in respect of partner, children, vehicles and wealth; elevation of status (the text adds: promotion in job), gains from business.",
     "Generally favourable in respect of partner, children, vehicles and wealth; elevation of status, gains from business."),
    ("Fear from foes, quarrels, instability of temper. Also, the text states, separation from the partner or a divorce.",
     "Fear from foes, quarrels, instability of temper. Also, separation from the partner or a divorce."),
    ("Illness to the partner, domestic strife. The text carries K.N. Rao's note that a marriage arranged for that year may break down.",
     "Illness to the partner, domestic strife. A marriage arranged for that year may break down."),
    ("Serious illness, blood disorders. (Footnote: Ketu in the eighth acts in a similar way.)",
     "Serious illness, blood disorders."),
    # mid-sentence names and loci
    ("Sārāvalī 22.4 states that the native is fond of travel; BPHS ch.11 v.2 (p.121) gives the house its significations.",
     "The native is fond of travel; the tradition gives the house its significations."),
    ("In the Sun's deep exaltation the text raises the same signature: very famous, clever, wealthy.",
     "In the Sun's deep exaltation the tradition raises the same signature: very famous, clever, wealthy."),
    # short names in the house-axis corpora; a bare aside
    ("Brihat reads a native with the Sun in the 5th bhava as without wealth and as strained in the sphere of progeny.",
     "A native with the Sun in the 5th bhava is without wealth and as strained in the sphere of progeny."),
    ("Chamatkara reads a native with the sun in the fifth bhava as sharp and intelligent; the text also states hardship.",
     "A native with the sun in the fifth bhava is sharp and intelligent; the tradition also states hardship."),
    ("A long neck and ears. (the text)", "A long neck and ears."),
    ("Devoid of wealth (framed as the ~10th-c. reading, not fate). the text adds: e.g. travel.",
     "Devoid of wealth. E.g. travel."),
    ("Ill-tempered, e.g. in company; the tradition's view is kept plainly here. A ~1,000-year-old text's stated reading, cited and dated.",
     "Ill-tempered, e.g. in company."),
    # hedges
    ("Labouring at others' behest — and, as the text's dated view (not fate), of poor means.",
     "Labouring at others' behest — and of poor means."),
    ("A native with the Moon in the 12th bhava is wickedly disposed and defective in some limb — the bodily defect kept as the text's dated stated-effect, cited, not fate or medical advice.",
     "A native with the Moon in the 12th bhava is wickedly disposed and defective in some limb."),
    ("With offspring hard to come by, and — in the text's own dated and much-qualified view, not any prediction — short-lived.",
     "With offspring hard to come by, and short-lived."),
    ("Brihat reads a native with the Sun in the 5th bhava as without wealth and as strained in the sphere of progeny - the source's 'childless' clause kept progeny-neutrally, as difficulty in that sphere rather than a prediction of childlessness.",
     "A native with the Sun in the 5th bhava is without wealth and as strained in the sphere of progeny."),
    ("Educated and learned, earning a livelihood through astrology, and wealthy — given as the text's stated effect, not as the reader's fate.",
     "Educated and learned, earning a livelihood through astrology, and wealthy."),
    ("It also states, as a dated effect not fate, poor means. Its \"mean\" moral ranking is dropped.",
     "It also states poor means."),
    ("Benefit coming through one's partner [neutralised from the verse's \"fortunate through housewives\"], while otherwise steady.",
     "Benefit coming through one's partner, while otherwise steady."),
    ("Few children (neutralised from the text's 'few sons'). Shown as the text's dated (~550 CE) reading, not as fate.",
     "Few children."),
    ("It reads the person as liberal (generous), skilful, and fortunate. In its own idiom it also assigns \"two mothers,\" traditionally understood as two mother-figures.",
     "The person is liberal (generous), skilful, and fortunate. The native is assigned \"two mothers,\" traditionally understood as two mother-figures."),
    ("Though bereft of co-born (siblings). No dated social content attaches; the traits ship plainly.",
     "Though bereft of co-born (siblings)."),
    ("Agitated, and poor (its dated view, not fate); any word on offspring is kept only as strain in the progeny sphere, no count asserted.",
     "Agitated, and poor."),
    ("Having many foes, easily startled, and mean; and — as the text's dated stated-effect — devoid of wealth (framed as the ~10th-c. reading, not fate).",
     "Having many foes, easily startled, and mean; devoid of wealth."),
    ("Wanting for progeny, wealth and happiness. Stated as the classical view, not a prediction and not medical advice.",
     "Wanting for progeny, wealth and happiness."),
    # untouched
    ("Gain of wealth without effort, much comfort to partner and children.",
     "Gain of wealth without effort, much comfort to partner and children."),
]

FORBIDDEN = re.compile(r"Bṛhat|BPHS|Sārāvalī|Charak|Rao|Patel|Phaladīpikā|\bthe text\b|\bThe text\b|\bch\.\d|\bp\.\d", re.I)


def _ok(name, cond, detail=""):
    print(f"  {'OK ' if cond else 'XX '}{name:60s} {detail}")
    assert cond, f"{name} {detail}"


def test_cases():
    for src, want in CASES:
        got = prose.scrub(src)
        _ok(src[:56], got == want, "" if got == want else f"\n      got:  {got}\n      want: {want}")


def test_no_source_survives_in_the_corpora():
    import brihat_jataka_rules as bj
    import charak_annual_rules as ch
    gists = [e["gist"] for g in bj.IN_SIGN.values() for e in g.values()]
    gists += [e["gist"] for g in ch.IN_HOUSE.values() for e in g.values()]
    gists += [e["gist"] for g in ch.BY_STRENGTH.values() for e in g.values()]
    left = [g for g in gists if FORBIDDEN.search(prose.scrub(g))]
    _ok(f"{len(gists)} gists scrubbed, none still names a source", not left, "\n      " + "\n      ".join(x[:120] for x in left[:6]))
    bad_start = [prose.scrub(g) for g in gists if prose.scrub(g) and not prose.scrub(g)[0].isupper() and not prose.scrub(g)[0] in "\"“'‘(—"]
    _ok("every scrubbed gist starts with a capital", not bad_start, "\n      " + "\n      ".join(x[:100] for x in bad_start[:5]))


def test_payload_walk_keeps_the_references():
    pay = {"gist": "Bṛhat Jātaka states that the native is kind.", "citation": "Bṛhat Jātaka 18.1",
           "source": {"text": "A Textbook of Varshaphala", "author": "K.S. Charak"},
           "sources": [{"gist": "The text reads the native as calm.", "citation": "Sārāvalī 22.4"}],
           "adaptation": {"note": "the text's clause omitted"}, "n": 3}
    out = prose.scrub_payload(pay)
    _ok("gist scrubbed", out["gist"] == "The native is kind.", out["gist"])
    _ok("citation untouched", out["citation"] == "Bṛhat Jātaka 18.1")
    _ok("source registry untouched", out["source"]["author"] == "K.S. Charak")
    _ok("nested sources: gist scrubbed, citation kept", out["sources"][0]["gist"] == "The native is calm." and out["sources"][0]["citation"] == "Sārāvalī 22.4")
    _ok("adaptation untouched", out["adaptation"]["note"].startswith("the text"))
    _ok("non-strings pass through", out["n"] == 3)


def main():
    failed = 0
    for n in [k for k in globals() if k.startswith("test_")]:
        print(f"\n{n}")
        try:
            globals()[n]()
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAILED: {e}")
    print("\n" + ("ALL PASS ✓" if not failed else f"{failed} FAILED ✗"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
