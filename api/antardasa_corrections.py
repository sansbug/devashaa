"""
Corrections to the mined antardaśā corpus (antardasa_rules.py), each checked
against the PAGE IMAGE of R. Santhanam's BPHS Vol II.

antardasa_rules.py is generated from the original extraction and is not edited by
hand. Where that extraction carried a scanning slip into a quoted string, the
corrected string lives HERE, with the page it was read from, and is applied when
antardasa.py loads the corpus. A correction names the exact damaged string it
replaces: if the corpus is ever regenerated and that string is gone, the
correction simply no longer matches (test_antardasa_corrections.py reports it)
rather than overwriting good text.

How these were found (2026-11-16): every result list in the corpus (427 of them)
was scanned for tokens that are not word-shaped (a character-trigram check
against the repo's own vocabulary). Three lists were flagged; two were damaged
and are corrected below; the third ("bleeding gulms", ch.57 vv.4-5½) is what the
page prints. This is NOT a full re-verification of the corpus: a slip that
happens to spell a real word would not have been caught.
"""

# (maha, antar, field, damaged string as mined, corrected string, where it was read)
CORRECTIONS = [
    ("saturn", "saturn", "results",
     "acquidtion of a kingdom (attainment of a high positibn in government), happiness from rl'ife and children, "
     "acquisition of conveyances like elephants, gain of clothes, attainment of the position of a connmander. of the "
     "armyby the beneficence of the king, acquisition'cf cattle, villages and land etc., will be derived",
     "acquisition of a kingdom (attainment of a high position in government), happiness from wife and children, "
     "acquisition of conveyances like elephants, gain of clothes, attainment of the position of a commander of the "
     "army by the beneficence of the king, acquisition of cattle, villages and land etc., will be derived",
     "BPHS Vol II ch.57 vv.1-3 — page image, PDF p.201"),
    ("saturn", "saturn", "quote",
     "l-3. Effects like acquidtion of a kingdom ... will be derived in' .the Antardasa of Saturn in the Dasa of Saturn, "
     "if Saturn be in his own sign, in his sign of exaltation or in deep exaltation, or be in kendta or trikona from "
     "the Ascendant, or be a yogakaraka.",
     "1-3. Effects like acquisition of a kingdom ... will be derived in the Antardasa of Saturn in the Dasa of Saturn, "
     "if Saturn be in his own sign, in his sign of exaltation or in deep exaltation, or be in kendra or trikona from "
     "the Ascendant, or be a yogakaraka.",
     "BPHS Vol II ch.57 vv.1-3 — page image, PDF p.201"),
    ("rahu", "mercury", "results",
     "same list as vv.30-33, plus: 'Good results like Raja Vogu,-f\"ntn\"ence of the king and gain-of wealth and "
     "reputation, *iff be realised particularly on wednesday in the month of MercurY.'",
     "same list as vv.30-33, plus: 'Good results like Raja yoga, beneficence of the king and gain of wealth and "
     "reputation, will be realised particularly on wednesday in the month of Mercury.'",
     "BPHS Vol II ch.55 vv.30-33 — page image, PDF p.179 (printed p.669)"),
    ("rahu", "mercury", "quote",
     "in kendra or in the Stn anA be endowed with strength'",
     "in kendra or in the 5th and be endowed with strength",
     "BPHS Vol II ch.55 vv.30-33 — page image, PDF p.179 (printed p.669)"),
]


def apply(matrix: dict) -> dict:
    """Apply every correction whose damaged string is still present. Returns {"applied": n, "unmatched": [...]}."""
    applied, unmatched = 0, []
    for maha, antar, field, was, now, where in CORRECTIONS:
        cell = matrix.get((maha, antar))
        hit = 0
        for cond in (cell or {}).get("conditions", []):
            if cond.get(field) == was:
                cond[field] = now
                hit += 1
            elif cond.get(field) == now:
                hit += 1                      # already applied (the module was loaded before)
        if hit:
            applied += hit
        else:
            unmatched.append((maha, antar, field, where))
    return {"applied": applied, "unmatched": unmatched}
