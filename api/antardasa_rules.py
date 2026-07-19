"""The 81-cell antardaśā condition matrix — BPHS Vol II ch.52-60.

GENERATED from a mined-and-adversarially-verified extraction. Not retyped:
nine chapters, 81 cells, 559 conditions, each carrying its own frame, source,
quote and page. Hand-transcribing that is where this project's errors have
come from.

WHAT THIS FILE IS FOR, AND WHAT IT IS NOT
-----------------------------------------
It supports a CONDITION-FIRING engine, not a verdict engine. The distinction is
forced by two censuses over the corpus.

FRAMES. 326 of the 559 conditions reference a house. Of those, 111 are counted
from the lagna, 107 from the daśā lord, 1 from the Moon — and 107 STATE NO
FRAME AT ALL. One house condition in three has no anchor.

That third is adversarially placed. It clusters on the OPENING kendra/trikoṇa
branch of a cell — the branch a real chart most often lands on. Roughly 25-30
of the 81 cells have their headline favourable branch unevaluable, and ch.54's
entire Mars-in-Mars cell is frameless, which is the first cell any engine hits.
So an evaluator that quietly skips unframed conditions will report "nothing
fires" on charts where BPHS does state something — it just does not say from
where. Those conditions are therefore returned as UNAVAILABLE, loudly, never
omitted.

POLARITY. Roughly one branch in five carries a valence word at all, and the
mined tagging does NOT distinguish a branch-level label ("will be the EVIL
effects") from an item-level noun ("...LOSS of position, quarrels ... will be
realised"). The verifiers found most hits are item-level — one counted 19 of 24
in its chapter. Treating a result-list noun as a verdict is keyword-driven
inference, which is precisely the uncited judgement this project refuses.

Since that distinction is not recoverable from this extraction, `polarity` here
is carried through for display beside its quote and is NEVER used to derive a
state. No antardaśā band is coloured. See POLARITY_SCOPE_UNRESOLVED.

ABSENCES ARE DATA. `maraka=None` and `remedy=None` mean the cell has no such
clause — ch.52's Jupiter cell is the only one in its chapter with no death
clause at all. Absent is not empty and neither is inherited from a sibling cell.
"""

POLARITY_SCOPE_UNRESOLVED = (
    "BPHS labels only about one antardaśā branch in five, and this extraction "
    "does not record whether a valence word governs the whole branch or merely "
    "names one item in an outcome list. The verifiers found most are the "
    "latter. Polarity is therefore shown beside its quote and never turned "
    "into a verdict."
)

CITATION = "BPHS Vol II ch.52-60"

# ch.52..ch.60, in Viṁśottarī order.
CHAPTER_OF = {"sun": "52", "moon": "53", "mars": "54", "rahu": "55",
              "jupiter": "56", "saturn": "57", "mercury": "58",
              "ketu": "59", "venus": "60"}


CHAPTER_NOTES = {'jupiter': {'chapter': 'Vol II ch.56 — Effects of the Antardasas of Jupiter',
             'frame_summary': '77 conditions extracted across the nine cells. '
                              'from_dasa_lord = 13 (the workhorse, and in this '
                              'chapter it is usually glossed "from the lord of the '
                              'Dasa (Jupiter)"; three instances omit the gloss). '
                              'from_lagna = 11. from_moon = 0 — the Moon is NEVER '
                              'used as a reference frame anywhere in ch.56. '
                              'unstated = 11, of which 8 are the maraka lordship '
                              'clauses ("lord of the 2nd or the 7th" — house '
                              "numbers with no stated frame; only Rahu's clause "
                              'states "from the Ascendant") and 3 are genuine '
                              'placement conditions where the text names '
                              'kendra/trikona and gives no frame at all: Saturn '
                              'vv.8-11 ("kendra or trikona endowed with '
                              'strength"), Mercury vv.20-21.5 ("or in kendra, '
                              'trikona or be associated with the lord of the Dasa '
                              '(Jupite.r)" — the (Jupiter) gloss belongs to the '
                              'ASSOCIATION clause, not to a house frame), and Mars '
                              'vv.67-68 ("if Mars be in kendra, trikona, the llth '
                              'or the 2nd and be associated with or aspcctcd by '
                              'benefics"). not_a_house = 42 (exaltation, '
                              'debilitation, own sign, Navamsa, combustion, '
                              'strength/weakness, association, aspect). Two '
                              'branches state a DISJUNCTION of frames in one '
                              'sentence (Sun vv.54-55.5 and Moon vv.61-63: "from '
                              'the Ascendant or the lord of the Dasa (Jupiter)"); '
                              'each is recorded as two conditions so no frame is '
                              'silently dropped.',
             'gaps': '1. UNDEFINED PREDICATE — Moon vv.58-60.5 requires the Moon '
                     'to be "in an auspicious houge {rog ttre, lold of.,!,11e, '
                     'Qasa (J uO iter)" [in an auspicious house from the lord of '
                     'the Dasa (Jupiter)]. The text NOWHERE enumerates which '
                     'houses are "auspicious". Not computable as stated; do not '
                     'import kendra/trikona from elsewhere in the chapter. 2. '
                     'THREE UNSTATED-FRAME PLACEMENT RULES (Saturn vv.8-11, '
                     'Mercury vv.20-21.5, Mars vv.67-68) all name kendra/trikona '
                     'with no frame. The chapter proves it knows how to state a '
                     'frame when it wants one — the adjacent Jupiter, Venus, Sun, '
                     'Moon and Rahu benefic branches all say "from the Ascendant", '
                     'and Saturn vv.15-15.5 states the exact same house set as '
                     'Mars vv.67-68 (kendra, trikona, 11th, 2nd) and DOES gloss it '
                     '"from the lord of the Dasa (Jupiter)". The omission is '
                     'therefore not obviously a scribal slip, but it is equally '
                     'not resolvable from the text. Leave unstated. 3. THE '
                     'DUSTHANA SET IS NOT CONSTANT. Eleven branches use "the 6th, '
                     'the 8th or the 12th", but Mars vv.69-71 and Rahu vv.76-78 '
                     'use only "the 8th or the l2th" — the 6th is absent in both. '
                     'Whether deliberate or lost in printing cannot be determined. '
                     '4. MARAKA LORDSHIP FRAME. Eight of the nine maraka clauses '
                     'say "lord of the 2nd or the 7th" with no frame stated. '
                     'Rahu\'s alone says "in the 2nd or the 7th from the '
                     'Ascendant" — and it is occupancy, not lordship. Ketu\'s '
                     'carries an editorial parenthetical offering BOTH readings: '
                     '"the lord ofthc 2nd or rhe 7th (or in the 2nd or thc Zth)". '
                     "Jupiter's inverts the order with a parenthetical too: "
                     '"lordof rhc 7th (or 2nd)". The text does not settle '
                     'lordship-vs-occupancy. 5. OCR DAMAGE, MATERIAL. (a) Venus '
                     'v.44 reads "from the lord of the Dasa of Ascendant" — the '
                     '"of" before "Ascendant" is almost certainly "or", which '
                     'would make this a two-frame disjunction like Sun v.54 and '
                     'Moon v.61; as printed it is ambiguous, so only '
                     'from_dasa_lord is asserted. (b) Jupiter vv.4-5.5 is badly '
                     'interleaved across the p.188/189 break: the condition tail '
                     '"in hi: Jsfililated Navamsa, or in" ... "the 6th, the 8th or '
                     'the l2th" ... "from the Ascendant" is split across three '
                     'lines with the Saturn section heading spliced between them; '
                     'the reconstruction is confident but IS a reconstruction. (c) '
                     'Moon v.61-63 prints the dusthana list as "the '
                     '6th-tn.,9,h..ot, rthe l2th" — the middle house glyph is '
                     'mangled and could be read 9; taken as 8th by analogy, and '
                     'flagged. (d) Mercury v.23-24 "the 5th or the gth" = 9th. 6. '
                     'TIME-SPLIT RESULTS, NO MECHANISM. Mercury vv.29-29.5 splits '
                     'one condition into "at the commencemdnt of the Antardasa" vs '
                     '"At the end of the Dasa" with opposite outcomes (and says '
                     '"Dasa" where "Antardasa" is likely meant); Mars vv.69-71 '
                     'says effects are "particularly adverse at the commencement" '
                     'with "some mitigation of evil efects later"; Rahu vv.72-75 '
                     'confines part of its gain to "the first five months". The '
                     'text gives no rule for subdividing the antardasa period. 7. '
                     'RAHU DIGNITY UNDEFINED HERE. Rahu vv.72-75 conditions on '
                     '"his sign of exaltation, in his own sign, in his '
                     'moolatrikona" without saying which signs those are; ch.56 '
                     'does not settle it. Likewise "aspected by the lord of '
                     'kendra" does not say kendra reckoned from what. 8. NO NOTES. '
                     'Santhanam supplies no commentary notes anywhere in ch.56 — '
                     'every condition below is mula sloka translation, so source '
                     'is "sloka" throughout.',
             'pdf_pages': '188-200',
             'polarity_summary': 'Of 77 conditions, only 32 carry an explicit '
                                 'valence word and 45 carry NONE. Favourable = 7 '
                                 'conditions, arising from just THREE branches, '
                                 'all using the single word "auspicious": Sun '
                                 'vv.51-53 ("will be the auspicious results", 4 '
                                 'conditions), Ketu vv.35-36.5 ("will be the '
                                 'ruspicious effects", 1 condition), Mars vv.67-68 '
                                 '("and other auspicious effects", 2 conditions). '
                                 'Adverse = 25 conditions across 13 branches, '
                                 'keyed on "Evil" (Venus v.44), "inauspicious" '
                                 '(Saturn vv.12-14, Mars vv.69-71), "adverse" '
                                 '(Mars vv.69-71), "Loss/loss" (many) and '
                                 '"danger/Danger" (many). The remaining 45 '
                                 'conditions use neutral verbs — "will be '
                                 'experienced", "will be derived", "will result", '
                                 '"will be the results", "will be realised" — and '
                                 'list outcomes with no valence word attached; '
                                 'these are recorded polarity "none" even where '
                                 'the listed outcomes sound plainly pleasant '
                                 '(Jupiter vv.1-3 "sovereignty over many kings"; '
                                 'Moon vv.58-60.5 "opulence and glory") or plainly '
                                 'unpleasant (Sun vv.54-55.5 "nervous disorder, '
                                 'fever ... indulgence in sins"). This confirms '
                                 "the prior pass's finding: explicit valence is a "
                                 'minority — about 42% of conditions — and is '
                                 'heavily concentrated in the negative branches '
                                 '(25 adverse vs 7 favourable).'},
 'ketu': {'chapter': 'Vol II ch.59 — Effects of the Antardasas in the Dasa of Ketu',
          'frame_summary': '45 conditions extracted across the 9 cells. '
                           'from_lagna: 21 (47%). from_dasa_lord: 12 (27%), always '
                           'glossed "from the lord of the Dasa (Ketu)". from_moon: '
                           '0 — the Moon is NEVER used as a reference frame '
                           'anywhere in ch.59. unstated: 8 (18%). not_a_house: 4 '
                           '(9%). The from_dasa_lord count (12) is well below the '
                           '~50-per-chapter figure reported for the corpus as a '
                           'whole; in ch.59 the lagna is the dominant frame and '
                           'two cells (Ketu-in-Ketu, Rahu) contain NO '
                           'from_dasa_lord condition at all. The 8 unstated cases '
                           'fall into two recognisable shapes: (a) bare '
                           'kendra/trikona lists with no frame attached — Venus '
                           'vv.7-9.5 "in a kendra or trikona" and Sun vv.16-17 "in '
                           'kendra, trikoia or the 1lth", both of which are the '
                           "cell's OPENING favourable branch, i.e. the "
                           'highest-traffic condition in the cell; and (b) bare '
                           'lordship references — "lords of the 9th, the loth or '
                           'tbe +rh" (Ketu), "the lords of the 9th or the l0th" '
                           '(Mars), "the lorC of the 9th or the 10th" (Mercury). '
                           'Note the maraka clauses split on frame: 5 of 9 say '
                           '"from the Ascendant" explicitly (Mars, Jupiter, '
                           "Saturn, Mercury, and Rahu's 2nd/7th clause) while 4 of "
                           '9 say only "be the lord of the 2nd or the 7th" with no '
                           'frame (Ketu-in-Ketu, Venus, Sun, Moon) — recorded as '
                           'unstated, not silently normalised to lagna.',
          'gaps': '(1) OCR ORDERING — Rahu cell: the English gloss of vv.48-50 is '
                  'printed BEFORE that of vv.45-47 on PDFPAGE 234 (file lines '
                  '10087-10089 precede 10090-10096). The 48-50 gloss is also '
                  'split, its tail landing on PDFPAGE 235. Verse content is '
                  'recoverable; only the print order is wrong. (2) OCR ORDERING — '
                  'Saturn cell: vv.67-68 are printed BEFORE vv.63-65 on PDFPAGE '
                  '237. (3) MISSING VERSE — Saturn cell: no English gloss for '
                  'verse 66 exists anywhere in the chapter; the sequence runs '
                  '61-62.5, then 63-65, then 67-68. Whatever v.66 states is '
                  'UNAVAILABLE. (4) OCR TEXT LOSS — Rahu vv.45-47: the left margin '
                  'is cropped on every line of this paragraph, and one house '
                  'number is lost at a line break: "in kendra, trikona, the llth, '
                  'the / or the 2nd from the Ascendant". A house between "the '
                  '11th" and "the 2nd" is missing. Do NOT guess it (3rd would be '
                  'the pattern-match, but the text does not say). (5) OCR TEXT '
                  'LOSS — Ketu-in-Ketu vv.1-2.5 and 3-4, PDFPAGE 227: left margin '
                  'cropped, e.g. "lords of the 9th, the loth or tbe +rh" — the '
                  'third house reads "+rh", most consistent with 4th but not '
                  'legible with certainty; flagged rather than resolved. (6) '
                  'AMBIGUOUS CONDITION — Saturn vv.63-65: "if Saturn be in trikoo" '
                  'lnPisces" = "in trikona in Pisces". Whether this means a '
                  'trikona that happens to be Pisces, or Pisces as counted '
                  'trikona-wise from something, is not settled by the text. Left '
                  'as quoted. (7) NO FRAME for the two opening favourable branches '
                  'of the Venus and Sun cells (see frame_summary) — these are the '
                  'highest-risk cells to ship, because the branch a real chart '
                  'most often lands on is the one whose frame the text never '
                  'states. (8) The Rahu cell is unusually short (vv.45-50, 6 '
                  'verses vs 8-12 elsewhere) and contains no from_dasa_lord '
                  'condition and no remedy-independent favourable/adverse label; '
                  'the Ketu-in-Ketu cell likewise has no from_dasa_lord condition. '
                  '(9) Moon maraka clause uniquely adds the 8th to the usual '
                  '2nd/7th pair ("lord of the 2nd, the 7th or the gth") — "gth" is '
                  'OCR for 8th, consistent with the surrounding text but a '
                  'single-character read. (10) Only ONE note by Santhanam appears '
                  'in the whole chapter (Saturn cell, citing Brihat Jataka); every '
                  'other statement recorded here is mula sloka gloss.',
          'pdf_pages': '227-239 (chapter opens on PDFPAGE 227, ends on PDFPAGE '
                       '239; Chapter 60 begins on PDFPAGE 240)',
          'polarity_summary': '24 of 45 branches (53%) carry a word from the '
                              'target valence list; 21 (47%) carry none. BUT this '
                              'headline number overstates the case and should not '
                              'be used as-is. 19 of those 24 hits are the words '
                              '"loss", "danger" or "death" occurring INSIDE an '
                              'outcome list ("loss of wealth", "danger from '
                              'thieves", "fear of premature death") — they name a '
                              'specific misfortune, they do not label the branch. '
                              'Only 5 branches in the whole chapter carry a '
                              'genuine branch-level valence label: Moon vv.25-28 '
                              '"The beneficial results will be realised fulty if '
                              'the Moon be waxing"; Moon vv.31-33 "Thcre wilr be '
                              'auspicious results. at the connmencement"; Mars '
                              'vv.41-42 "amidst evil effects there will be some '
                              'auspicious effects also"; Jupiter vv.55-56 "there '
                              'will be onlY adverse results-later"; Mercury '
                              'vv.73-74.5 "beneficial effEcts ... but inauspicious '
                              'at the end". That is 5 of 45, ~11% — consistent '
                              'with the minority finding from ch.54 and ch.57. '
                              'Three of those five are STAGED rather than flat '
                              '(start/middle/end of the antardasa) and one (Mars '
                              '41-42) is self-contradictory by design ("amidst '
                              'evil effects there will be some auspicious effects '
                              'also"), so even the explicit labels do not reduce '
                              'cleanly to a single favourable/adverse verdict. One '
                              'near-miss trap was excluded: Saturn vv.63-65 "be in '
                              'an auspicious Navamsa" — "auspicious" there '
                              'qualifies the CONDITION (the navamsa), not the '
                              'result, and was NOT counted as polarity.'},
 'mars': {'chapter': 'Vol II ch.54 — Effects of Antardasas in the Dasa of Mars',
          'frame_summary': '62 conditions extracted across the 9 cells (60 from '
                           "sloka, 2 from Santhanam's notes). By frame: "
                           'from_dasa_lord 10 (16%) — Jupiter 1, Saturn 3 (incl. 1 '
                           'note), Mercury 2, Ketu 1, Venus 2, Sun 1; from_lagna 8 '
                           '(13%) — Rahu 2, Jupiter 1, Mercury 2, Ketu 2, Venus 1; '
                           'from_moon 0 (the Moon is never used as a reference '
                           'point anywhere in this chapter, including in its own '
                           'cell); unstated 10 (16%) — Mars 2, Rahu 2, Jupiter 1, '
                           'Saturn 2, Sun 1, Moon 2; not_a_house 34 (55%) — '
                           'dignity, combustion, strength, benefic/malefic '
                           'association, aspect, Navamsa, lordship, waxing/waning. '
                           'CAVEATS ON THESE COUNTS: (1) Of the 8 from_lagna '
                           'conditions, 2 (Mercury vv.38-39, Ketu vv.48-49½) '
                           'derive their frame ONLY from a parenthesised "(from '
                           'the Ascendant)" — a translator-supplied gloss, not '
                           'words of the sloka. On a strict mula reading those '
                           'become unstated and the split is from_lagna 6 / '
                           'unstated 12. (2) The Moon vv.74-76 frame is '
                           'OCR-unrecoverable ("from t[he] Ascendant of the lord '
                           'of the Dasa (Mars)") and could be from_lagna, '
                           'from_dasa_lord, or both; booked as unstated. (3) Every '
                           'house list in the Mars-in-Mars cell (vv.1-2½ and 5-5½) '
                           "is frameless, so the chapter's opening cell — the "
                           'first one any engine hits — cannot be evaluated at all '
                           'without an uncited assumption. (4) from_dasa_lord is '
                           'stated by the standard formula "from the lord of the '
                           'Dasa (Mars)" in 8 places and by naming the graha '
                           'directly, "from Mars", once (Mercury vv.44-45½); Venus '
                           'v.55 uses the unique wording "in kendra TO the '
                           'Ascendant".',
          'gaps': '1. FRAME UNRESOLVABLE — Moon vv.74-76, pdf 173: "or be in the '
                  '6th, the gth or the l2th from tAscendant of the lord of the '
                  'Dasa (Mars)." Right-margin truncation destroys the conjunction. '
                  'Could be "from the Ascendant OR the lord of the Dasa" (two '
                  'alternative frames) or a single garbled one. Booked as '
                  'unstated. The only place in ch.54 where a frame is present but '
                  'undecidable — and it governs a branch whose stated result is '
                  'death.\n'
                  '2. PARENTHESISED FRAMES — Mercury vv.38-39 and Ketu vv.48-49½ '
                  'state their frame only as "(from the Ascendant)". In this '
                  'translation round brackets consistently mark '
                  'translator-supplied glosses (cf. "(government)", "(Mars)"). '
                  'Booked as from_lagna but flagged low-confidence; a strict mula '
                  'reading makes both unstated.\n'
                  '3. HOUSE NUMBER IN DOUBT — Jupiter vv.20-22, pdf 164: printed '
                  '"if Jupiter be in the 5th, the 8th or the l2th". Every other '
                  'dusthana branch in ch.54 reads 6/8/12. "5th" may be OCR of '
                  '"6th", but it is what the page shows and has NOT been '
                  'corrected. Load-bearing, since this is one of only two branches '
                  'carrying an explicit adverse label.\n'
                  '4. JUPITER\'S MARAKA CLAUSE NAMES ONLY THE 2ND — "if Jupiter be '
                  'the lord of the 2nd". The 7th is absent, unlike all seven other '
                  'maraka clauses in the chapter. Not visibly an OCR artifact; '
                  'recorded as-is.\n'
                  '5. KETU HAS NO MARAKA LORDSHIP CLAUSE AT ALL — the only 2nd/7th '
                  'reference in the Ketu cell is a PLACEMENT clause. Ch.54 '
                  'therefore supplies a 2nd/7th-lordship rule for 8 of 9 antar '
                  'lords, not 9.\n'
                  '6. KETU HAS NO PRESCRIBED REMEDY — the text prescribes none; '
                  'Santhanam supplies a speculative one ("Perhaps recitation of '
                  'Vishnu Sahasranam and giving a goat in charity"). Must never be '
                  'presented as mula.\n'
                  '7. SATURN REVERSAL — vv.30-32: kendra/11th/5th FROM THE DASA '
                  'LORD, normally the favourable configuration, produces adverse '
                  'results here. The sloka states NO valence label; "very '
                  'inauspicious" is Santhanam\'s note only. Any engine '
                  'generalising "good house from dasa lord = good" is wrong in '
                  "exactly this cell, and the text's own words do not label it.\n"
                  '8. RAHU\'S 2ND/7TH CLAUSE IS PLACEMENT, NOT LORDSHIP ("if Rahu '
                  'be in the 2nd", "if he be in the 7th") and carries NO frame — '
                  'yet it is the clause stating "great danger of premature death". '
                  'The most consequential verdict in that cell rests on an '
                  'unframed house number.\n'
                  '9. MERCURY vv.36-37½ ends with a dangling comma after "frorn '
                  'the r\\scendant," — a further limb of the condition may have '
                  'been lost in OCR.\n'
                  '10. VERSE ORDER SCRAMBLED on pdf 169 (Ketu): the 52-54 '
                  'translation block is printed above the 50-51½ block and '
                  "Santhanam's yogakaraka note is split around it. Verse "
                  'attributions there were reconstructed from printed verse '
                  'numbers, not reading order.\n'
                  '11. NO CONTESTED-CASE TIE-BREAK. Several cells allow a '
                  'favourable-side and an adverse-side condition to fire together '
                  '(e.g. Saturn in exalted Navamsa AND in the 8th from Mars; Venus '
                  'lord of the Ascendant AND in the 6th from Mars). Ch.54 states '
                  'no precedence rule, exactly as ch.47 vv.5-6 states none for the '
                  'mahadasa. Such cases must remain "contested".\n'
                  '12. NO FRAME IS EVER "FROM THE MOON" in this chapter — 0 of 62 '
                  'conditions. If the engine offers a from-Moon frame, ch.54 '
                  'supplies no warrant for it.\n'
                  "13. Ch.34's prohibition on mixing a maraka verdict with a "
                  'benefic/malefic nature is respected here: no maraka clause in '
                  'ch.54 carries an explicit valence label, so none was assigned '
                  'one.',
          'pdf_pages': '161-173 (chapter heading on PDFPAGE 161; ch.55 begins on '
                       'PDFPAGE 174)',
          'polarity_summary': 'Explicit valence LABELS are rare, matching the '
                              "prior pass's count of five for this chapter. Only 5 "
                              'of the 33 sloka BRANCHES carry one: Rahu vv.9-10½ '
                              '"auspicious", Jupiter vv.17-19½ "beneficial", '
                              'Jupiter vv.20-22 "evil", Mercury vv.41-43½ "very '
                              'auspicious", Ketu vv.50-51½ "beneficial". Counting '
                              'by CONDITION: 10 of 60 sloka conditions carry '
                              'explicit polarity (7 favourable — Rahu 3, Jupiter '
                              '2, Mercury 1, Ketu 1; 3 adverse — Jupiter\'s "evil '
                              'effects" branch has 3 sub-conditions) and 50 of 60 '
                              '(83%) are polarity "none". Plus 1 note-sourced '
                              'adverse (Santhanam on Saturn, "very inauspicious"). '
                              'The remaining 28 branches use bare neutral verbs — '
                              '"will arise", "will be the effects", "will be the '
                              'results", "will be realised", "will be '
                              'experienced"/"experinced", "will result", "will be '
                              'felt", "will be derived", "there will be". DECISION '
                              'RULE APPLIED (the single most consequential '
                              'judgement in this extraction, and it should be '
                              'reviewed before it drives any verdict): only '
                              'label-type valence words attaching to the effects '
                              'as a whole ("auspicious", "beneficial", "evil", '
                              '"inauspicious", "favourable", "adverse") were '
                              'counted. Outcome NOUNS inside the result list — '
                              '"danger from snakes", "loss of wealth", "fear of '
                              'death", "death" — were NOT counted as polarity, '
                              'because treating them as such would mark nearly '
                              'every dusthana branch adverse by inference rather '
                              'than by citation, and would symmetrically have '
                              'forced Moon vv.70-73 to favourable on the strength '
                              'of "celebrations of auspicious functions like '
                              'marriage". Two further near-misses were '
                              'deliberately excluded: Rahu vv.11-14, where "evil" '
                              'appears only in the following remedy sentence '
                              '("relief from the above evil effects"), and Saturn '
                              'vv.30-32, where "inauspicious" appears only in the '
                              "commentator's note."},
 'mercury': {'chapter': 'Vol II ch.58 — Effects of the Antardasas in the Dasa of '
                        'Mercury',
             'frame_summary': '61 conditions extracted across the nine antar '
                              'cells. FRAME COUNTS: not_a_house 22 (36%) — '
                              'dignity, combustion, conjunction/aspect, rasi and '
                              'strength predicates; from_lagna 20 (33%); '
                              'from_dasa_lord 13 (21%); UNSTATED 6 (10%); '
                              'from_moon 0 (ZERO — the Moon is never used as a '
                              'reference frame anywhere in ch.58). Per-cell '
                              'from_dasa_lord counts: Mercury 0, Ketu 2, Venus 2, '
                              'Sun 1, Moon 2, Mars 2, Rahu 1, Jupiter 2, Saturn 1. '
                              'The Mercury-in-Mercury cell is the ONLY cell with '
                              'no dasa-lord-framed condition, expected since antar '
                              'lord and dasa lord are the same graha. When the '
                              'dasa-lord frame is used it is almost always glossed '
                              '"(Mercury)"; the sole exception is Venus '
                              'vv.16-17.5, which reads only "from the lord of the '
                              'Dasa". The six UNSTATED-frame conditions are: (1) '
                              'Mercury maraka vv.4-5, "if the Mercury be the lord '
                              'of the 2nd or the 7th" with no Ascendant gloss; (2) '
                              'Sun vv.20-22 "or in kendra, trikona, the 2nd or the '
                              'llth" — a bare house list with no reference point, '
                              'the most consequential gap in the chapter; (3) Moon '
                              'vv.28-29.5 "In the circumstances mentioned above" — '
                              'additive result clause inheriting a mixed condition '
                              'set; (4) Rahu v.49 "some evil effects at the '
                              'commencement" — timing rider inheriting a mixed '
                              'condition set; (5) and (6) Jupiter vv.65-66, both '
                              'the lordship and the placement halves of "if '
                              'Jupiter be thq lord of the 2nd or the 7th or be in '
                              'the 2nd or the 7th", which carries no frame gloss '
                              'of any kind. NONE of these six should be resolved '
                              'by inference.',
             'gaps': '1. FRAME NOT STATED, six times — enumerated in '
                     'frame_summary. Sun vv.20-22 "kendra, trikona, the 2nd or the '
                     'llth" and Jupiter vv.65-66 "or be in the 2nd or the 7th" are '
                     'the two that would actually change a verdict on a real '
                     'chart. Ship these as unavailable. 2. RAHU MARAKA IS '
                     'STRUCTURALLY UNIQUE (vv.54-55): "if Rahu be IN the 2nd or '
                     'the 6th from the Ascendant" — placement not lordship, and '
                     '6th not 7th, against lordship/2nd-7th clauses everywhere '
                     'else. Both anomalies are as printed. Do not normalise. 3. '
                     'INTERNAL CONTRADICTION, Rahu cell: the 8th from the '
                     'Ascendant produces "Loss of wealth, rheumatic fever, and '
                     'indigestion" (v.50) AND "an opportunity to have conversation '
                     'or a meeting with the king" (v.51). No tie-break stated — a '
                     'genuine "contested" cell in the ch.47 vv.5-6 sense. 4. HOUSE '
                     'NUMBERS DESTROYED BY OCR, three places: (a) Moon vv.32-33 '
                     'prints "the 6th, the 6th or the l2th" — 6th twice, second '
                     'presumably 8th but not legible as such; (b) Mars vv.39-40.5 '
                     'prints "in the g:.rr r: the l2th" — first house number '
                     'entirely unreadable; (c) Saturn vv.69-70.5 prints "in the '
                     'sth or the l2th" — could be 8th or 5th. All flagged, none '
                     'silently corrected. 5. MARAKA POLARITY IS NOT UNIFORM: five '
                     'clauses predict "fear of premature death" (Venus, Sun, Mars, '
                     'Rahu, Saturn); three predict only "physical distress" (Ketu, '
                     'Moon, Jupiter); Mercury\'s predicts "death of members of the '
                     'family", not of the native. Per ch.34 a maraka verdict must '
                     'not be blended with a benefic/malefic nature verdict, so '
                     'surface these separately from the branch verdict. 6. '
                     'PARENTHESISED FRAME GLOSSES: the maraka clauses in the Ketu, '
                     'Venus, Sun and Moon cells append "(from the Ascendant)" '
                     'inside PARENTHESES, which in this edition normally marks a '
                     'translator insertion; Mars and Saturn state it '
                     'unparenthesised; Mercury and Jupiter omit it entirely. The '
                     'frame for the parenthesised four is weaker evidence than a '
                     'bare from_lagna label suggests. 7. AMBIGUOUS '
                     'CONJUNCTION/SCOPE, unresolved by the text: Ketu vv.6-8.5 "or '
                     'a yogakaraka" (conjunct-a-yogakaraka vs is-a-yogakaraka); '
                     'Sun vv.20-22 whether the Navamsa clause is an alternative or '
                     'an added requirement; Sun vv.23-24 whether "be weak and be '
                     'associated with Saturn, Mars and Rahu" is required on top of '
                     'the house placement or is a further alternative, and whether '
                     'the three malefics are conjunctive; Moon vv.26-27 whether '
                     '"associated with or aspected by Jupiter" scopes over '
                     'exaltation as well as own sign; Jupiter vv.59-61 whether '
                     '"Saturn and Mars" requires both. 8. MIXED-VALENCE TIME '
                     'SPLIT, Mars vv.43-44.5: the same protasis (malefics with '
                     'Mars in the 8th/12th from Mercury) yields danger at the '
                     'commencement, ENJOYMENTS AND GAINS in the middle, and danger '
                     'at the end. A single adverse label would misreport the text; '
                     'the sub-period structure must be preserved. Similar timing '
                     'riders at Moon vv.30-31.5 ("at the commencement") and Rahu '
                     'v.49. 9. "or otherwise" in Mercury vv.1-3.5 ("if Mercury be '
                     'placed in his sign of exaltation or otherwise") and the '
                     'trailing "etc." in "his sign of debilitation etc." leave the '
                     'dignity condition open-ended and untestable as printed. 10. '
                     'NO SANTHANAM NOTES exist in this chapter — verified by grep '
                     'across PDFPAGE 215-226. Every condition is mula (sloka); the '
                     'only editorial intrusions are the parenthetical glosses '
                     '"(Mercury)" and "(from the Ascendant)".',
             'pdf_pages': '215-226 (book pp. 705-716); ch.59 begins at PDFPAGE 227',
             'polarity_summary': 'Of 61 conditions, only 28 (46%) carry an '
                                 'EXPLICIT valence word in the sloka clause; 33 '
                                 '(54%) carry NONE. Of the 28: 25 adverse, 3 '
                                 'favourable. The three favourable are all in the '
                                 'Moon cell and all share the single word '
                                 '"beneficial" from vv.26-27 ("The yoga becomes '
                                 'very strong for beneficial effects"). The '
                                 'adverse words actually used are '
                                 '"danger"/"Danger" (Ketu, Sun x3, Moon, Mars, '
                                 'Jupiter x4, Saturn), "loss"/"Loss" (Mercury x3, '
                                 'Mars, Rahu), "evil" (Rahu v.49 timing rider), '
                                 'and "death" in the maraka clauses. NOT ONE '
                                 'branch in this chapter uses "auspicious", '
                                 '"inauspicious", "favourable" or "adverse" as a '
                                 'branch verdict. The word "auspicious" occurs '
                                 'once (Jupiter vv.56-58.5) but describes the '
                                 'EVENTS predicted ("celebration of auspicious '
                                 'functions like marriage"), not the branch — a '
                                 'genuine trap, recorded as polarity none. The '
                                 'dominant apodosis verbs are the neutral "will be '
                                 'derived" (Venus, Sun, Mars, Jupiter, Saturn), '
                                 '"will be experienced" (Ketu), "are derived" '
                                 '(Rahu) and "will be the results" (throughout), '
                                 'none of which is a valence word. Every remedy '
                                 'clause says "relief from the above evil '
                                 'effects", but per the brief that phrasing sits '
                                 'in the REMEDY and is not treated as a branch '
                                 'polarity marker.',
             'structural_note': 'STRUCTURAL NOTE (not a tenth antar cell)'},
 'moon': {'chapter': 'Vol II ch.53 — Effects of the Antardasas in the Dasa of the '
                     'Moon',
          'frame_summary': '60 conditions recorded across 9 cells. 40 are house '
                           'conditions; 20 are not house conditions at all '
                           '(exaltation, debilitation, combustion, own '
                           'sign/Navamsa, strength, malefic/benefic association or '
                           'aspect, Yogakaraka association, conjunction with the '
                           'Dasa lord). Of the 40 house conditions: unstated 21 '
                           '(52.5%), from_dasa_lord 12, from_lagna 6, from_moon 1. '
                           'The unstated frame is therefore the SINGLE LARGEST '
                           'category in this chapter and outnumbers from_dasa_lord '
                           'almost 2:1 — the reported "from the lord of the Dasa '
                           'is the workhorse" pattern does NOT hold in ch.53. '
                           'from_dasa_lord is glossed "from the lord of the Dasa '
                           '(the Moon)" in 11 of 12 cases; the twelfth (Sun antar, '
                           'vv.68-70) says only "from the lord of the Dasa" with '
                           'no gloss. The single from_moon instance (Jupiter '
                           'antar, vv.29-31, "from the Moon") is textually '
                           'distinct from the from_dasa_lord phrasing even though '
                           'the Dasa lord IS the Moon here — the chapter uses two '
                           'different phrasings and this pass does not collapse '
                           'them. Only ONE from_lagna instance carries an explicit '
                           'frame on a lordship rather than a placement (Jupiter '
                           'maraka, "lord of 2nd or 7th from the Ascendant"); the '
                           'other seven 2nd/7th clauses in the chapter state no '
                           'frame.',
          'gaps': '1. VERSE 56 IS MISSING. Venus antardasa numbering jumps from '
                  '"55." straight to "57-57t," with no verse 56 in the OCR. '
                  'Content is lost, not merely garbled.\n'
                  '2. Mars antar vv.9-12 has a broken sentence boundary: "if he be '
                  'posited in the 6th, the Sth or the l2th from the Ascendant. be '
                  'associated with or aspected by malefics in the 6th, the Sth or '
                  'the l2th from the lord of the Dasa (the Moon)." The stray full '
                  'stop before "be associated" makes it UNRESOLVABLE whether these '
                  'are two alternative conditions (or/either) or one conjunctive '
                  'condition. I have recorded them as two separate conditions and '
                  'flagged it. Do not implement a conjunction the text does not '
                  'settle.\n'
                  '3. Ketu antar vv.49-49½: the result noun is destroyed — "will '
                  'be the -,ieers if". Recorded as unreadable.\n'
                  '4. Ketu antar: an UNNUMBERED fragment sits between v.49½ and '
                  'v.50 — "Effects like acquisition of a kingdom (attainment of a '
                  'high position in governnent), gain of clothes, ornanents, '
                  'cattle," — with no condition clause attached anywhere near it, '
                  'and the Sanskrit/English are interleaved out of order on the '
                  'page. It may be the tail of 49½ or the head of 50. NOT recorded '
                  'as a condition because no protasis survives.\n'
                  '5. Rahu antar v.20-21: "if Rahu be in the 2nd or 7t|" — the '
                  'house number is truncated at the line break. Read as 7th from '
                  'context of the parallel clauses, but flagged.\n'
                  '6. Jupiter antar vv.29-31 contains an UNCONDITIONAL timing '
                  'statement ("good effects at the commencement... distress at its '
                  'end") with no protasis. Recorded with predicate "(none — '
                  'unconditional)" so it is never fired as a rule.\n'
                  '7. Ketu 47-48 and 49-49½ likewise carry unconditional timing '
                  'riders (loss at commencement / loss at end) folded into '
                  'results, not into predicates.\n'
                  '8. Rahu vv.13-14 is a SINGLE condition (kendra or trikona) that '
                  'the text explicitly splits into an auspicious early phase and '
                  'an adverse later phase. I have emitted it as two condition rows '
                  'sharing one predicate and quote so neither polarity is dropped; '
                  'a consumer must not treat these as two independent rules.\n'
                  '9. Chapter 53 contains NO Santhanam notes — grep for "note" '
                  'over the whole chapter range returns nothing. Every condition '
                  'here is source: sloka.\n'
                  '10. Saturn 36-38 and Ketu 50-52 use 2nd/7th as a PLACEMENT ("if '
                  'Saturn be in 2nd, the 7th or the 8th"), not a lordship, and '
                  "Saturn's adds the 8th. These are not maraka clauses in the "
                  'ch.47 sense and must not be routed to maraka logic.\n'
                  '11. Moon antar vv.1-2½ and Venus 58-60 condition on association '
                  'with a house LORD (9th/10th, 11th, 9th-or-11th). The house '
                  'those lords are reckoned from is never stated. Recorded as '
                  'frame "unstated".',
          'pdf_pages': '149-160 (chapter heading on 149, ends mid-160; ch.54 '
                       'begins on 161)',
          'polarity_summary': 'Of 60 branches, 30 (exactly 50%) carry NO explicit '
                              'valence word — they use neutral verbs: "will be '
                              'experienced" (Saturn 32-34, Mercury 39-41, Venus '
                              '53-54), "will be derived" (Mars 7-8½ second clause, '
                              'Rahu 15-16, Saturn 35-35½, Mercury 42-43½, Jupiter '
                              '29-31), "will result" (Venus 55, 58-60), "will '
                              'arise" (Ketu 47-48), "will be realised" (Saturn '
                              '36-38), "will be the results" (Rahu 19-21), "are '
                              'the likely results" (Sun 68-70 lordship clause). 30 '
                              'branches carry an explicit valence word: 12 '
                              'favourable ("beneficial" x3, "favourable" x3, '
                              '"auspicious" x1, "good effects" x1, plus repeats '
                              'within multi-predicate branches) and 18 adverse '
                              '("evil" x5, "inauspicious" x1, "danger" x5, "loss" '
                              'x3, "death" x4 — counted per condition entry). The '
                              'entire Saturn cell (8 conditions) carries ZERO '
                              'explicit valence words in any branch, favourable or '
                              'adverse. Three 2nd/7th-lordship clauses produce '
                              'only fever or body pain with no valence word at all '
                              '(Mercury 44-46, Sun 68-70) — these must not be read '
                              'as death clauses.'},
 'rahu': {'chapter': 'Vol II ch.55 — "Effects in the Antardasas of Rahu" '
                     '(antardasas within the Rahu Mahadasa), vv.1-83',
          'frame_summary': '58 sloka-level conditions + 2 Santhanam notes = 60 '
                           'entries. Frame tally over the 58 SLOKA conditions: '
                           'from_dasa_lord 12 (always glossed "from the lord of '
                           'the Dasa (Rahu)"); not_a_house 22 (dignity, '
                           'combustion, navamsa, strength, association/aspect, '
                           'lordship-conjunction); from_lagna 11; UNSTATED 13; '
                           'from_moon 0 — the Moon is never used as a reference '
                           'frame anywhere in ch.55. The 13 unstated split into 9 '
                           'maraka/lordship clauses ("if X be the lord of the 2nd '
                           'or the 7th" — no frame word, lordship is presumptively '
                           'lagna-referred but the text does not say so) and 4 '
                           'genuine bare house conditions that are the dangerous '
                           'ones: Saturn vv.21-24 "if Saturn be in kendra, trikona '
                           '... the 3rd or the I lth" (no frame), Mercury vv.30-33 '
                           '"if Mercury be in his sign of exaltation, in kendra or '
                           'in the 5th" (no frame), Mercury vv.36-38 "if Mercury '
                           'be in the 6th, the 8th or the 12th" (no frame — and '
                           'note the immediately preceding branch vv.34-35 IS '
                           'glossed from the Dasa lord, so neither Ascendant nor '
                           'Dasa-lord can be assumed by adjacency), Moon vv.68-70 '
                           '"kendra, trikona or the llth" (no frame — again the '
                           'next branch vv.71-72 is explicitly from the Dasa '
                           'lord). Two further from_lagna readings rest ONLY on a '
                           "translator's parenthesis, not on words in the running "
                           'translation: Ketu vv.42-42.5 "in a kendra or trikona '
                           '(from the Ascendant)" and Sun vv.60-61.5 "a kendra or '
                           'trikona (from the Ascendant)" — both flagged; if '
                           "parentheses are treated as gloss (the project's "
                           'standing rule for Santhanam), these two revert to '
                           'unstated, making from_lagna 9 and unstated 15.',
          'gaps': '1) SEVERE OCR DAMAGE on the Mars cell, PDFPAGE 186-187: the '
                  'page is left-margin-truncated on nearly every line of the '
                  'English. In vv.76-77.5 the FIRST house number is destroyed — '
                  '"if Mars be in the , the 5th, the 9th or kendra from the '
                  'Ascendant" — one house is simply missing and I will not guess '
                  'it. In vv.78-79.5 the line break eats a house: "if Mars be in '
                  'kendra, the 5th / th, the 3rd or the llth from the lord of the '
                  'Dasa (Rahu)" — the fragment "th" is a lost ordinal (plausibly '
                  '9th, unverifiable). In vv.80-82 the third house is lost: "if '
                  'Mars be in the 6th. the 8th or the / from the lord of the Dasa '
                  '(Rairu)" — 12th by pattern, but the text as extracted does not '
                  'say it. In v.83 the graha name is truncated to "if J / be the '
                  'lord of the 2nd or the 7th" — inside the Mars antardasa this '
                  'must be Mars, but the extracted glyph is "J". The Mars cell '
                  "should be re-OCR'd before it ships.\n"
                  '2) ANOMALOUS MARAKA HOUSES IN THE MOON CELL: v.75 reads "if the '
                  'Moon be the lord of the 2nd or the l2th" — TWELFTH, not '
                  'seventh. Every other cell in ch.55 reads 2nd/7th. This is '
                  'either a genuine variant or an OCR corruption of 7th; the text '
                  'as extracted says 12th and I have recorded it as it stands, '
                  'flagged.\n'
                  '3) MARAKA RESULTS ARE NOT UNIFORMLY DEATH. Rahu v.7 gives '
                  '"distress and diseases"; Ketu v.45 gives "distress to the '
                  'body"; Sun v.67 gives "danger of critical illnesy [illness]". '
                  'Only Jupiter, Saturn, Venus, Moon and Mars give premature '
                  'death. A generic "2nd/7th lord = maraka death" implementation '
                  'would over-state five of these.\n'
                  '4) Jupiter vv.18-20 reads "if Jupiter be the Ioid of the 2nd '
                  'and the 7th" — AND, not OR, unlike all eight sibling clauses. '
                  'Conjunctive vs disjunctive is undecidable from the text.\n'
                  '5) Rahu v.7 is the only lordship clause that ALSO fires on '
                  'placement: "be the lord of the 2nd or the 7th OR be in any of '
                  'those hottses". No frame is stated for that placement.\n'
                  '6) TRANSLATOR PARENTHESES supply the only frame in Ketu '
                  'vv.42-42.5 and Sun vv.60-61.5. Under the project rule that '
                  "Santhanam's supplied material is not mula, both should be "
                  'treated as unstated.\n'
                  '7) CONJUNCTIVE CONDITIONS the text does not disambiguate: Rahu '
                  'vv.1-4 chains "be in Cancer, Scorpio, Virgo or Sagittarius AND '
                  'be in the 3rd/6th/10th/11th from the Ascendant, OR be '
                  'associated with yogakaraka planet in his sign of exaltation" — '
                  'whether "in his sign of exaltation" qualifies Rahu or the '
                  'yogakaraka is not settled. Venus vv.56-59 and Mars vv.80-82 '
                  'require the malefic association AND the 6/8/12 placement '
                  'jointly.\n'
                  '8) Rahu vv.1-4 requires Rahu to be in one of four SIGNS '
                  '(Cancer, Scorpio, Virgo, Sagittarius). This is a raw sign list, '
                  'not a dignity — dignity.py will not cover it.\n'
                  '9) SECTION HEADING ERROR at PDFPAGE 183: "Effects of the '
                  'Antardasa of the Sun in the Antardasa of Rahu" — should read '
                  '"in the Dasa of Rahu". Cosmetic OCR/typesetting error.\n'
                  "10) Santhanam's note on Jupiter vv.13-14.5 states the ORIGINAL "
                  'TEXT IS PROBABLY CORRUPT ("There is perhaps some rnistake in '
                  'the original text") because "entrustment of governmental '
                  'authority" sits inside an otherwise adverse list; his '
                  'conjecture is "punishment by government". His note on Saturn '
                  'vv.25-26 raises the same problem for "sudden gain of '
                  'ornaments". Both are NOTES, not mula — the sloka as printed '
                  'lists these outcomes and I have left them in the result strings '
                  'unaltered.\n'
                  '11) Ketu vv.40-41 opens with an UNCONDITIONAL result ("During '
                  'the Antardasa of Ketu in the Dasa of Rahu, there will be '
                  'journeys to foreign countries, danger from the king...") with '
                  'no condition attached at all. This is the only unconditional '
                  'branch in the chapter. It is unclear whether it is a default '
                  'that the subsequent conditional branches override, or an '
                  'always-on overlay; the text does not say.\n'
                  '12) Rahu vv.1-4 and Ketu vv.42-42.5 make no provision for a tie '
                  'when a favourable and an adverse branch both fire — same '
                  'structural gap as ch.47 vv.5-6, so the four-state (favourable / '
                  'adverse / contested / not_stated) machinery from '
                  'dasha_effects.py is the right shape here too.\n'
                  '13) The Sanskrit devanagari is essentially unreadable in this '
                  'extraction (mojibake throughout), so every quote below is '
                  "Santhanam's ENGLISH translation only. No independent check "
                  'against the Sanskrit was possible.',
          'pdf_pages': '174-187',
          'polarity_summary': '~40 result-branches in the chapter (31 non-maraka + '
                              '9 maraka/lordship). An explicit valence word '
                              'appears in 15 of the 31 non-maraka branches: Rahu '
                              '1, Jupiter 2, Saturn 2, Mercury 2, Ketu 2, Venus 3, '
                              'Sun 1, Moon 1, Mars 1. CRITICAL QUALIFICATION: only '
                              'TWO of those 15 are branch-LEVEL labels, i.e. the '
                              'text calling the whole result '
                              'auspicious/inauspicious — Mercury vv.30-33 '
                              '"Auspicious effects like Raja yoga..." and Venus '
                              'vv.48-50.5 "...will be the auspicious results". The '
                              'other 13 are ITEM-level: the words "danger" and '
                              '"loss" occurring inside an enumerated outcome '
                              '("danger from thieves", "loss of wealth"), which '
                              'labels one listed item, not the branch. Zero '
                              'occurrences of "inauspicious", "adverse", "evil" or '
                              '"favourable" inside any sloka clause in this '
                              'chapter — "evil effects" appears only in the remedy '
                              'sentences ("relief from the above evil effects"), '
                              'which per the brief is NOT a polarity marker, and '
                              '"inauspicious" appears only inside Santhanam\'s '
                              'note on Jupiter vv.13-14.5. So on a branch-level '
                              'reading, 2 of 31 carry stated valence and 29 do '
                              'not; on the item-level reading directed by the '
                              'brief, 15 of 31. I have recorded the item-level '
                              'hits (with polarity_word quoted) so the caller can '
                              'discount them. Saturn vv.21-24 is recorded polarity '
                              '"none" deliberately: that single branch contains '
                              'BOTH "auspicious functions" and "loss of wealth '
                              'caused by the king" in one result list, so no '
                              'branch valence is readable. All 9 maraka/lordship '
                              'clauses are recorded polarity "none" per ch.34\'s '
                              'prohibition on mixing a maraka verdict with a '
                              'benefic/malefic nature, even though "death" or '
                              '"danger" occurs in 6 of them.'},
 'saturn': {'chapter': 'Vol II, Chapter 57 — "Effects of the Antardasas in the '
                       'Dasa of Saturn"',
            'frame_summary': '72 condition-rows extracted across the 9 cells. By '
                             'frame: not_a_house 33 (46%) — '
                             'dignity/association/transit/sign/strength conditions '
                             'that are not house counts at all; from_lagna 18 '
                             '(25%); from_dasa_lord 12 (17%), always glossed "from '
                             'the lord of the Dasa (Saturn)" or "from the Dasa '
                             'lord"; unstated 9 (12%); from_moon 0 (the Moon is '
                             'never used as a reference frame anywhere in this '
                             'chapter). The 9 unstated rows are the ones that '
                             'matter: (a) FOUR are bare house terms with no frame '
                             'at all — Ketu vv.16-18 "in kendra or trikona", Venus '
                             'vv.24-27½ "in kendra, trikona or the llth", Jupiter '
                             'vv.71-73½ "in kendra or trikona", and these sit '
                             'inside otherwise identical sentences where sibling '
                             'cells DO name a frame; (b) THREE are '
                             '2nd/7th-lordship maraka clauses that omit "from the '
                             'Ascendant" while five other cells include it (Saturn '
                             'vv.6-7, Mercury vv.14-15, Rahu vv.69-70); (c) TWO '
                             'are Santhanam notes. Additionally THREE from_lagna '
                             'rows rest on a PARENTHESISED frame — "(from the '
                             'Ascendant)" in Mercury vv.8-11, Venus vv.28-29, '
                             'Jupiter vv.81-82 — parentheses in this edition mark '
                             'translator interpolation, so those three are weaker '
                             'evidence than the unbracketed ones and are flagged '
                             'individually in ocr_flag. Five branches state TWO '
                             'frames disjunctively in one sentence ("from the '
                             'Ascendant or the lord of the Dasa"): Mercury '
                             'vv.12-13½, Ketu vv.20-21½, Sun vv.39-41, Rahu '
                             'vv.65-67; these are split into two rows each, both '
                             'quoting the same sentence.',
            'gaps': '1. TWO PAGES ARE COLUMN-SCRAMBLED IN THE OCR. p.205: verses '
                    '28-29 (a Venus condition) are printed BEFORE the "Effects of '
                    'the Antardasa of Venus in the Dasa of Saturn" heading and '
                    'before verses 24-27½; the Ketu remedy (goat) is interleaved '
                    'between them. I assigned 28-29 to Venus on verse-number '
                    'grounds (24-27½ opens Venus), but the physical ordering does '
                    'not support it and this should be checked against the printed '
                    'book. p.210: verses 61-62 are printed BEFORE verses 58-60 in '
                    'the Mars section. Verse content is intact in both cases; only '
                    'the ordering is damaged.\n'
                    '2. MISSING VERSE RUN: verses 24-27½ are the Venus opening, '
                    'but the Devanagari for the Ketu remedy and the transition is '
                    'heavily degraded on p.205; no verse numbers are lost, but I '
                    'cannot confirm from OCR alone that nothing sits between v.23 '
                    'and v.24.\n'
                    '3. "trikona" and "kendra" are NEVER enumerated as house '
                    'numbers anywhere in this chapter. I have not expanded them '
                    '(kendra→1,4,7,10 and trikona→1,5,9 vs 5,9 are both live '
                    'readings in BPHS). Every such row has houses recorded as the '
                    'literal word.\n'
                    '4. THE MARAKA SLOT IS NOT UNIFORM ACROSS THE NINE CELLS and '
                    'the variation is almost certainly meaningful, not OCR noise: '
                    'six cells say the antar lord "be the LORD of the 2nd or the '
                    '7th"; Ketu vv.22-23 says "be IN the 2nd or the 7th" '
                    '(placement, not lordship); Rahu vv.69-70 says "be ASSOCIATED '
                    'WITH the lord of the 2nd or the 7th"; Mars vv.61-62 is a '
                    'hybrid — "be in the 2nd or be the lord of the 7th or the 8th" '
                    '— the only place in the chapter where the 8th enters a maraka '
                    'clause. Do not normalise these to one rule.\n'
                    '5. Also non-uniform: only Saturn (danger of premature death), '
                    'Mars (fear of premature death) and Jupiter (death of the '
                    'native or any member of family) state DEATH in the 2nd/7th '
                    'clause. The other six state only "physical distress". Per '
                    'ch.34 no benefic/malefic polarity is attached to any of these '
                    'rows.\n'
                    '6. Ketu vv.16-18 is structurally unique in the chapter: it is '
                    'a CONCESSIVE branch — "Evil effects ... will be derived ... '
                    'EVEN IF Ketu be in his sign of exaltation, in his own sign, '
                    'in a benefic sign or in kendra or trikona or be associated '
                    'with or aspected by benefics". The good placements produce '
                    'the evil result. Any engine that treats exaltation as '
                    'favourable will invert this cell.\n'
                    '7. Venus vv.24-27½ makes two of its clauses depend on TRANSIT '
                    '("If Jupiter be favourable in transit", "If Saturn be '
                    'favourable in transit") — the only transit conditions in the '
                    'chapter. "Favourable in transit" is nowhere defined here; the '
                    'criterion is not in this chapter.\n'
                    '8. Rahu vv.63-64 is stated NEGATIVELY ("if Rahu not be in his '
                    'house of exaltation or any other auspicious position") and '
                    '"any other auspicious position" is left undefined — an open '
                    'term the text does not settle.\n'
                    '9. Rahu vv.68-68½ gives a SIGN list (Aries, Virgo, Cancer, '
                    'Taurus, Pisces, Sagittarius) with no house frame at all — the '
                    "only rasi-based condition in the chapter. Santhanam's note "
                    'immediately qualifies it, and the note contradicts the plain '
                    'sloka by adding a house requirement the sloka does not '
                    'state.\n'
                    '10. OCR text damage inside otherwise usable clauses: Jupiter '
                    'vv.76-78 renders the 5th as "the\'Sth" (read as 5th from the '
                    'sequence 5/9/11/2/kendra, but ambiguous with 8th on the glyph '
                    'alone) — FLAGGED as a real ambiguity, not resolved; Venus '
                    'vv.28-29 "debiliiation"/"bQ"; Sun vv.37-38½ "a:nccted by '
                    'bcnefics" (read as "aspected"); Rahu vv.65-67 "exaltatio!"; '
                    'several verse-number markers carry stray glyphs.\n'
                    '11. TWO Santhanam notes are recorded as source "note" and '
                    'must never be promoted to mula: the ch.57 note on Mercury '
                    'vv.12-13½ openly doubts the sloka ("we dare not question '
                    'Parasara"), and the note on Moon vv.46-48½ states a general '
                    'belief ("nothing good may be expected if the Antardasa lord '
                    'is ill placed") that has no sloka behind it in this chapter.\n'
                    '12. No sub-period (commencement/middle/last) rule is given a '
                    'frame or a duration anywhere; where the text splits a branch '
                    'by portion of the Dasa I have kept the words in `results` and '
                    'not converted them into anything computable.',
            'pdf_pages': '201-214 (chapter heading on p.201, ends p.214; ch.58 '
                         'heading begins p.215)',
            'polarity_summary': 'Only FOUR explicit valence labels on results '
                                'exist in the whole chapter (82 verses, 14 pages): '
                                '"will be the evil effects" (vv.4-5½), "The last '
                                'part of the Dasa will yield beneficial results" '
                                '(v.5½), "Evil effects like..." (vv.16-18), "There '
                                'will, however, be good effects" (vv.46-48½). '
                                'Spread over the condition-rows they belong to, '
                                'that is 7 rows of 72 carrying a polarity (10%) — '
                                '3 favourable, 4 adverse — and 65 rows (90%) with '
                                'polarity "none". Every other branch uses a '
                                'neutral verb: "will be derived", "will be '
                                'experienced", "will be the results", "will be the '
                                'effects", "may be expected", "There will be". TWO '
                                'DELIBERATE NON-MARKINGS, both traps: (1) '
                                'vv.24-27½ "If Jupiter be favourable in transit" '
                                'and vv.63-64 "or any other auspicious position" — '
                                'here "favourable"/"auspicious" qualify the '
                                'CONDITION, not the result, and are not polarity; '
                                '(2) the recurring remedy sentence "to obtain '
                                'relief from the above evil effects" contains '
                                '"evil" but is a remedy clause sitting after both '
                                'branches, so it is excluded per the standing '
                                'rule. Words like "loss", "danger", "death" occur '
                                'constantly inside outcome LISTS (loss of '
                                'position, danger from thieves, fear of premature '
                                'death) — these are outcomes, not branch labels, '
                                'and are NOT recorded as polarity; they are '
                                'visible in the `results` text for anyone who '
                                'wants them.'},
 'sun': {'chapter': 'Vol II ch.52 — Effects of the Antardasas in the Dasa of the '
                    'Sun (Vimsottari)',
         'frame_summary': '60 conditions. from_dasa_lord = 12 (the workhorse, as '
                          'reported; every instance is explicitly glossed, e.g. '
                          '"from the lord of the Dasa", "from the lord of the Dasa '
                          '(the Sun)", "with reference to the lord of the Dasa '
                          '(the Sun)"). from_lagna = 7 ("from the Ascendant", "to '
                          'the Ascendant"). from_moon = 0 — the Moon is NEVER used '
                          'as a reference frame anywhere in ch.52. unstated = 9 — '
                          'house numbers given with NO frame word: Sun v.1-3 "the '
                          '11th, Kendra or trikona" / "an inauspicious house or '
                          'sign" / "in other houses"; Moon v.4-5 "in a kendra or '
                          'trikona" and v.7-10 "in the 6th, the 8th or the 12th '
                          'house"; Mars v.15-18 "in kendra or trikona"; Rahu '
                          'v.30-31 "in the 2nd or 7th"; Mercury v.50-51 "in the '
                          '9th, the 5th or the 10th"; Venus v.65-68 "posited in a '
                          'kendra trikona". These 9 are left unstated and MUST NOT '
                          'be defaulted to the Ascendant — note that the chapter '
                          'proves it can say "from the Ascendant" when it means it '
                          '(7 times), so the omission is meaningful, not '
                          'shorthand. not_a_house = 32 (dignity, conjunction, '
                          'lordship, strength, navamsa, waning).',
         'gaps': 'STRUCTURAL / TEXTUAL GAPS AND FLAGS — none resolved, only '
                 'reported.\n'
                 '\n'
                 '1. PAGE-ORDER SCRAMBLE IN THE SOURCE OCR. The extracted text '
                 'does not run in book-page order through ch.52. PDFPAGE 141 '
                 'prints vv.27-29 BEFORE vv.23-26. PDFPAGE 142 carries book pages '
                 '632 and 634 material interleaved: it holds the tail of Rahu '
                 'vv.30-31, then Saturn vv.43-47, plus the CONDITION clause of '
                 'Saturn vv.40-42 whose RESULT clause is printed at the foot of '
                 'PDFPAGE 144. I reconstructed the Saturn 40-42 sentence across '
                 'that break on grammar and content; the join is confident but it '
                 'IS a reconstruction and should be re-verified against the '
                 'physical page before it ships.\n'
                 '\n'
                 '2. DAMAGED HOUSE NUMBERS — three places where a rule cannot be '
                 'implemented as printed:\n'
                 '   - Jupiter vv.37-39, PDFPAGE 144: "if the Jupiter be in the '
                 '6th or the6rh f\'om the lord of the Dasa". The second house is '
                 'unreadable. Parallel cells suggest 8th or 12th; the text does '
                 'not settle it. DO NOT IMPLEMENT the second house.\n'
                 '   - Mercury vv.50-51, PDFPAGE 145: "in the 9th, the Sth or the '
                 'l0th" — "Sth" is most likely 5th (giving 5/9/10) but 8th is not '
                 'excluded.\n'
                 '   - Ketu vv.62-64, PDFPAGE 147: "in the 3rd, the fth, the 10th '
                 'or the llth from the Ascendant" — "fth" is most likely 6th (the '
                 'upachaya set, which the Rahu section spells out as 3,6,10,11 on '
                 'PDFPAGE 141) but the glyph is destroyed.\n'
                 '\n'
                 '3. NINE CONDITIONS STATE A HOUSE WITH NO FRAME (listed in '
                 'frame_summary). The chapter demonstrably CAN say "from the '
                 'Ascendant" — it does so seven times — so silence is evidence, '
                 'not shorthand. All nine are recorded frame="unstated" and must '
                 'surface as "unavailable" rather than being defaulted to the '
                 'Ascendant. This is the single largest correctness risk in the '
                 "cell set: four of the nine are the headline 'kendra or trikona' "
                 'branch of their cell (Sun, Moon, Mars, Venus), i.e. the branch '
                 'most likely to fire on a real chart.\n'
                 '\n'
                 '4. PREDICATES NOT TESTABLE AS WRITTEN — the text names a '
                 'condition but never enumerates it:\n'
                 '   - Sun vv.1-3: "an in auspicious house or sign" — which '
                 'houses? Never said.\n'
                 '   - Rahu vv.23-26: "be placed auspiciously fron the loro of the '
                 'l)asa" — which positions count as auspicious from the dasa lord? '
                 'Never said.\n'
                 '   - Jupiter vv.34-36 (PDFPAGE 144): "well placed with reference '
                 'to rhe lord of the Dasa (the Sun)" — the frame is explicit and '
                 "unambiguous, but 'well placed' is never enumerated. The clearest "
                 'case in the chapter of a stated frame with an unstated '
                 'predicate.\n'
                 '   - Mercury vv.52-53: "an auspicious house like trikona etc\'\' '
                 'from the lord of the Dasa" — the \'etc.\' is open-ended.\n'
                 '   - Jupiter vv.32-33 and Venus vv.65-68: "in his own Varga" — '
                 'which of the sodasavarga is meant is not specified.\n'
                 '   - Moon vv.13-14, Mars vv.19-22, Rahu vv.27-29: "weak" / '
                 '"without dignity and strength" — no strength metric is defined '
                 'in ch.52.\n'
                 '\n'
                 '5. THE MARAKA CLAUSE IS NOT UNIFORM ACROSS THE NINE CELLS, and '
                 'must not be normalised:\n'
                 '   - Death verdict on 2nd/7th LORDSHIP: Sun, Moon, Saturn, Ketu '
                 "(Ketu's via an editorial bracket, since Ketu holds no "
                 'lordship).\n'
                 '   - Death verdict on OCCUPANCY of, or association with the '
                 'lords of, the 2nd/7th: Rahu (stated in the running text).\n'
                 '   - ILLNESS only, no death, from 2nd/7th lordship: Mars '
                 '(diseases of mind and body), Mercury (pains and fever), Venus '
                 '(pains and diseases).\n'
                 '   - Death verdict from association with the 6TH OR 8TH LORDS, '
                 'not the 2nd/7th at all: Venus.\n'
                 '   - NO maraka clause whatsoever: Jupiter.\n'
                 '   Per ch.34, a maraka verdict must be kept on a separate axis '
                 'from the benefic/malefic nature verdict; ch.52 gives no '
                 'tie-break where both fire.\n'
                 '\n'
                 '6. TIMED / PHASED CLAUSES that a whole-period verdict cannot '
                 'represent: Rahu vv.23-26 (first two months vs after), Saturn '
                 'vv.45-47 (unconditional, thirds), Mercury vv.54-57 '
                 '(unconditional, thirds), Ketu vv.58-59 (conditional on '
                 'lagna-lord association, thirds), Venus vv.69-71 (unconditional, '
                 'thirds). Saturn\'s says "at the end of the Dasa" — Dasa, not '
                 'Antardasa — leaving it genuinely ambiguous whether the thirds '
                 'partition the Saturn antardasa or the whole Sun mahadasa. '
                 'UNRESOLVED.\n'
                 '\n'
                 "7. THE KETU CELL'S OPENING CLAUSE (vv.58-59) HAS NO CONDITION AT "
                 'ALL — the effects are stated flatly for the Ketu antardasa in a '
                 "Sun mahadasa. Every other cell opens with an 'if'. This is a "
                 'real asymmetry in the text, not an extraction failure.\n'
                 '\n'
                 '8. ONE EDITORIAL NOTE FOUND, marked source="note": "(Mercury '
                 'cannot be in the 6th or 8th from the Sun)" (PDFPAGE 146). It is '
                 'astronomically correct and means two of the three limbs of '
                 'Mercury vv.54-57 can never fire during a Sun mahadasa. The '
                 'identical reachability problem applies to Venus vv.69-71 '
                 '(6th/8th from the Sun) but the text offers NO note there, and I '
                 'have not supplied one.\n'
                 '\n'
                 '9. OTHER EDITORIAL PARENTHETICALS treated as gloss rather than '
                 'mula: "(motor car in the present times)" (Jupiter, PDFPAGE 143), '
                 '"(3,6,10,11)" after \'upachaya house\' (Rahu, PDFPAGE 141), '
                 '"(2nd or 7th)" after \'maraka house\' (Moon, PDFPAGE 139), "(or '
                 'be in any of those houses)" (Ketu, PDFPAGE 147), "(and 2nd)" '
                 '(Venus, PDFPAGE 148).\n'
                 '\n'
                 '10. Saturn\'s dignity branch reads "in his sign of exaltation, '
                 'in his own sign, in a friendly sign AND in conjunction with a '
                 'friendly planet" — a conjunctive \'and\' where every other cell '
                 "in the chapter uses 'or'. Taken literally it demands all four at "
                 'once, which is near-impossible. Most likely a translation '
                 'artifact, but the text does not settle it. FLAGGED.\n'
                 '\n'
                 '11. NO CONDITION ANYWHERE IN CH.52 USES THE MOON AS A REFERENCE '
                 'FRAME. Zero instances of "from the Moon". If the engine offers a '
                 'from_Moon frame, nothing in this chapter feeds it.\n'
                 '\n'
                 '12. RESULT-LIST ANOMALY, Rahu vv.27-29 (PDFPAGE 141): "happiness '
                 'to wife and chilciren" appears inside an otherwise wholly '
                 'afflictive list (imprisonment, loss of position, destruction of '
                 'cattle, diseases). Either an OCR corruption of a negative phrase '
                 'or a genuine oddity of the text. Cannot be resolved from this '
                 'edition.',
         'pdf_pages': '137-148 (book pp. 627-638); vv. 1-73',
         'polarity_summary': '60 conditions extracted. 27 carry an EXPLICIT '
                             'valence word in the sloka clause itself (16 '
                             'favourable: '
                             '"Good"/"Auspicious"/"auspicious"/"favourable"/"good"/"beneficial"/"Beneficial"; '
                             '11 adverse: '
                             '"Adverse"/"inauspicious"/"evil"/"danger"/"death"). '
                             '33 conditions — 55% — carry NO valence word at all: '
                             'the text uses neutral verbs ("will be the effects", '
                             '"will be derived", "will result", "will be '
                             'experienced", "will be the results") followed by a '
                             'bare list of outcomes. This confirms the prior pass: '
                             'explicit valence is a minority. Deliberate cautious '
                             'calls: (a) "Medium effects will be realised" (v.1-3) '
                             'is recorded polarity=none — "medium" is a magnitude '
                             'grade, not a valence word; (b) branches whose '
                             'outcome LISTS contain nouns like "loss of servants", '
                             '"danger from water", "destruction of wealth" but '
                             'carry no branch-level label are recorded none — e.g. '
                             'Moon vv.7-10 both branches, Mars vv.19-20 and 21-22, '
                             'Rahu vv.27-29; (c) the three unconditional TIMED '
                             'clauses (Saturn vv.45-47, Mercury vv.54-57, Venus '
                             'vv.69-71) mix "good effects during the middle part" '
                             'with "distress/evil at the end" in one sentence and '
                             'are recorded none rather than forced to a single '
                             "sign. Where the branch's entire stated result IS the "
                             'valence claim ("there will be danger of premature '
                             'death", "There will be premature death") polarity is '
                             'recorded adverse with that word quoted.'},
 'venus': {'chapter': 'Vol II ch.60 — Effects of the Antardasas in the Dasa of '
                      'Venus',
           'frame_summary': '60 conditions extracted across the 9 antar cells. '
                            'Frame distribution: not_a_house 21 (35%); from_lagna '
                            '19 (32%); from_dasa_lord 11 (18%); UNSTATED 9 (15%); '
                            'from_moon 0 (0%). THE MOON IS NEVER USED AS A '
                            'REFERENCE FRAME ANYWHERE IN CH.60. from_dasa_lord is '
                            "always glossed '(Venus)' except in the Mars adverse "
                            "branch (v.34), which reads bare 'the lord of the "
                            "Dasa'. The 9 unstated-frame conditions — the ones "
                            'that must NOT be silently anchored — are: (1) Moon '
                            "vv.21-22 'or be in a kendra. trikona or the llth', "
                            'the sentence ends with no anchor; (2) Moon vv.23-23½ '
                            "'In the above circumstances', which inherits (1); (3) "
                            'Moon closing Note on 2nd/7th lordship, where the '
                            'translator concedes it is not mentioned; (4) Rahu '
                            "vv.36-37½ 'if Rahu be in kendra or trikona or the "
                            "llth', no anchor; (5) Rahu vv.40-41½ 'In the above "
                            "circumstances', inheriting vv.38-39; (6) Jupiter v.51 "
                            "'if Jupiter be the lord of the 2nd and the 7th', "
                            "where 'from the Ascendant' is ABSENT although present "
                            'in all seven parallel maraka clauses; (7) Saturn '
                            "vv.52-54 'in his own sign in kendra, trikona or in "
                            "his own Navamsa', no anchor; (8) Ketu vv.69-69½ 'In "
                            "the above circumstances'; (9) the Sun's untranslated "
                            'Chowkhamba Note. SIX sections do offer a DUAL frame '
                            "('from the Ascendant OR the lord of the Dasa "
                            "(Venus)'): Sun v.15, Moon vv.24-26½, Mars v.34, "
                            'Jupiter vv.45-48, Saturn vv.55-57, Mercury vv.60-62. '
                            'Each is recorded as TWO separate conditions rather '
                            'than collapsed, because the text presents them as '
                            'alternatives and states no priority between them — '
                            'the tie-break is not in the text. Note also that the '
                            'Mercury dual frame is the only one printed in '
                            'parentheses, which may make it a translator insertion '
                            'rather than mula (flagged in that cell).',
           'gaps': '1. OCR-DESTROYED HOUSE NUMBERS — do not guess: (a) Venus '
                   "vv.7-8 'in the 3rd, thd: ;,ti: or the llth' — the middle house "
                   "is unreadable; (b) Rahu vv.38-39 'the 3rd, the 6th, the lfth "
                   "or tbe llth' — 'lfth' is unreadable (plausibly 10th, "
                   "unverified), and a '6th' inside a FAVOURABLE list is itself "
                   'anomalous for this chapter and may also be corrupt; (c) Saturn '
                   "vv.55-57 'in the 8th, the llth or the l2th' — an '11th' in an "
                   "ADVERSE house-set contradicts this chapter's own consistent "
                   'use of the 11th as favourable and is very likely corrupt for '
                   "'6th'. All three need the Devanagari before shipping. 2. SUN "
                   "v.12 IS REPUDIATED BY THE TRANSLATOR ('This verse does not "
                   "appear to be correctly worded') and the corrected Chowkhamba "
                   'reading he cites is printed only in Devanagari, which this OCR '
                   "renders unusably. The Sun antar's 'any sign other than "
                   "exaltation or debilitation' rule is therefore UNAVAILABLE, not "
                   'merely doubtful. 3. NO MARAKA CLAUSE EXISTS FOR THE MOON in '
                   "the mula; Santhanam's note openly says 'it is not mentioned' "
                   'and supplies it by analogy. Must not ship as a rule. 4. '
                   'JUPITER v.51 states no reference frame for the 2nd/7th '
                   "lordship and reads 'and' where all parallels read 'or'. 5. "
                   'MARS has NO remedial measure in the mula; the bull-in-charity '
                   "remedy is the translator's own conjecture ('we believe'). The "
                   'MOON section has no remedy at all, from either source. 6. '
                   "UNDEFINED STRENGTH PREDICATES: Venus vv.1-2½ 'endowed with "
                   "strength'; Mercury vv.63-65 'be weak'; Ketu vv.67-68 "
                   "'positional strength' — the last is explicitly flagged by the "
                   "translator as never laid down anywhere ('It is not laid down "
                   "any where in which house does Ketu get positional strength'), "
                   "so it is permanently unavailable. 7. MERCURY vv.60-62's second "
                   "frame '(or from the lord of the Dasa Venus)' is PARENTHESISED "
                   'in the printed English, unlike every other dual frame in the '
                   'chapter; it may be a translator insertion rather than mula. 8. '
                   'PDFPAGE 246 (the whole Rahu favourable section, vv.36-41½) has '
                   'the worst OCR in the chapter — the English is recoverable by '
                   "context but every word there should be re-verified. Its 'at "
                   "the end of the Dasa' (rather than Antardasa) may also be "
                   'corrupt. 9. ADVERSE HOUSE-SETS ARE NOT UNIFORM: most branches '
                   'use 6/8/12, but Rahu vv.42-44 and Ketu vv.70-72 use 8/12 only, '
                   'and Saturn vv.55-57 reads 8/11/12. Recorded as printed, not '
                   'normalised. 10. Several branches carry internal '
                   'TIME-SEGMENTATION (Moon vv.27-29 fit-then-distress; Rahu '
                   'vv.38-39 good for 5 months then danger; Mercury vv.63-65 '
                   'good/moderate/distress; Ketu vv.69-69½ victory at end, '
                   'moderate in middle) which the existing four-state verdict '
                   'model (favourable/adverse/contested/not_stated) cannot '
                   'express. A modelling gap, not a text gap. 11. LORDSHIP ANCHORS '
                   "UNSTATED: 'lord of the 9th', 'lord of the 10th', 'lord of the "
                   "Ascendant' (Moon vv.21-22, Mars vv.30-31½) are stated without "
                   'saying from what the 9th/10th are counted. 12. The chapter '
                   'states no rule at all for a Venus antar cell where none of the '
                   'listed disjuncts fires — the not_stated state is reached by '
                   'silence, exactly as in ch.47.',
           'pdf_pages': '240-251 (printed pages 730-741); chapter head on PDFPAGE '
                        "240, ends immediately before 'Chapter 61' on PDFPAGE 252",
           'polarity_summary': 'Of the 60 conditions, 39 (65%) carry NO explicit '
                               "valence word and are recorded polarity 'none'; 21 "
                               '(35%) carry one — 19 adverse, 2 favourable. '
                               'Crucially, only FOUR of those 21 use the valence '
                               'word as a genuine BRANCH-LEVEL LABEL: Sun vv.19-20 '
                               "'evil influence of the planets'; Rahu vv.40-41½ "
                               "'auspicious results'; Rahu vv.42-44 'inauspicious "
                               "effects'; Ketu vv.67-68 'Auspicious effects "
                               "like...'. The other 17 have a listed word ('loss', "
                               "'losses', 'danger', 'death') buried inside ONE "
                               "ITEM of an outcome list — e.g. 'loss of position' "
                               'among six other items — and several of those 17 '
                               'are the same results clause duplicated across two '
                               'frames. Counting DISTINCT SLOKA BRANCHES rather '
                               'than conditions, roughly 4 of ~30 branches carry a '
                               'true valence label: about 13%, consistent with the '
                               'prior passes on ch.54 and ch.57. Two judgement '
                               'calls, both made in the cautious direction and '
                               "disclosed here: (a) Rahu vv.38-39 contains 'danger "
                               "from fevers and indigestion' but ONLY in an "
                               'end-of-period tail attached to an otherwise '
                               "favourable list headed by 'Good effects' (not a "
                               "listed valence word) — recorded polarity 'none' "
                               'rather than stamp an adverse verdict on a branch '
                               'the text does not so characterise; (b) Saturn v.55 '
                               "('lethargy and more expenditure than income' on "
                               "debilitation) and every 'physical distress' maraka "
                               "clause are recorded 'none' because 'distress', "
                               "'agony' and 'lethargy' are NOT among the listed "
                               'valence words, despite obviously unpleasant '
                               'content. Ten branches with plainly pleasant '
                               'content — Venus vv.1-2½, vv.3-6, vv.7-8; Sun '
                               'vv.13-15; Moon vv.21-22, vv.27-29; Mars vv.30-31½; '
                               'Jupiter vv.45-48; Saturn vv.52-54; Mercury '
                               "vv.60-62 — use only neutral verbs ('will be "
                               "derived', 'will be the results', 'will be "
                               "experienced') and are recorded 'none'. No "
                               "condition in this chapter fires as 'contested' at "
                               'the text level; the contested state would only '
                               'arise on a real chart when disjuncts from opposite '
                               'branches both match.'}}

# (maha_lord, antar_lord) -> cell. All 81 present; none synthesised.
# maraka=None / remedy=None mean the cell HAS no such clause. Where the
# extraction described that absence in prose, the prose is kept under
# 'absence_notes' and the field itself reads as absent.
MATRIX = {
    ('jupiter', 'jupiter'): {'verses': '1-7',
 'conditions': [{'predicate': 'in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'sovereignty over many kings, very well-endowed with '
                            'riches, revered by the king, gains of cattle, '
                            'clothes, ornaments, conveyances, construction of a '
                            'new house and a decent mansion, opulence and glory, '
                            'dawn of fortune, success in ventures, meetings with '
                            'Brahmins and the king, extraordinary profits from the '
                            'employer, happiness to wife and children',
                 'source': 'sloka',
                 'quote': 'l-33. Effects like sovereignty over many kings, very '
                          'wellendowed with riches, reverred by the king, ... will '
                          "be experienced i' the Antardasa of Jupiter in liis "
                          'own.Dasa, if Jupiter be in his sign of exaltation, in '
                          'his ownsign, in kendra or trikona.from the Asceudant.',
                 'pdf_page': '188',
                 'ocr_flag': "Verse number printed 'l-33' for 1-3; 'Asceudant' = "
                             'Ascendant.'},
                {'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if Jupiter be in his sign of exaltation, in his '
                          'ownsign, in kendra or trikona.from the Asceudant.',
                 'pdf_page': '188',
                 'ocr_flag': ''},
                {'predicate': 'in a kendra or trikona from the Ascendant',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Asceudant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if Jupiter be in his sign of exaltation, in his '
                          'ownsign, in kendra or trikona.from the Asceudant.',
                 'pdf_page': '188',
                 'ocr_flag': "'Asceudant' = Ascendant."},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'association with the menials, great distress, slander '
                            'by co-parceners, wrath of the employer, danger of '
                            'premature death, separation from wife and children, '
                            'loss of wealth and grains',
                 'source': 'sloka',
                 'quote': '4-5$. Association with the menials, great distress, '
                          'slander by co-parceners, wrath of the employet, danger '
                          'of prematu.:e death, separation from wife and children '
                          'and loss of wealth an<! grains, will be the results, if '
                          'Jupiter be in his sign of debilitatiw,',
                 'pdf_page': '188',
                 'ocr_flag': "'debilitatiw' = debilitation; the branch continues "
                             'across the page break onto p.189 interleaved with '
                             'the Saturn section heading.'},
                {'predicate': 'in his debilitated Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'in hi: Jsfililated Navamsa, or in',
                 'pdf_page': '189',
                 'ocr_flag': "SEVERE. 'in hi: Jsfililated Navamsa' reconstructed "
                             "as 'in his debilitated Navamsa'. The line is split "
                             "by the interposed heading 'Effects of the AntarAo.* "
                             "oi Saturn in the Dasa of Jupiter'."},
                {'predicate': 'in the 6th, the 8th or the 12th from the Ascendant',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'the 6th, the 8th or the l2th ... from the Ascendant.',
                 'pdf_page': '189',
                 'ocr_flag': "SEVERE. 'the 6th, the 8th or the l2th' and 'from the "
                             "Ascendant' appear on separate OCR lines on p.189, "
                             'separated by the Saturn section heading and '
                             'Devanagari fragments. Reconstruction is confident '
                             'but is a reconstruction.'},
                {'predicate': 'lord of the 7th (or the 2nd) — maraka clause',
                 'houses': '7,2',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'pains in the body',
                 'source': 'sloka',
                 'quote': '6-7. There will be pains in the body if Jupiter be tire '
                          'lordof rhc 7th (or 2nd).',
                 'pdf_page': '189',
                 'ocr_flag': "'tire lordof rhc 7th' = 'be the lord of the 7th'. "
                             "Note the unusual 7th-first ordering with '(or 2nd)' "
                             'parenthetical.'}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'ketu'): {'verses': '32-38',
 'conditions': [{'predicate': 'associated with or aspected by a benefic',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'moderate enjoyment, moderate gain of wealth, coarse '
                            'food or food given by others, food given at the time '
                            'of death ceremonies, acquisition of wealth through '
                            'undesirable means',
                 'source': 'sloka',
                 'quote': "12'32*. Moderate enjoyment, moderate gain of wealth' "
                          'coarse food or food given b! -others, food given at the '
                          'time of death ceremonies and acquisition of wealth '
                          'through undesirable means, will be the rc,",its, in the '
                          "Antardasa of Ketu in the Dasa 'of Jupiter, if Ketu bc "
                          "associated with or aspected by berrefic'",
                 'pdf_page': '193',
                 'ocr_flag': "Verse number printed '12'32*' for 32-32.5; "
                             '\'rc,",its\'=results; \'berrefic\'=benefic. NOTE: '
                             "'death' occurs here only inside the RESULT phrase "
                             "'food given at the time of death ceremonies' "
                             '(sraddha food) — descriptive, not a valence label. '
                             'Polarity recorded as none.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the .Dasa',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'loss of wealth by the wrath of the king, '
                            'imprisonment, diseases, loss of physical strength, '
                            'antagonism with father and brother, mental agony',
                 'source': 'sloka',
                 'quote': '33-34. Effects like loss of wealth by the wrath of the '
                          "king' .inrpriso*n:.ent, diseases, loss of physical "
                          'strength, antagonisrrl with famdr and brother and '
                          "mental agony' will be experienced if Ketu be in the "
                          '6th, the 8th or thd l2th from the lord of the .Dasa or '
                          'tre associated with malefics.',
                 'pdf_page': '193',
                 'ocr_flag': "'.inrpriso*n:.ent'=imprisonment; 'famdr'=father; "
                             "'thd'=the; 'tre'=be. This from_dasa_lord clause "
                             "carries NO '(Jupiter)' gloss."},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or tre associated with malefics.',
                 'pdf_page': '193',
                 'ocr_flag': "'tre'=be."},
                {'predicate': 'in the 5th, the 9th, the 4th or the 10th from the '
                              'lord of the Dasa (Jupiter)',
                 'houses': '5,9,4,10',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Jupiter)',
                 'polarity': 'favourable',
                 'polarity_word': 'ruspicious [auspicious]',
                 'results': 'acquisition of a palanquin (motor car), elephants '
                            'etc., beneficence of the king, success in the desired '
                            'spheres, profits in business, increase in the number '
                            'of cattle, gain of wealth, clothes etc. from a Yavana '
                            'king (muslim dignitary)',
                 'source': 'sloka',
                 'quote': '35-36{. Acquisition of a palanquin (motor car), '
                          'elephants etc., beneficence of the king, success in the '
                          "desired spheres''profits ir, business, increase in the "
                          'number of cattle, gain of wealth, clothes etc. from a '
                          'Yavana king (muslim dignitary), will be the ruspicious '
                          'effects if Ketu be in the 5th, the 9th, the 4th or the '
                          'l0th from the lord of the Dasa (Jupiter).',
                 'pdf_page': '193',
                 'ocr_flag': "'ruspicious' = auspicious (single-character "
                             'corruption of the valence word). Houses are '
                             'enumerated individually (5,9,4,10), NOT the full '
                             'kendra/trikona set — the 1st and 7th are absent.'},
                {'predicate': 'lord of the 2nd or the 7th (or placed in the 2nd or '
                              'the 7th) — maraka clause',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '37-38. Thcre will be pbysical drstress if Ketu be thc '
                          'lord ofthc 2nd or rhe 7th (or in the 2nd or thc Zth).',
                 'pdf_page': '194',
                 'ocr_flag': "'Thcre'=There; 'pbysical drstress'='physical "
                             "distress'; 'thc Zth'='the 7th'. The parenthetical "
                             'explicitly offers BOTH lordship and occupancy '
                             'readings; the text does not settle which.'}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'mars'): {'verses': '65-71',
 'conditions': [{'predicate': 'in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'celebration of functions such as marriage etc., gain '
                            'of land and villages, growth of strength and valour, '
                            'success in all ventures',
                 'source': 'sloka',
                 'quote': '65-66. Effects like celebration of functions such ag '
                          'marriage etc., gain of land villages, growth of '
                          'strangth and valour, sucress in all ventures, will be '
                          'derived in the Antardasa of Mars in the f)asa of '
                          'Jupiter, if Mars be in his sign of exaltation, in his '
                          'own sign, in his cxalted or own Navamsa.',
                 'pdf_page': '198',
                 'ocr_flag': "'ag'=as; 'strangth'=strength; 'sucress'=success; "
                             "'f)asa'=Dasa; 'cxalted'=exalted."},
                {'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if Mars be in his sign of exaltation, in his own sign, '
                          'in his cxalted or own Navamsa.',
                 'pdf_page': '198',
                 'ocr_flag': ''},
                {'predicate': 'in his exalted or own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'in his cxalted or own Navamsa.',
                 'pdf_page': '198',
                 'ocr_flag': "'cxalted'=exalted. This is one of only two "
                             'Navamsa-based conditions in the chapter (the other '
                             'is Jupiter v.4-5.5).'},
                {'predicate': 'in a kendra, trikona, the 11th or the 2nd — NO '
                              'FRAME STATED',
                 'houses': '1,4,7,10,5,9,11,2',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'gain of wealth and grains, availability of good '
                            'sweetish preparations, pleasure of the king '
                            '(government), happiness from wife and children and '
                            'other auspicious effects',
                 'source': 'sloka',
                 'quote': '67-68. There will be gain of wealthand grains, '
                          'availability of good sweetish preparations, pleasure of '
                          'the king (govern-ment), happiness from wife 1nd '
                          'children and other auspicious effects, if Mars be in '
                          'kendra, trikona, the llth or the 2nd and be associated '
                          'with or aspcctcd by benefics.',
                 'pdf_page': '198',
                 'ocr_flag': "CRITICAL: the sentence reads 'in kendra, trikona, "
                             "the llth or the 2nd and be associated with...' — no "
                             "'from the Ascendant' and no 'from the lord of the "
                             "Dasa' anywhere. Saturn vv.15-15.5 states the "
                             "IDENTICAL house set and DOES gloss it 'from the lord "
                             "of the Dasa (Jupiter)', which is suggestive but is "
                             'not what this sentence says. Frame recorded as '
                             "unstated. 'aspcctcd'=aspected; 'wealthand'='wealth "
                             "and'; '1nd'=and."},
                {'predicate': 'associated with or aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': "as above (same branch); joined by 'and', so a "
                            'REQUIRED conjunct',
                 'source': 'sloka',
                 'quote': 'and be associated with or aspcctcd by benefics.',
                 'pdf_page': '198',
                 'ocr_flag': "'aspcctcd'=aspected."},
                {'predicate': 'in the 8th or the 12th from the lord of the Dasa '
                              '(Jupiter) — the 6th is NOT listed',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Jupiter)',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'loss of wealth and house, eye trouble and other '
                            'inauspicious effects; the effects will be '
                            'particularly adverse at the commencement of the '
                            'Antardasa, with some mitigation of evil effects later',
                 'source': 'sloka',
                 'quote': '69-71. Loss of wealth and house, eye trouble and othcr '
                          'inauspicious effects will be the results, if Mars be in '
                          'the 8th or the l2th from the lord of the Dasa (Jupiter) '
                          'or be in his sign of debilitation associated with or '
                          'aspected by malefics. Thc cffects will be particularly '
                          'adverse at the commencement of thc Antardasa. There '
                          'will be some mitigation of evil efects later.',
                 'pdf_page': '198',
                 'ocr_flag': "'othcr'=other; 'Thc cffects'='The effects'; "
                             "'efects'=effects. NOTE the dusthana set here is only "
                             '8th/12th — the 6th is absent, unlike the eleven '
                             'other dusthana clauses in the chapter. This branch '
                             "carries three valence words: 'inauspicious', "
                             "'adverse', 'evil'."},
                {'predicate': 'in his sign of debilitation AND associated with or '
                              'aspected by malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or be in his sign of debilitation associated with or '
                          'aspected by malefics.',
                 'pdf_page': '198',
                 'ocr_flag': "As printed there is no comma, so 'debilitation' and "
                             "'associated with or aspected by malefics' read as a "
                             'conjunction; a reading in which they are two '
                             'separate alternatives cannot be excluded. Flagged, '
                             'not resolved.'},
                {'predicate': 'lord of the 2nd or the 7th — maraka clause',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress and mental agony',
                 'source': 'sloka',
                 'quote': 'There will be physical distress and mental agony if '
                          'Mars be the lord of the 2nd or the 7th.',
                 'pdf_page': '199',
                 'ocr_flag': 'Runs on from v.71 across the p.198/199 break without '
                             'its own verse number.'}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'mercury'): {'verses': '20-31',
 'conditions': [{'predicate': 'in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of wealth, bodily felicity, acquisition of a '
                            'kingdom (attainment of a high position in '
                            'government), fulfilment of ambitions by the '
                            'beneficence of the king (government), gain of '
                            'conveyances, clothes and cattle',
                 'source': 'sloka',
                 'quote': '2U21+. Effects like gains of wealth, bodily felicit-v, '
                          'acquisition of a kingdom ... rvill be rjerived in the '
                          'Antardasa of Mercury in tlie Dass of Jupiler, if '
                          'Mercury be in his sign of exaltation, in his orvn sign '
                          'or in kendra, trikona or be associated with the lord of '
                          'the Dasa (Jupite.r).',
                 'pdf_page': '191',
                 'ocr_flag': "'rvill be rjerived'='will be derived'; 'Dass'=Dasa; "
                             "'Jupiler'=Jupiter; 'orvn'=own."},
                {'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if Mercury be in his sign of exaltation, in his orvn '
                          'sign or in kendra, trikona or be associated with the '
                          'lord of the Dasa (Jupite.r).',
                 'pdf_page': '191',
                 'ocr_flag': ''},
                {'predicate': 'in a kendra or trikona — NO FRAME STATED',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or in kendra, trikona or be associated with the lord of '
                          'the Dasa (Jupite.r).',
                 'pdf_page': '191',
                 'ocr_flag': "CRITICAL: the gloss '(Jupiter)' belongs to the "
                             "ASSOCIATION clause ('associated with the lord of the "
                             "Dasa'), a separate alternative joined by 'or'. It "
                             'does NOT supply a house frame for kendra/trikona. '
                             'Frame recorded as unstated.'},
                {'predicate': 'associated with the lord of the Dasa (Jupiter)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or be associated with the lord of the Dasa (Jupite.r).',
                 'pdf_page': '191',
                 'ocr_flag': "'Jupite.r'=Jupiter."},
                {'predicate': 'aspected by Mars',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'increase in the number of enemies, loss of enjoyment '
                            'and comforts, loss in business, affliction with fever '
                            'and dysentry',
                 'source': 'sloka',
                 'quote': '22-22*. There will be increase in 1[r number of '
                          'enemies, loss of enjoyment and comiorts, loss in '
                          'business, afliction with fever and dysentry, if Mercury '
                          'be aspected by Man.',
                 'pdf_page': '191',
                 'ocr_flag': "'Man' = Mars; '1[r'=the; 'comiorts'=comforts; "
                             "'afliction'=affliction."},
                {'predicate': 'in a kendra, the 5th or the 9th from the lord of '
                              'the Dasa',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of wealth in his own country, happiness from '
                            'parents, acquisition of conveyances by the '
                            'beneficence of the king (government)',
                 'source': 'sloka',
                 'quote': '23-24. Gains of wealth in his own country, happiness '
                          'from parents, acquisition of conveyances by the '
                          'beneficence of the king (government), will result if '
                          'Mercury be in kendra, the 5th or the gthfrom the lord '
                          'of the Dasa or- be in his sien of cxaltation.',
                 'pdf_page': '191',
                 'ocr_flag': "'the gthfrom' = 'the 9th from'; 'sien of "
                             "cxaltation'='sign of exaltation'. Unlike most "
                             'from_dasa_lord clauses here, this one carries NO '
                             "'(Jupiter)' gloss."},
                {'predicate': 'in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or- be in his sien of cxaltation.',
                 'pdf_page': '191',
                 'ocr_flag': "'sien of cxaltation'='sign of exaltation'."},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (Jupiter)',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'frtrm the lord of Dasa (Jupiter)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'loss of wealth, journeys to foreign countries, danger '
                            'from thieves while travelling, wounds, burning '
                            'sensations, eye troubles, wanderings in foreign lands',
                 'source': 'sloka',
                 'quote': '25-?6: Therc wil! .be ,i9$, ,gf weallh,, journeys to '
                          'foreign countries, danger from thieveswhile traveliing, '
                          'wounds, burning sensations, eye trou o-les, t*andbrings '
                          'in\' foreigrr lands, if Mercury be in the" 6tli, the '
                          'iSth or ttre i2th frtrm the lord of Dasa (Jupiter) or '
                          'bei4ssociqted 1vj1-fo ,4 .analefic withou.t, the, '
                          'Aspect of a benefic.',
                 'pdf_page': '192',
                 'ocr_flag': "HEAVY. ',i9$, ,gf weallh,'='loss of wealth'; "
                             "'iSth'=8th; 'ttre i2th'='the 12th'; "
                             "'t*andbrings'='wanderings'; 'bei4ssociqted 1vj1-fo "
                             ",4 .analefic withou.t, the, Aspect'='be associated "
                             "with a malefic without the aspect'."},
                {'predicate': 'associated with a malefic without the aspect of a '
                              'benefic',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or bei4ssociqted 1vj1-fo ,4 .analefic withou.t, the, '
                          'Aspect of a benefic.',
                 'pdf_page': '192',
                 'ocr_flag': "HEAVY; reconstructed as 'or be associated with a "
                             "malefic without the aspect of a benefic'."},
                {'predicate': 'associated with a malefic or malefics AND in the '
                              '6th, the 8th or the 12th from the Ascendant',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'distress without reason, anger, loss of cattle, loss '
                            'in business, fear of premature death',
                 'source': 'sloka',
                 'quote': '27-28. Distress without reason, anger, lohs of cattle, '
                          "loss inbusiness, fear of'lremature death etc., will:be' "
                          'the results if Mercury be associated with a rnalefic or '
                          'malefics in the 6th, the 8th or the l2th from the '
                          'Ascendant.',
                 'pdf_page': '192',
                 'ocr_flag': "'lohs'=loss; ''lremature'=premature; "
                             "'rnalefic'=malefic. Note this is a CONJUNCTION "
                             '(malefic association AND dusthana), unlike the '
                             'disjunctions elsewhere in the chapter.'},
                {'predicate': 'associated with a malefic but aspected by a benefic '
                              '— effects at the COMMENCEMENT of the Antardasa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'enjoyment, gains of wealth, conveyances and clothes '
                            'at the commencement of the Antardasa',
                 'source': 'sloka',
                 'quote': '29-291r, There will be enjoyment, gains of wealth, '
                          '@nveyances and clothes at the commencemdnt of the '
                          'Antar-dasa, even if Mercury be associated with,a '
                          'malefic but aspected by a benefic.',
                 'pdf_page': '192',
                 'ocr_flag': "'@nveyances'=conveyances; "
                             "'commencemdnt'=commencement."},
                {'predicate': 'associated with a malefic but aspected by a benefic '
                              '— effects at the END of the period',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'loss of wealth and bodily distress',
                 'source': 'sloka',
                 'quote': 'At the end of the Dasa, hgryeyer, there will be loss of '
                          'wealth anO boaitV distress.',
                 'pdf_page': '192',
                 'ocr_flag': "'hgryeyer'=however; 'anO boaitV'='and bodily'. The "
                             "text says 'end of the Dasa' where 'end of the "
                             "Antardasa' is likely meant — NOT resolved here."},
                {'predicate': 'lord of the 2nd or the 7th — maraka clause',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'premature death may be expected',
                 'source': 'sloka',
                 'quote': '30-31. Premature death may be expected if Mercury be '
                          'the lord of the 2nd or the 7th.',
                 'pdf_page': '192',
                 'ocr_flag': ''}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'moon'): {'verses': '58-64',
 'conditions': [{'predicate': 'in a kendra, trikona or the 11th from the Ascendant',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'frbni"the Ascenddnt [from the Ascendant]',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'reverence from the king (government), opulence and '
                            'glory, happiness from wife and children, availability '
                            'of good food, gain of reputation by performance of '
                            'good deeds, increase in the number of children and '
                            'grand children, all comforts by the beneficence of '
                            'the king, religious and charitable inclinations',
                 'source': 'sloka',
                 'quote': 'sa,oo+:\'ef;cts like i.u.r.nr" iiom the"ilqrg '
                          "(government), oprilence'and glory, happiness from wife "
                          "and children, ... r*'lll be derived in th.e..Autardasa "
                          'of the lvfoon in the Dasa of Jupiier, il the Moon be in '
                          'kenrtra, trikona or thet:\'ilth :frbni"the Ascenddnt, '
                          "be in het'sign of exaltation or: in,her own:sign "
                          'aad,:be full aFS r strong and in an auspicious houge '
                          '{rog ttre, lold of.,!,11e, Qasa (J uO iter).',
                 'pdf_page': '197',
                 'ocr_flag': "HEAVY throughout. Verse marker 'sa,oo+' = 58-60.5; "
                             "'kenrtra'=kendra; 'thet:'ilth'='the 11th'; "
                             '\'frbni"the Ascenddnt\'=\'from the Ascendant\'; '
                             "'het'=her; 'aad,:be full aFS r strong'='and be full "
                             "and strong'."},
                {'predicate': 'in her sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': "be in het'sign of exaltation or: in,her own:sign",
                 'pdf_page': '197',
                 'ocr_flag': "'het'=her."},
                {'predicate': 'in her own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or: in,her own:sign',
                 'pdf_page': '197',
                 'ocr_flag': ''},
                {'predicate': 'full and strong',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "as above (same branch); joined by 'and', so a "
                            'REQUIRED conjunct',
                 'source': 'sloka',
                 'quote': 'aad,:be full aFS r strong',
                 'pdf_page': '197',
                 'ocr_flag': "'aad,:be full aFS r strong' = 'and be full and "
                             "strong'."},
                {'predicate': 'in an auspicious house from the lord of the Dasa '
                              '(Jupiter) — HOUSES NOT ENUMERATED ANYWHERE IN THE '
                              'TEXT',
                 'houses': 'UNSPECIFIED — the text never says which houses count '
                           "as 'auspicious'",
                 'frame': 'from_dasa_lord',
                 'frame_quote': '{rog ttre, lold of.,!,11e, Qasa (J uO iter) [from '
                                'the lord of the Dasa (Jupiter)]',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "as above (same branch); joined by 'and', so a "
                            'REQUIRED conjunct',
                 'source': 'sloka',
                 'quote': 'and in an auspicious houge {rog ttre, lold of.,!,11e, '
                          'Qasa (J uO iter).',
                 'pdf_page': '197',
                 'ocr_flag': 'HEAVY but the frame words are legible and '
                             "unambiguous. NOTE: 'auspicious' here qualifies the "
                             'HOUSE (i.e. it is part of the predicate), not the '
                             'results — it is NOT a valence label, so polarity '
                             "stays 'none'. The predicate itself is not computable "
                             'and is FLAGGED, not resolved.'},
                {'predicate': 'weak',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'loss of wealth and kinsmen, wanderings in foreign '
                            'lands, danger from the king (government) and thieves, '
                            'quarrels with co-parceners, separation from maternal '
                            'uncle, distress to mother',
                 'source': 'sloka',
                 'quote': "6l-63. There'will be loss of wealih :,nd kinsmen' "
                          'wander-ings in foreign lands, danger from the king '
                          '(government) and threves, quariel$r '
                          ".with''c'o.:paiceners, 3€paration' frodl maternal "
                          'uncle, disfress ts: mo(hgr etc., if the-,Moog be wcak '
                          "or'associated with malefict ol,bg in the "
                          '6th-tn.,9,h..ot, rthe l2th from the Ascendant or the '
                          'lbrd of the Dasa (Jupiter).',
                 'pdf_page': '197',
                 'ocr_flag': "HEAVY. 'threves'=thieves; 'quariel$r "
                             ".with''c'o.:paiceners'='quarrels with co-parceners'; "
                             "'3€paration' frodl'='separation from'; 'wcak'=weak; "
                             "'malefict ol,bg'='malefics or be'."},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': "or'associated with malefict ol,bg in the "
                          '6th-tn.,9,h..ot, rthe l2th',
                 'pdf_page': '197',
                 'ocr_flag': "'malefict ol,bg'='malefics or be'."},
                {'predicate': 'in the 6th, the 8th or the 12th from the Ascendant',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'in the 6th-tn.,9,h..ot, rthe l2th from the Ascendant or '
                          'the lbrd of the Dasa (Jupiter).',
                 'pdf_page': '197',
                 'ocr_flag': "MATERIAL: 'the 6th-tn.,9,h..ot, rthe l2th' — the "
                             'middle house glyph is mangled and could be read as '
                             '9. Taken as 8th by analogy with the eleven other '
                             'dusthana clauses in ch.56, but FLAGGED as not '
                             'certain from the page.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (Jupiter)',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lbrd of the Dasa (Jupiter)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'from the Ascendant or the lbrd of the Dasa (Jupiter).',
                 'pdf_page': '197',
                 'ocr_flag': "'lbrd'=lord. Second limb of the same disjunction, "
                             'recorded separately so neither frame is dropped. '
                             'Same 8th-vs-9th uncertainty as the preceding '
                             'condition.'},
                {'predicate': 'lord of the 2nd or the 7th — maraka clause',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '64. Physical distress will be experienced if the lvloon '
                          "be ihi torc'br the 2hd or the'7th.'",
                 'pdf_page': '197',
                 'ocr_flag': "'lvloon'=Moon; 'ihi torc'br'='the lord of'; "
                             "'2hd'=2nd."}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'rahu'): {'verses': '72-80',
 'conditions': [{'predicate': 'in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'attachment to yoga, gain of wealth and grains during '
                            'the first five months, sovereignty over a village or '
                            'a country, meeting with a foreign king (high '
                            'dignitary), well being in the family, journeys to '
                            'distant lands, bathing in holy places',
                 'source': 'sloka',
                 'quote': '72-75. Effects like attachment to yoga, gain of wealth '
                          'and grains during the first five months, sovereignty '
                          'over a village or a country, meeting with a foreign '
                          'king (high dignitary), well being in the family, '
                          'journeys to distant lands, bathing in holy places, will '
                          'be derived in the Antardasa of Rahu in the Dasa of '
                          'Jupiter, if Rahu be in his sign of exaltation, in his '
                          'own sign, in his moolatrikona or be in kendra or '
                          'trikona from the Ascendant or be aspected by the lord '
                          'of kendra or be associated with or aspected by a '
                          'benefic',
                 'pdf_page': '199',
                 'ocr_flag': 'The sentence ends without a full stop in the OCR. '
                             "Note the time-qualified sub-result 'during the first "
                             "five months', with no stated mechanism for "
                             'subdividing the period.'},
                {'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if Rahu be in his sign of exaltation, in his own sign, '
                          'in his moolatrikona',
                 'pdf_page': '199',
                 'ocr_flag': 'The text assigns Rahu an exaltation, own sign and '
                             'moolatrikona without saying which they are; ch.56 '
                             'does not settle this.'},
                {'predicate': 'in his moolatrikona',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'in his moolatrikona or be in kendra or trikona from the '
                          'Ascendant',
                 'pdf_page': '199',
                 'ocr_flag': 'Moolatrikona sign for Rahu not stated here.'},
                {'predicate': 'in a kendra or trikona from the Ascendant',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or be in kendra or trikona from the Ascendant or be '
                          'aspected by the lord of kendra',
                 'pdf_page': '199',
                 'ocr_flag': ''},
                {'predicate': 'aspected by the lord of a kendra',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or be aspected by the lord of kendra or be associated '
                          'with or aspected by a benefic',
                 'pdf_page': '199',
                 'ocr_flag': "'the lord of kendra' — the text does not say kendra "
                             'reckoned FROM WHAT for the purpose of identifying '
                             'this lord. The sub-frame is unstated.'},
                {'predicate': 'associated with or aspected by a benefic',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or be associated with or aspected by a benefic',
                 'pdf_page': '199',
                 'ocr_flag': ''},
                {'predicate': 'associated with a malefic AND in the 8th or the '
                              '12th from the lord of the Dasa (Jupiter) — the 6th '
                              'is NOT listed',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of:tha Dasa (Jupiter) [from the '
                                'lord of the Dasa (Jupiter)]',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'danger from thieves, snakes, the king (government), '
                            'wounds, troubles in domestic affairs, antagonism with '
                            'co-borns and co-parceners, bad dreams, quarrels '
                            'without reason, danger from diseases',
                 'source': 'sloka',
                 'quote': '76-78. Danger from thieves, snakes, the king '
                          '(government), wounds, troubles in domestic affairs, '
                          "antagonism with co-borns and'copaiceners, bad dreams, "
                          "quarreli without'i€aS:'on ;danger from diseases ete., "
                          "will result if Rahu be associated with'a maicfic in the "
                          '8th or the l2th from the lord of:tha Dasa (Jupiter).',
                 'pdf_page': '199-200',
                 'ocr_flag': "'copaiceners'=co-parceners; 'quarreli "
                             "without'i€aS:'on'='quarrels without reason'; "
                             "'maicfic'=malefic; 'of:tha'='of the'. NOTE the "
                             'dusthana set is only 8th/12th — the 6th is absent, '
                             'as in Mars vv.69-71. This is a CONJUNCTION (malefic '
                             'association AND placement), not a disjunction.'},
                {'predicate': 'placed IN the 2nd or the 7th from the Ascendant — '
                              'maraka clause (occupancy, not lordship)',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '79-80. Therp,will be physical distlpss $."RahU,be in '
                          "thc 2nd or the 7th from the Ascendant. .'",
                 'pdf_page': '200',
                 'ocr_flag': "'Therp'=There; 'distlpss $.'='distress if'; "
                             "'thc'=the. IMPORTANT: this is the ONLY maraka clause "
                             'in ch.56 that (a) states OCCUPANCY rather than '
                             'lordship and (b) states a frame. Both features are '
                             'quotable from the printed page and are not OCR '
                             'artefacts.'}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'saturn'): {'verses': '8-19',
 'conditions': [{'predicate': 'in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of a kingdom (attainment of high position '
                            'in government), gain of clothes, ornaments, wealth, '
                            'conveyances, cattle and position, happiness from sons '
                            'and friends, gains specially of a blue coloured '
                            'horse, journey to the West, audience with the king '
                            'and receipt of wealth from him',
                 'source': 'sloka',
                 'quote': '8-li ]. Eflccts like acquisition of a kin-edom '
                          '(attainment ofhigh position in governmeut), ... will he '
                          'derived irr the Antardasa of Satum in the Dasa '
                          'ofJupiter, if Saturn be in his sign of exaltation, iu '
                          'his own sign,kendra or trikona endowed with strength.',
                 'pdf_page': '189',
                 'ocr_flag': "'Eflccts', 'kin-edom', 'governmeut', 'Satum', 'iu' — "
                             'routine OCR noise.'},
                {'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if Saturn be in his sign of exaltation, iu his own '
                          'sign,kendra or trikona endowed with strength.',
                 'pdf_page': '189',
                 'ocr_flag': ''},
                {'predicate': 'in a kendra or trikona — NO FRAME STATED',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if Saturn be in his sign of exaltation, iu his own '
                          'sign,kendra or trikona endowed with strength.',
                 'pdf_page': '189',
                 'ocr_flag': "CRITICAL: no 'from the Ascendant' and no 'from the "
                             "lord of the Dasa' appears anywhere in this sentence. "
                             'Frame recorded as unstated; do not infer.'},
                {'predicate': 'endowed with strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'kendra or trikona endowed with strength.',
                 'pdf_page': '189',
                 'ocr_flag': ''},
                {'predicate': 'in the 6th, the 8th or the 12th from the Ascendant',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'ir-* ,1. Asceltdant [from the Ascendant]',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'loss of wealth, affliction with fever, mental agony, '
                            'infliction of wounds to wife and children, '
                            'inauspicious events at home, loss of cattle and '
                            'employment, antagonism with kinsmen',
                 'source': 'sloka',
                 'quote': "12-14.Lossofwealth,afllictionwithfever,mentalagony' "
                          'inflictionofwoundstowifeandchildren,inauspicioustlvertsat '
                          'ito*", loss of cattle and employment, antagoriism wi"n '
                          '\'llinstneu\' "o *ttt be rer,ults if saturn be in the '
                          "6th, the 8th r''r the t2th ir-* ,1. Asceltdant, be "
                          "combust or be in an enei'ly's sign'",
                 'pdf_page': '190',
                 'ocr_flag': "HEAVY. Word-spacing collapsed; 'ir-* ,1. Asceltdant' "
                             "reconstructed as 'from the Ascendant'; "
                             '\'inauspicioustlvertsat ito*"\' = \'inauspicious '
                             "events at home'; 'enei'ly's' = enemy's."},
                {'predicate': 'combust',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': "be combust or be in an enei'ly's sign'",
                 'pdf_page': '190',
                 'ocr_flag': "'enei'ly's' = enemy's."},
                {'predicate': "in an enemy's sign",
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': "be combust or be in an enei'ly's sign'",
                 'pdf_page': '190',
                 'ocr_flag': "'enei'ly's' = enemy's."},
                {'predicate': 'in a kendra, trikona, the 11th or the 2nd from the '
                              'lord of the Dasa (Jupiter)',
                 'houses': '1,4,7,10,5,9,11,2',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (JuPiter)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of land, house, son and cattle, acquisition of '
                            'riches and property through the enemy',
                 'source': 'sloka',
                 'quote': 'l5-15*. There will be gain of larrd, house, son and '
                          'cattle\' acquisition of ,i.h"t andprop:rty through-the '
                          "enemy' etc'' ifl Saiurn be in kendra, trikbna, the llth "
                          "or the 2nd from the lord of the Dasa (JuPiter)'",
                 'pdf_page': '190',
                 'ocr_flag': '\'larrd\'=land; \'trikbna\'=trikona; \',i.h"t '
                             "andprop:rty'='riches and property'."},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (Jupiter)',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Jupiter)',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'loss of wealth, antagonistic relations with kinsmen, '
                            'obstacles in industrial ventures, pains in the body, '
                            'danger from the members of the family',
                 'source': 'sloka',
                 'quote': '16.lT.Effectslikclossofwealth,antagonisticrelations. '
                          'with kinsmen, obstacles ,n industrial ventures, pains '
                          "in the body' danger from the members of the family "
                          'etc., will be realised if Satirnbe in the 6th, the 8th '
                          'or the l2th from the lord of the Dasa (Jupiter) or be '
                          "associated with a malefic'",
                 'pdf_page': '190',
                 'ocr_flag': "'Satirnbe'='Saturn be'; word-spacing collapsed in "
                             'the first line.'},
                {'predicate': 'associated with a malefic',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': "or be associated with a malefic'",
                 'pdf_page': '190',
                 'ocr_flag': ''},
                {'predicate': 'lord of the 2nd or the 7th — maraka clause',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'fear of premature death',
                 'source': 'sloka',
                 'quote': '1g-t9. fhere will be fear of premature death, if Saturn '
                          'be lord of the 2nd or the 7th.',
                 'pdf_page': '190',
                 'ocr_flag': "'fhere'=There."}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'sun'): {'verses': '51-57',
 'conditions': [{'predicate': 'in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'gain of wealth, reverence, happiness and acquisition '
                            'of conveyances, clothes, ornaments etc., birth of '
                            'children, cordial relations with the king '
                            '(government), success in ventures',
                 'source': 'sloka',
                 'quote': '5l-53. Gain of wealth, reverence, happiness and '
                          'acquisition of cbnveyances, clothes. .ornaments etc., '
                          'birth of children, cordial relations with the king '
                          '(government), success in venturesn etc., will be the '
                          'auspicious results in the Antardasa of the Sun in the '
                          'Dasa of Jupiter, if the Sun be in his sign of '
                          'exaltation, in his own sign, in kendra, trikona, the '
                          '3rd, the llth or the 2nd from the Ascendant and be '
                          'endowed with strength.',
                 'pdf_page': '195-196',
                 'ocr_flag': "'cbnveyances'=conveyances; 'venturesn'=ventures."},
                {'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if the Sun be in his sign of exaltation, in his own '
                          'sign, in kendra, trikona, the 3rd, the llth or the 2nd '
                          'from the Ascendant and be endowed with strength.',
                 'pdf_page': '196',
                 'ocr_flag': ''},
                {'predicate': 'in a kendra, trikona, the 3rd, the 11th or the 2nd '
                              'from the Ascendant',
                 'houses': '1,4,7,10,5,9,3,11,2',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'in kendra, trikona, the 3rd, the llth or the 2nd from '
                          'the Ascendant and be endowed with strength.',
                 'pdf_page': '196',
                 'ocr_flag': 'This is the widest favourable house set in the '
                             'chapter (kendra + trikona + 3rd + 11th + 2nd).'},
                {'predicate': 'endowed with strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': "as above (same branch); joined by 'and', so a "
                            'REQUIRED conjunct',
                 'source': 'sloka',
                 'quote': 'and be endowed with strength.',
                 'pdf_page': '196',
                 'ocr_flag': ''},
                {'predicate': 'in the 6th, the 8th or the 12th from the Ascendant',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'nervous disorder, fever, laziness or reluctance in '
                            'the performance of good deeds, indulgence in sins, '
                            'antagonistic attitude towards all, separation from '
                            'kinsmen, distress without reasons',
                 'source': 'sloka',
                 'quote': "54-55+. Effects like nervous disorder, fever, 'laziness "
                          'or reluctance in the performance of good deeds; '
                          'indulgence in 8ins, antagonistic attitude towards all, '
                          'separation from kinsmen and distress without reasons, '
                          'will be experienced, if the Sun be in thc 6th, the 8th '
                          'or the 12th from the Ascendant or the lord of the Dasa '
                          '(Jufiter).',
                 'pdf_page': '196',
                 'ocr_flag': "'8ins'=sins; 'Jufiter'=Jupiter. This branch states "
                             'TWO frames disjunctively; recorded as two conditions '
                             'so neither is dropped. No valence word appears '
                             'despite the plainly unpleasant result list.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (Jupiter)',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lord of the Dasa (Jufiter)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'if the Sun be in thc 6th, the 8th or the 12th from the '
                          'Ascendant or the lord of the Dasa (Jufiter).',
                 'pdf_page': '196',
                 'ocr_flag': "'Jufiter'=Jupiter."},
                {'predicate': 'lord of the 2nd or the 7th — maraka clause',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '56-57. There will be physical distress if the Sun be '
                          'the lord of the 2nd or the 7th.',
                 'pdf_page': '196',
                 'ocr_flag': 'The sentence is scattered across several OCR lines '
                             "('There will be' / 'physical' / 'distress' / 'lord "
                             "of the 2nd or the 7th'); reconstruction is "
                             'confident.'}],
 'maraka': None,
 'remedy': None},
    ('jupiter', 'venus'): {'verses': '39-50',
 'conditions': [{'predicate': 'in a kendra, trikona or the 11th from the Ascendant',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of conveyances like palanquin, elephants '
                            'etc., gain of wealth by the beneficence of the king, '
                            'enjoyment, gain of blue and red articles, '
                            'extraordinary income from journeys to the East, well '
                            'being in the family, happiness from parents, devotion '
                            'to deities, construction of reservoirs, charities',
                 'source': 'sloka',
                 'quote': '39-43. Effects like acquisition of conveyances like '
                          'palan-quin, elephants etc., gain of wealth by the '
                          'beneficence of tn"xlng, ... will be derived in the '
                          'Antardasa ofVenus if he be in kendra, trikona, the llth '
                          'from the Ascendant or be in his own sign, and be '
                          'aspectcd by a benefic or benefics.',
                 'pdf_page': '194',
                 'ocr_flag': '\'tn"xlng\'=\'the king\'; \'aspectcd\'=aspected.'},
                {'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': 'or be in his own sign, and be aspectcd by a benefic or '
                          'benefics.',
                 'pdf_page': '194',
                 'ocr_flag': ''},
                {'predicate': 'aspected by a benefic or benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "as above (same branch); joined by 'and', so a "
                            'REQUIRED conjunct with whichever placement '
                            'alternative fires',
                 'source': 'sloka',
                 'quote': 'and be aspectcd by a benefic or benefics.',
                 'pdf_page': '194',
                 'ocr_flag': "'aspectcd'=aspected."},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              "the Dasa [text may also intend 'or the Ascendant']",
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa of Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'Evil',
                 'results': 'quarrels, antagonism with kinsmen, distress to wife '
                            'and children',
                 'source': 'sloka',
                 'quote': 'U-44t. Evil effects like quarrels, antagonism with '
                          'kinsmcn,distress to wife and children, wil be fett -ir '
                          'venus be in the 6th, the 8th or the t2th from the lord '
                          'of the Dasa of Ascendant ,or be in his sign of '
                          'debilitation .',
                 'pdf_page': '194-195',
                 'ocr_flag': "MATERIAL. 'from the lord of the Dasa of Ascendant' — "
                             "the 'of' before 'Ascendant' is almost certainly "
                             "'or', which would make this a two-frame disjunction "
                             'like Sun v.54 and Moon v.61. As printed it is '
                             "ambiguous; only 'from the lord of the Dasa' is "
                             'quotable with confidence, so that alone is recorded '
                             'and the possible second frame is FLAGGED, not '
                             "asserted. Also 'kinsmcn'=kinsmen; 'wil be "
                             "fett'='will be felt'; '-ir'=if."},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Evil',
                 'results': 'as above (same branch)',
                 'source': 'sloka',
                 'quote': ',or be in his sign of debilitation .',
                 'pdf_page': '195',
                 'ocr_flag': ''},
                {'predicate': 'associated with Saturn or Rahu or with both',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'quarrels, danger from the king, antagonism with the '
                            'wife, disputes with the father-in-law and brothers, '
                            'loss of wealth',
                 'source': 'sloka',
                 'quote': 'There will be quarrels, danger from the king, '
                          'antagonism with the wife, disputes with t-he '
                          'fathcr-in-law and brothers, loss of wealth etc., if '
                          'Vcnus be "associated with Saturn or Rahu or with both.',
                 'pdf_page': '195',
                 'ocr_flag': "'fathcr'=father; 'Vcnus'=Venus."},
                {'predicate': 'in a kendra, trikona or the 2nd from the lord of '
                              'the Dasa (Jupiter)',
                 'houses': '1,4,7,10,5,9,2',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from thc lord of thc Dasa (Jupiter)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of wealth, happiness from wife, meeting with the '
                            'king, increase in the number of children, conveyances '
                            'and cattle, enjoyment of music, society with men of '
                            'learning, availability of sweetish preparations, '
                            'giving help and assistance to kinsmen',
                 'source': 'sloka',
                 'quote': '4547tr. There will be gain of weatth, happiness from '
                          'wife, meeting with thc king, increase in the number of '
                          'childrcn,conveyances and cattle, enjoyment of music, '
                          'society with men of learning, availability of sweetish '
                          'preparations, giving hclpand assistanca to kinsmcn '
                          'etc., if Venus be in kendra, trikonaor the Znd from thc '
                          'lord of thc Dasa (Jupiter).',
                 'pdf_page': '195',
                 'ocr_flag': "'the Znd'='the 2nd'; 'weatth'=wealth; 'hclpand "
                             "assistanca'='help and assistance'."},
                {'predicate': 'lord of the 2nd or the 7th — maraka clause',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'loss of wealth, fear of premature death, antagonism '
                            'with wife',
                 'source': 'sloka',
                 'quote': '48-50. Loss of wealth, fear of premature death, '
                          'antagonism vith wife etc., will be experienci,l if '
                          'Venus be the lord of the2nd or thc 7th.',
                 'pdf_page': '195',
                 'ocr_flag': "'vith'=with; 'experienci,l'=experienced. Polarity "
                             "left 'none' per ch.34, which forbids mixing a maraka "
                             'verdict with a benefic/malefic nature, despite '
                             "'Loss' and 'death' appearing in the result list."}],
 'maraka': None,
 'remedy': None},
    ('ketu', 'jupiter'): {'verses': '51-60',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, or '
                              'associated with the lord of the Ascendant, the 9th '
                              'or the 10th, in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'increase in wealth and grains, beneficence of the '
                            'king, enthusiasm, gain of conveyances etc., '
                            'celebration like birth of a son at home, performance '
                            'of pious deeds, yajanas, conquest of the enemy, '
                            'enjoyments',
                 'source': 'sloka',
                 'quote': "5l-54. Ffl'ects like jncrease in wealth and grains, "
                          'bene.ficence of the king, enthusiasm, gain of '
                          'conveyances etc. celebration like birtli of a son at '
                          'horreo performance of piour deeds, yajanas, conquest of '
                          'the enemy and enjoyments, wili br dcrived in the '
                          'Antardasa of . Juplter in the Dasa of Ketu, il Jupiter '
                          'be in his sign of exaltation, in his own sign or bt '
                          'associated with the lord of the Ascendant, the 9th or '
                          'rhe l0tt in a kendra or trikona from the Ascendant.',
                 'pdf_page': '235',
                 'ocr_flag': "Right margin clipped throughout: 'Ffl'ects'=Effects, "
                             "'birtli'=birth, 'horreo'='home,', 'piour'=pious, "
                             "'wili br'='will be', 'il'=if, 'bt'=be, 'rhe "
                             "l0tt'='the 10th'. NOTE: unlike the Venus and Sun "
                             'opening branches, this one DOES state its frame '
                             'explicitly.'},
                {'predicate': 'in his sign of debilitation, or in the 6th, the 8th '
                              'or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'adverse',
                 'results': 'danger from thieves, snakes and wounds, destruction '
                            'of wealth, separation from wife and children, '
                            'physical distress etc.; some good effects may be felt '
                            'at the commencement of the Antardasa but only adverse '
                            'results later',
                 'source': 'sloka',
                 'quote': '55-56. Danger from thieves, snakes and wouncls, '
                          'destru.ction of wealth, separation from wife and '
                          'children. physical disttess etc., will be the results '
                          'if Jupirer be in his sign oI debilitation or be in the '
                          '6th, the gth or rhe l2th from the Ascendant. Though '
                          's,:me good effects may be felt at tb€ gommencement of '
                          "the Antardasa' there will be onlY adverse "
                          'results-later.',
                 'pdf_page': '235-236',
                 'ocr_flag': 'Split across the page break with a stray page number '
                             "'72' interleaved. 'wouncls'=wounds, "
                             "'disttess'=distress, 'Jupirer'=Jupiter, 'gth'=8th, "
                             "'s,:me'=some, 'tb€'=the, 'onlY'=only. STAGED: "
                             "explicitly 'adverse' but only LATER, with good "
                             'effects conceded at the commencement. One of the 5 '
                             'genuine branch-level valence labels.'},
                {'predicate': 'associated with a benefic in kendra, trikona, the '
                              '3rd or the 11th',
                 'houses': '1,4,7,10,5,9,3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Ketu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of many varieties of garments, ornaments by the '
                            'beneficence of the king, foreign journeys, taking '
                            'care of kinsmen, availability of decent food',
                 'source': 'sloka',
                 'quote': '57-58+. There will be gains of many varieties of '
                          "garments' ornaments by the beneficence of the king, "
                          'foreign journeys, taking "urc of kinsmen, availability '
                          "of decent food' if Jupiter be asJociated with a benefic "
                          'in kendra, trikona, the 3rd or the 1lth from the lord '
                          "of the Dasa (Ketu)'",
                 'pdf_page': '236',
                 'ocr_flag': 'Verse number \'57-58+\' = 57-58.5. \'"urc\'=care, '
                             "'asJociated'=associated. Frame explicit and clean."},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'fear of premature death',
                 'source': 'sloka',
                 'quote': "59-60. Fear of premature death w;ill be 'caused if "
                          'Jupiter be the lord of the 2nd or the 7th from the '
                          "Ascendant'",
                 'pdf_page': '236',
                 'ocr_flag': "'w;ill'=will; trailing apostrophes are OCR noise for "
                             'the full stop. Frame explicit.'}],
 'maraka': "59-60. Fear of premature death w;ill be 'caused if Jupiter be the lord "
           "of the 2nd or the 7th from the Ascendant' — frame EXPLICIT.",
 'remedy': 'The remedial measures to obtain relief from the above evil effects are '
           'Mrityunjaya Japa. recitation of Shiva Sahasra-nama. (PDFPAGE 236) — '
           'sits after BOTH branches; not a polarity marker.'},
    ('ketu', 'ketu'): {'verses': '1-6',
 'conditions': [{'predicate': 'in kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascen-[dant]',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'happiness from wife and children, recognition from '
                            'the king (government) but mental agony, gain of land, '
                            'village etc.',
                 'source': 'sloka',
                 'quote': 'l-2-$. Effects like happiness from wife and children, '
                          'rognition from the king (government) but mental agony, '
                          'gain land, village etc., will be derived in the '
                          'Antardasa of Ketu in own Dasa, if Ketu be in kendra or '
                          'trikona from the Ascen- rt or be associated with the '
                          'lord of thc .{ssgndsnt, or be ated to lords of the 9th, '
                          'the loth or tbe +rh.',
                 'pdf_page': '227',
                 'ocr_flag': 'Left margin cropped on every line; '
                             "'rognition'=recognition, 'Ascen-rt'=Ascendant, "
                             "'.{ssgndsnt'=Ascendant. Verse number 'l-2-$' = "
                             '1-2.5.'},
                {'predicate': 'associated with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': 'be associated with the lord of thc .{ssgndsnt',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as the kendra/trikona branch '
                            '(alternative disjunct of vv.1-2.5)',
                 'source': 'sloka',
                 'quote': 'or be associated with the lord of thc .{ssgndsnt',
                 'pdf_page': '227',
                 'ocr_flag': "'.{ssgndsnt' = Ascendant."},
                {'predicate': 'related to the lords of the 9th, the 10th or the '
                              '4th',
                 'houses': '9,10,4',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as the kendra/trikona branch '
                            '(alternative disjunct of vv.1-2.5)',
                 'source': 'sloka',
                 'quote': 'or be ated to lords of the 9th, the loth or tbe +rh.',
                 'pdf_page': '227',
                 'ocr_flag': "'ated'=related, 'loth'=10th, '+rh' most consistent "
                             'with 4th but not legible with certainty. NO frame '
                             "stated for these lordships — the 'from the "
                             "Ascendant' earlier in the verse attaches to the "
                             'kendra/trikona clause only.'},
                {'predicate': 'in his sign of debilitation AND in the 8th or the '
                              '12th AND alongwith a combust planet (conjunctive — '
                              "the text joins with 'and')",
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'heart disease, defamation, destruction of wealth and '
                            'cattle, distress to wife and children, instability of '
                            'mind etc.',
                 'source': 'sloka',
                 'quote': '3-4. Heart disease, defamation, destruction of wealth '
                          'and tle, distress to wife and children, instability of '
                          'mind etc., will the results, if Ketu be in his sign of '
                          'debilitation and be in 8th or the l2th from the '
                          'Ascendant alongwith a combust ret.',
                 'pdf_page': '227',
                 'ocr_flag': "Left margin cropped: 'tle'=cattle, 'ret'=planet, 'in "
                             "8th'=in the 8th. No valence word: 'heart disease' "
                             'etc. are named outcomes, not a branch label.'},
                {'predicate': 'related to the lords of the 2nd or the 7th, or in '
                              'the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger from diseases, great distress and separation '
                            'from kinsmen',
                 'source': 'sloka',
                 'quote': '5.6. There will be danger from diseases, greqt distress '
                          'and separation from kinsmen, if Kctu be related to lthe '
                          'lords ofthc2ndorthe?thor be in the 2nd or the 7thfrom '
                          'the Ascendant.',
                 'pdf_page': '228',
                 'ocr_flag': "Word-spacing collapsed: 'ofthc2ndorthe?thor'='of the "
                             "2nd or the 7th or'. 'greqt'=great, 'Kctu'=Ketu. The "
                             "frame 'from the Ascendant' is stated for the "
                             'PLACEMENT disjunct; whether it also governs the '
                             'LORDSHIP disjunct is not settled by the text. '
                             "Polarity word 'danger' occurs inside the outcome "
                             'list, not as a branch-level label.'}],
 'maraka': '5.6. There will be danger from diseases, greqt distress and separation '
           'from kinsmen, if Kctu be related to lthe lords ofthc2ndorthe?thor be '
           "in the 2nd or the 7thfrom the Ascendant. [= 'related to the lords of "
           "the 2nd or the 7th or be in the 2nd or the 7th from the Ascendant'] "
           'NOTE: this clause names danger from diseases and separation from '
           'kinsmen, NOT death; it is the 2nd/7th clause of this cell but does not '
           'itself pronounce a death verdict.',
 'remedy': 'The remedial measures to obtain relief from the above cvil effects are '
           'performance of Durga Saptashati Japa and Mrityunjaya Japa. (PDFPAGE '
           '228) — sits after BOTH branches; not a polarity marker.'},
    ('ketu', 'mars'): {'verses': '37-44',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, '
                              'associated with or aspected by the benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of land, village etc., increase in wealth '
                            'and cattle, laying out of a new garden, gain of '
                            'wealth by the beneficence of the king',
                 'source': 'sloka',
                 'quote': '37-39. Effects like acquisition of land, village etc., '
                          'increase in wealth and cattle, laying out of a new '
                          'garden, gain of wealth by the beneficenc: of the king, '
                          'wili be derived in the Antardasa of Mars in the Dasa of '
                          'Ketu, if Mars be in his sign of exaltation in his own '
                          'sign associated with or aspected by the benefics.',
                 'pdf_page': '233',
                 'ocr_flag': "'beneficenc:'=beneficence, 'wili'=will. Conjunctions "
                             'between the disjuncts are missing in the OCR '
                             "('exaltation in his own sign associated with') — "
                             'whether these are OR-ed or AND-ed is NOT settled by '
                             'the text as printed; the parallel with other cells '
                             'suggests OR but this is flagged, not resolved.'},
                {'predicate': 'related to the lords of the 9th or the 10th',
                 'houses': '9,10',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'definitely gain of land and enjoyment',
                 'source': 'sloka',
                 'quote': 'If Mars be related to the lords of the 9th or the l0th, '
                          'there will definitely be gain of land and enjoyment.',
                 'pdf_page': '233',
                 'ocr_flag': 'Clean. No frame stated for the lordships. Note the '
                             "intensifier 'definitely' — a confidence marker, not "
                             'a valence word.'},
                {'predicate': 'in kendra, trikona, the 3rd or the 11th',
                 'houses': '1,4,7,10,5,9,3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of ihe Dasa (Ketu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'recognition from the king, great popularity and '
                            'reputation, happiness from children and friends',
                 'source': 'sloka',
                 'quote': '40. There will be recognition from the . king, great '
                          'popularity and reputation and happiness from children '
                          'and friends, if Mars be in kendra, trikona, the 3rd or '
                          'the llth from the lord of ihe Dasa (Ketu).',
                 'pdf_page': '233',
                 'ocr_flag': "'ihe'=the. Frame explicit."},
                {'predicate': 'in the 8th, the 12th or the 2nd',
                 'houses': '8,12,2',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Ketu)',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'fear of death, disaster during a foreign journey, '
                            'diabetes, unnecessary troubles, danger from thieves '
                            "and the king, quarrels — but 'amidst evil effects "
                            "there will be some auspicious effects also'",
                 'source': 'sloka',
                 'quote': '4l-42. There will be fear of death, disaster during a '
                          'foreign journey, diabetes, unnecessary troubles, danger '
                          'from thieves and the king and quarrels if Mars be in '
                          'the 8th, the l2th or the 2nd from the lord of the Dasa '
                          '(Ketu). In the above circumstances amidst evil effects '
                          'there will be some auspicious effects also.',
                 'pdf_page': '233-234',
                 'ocr_flag': 'Clean. NOTE: this branch is SELF-CONTRADICTORY by '
                             "design — it carries both 'evil' and 'auspicious' as "
                             'branch-level labels in the same sentence and the '
                             'text states no tie-break. It should NOT be shipped '
                             'as a flat adverse verdict; it is the closest thing '
                             "in this cell to the 'contested' state. Uniquely "
                             'among from_dasa_lord adverse branches in this '
                             'chapter it uses 8/12/2 rather than 6/8/12.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'frbm the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'high fever, danger from poison, distress to wife, '
                            'mental agony, fear of premature death',
                 'source': 'sloka',
                 'quote': '43-44. High fever, danger from poison, distress to '
                          'wife,:ntal agony and fear of premature death, will be '
                          'the results, if Mars be the lord of the.2nd or the 7th '
                          'frbm the Ascendant.',
                 'pdf_page': '234',
                 'ocr_flag': "Left margin cropped: ':ntal'=mental. 'frbm'=from — "
                             "frame legible. Both 'danger' and 'death' occur in "
                             'the outcome list.'}],
 'maraka': '43-44. High fever, danger from poison, distress to wife, mental agony '
           'and fear of premature death, will be the results, if Mars be the lord '
           'of the.2nd or the 7th frbm the Ascendant. — frame EXPLICIT here, '
           'unlike the Ketu, Venus, Sun and Moon cells.',
 'remedy': 'By the beneficence of Mars there will be eajoyment and [ga]in of '
           'property, if as a remedial measure, a bull is given in [ch]arity. '
           '(PDFPAGE 234) — sits after BOTH branches; not a polarity marker. Note '
           'this remedy is phrased as a positive promise rather than as relief '
           'from evil effects.'},
    ('ketu', 'mercury'): {'verses': '69-79',
 'conditions': [{'predicate': 'in a kendra or trikona, and in his sign of '
                              'exaltation or in his own sign',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of a kingdom (attainment of a high '
                            'position in government), enjoyments, charities, gain '
                            'of wealth and land, birth of a son, celebration of '
                            'religious functions and functions like marriage '
                            'suddenly, well being in the family, gain of clothes, '
                            'ornaments etc.',
                 'source': 'sloka',
                 'quote': '69-71. Effects like acqui:;ition of a kingtlcw '
                          "(atlainment oi'a high position in governrnet:r), c,nj* "
                          ".'uents, cirarities, gain of wealih and land, birth of "
                          "a son, ';cLubration of religious functions and "
                          'functions like marriage sr.ddenly, well being in the '
                          'family, eain of clothes, ornaments etc., will be '
                          'derived in the Antardasa of Mercury in the Dasa of '
                          'Ketu, if Mercury be in a kefidra or trikona from the '
                          'Ascendant, be in his sigrr of exaltation or in his own '
                          'sign.',
                 'pdf_page': '238',
                 'ocr_flag': "Heavy speckle: 'acqui:;ition'=acquisition, "
                             "'kingtlcw'=kingdom, 'atlainment'=attainment, "
                             '"oi\'a"=\'of a\', \'governrnet:r\'=government, '
                             '"c,nj* .\'uents"=enjoyments, '
                             "'cirarities'=charities, "
                             '"\';cLubration"=celebration, \'sr.ddenly\'=suddenly, '
                             "'eain'=gain, 'kefidra'=kendra, 'sigrr'=sign. Frame "
                             'explicit and legible.'},
                {'predicate': 'associated with the lord of the 9th or the 10th',
                 'houses': '9,10',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'association with the men of learning, dawn of '
                            'fortune, listening to religious discourses',
                 'source': 'sloka',
                 'quote': '?2. There will be association with the men of learning, '
                          'dawn of fortune and listening to religious discourses, '
                          'if Mercury be associated with the lorC of the 9th or '
                          'the 10th.',
                 'pdf_page': '238',
                 'ocr_flag': "'?2'=72, 'lorC'=lord. NO frame stated for the "
                             'lordships — matches the same shape in the Ketu and '
                             'Mars cells.'},
                {'predicate': 'associated with Saturn, Mars or Rahu in the 6th, '
                              'the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Asccndant',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'antagonism with government officials, residing in '
                            "other people's houses, destruction of wealth, "
                            'clothes, conveyances and cattle; some beneficial '
                            'effects at the commencement, still better in the '
                            'middle, but inauspicious at the end',
                 'source': 'sloka',
                 'quote': '73-74t. Antagonisbr with government officials, residing '
                          "in other people's houses, destruction of wealth, "
                          'clothes, convey-ances auC cattle, will be the results '
                          'if Mercury be associa,ed [...] with Saturn, 1,4&rs or '
                          'Rahu in the 6th, the 8th or the 121fu flrun the '
                          'Asccndant. Tbere will be some beneficial effEcts of the '
                          'commencement of tbc Dasa, stllt bctter results in the '
                          'middle bu; inauspicious at the end.',
                 'pdf_page': '238-239',
                 'ocr_flag': 'Split across the page break. '
                             "'Antagonisbr'=Antagonism, 'auC'=and, "
                             "'associa,ed'=associated, '1,4&rs'=Mars, '121fu "
                             "flrun'='12th from', 'Asccndant'=Ascendant, 'effEcts "
                             "of the'='effects at the', 'stllt bctter'='still "
                             "better', 'bu;'=but. STAGED polarity: explicitly "
                             "'beneficial' at the start and 'inauspicious' at the "
                             'end within one branch. One of the 5 genuine '
                             'branch-level valence labels; must NOT be flattened '
                             'to a single adverse verdict.'},
                {'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of t\\e Dasa (iietu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'good health, happiness from son, opulence and glory, '
                            'availability of good food and clothes, unbounded '
                            'profit in business',
                 'source': 'sloka',
                 'quote': '"15-76. Thereu:il bc good healt!, happines from son\' '
                          "ooulence and gl'ory, availabiity of good food ahd "
                          'clothes arrd ulnotta proi, in business, if Mercury be '
                          "in a keudra' trikone or tho I lth from the lord of t\\e "
                          'Dasa (iietu)',
                 'pdf_page': '239',
                 'ocr_flag': 'Verse number \'\\"15-76\' = 75-76. \'Thereu:il '
                             "bc'='There will be', 'healt!'=health, "
                             "'happines'=happiness, 'ooulence'=opulence, "
                             '"gl\'ory"=glory, \'availabiity\'=availability, '
                             "'ahd'=and, 'arrd'=and, 'ulnotta proi,'='unbounded "
                             "profit', 'keudra'=kendra, 'trikone'=trikona, "
                             "'tho'=the, 't\\\\e Dasa (iietu)'='the Dasa (Ketu)'. "
                             'Frame legible despite heavy damage.'},
                {'predicate': 'weak, in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lorcl ot tl.lc Dasa {Keiu)',
                 'polarity': 'adverse',
                 'polarity_word': 'dangpr',
                 'results': 'distress, unhappiness and troubles to wife and '
                            'children and danger from the king (government) at the '
                            'commencement of the Antardasa; visits to sacred '
                            'places in the middle of the Dasa',
                 'source': 'sloka',
                 'quote': '7749. Distrcss, unhappineis and trrubles to wife and '
                          'chitdrgtr and dangpr from thc king (government) utay '
                          'tre cf,pod€d at the comffncctnttrt of tlre Antardasa if '
                          'Mercury be wcak in th.e 6th, the 8th or the l2th from '
                          'the lorcl ot tl.lc Dasa {Keiu). There will, however, bc '
                          'visits to sacred placesrn th"iniddle of thc Daea.',
                 'pdf_page': '239',
                 'ocr_flag': "Verse number '7749' = 77-79. 'Distrcss'=Distress, "
                             "'unhappineis'=unhappiness, 'trrubles'=troubles, "
                             "'chitdrgtr'=children, 'dangpr'=danger, 'utay tre "
                             "cf,pod€d'='may be expected', "
                             "'comffncctnttrt'=commencement, 'wcak'=weak, 'lorcl "
                             "ot tl.lc Dasa {Keiu)'='lord of the Dasa (Ketu)'. "
                             "Frame legible. Polarity word 'danger' (OCR 'dangpr') "
                             'is inside the outcome list and is EXPLICITLY '
                             'time-boxed to the commencement, with a favourable '
                             'middle conceded.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from thc Ascendanl',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'fear of premature death',
                 'source': 'sloka',
                 'quote': 'Fear of premature death will be causccl if Mercury be '
                          'tht brd of ttte 2nd or the ?th from thc Ascendanl.',
                 'pdf_page': '239',
                 'ocr_flag': "'causccl'=caused, 'tht brd'='the lord', 'ttte'=the, "
                             "'?th'=7th, 'Ascendanl'=Ascendant. Frame explicit."}],
 'maraka': 'Fear of premature death will be causccl if Mercury be tht brd of ttte '
           "2nd or the ?th from thc Ascendanl. (PDFPAGE 239) = 'if Mercury be the "
           "lord of the 2nd or the 7th from the Ascendant' — frame EXPLICIT.",
 'remedy': "T'i,: rcrnedial mcbsure to obtain relief from the above evil cffcrts, "
           "ir recitation of Vi;hnu Sahasranama. (PDFPAGE 239) = 'recitation of "
           "Vishnu Sahasranama' — sits after BOTH branches; not a polarity marker."},
    ('ketu', 'moon'): {'verses': '25-36',
 'conditions': [{'predicate': 'in her sign of exaltation, in her own sign, in '
                              'kendra, trikona, the 11th or the 2nd',
                 'houses': '1,4,7,10,5,9,11,2',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'recognition from the king (government), enthusiasm, '
                            'well being, enjoyments, acquisition of a house, lands '
                            'etc., abnormal gains of food, clothes, conveyances, '
                            'cattle etc., success in business, construction of '
                            'reservoirs etc., happiness to wife and children',
                 'source': 'sloka',
                 'quote': '25-28. Effects like recognition from the king '
                          '(government), cnthusiasm, well being, enjoyments, '
                          'acquisition of a house, lands etc., abnormal gains of '
                          'food, clothes, conveyances, cattle etc., sucess in '
                          'business, construction of reservoirs etc., and '
                          'happiness to wife and children will be derived in the '
                          'Antardasa of the Moon in the Dasa of Ketu, if the Moon '
                          'be in her sign of exaltation, in her own sign, in '
                          'kendra, trikona, the l lth or f,the 2nd, from the '
                          'Ascendant.',
                 'pdf_page': '231',
                 'ocr_flag': "'cnthusiasm'=enthusiasm, 'sucess'=success, "
                             "'f,the'=the. Frame explicit and clean."},
                {'predicate': 'the Moon be waxing (rider on the vv.25-28 branch)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'the beneficial results of the preceding branch will '
                            'be realised fully',
                 'source': 'sloka',
                 'quote': 'The beneficial results will be realised fulty if the '
                          'Moon be waxing.',
                 'pdf_page': '231',
                 'ocr_flag': "'fulty'=fully. This is one of only 5 genuine "
                             'branch-level valence labels in the chapter. It is a '
                             'MAGNITUDE rider on the preceding branch, not an '
                             'independent branch.'},
                {'predicate': 'in her sign of debilitation, or in the 6th, the 8th '
                              'or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from thsAsccndant',
                 'polarity': 'adverse',
                 'polarity_word': 'losses',
                 'results': 'unhappiness and mental agony, obstacles in ventures, '
                            'separation from parents, losses in business, '
                            'destruction of cattle etc.',
                 'source': 'sloka',
                 'quote': '29-30. Unhappiness and mental agony, obstacles '
                          "in'ventures, separation from parerits, losses in "
                          'business, destruction of cattle etc., will be caused if '
                          'the Moon be in her sign of debilitation or be in the '
                          '6th, the gth or the l2th from thsAsccndant.',
                 'pdf_page': '231-232',
                 'ocr_flag': "Split across the page break; 'parerits'=parents, "
                             "'gth'=8th, 'thsAsccndant'='the Ascendant'. Polarity "
                             "word 'losses' is inside the outcome list."},
                {'predicate': 'in kendra, trikona or the 11th AND endowed with '
                              'strength',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from tlie lord of the Dasa (Ketu)',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'acquisition of a cow or cows, land, agricultural '
                            'lands, meeting kinsmen and achievement of success '
                            "through them, increase in cow's milk and curd; "
                            'auspicious results at the commencement of the '
                            'Antardasa, cordial relations with the king in its '
                            'middle portion, and danger from the king / foreign '
                            'journey or journeys to distant places at its end',
                 'source': 'sloka',
                 'quote': '3l-3?. There will be acquisition of a cow or corvs, '
                          'land,agricultural lands, meeting kinsmen and '
                          "achievement of success through them, increase in col's "
                          'milk and curd, if the Moon beid kendra, trikona or the '
                          'l lth from tlie lord of the Dasa (Ketu) and be endowed '
                          'with strength. Thcre wilr be auspicious results. at the '
                          'connmencement of the Antardasa: cordial relations with '
                          'thc king (government) in its middie portion and danger '
                          'from thc king (government) foreign journey or journeys '
                          'to distant places at its end.',
                 'pdf_page': '232',
                 'ocr_flag': "Verse number '3l-3?' = 31-33. 'corvs'=cows, "
                             '"col\'s"=cow\'s, \'beid\'=\'be in\', \'Thcre '
                             "wilr'='There will', 'middie'=middle. STAGED "
                             "polarity: explicitly 'auspicious' at the start but "
                             "'danger from the king' at the end — the text does "
                             'not reduce this to one verdict, and it should not be '
                             'collapsed to a flat favourable.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Ketu)',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss',
                 'results': 'loss of wealth, anxiety, enmity with kinsmen, '
                            'distress to brother',
                 'source': 'sloka',
                 'quote': '34-36, Loss of wealth, anxiety, enmity with kinsmen and '
                          'distress to brother, will be the results, if the Moon '
                          'be in the 6th, the 8th or the l2th from the lord of the '
                          'Dasa (Ketu).',
                 'pdf_page': '232',
                 'ocr_flag': "Clean. Polarity word 'Loss' is inside the outcome "
                             'list.'},
                {'predicate': 'be the lord of the 2nd, the 7th or the 8th',
                 'houses': '2,7,8',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'fear of premature death',
                 'source': 'sloka',
                 'quote': 'If Moon be the lord of the 2nd, the 7th or the gth, '
                          'there will be fear of premature deatb.',
                 'pdf_page': '232',
                 'ocr_flag': "'gth'=8th (single-character read, consistent with "
                             "context but flagged), 'deatb'=death. NO frame "
                             'stated. UNIQUE inclusion of the 8th among the maraka '
                             'lordships in this chapter.'}],
 'maraka': 'If Moon be the lord of the 2nd, the 7th or the gth, there will be fear '
           "of premature deatb. (PDFPAGE 232) — 'gth'=8th. UNIQUE in this chapter: "
           'adds the 8th to the usual 2nd/7th pair. No frame stated.',
 'remedy': 'The remedial measures to obtain relief from the above effccts are '
           'recitation of mantras of the Moon anC giving in charity things '
           'connected with the Moon (See effects af Antar-dasas of the Moon in the '
           'Dasa of other planets). (PDFPAGE 232) — sits after BOTH branches; not '
           'a polarity marker.'},
    ('ketu', 'rahu'): {'verses': '45-50',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, in a '
                              "friend's sign, or in kendra, trikona, the 11th, the "
                              '[?] or the 2nd',
                 'houses': '1,4,7,10,5,9,11,?,2',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'increase of wealth and gain of wealth, grains, '
                            'cattle, lands, village from a yavana king (high '
                            'dignitary of a foreign country); some troubles at the '
                            'commencement of the Dasa but all will be well later',
                 'source': 'sloka',
                 'quote': '45-47. Effects like increase of wealth and gain of '
                          'wealth, ins, cattle, lands, village from a yavana ting '
                          'lhigh dignitary I foreign country) wilt be derived in '
                          'the Antardasa of Rahu he Dasa of Ketu, if Rahu be in '
                          "his sign of exaltation, in his r sign, in a friend's "
                          'sign or i.n kendra, trikona, the llth, the or the 2nd '
                          'from the Ascendant, There will be some troubles he '
                          'commencement of the Dasa but all will be well later.',
                 'pdf_page': '234',
                 'ocr_flag': 'SEVERE. (a) The whole paragraph has its left margin '
                             "cropped: 'ins'=grains, 'ting lhigh'='king (high', 'I "
                             "foreign'='of a foreign', 'he Dasa'='the Dasa', 'r "
                             "sign'='own sign', 'he commencement'='at the "
                             "commencement'. (b) A HOUSE NUMBER IS LOST between "
                             "'the llth, the' and 'or the 2nd' — the token fell "
                             'off the cropped left margin. Pattern-matching '
                             'against other cells would suggest the 3rd, but the '
                             'text as extracted does NOT say, and it is left '
                             'unresolved. (c) This gloss is printed AFTER that of '
                             "vv.48-50 in the OCR. 'all will be well later' is not "
                             'a listed valence word — polarity recorded as none.'},
                {'predicate': 'associated with a malefic in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from th Asceldant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'frequent urination, weakness in the body, cold fever, '
                            'danger from thieves, intermittent fever, opprobrium, '
                            'quarrels, diabetes, pain in stomach',
                 'source': 'sloka',
                 'quote': '48-50. Frequent urination, weakness in the body, cold '
                          'r, danger from thieves, intermittent fever, opprobrium, '
                          'rels, diabetes, pain in stomach, will be the results if '
                          'Rahu [...] be associated rvith a malefic in the 8th err '
                          'the tlili from th Asceldant.',
                 'pdf_page': '234-235',
                 'ocr_flag': 'The gloss is SPLIT across the OCR reordering: its '
                             'head sits on PDFPAGE 234 (before vv.45-47) and its '
                             "tail on PDFPAGE 235. Left margin cropped: 'cold "
                             "r'='cold fever', 'rels'=quarrels. 'err the "
                             "tlili'='or the 12th', 'th Asceldant'='the Ascendant' "
                             '— frame legible despite damage. Polarity word '
                             "'danger' is inside the outcome list."},
                {'predicate': 'in the 2nd or the 7th (placement, not lordship)',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascenciant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'distress and danger',
                 'source': 'sloka',
                 'quote': 'There will .br: disrress and Canger if Rahu be !n tli '
                          '2nd or the 7th from the Ascenciant.',
                 'pdf_page': '235',
                 'ocr_flag': "'.br:'=be, 'disrress'=distress, 'Canger'=danger, '!n "
                             "tli'='in the', 'Ascenciant'=Ascendant. Frame "
                             'legible. This cell has NO from_dasa_lord condition '
                             'anywhere — the shortest and thinnest cell in the '
                             'chapter.'}],
 'maraka': 'There will .br: disrress and Canger if Rahu be !n tli 2nd or the 7th '
           "from the Ascenciant. (PDFPAGE 235) = 'There will be distress and "
           "danger if Rahu be in the 2nd or the 7th from the Ascendant.' NOTE: "
           'this is a PLACEMENT test (Rahu in the 2nd/7th), NOT a lordship test — '
           'and Rahu owns no sign in the classical scheme. It names distress and '
           'danger, not death. The Rahu cell contains no maraka-lordship clause at '
           'all.',
 'remedy': 'The remedial measure to obtain rehei fron tle above evi effects, is '
           "Durga Saptashati Patlra. (PDFPAGE 235) = 'Durga Saptashati Patha' — "
           'sits after BOTH branches; not a polarity marker.'},
    ('ketu', 'saturn'): {'verses': '61-68 (v.66 has NO English gloss anywhere in the chapter)',
 'conditions': [{'predicate': 'deprived of strength and dignity',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'distress to self and kinsmen, agony, increase in '
                            'cattle wealth, loss of wealth as a result of '
                            'imposition of fines by government, resignation from '
                            'the existing post, journeys to foreign lands, danger '
                            'of thieves during travelling',
                 'source': 'sloka',
                 'quote': "6l-62+. Effects like distress to self and kinsmen' "
                          "agony' increase in cattle wealth, loss of wealth as a "
                          'result of imposition of fines by government, '
                          "resignation from the existing post' journeys to foreign "
                          'lands, and danger of thieves during travelling, will be '
                          'derived in the Antardasa of saturn in theDasa of Ketu, '
                          'if Saturn be deprived of strength and dignitn',
                 'pdf_page': '236-237',
                 'ocr_flag': "Verse number '6l-62+' = 61-62.5. Split across the "
                             "page break. 'dignitn'=dignity, 'theDasa'='the Dasa'. "
                             'NOTE this cell is UNUSUAL: its opening branch is the '
                             'ADVERSE one (weak Saturn), where every other cell in '
                             'the chapter opens with the favourable branch. Also '
                             "note the result list is internally mixed — 'increase "
                             "in cattle wealth' sits among losses. Polarity words "
                             "'loss' and 'danger' are inside the outcome list."},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'loss of wealth and lethargy',
                 'source': 'sloka',
                 'quote': 'Therq will be loss of wealtb and lethargy, if Saturn Ue '
                          'in\' ti"8th or the l2th from the Ascendant.',
                 'pdf_page': '237',
                 'ocr_flag': '\'Therq\'=There, \'wealtb\'=wealth, "Ue in\' '
                             'ti\\"8th"=\'be in the 8th\'. Frame legible.'},
                {'predicate': 'in trikona in Pisces, in Libra (his sign of '
                              'exaltation), in his own sign, in an auspicious '
                              'Navamsa, or associated with a benefic in kendra, '
                              'trikona or the 3rd',
                 'houses': '1,4,7,10,5,9,3',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'success in all ventures, happiness from the employer, '
                            'comforts during journeys, increase in happiness and '
                            "property in one's own village, audience with the king "
                            '(visits to high dignitaries) etc.',
                 'source': 'sloka',
                 'quote': '63-65. Success in all ventures, happiuessfrom the '
                          'employer,comforts during journeys, increase in '
                          'happiness and p*p"rty in one\'sown vilrage, '
                          "budience'with the king (visits to higirdignitaries), "
                          'etc., will be the results, if Saturn be in trikoo" '
                          'lnPisces, in Libra (his sign of exaltation), in his own '
                          ',ign oibe in an auspicious Navamsa or be associated '
                          'with a bJneficin kendra, trikona or the 3rd from the '
                          'Ascendant.',
                 'pdf_page': '237',
                 'ocr_flag': 'Printed AFTER vv.67-68 in the OCR. Spaces lost: '
                             "'happiuessfrom'='happiness from', "
                             '\'p*p\\"rty\'=property, "one\'sown vilrage"="one\'s '
                             'own village", "budience\'with"=\'audience with\', '
                             "'higirdignitaries'='high dignitaries', "
                             '\'trikoo\\" lnPisces\'=\'trikona in Pisces\', ",ign '
                             'oibe"=\'sign or be\', \'bJneficin\'=\'benefic in\'. '
                             "POLARITY TRAP AVOIDED: 'auspicious' here qualifies "
                             'the Navamsa (a CONDITION), not the result — it is '
                             'NOT a branch-level valence label, so polarity is '
                             "recorded as none. 'in trikona in Pisces' is "
                             'semantically unresolved (see gaps).'},
                {'predicate': 'Saturn in Libra, Pisces, Sagittarius, Capricorn or '
                              'Aquarius in the Ascendant gives Rajayoga',
                 'houses': '1',
                 'frame': 'from_lagna',
                 'frame_quote': 'in the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Rajayoga',
                 'source': 'note',
                 'quote': 'Nottis : According to Brihat lataka Saturn in Libra, '
                          'pisces, Sagittarius, Capricoin and Aquarius in the '
                          'Ascendant gives Rajayoga.',
                 'pdf_page': '237',
                 'ocr_flag': "'Nottis'=Notes, 'lataka'=Jataka, "
                             "'Capricoin'=Capricorn. THIS IS SANTHANAM'S NOTE, NOT "
                             'MULA — it cites Brihat Jataka, a different text, and '
                             'must never be shipped as a BPHS rule. It is the ONLY '
                             'note in the entire chapter.'},
                {'predicate': 'associated with a malefic, in the 6th, 8th or the '
                              '12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the Iord of the Dasa (Ketu)',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'physical distress, agony, obstacles in ventures, '
                            'lethargy, defamation, death of parents',
                 'source': 'sloka',
                 'quote': '67-68. There will be physical distress, agonlr, '
                          'obstacles in ventures, lethargy, defamation, death of '
                          'parents, if Saturn be associated with a malefic, in the '
                          '6th, 8th or the 12th from the Iord of the Dasa (Ketu).',
                 'pdf_page': '237',
                 'ocr_flag': "Printed BEFORE vv.63-65 in the OCR. 'agonlr'=agony. "
                             "Frame explicit and clean. Polarity word 'death' is "
                             "inside the outcome list ('death of parents') and "
                             'refers to the PARENTS, not the native — it must not '
                             'be routed to a maraka verdict.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'fear of premature death may be expected',
                 'source': 'sloka',
                 'quote': 'Fear of premature death may be expected if Saturn be '
                          'the loril of the 2nd or 7th from the Ascendant.',
                 'pdf_page': '237',
                 'ocr_flag': "'loril'=lord. Frame explicit. Note the hedge 'may be "
                             "expected' — weaker than the flat 'will be caused' "
                             'used in the Jupiter and Mercury cells; the text does '
                             'not say whether this hedge is meaningful.'}],
 'maraka': 'Fear of premature death may be expected if Saturn be the loril of the '
           '2nd or 7th from the Ascendant. (PDFPAGE 237) — frame EXPLICIT. '
           "'loril'=lord.",
 'remedy': 'The remedial measures to obtain relief from the ahove evil effects are '
           'performance of Havana with sesamum seeds (lav) and giving a black cow '
           'or female buffalo in charity. (PDFPAGE 238) — sits after BOTH '
           'branches; not a polarity marker.'},
    ('ketu', 'sun'): {'verses': '16-24',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, or '
                              'associated with or aspected by a benefic, in '
                              'kendra, trikona or the 11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of wealth, beneficence of the king, performance '
                            'of pious deeds and fulfilment of all ambitions',
                 'source': 'sloka',
                 'quote': 't6-17. The effects like gains of wealth, beneficence of '
                          'the king, performance of pious deeds and fulfilment of '
                          "all ambitions' will bc derived in the Antardasa of the "
                          'Sun in the Dasa of Ketu. If the Sun be in his sign of '
                          'exaltation, in his own signor be associated gr aspected '
                          'by a benefic. in kendra, trikoiaor the 1lth.',
                 'pdf_page': '229-230',
                 'ocr_flag': "CRITICAL: 'in kendra, trikoia or the 1lth' carries "
                             "NO frame — 'from the Ascendant' does not appear in "
                             'vv.16-17. Second of the two high-traffic unstated '
                             "opening branches in this chapter. 'trikoia'=trikona, "
                             "'gr'=or, 'bc'=be. Note the sentence break before 'If "
                             "the Sun' is an OCR artefact; the condition governs "
                             'the preceding result list.'},
                {'predicate': 'associated with a malefic or malefics, in the 8th '
                              'or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'danger from the king (government), separation from '
                            'parents, journeys to foreign lands, distress from '
                            'thieves, snakes and poison, punishment by government, '
                            'antagonism with the friends, sorrows, danger from '
                            'fever etc.',
                 'source': 'sloka',
                 'quote': '18-19+. Danger from the king (government), '
                          'separationrrom parents, journeys to foreign lands, '
                          'destress from thieves,tlul": and poison, punishment by '
                          'jovernment, antagonismwith- the friends, sorrows, '
                          'danger from-fever etc., rvill be theresults if tbe Sun '
                          'be associated with a malefic or malefics, inthe 8th or '
                          'the l2th from the Ascendant.',
                 'pdf_page': '230',
                 'ocr_flag': 'Line-wrap spaces lost throughout. '
                             "'separationrrom'='separation from', "
                             '\'destress\'=distress, \'tlul":\'= most consistent '
                             "with 'snakes' but NOT legible — flagged, not "
                             "resolved. 'jovernment'=government. Verse number "
                             "'18-19+' = 18-19.5."},
                {'predicate': 'in kendra, trikona, the 2nd or the 11th',
                 'houses': '1,4,7,10,5,9,2,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from thi: Dasa (tcctu j',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical fitness, gain of wealth, birth of a son, '
                            'success in performance of pious deeds, headship of a '
                            'small village etc.',
                 'source': 'sloka',
                 'quote': '20-21. There will be physical fitness, gain of '
                          'wealth,birth of a son, success in performance of pious '
                          'deeds, headshipof a small village etc., if the Sun be '
                          'in kendra, trikona, tG 2nd or the I lth from the lord '
                          'of thi: Dasa (tcctu j.',
                 'pdf_page': '230',
                 'ocr_flag': "'tG'=the, 'thi: Dasa (tcctu j'='the Dasa (Ketu)'. "
                             'Frame legible despite damage. Note this branch '
                             'uniquely uses the 2nd (not the 3rd) alongside '
                             'kendra/trikona/11th.'},
                {'predicate': 'associated with evil planets in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the )asa (Ketu)',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'obstacles in availability of food, fears, loss of '
                            'wealth and cattle; distress at the commencement of '
                            'the Antardasa with some mitigation at its end',
                 'source': 'sloka',
                 'quote': '2L24. Obstacles in availabjlity of food, fears, loss '
                          "of'ealth and cattle, will be the results if the sun be "
                          "associated''ith e'il planets in the 8th or the l2th "
                          'from the lord of the)asa (Ketu). There will be distress '
                          'at the commencement of the Antardasa with some '
                          'mitigation of its end.',
                 'pdf_page': '230-231',
                 'ocr_flag': 'Left margin cropped across the page break: '
                             '\'2L24\'=22-24, "loss of\'ealth"=\'loss of wealth\', '
                             '"\'\'ith e\'il"=\'with evil\', \'the)asa\'=\'the '
                             "Dasa'. Polarity word 'loss' is inside the outcome "
                             'list. The staged rider (distress at start, '
                             'mitigation at end) is a timing qualifier, not a '
                             'second branch.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'fear of premature death',
                 'source': 'sloka',
                 'quote': "There will be fear ofpremature death ifthe Sun be' the "
                          'lord of the 2nd or the 7th.',
                 'pdf_page': '231',
                 'ocr_flag': "'ofpremature'/'ifthe' — spaces lost. NO frame stated "
                             'for the lordship.'}],
 'maraka': "There will be fear ofpremature death ifthe Sun be' the lord of the 2nd "
           'or the 7th. (PDFPAGE 231) — no frame stated for the lordship.',
 'remedy': 'The remedial measure to obtain relief from the above cvileffects and '
           'to regain comforts.by thebeneficenceofthe Sun, is to give a cow and '
           'gold in charity. (PDFPAGE 231) — sits after BOTH branches; not a '
           'polarity marker.'},
    ('ketu', 'venus'): {'verses': '7-15',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, or '
                              'associated with the lord of the 10th in a kendra or '
                              'trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'beneficence from the king, good fortune, gain of '
                            'clothes etc., recovery of lost kingdom (reinstatement '
                            'in a high position in government), comforts of '
                            'conveyances etc., visits to sacred shrines, gain of '
                            'lands and villages by the beneficence of the king',
                 'source': 'sloka',
                 'quote': '7-9|. Efrects likebeneficence from the king, good '
                          'fortune, gein of clotheS etc., recovery of lost kingdom '
                          '(reinstatement in a high position in government), '
                          'comforts of conveyances etc., visits to sacred shrines, '
                          'gain of lands and villages by the bene-fiencc of the '
                          'king (government) witl be derived in the Antar-dasa of '
                          'Venus in the Dasa of Ketu, if Venus be in his sign of '
                          'exaltation, in his own sign or bs associated with the '
                          'lord of the l0th in a kendra or trikona and there will '
                          'be dawn of fortune if in such position he is associated '
                          'with the lord of the 9th also.',
                 'pdf_page': '228',
                 'ocr_flag': "CRITICAL: 'in a kendra or trikona' carries NO frame "
                             "— the words 'from the Ascendant' do not appear "
                             "anywhere in vv.7-9.5. This is the cell's opening "
                             'favourable branch, i.e. the one a real chart most '
                             'often lands on. Frame recorded as unstated; do NOT '
                             "infer lagna. 'Efrects'=Effects, 'gein'=gain, "
                             "'bene-fiencc'=beneficence, 'bs'=be."},
                {'predicate': 'associated with the lord of the 9th also, while in '
                              'the above position',
                 'houses': '9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'dawn of fortune (an additive rider on the vv.7-9.5 '
                            'branch)',
                 'source': 'sloka',
                 'quote': 'and there will be dawn of fortune if in such position '
                          'he is associated with the lord of the 9th also.',
                 'pdf_page': '228',
                 'ocr_flag': 'Rider clause, conditional on the preceding branch '
                             'already firing. No frame stated for the '
                             '9th-lordship.'},
                {'predicate': 'in kendra, trikona, the 3rd or the 11th',
                 'houses': '1,4,7,10,5,9,3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from tbe lorr: ol the i-)asa (Keirr)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'sound health, well being in the family, gains of good '
                            'food and conveyances etc.',
                 'source': 'sloka',
                 'quote': 'lGll. Sound health, well being in the family, gains of '
                          'good food and conveyances etc., will be the results, if '
                          'Venus be in kentjra, trikona, the 3rd or ths llth from '
                          'tbe lorr: ol the i-)asa (Keirr).',
                 'pdf_page': '228-229',
                 'ocr_flag': "Verse number 'lGll' = 10-11. Gloss badly mangled "
                             "across a page break: 'kentjra'=kendra, 'ths'=the, "
                             "'lorr: ol the i-)asa (Keirr)'='lord of the Dasa "
                             "(Ketu)'. Frame is legible despite damage."},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Ketu)',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'quarrels without any cause, loss of wealth, distress '
                            'to cattle',
                 'source': 'sloka',
                 'quote': "12-14. There will be quarrels without any cause' loss "
                          'of wealth, distress to cattle if Venus be in the 6th, '
                          'the Sth or the 12th from the lord of the Dasa (Ketu).',
                 'pdf_page': '229',
                 'ocr_flag': "'Sth'=8th. Polarity word 'loss' occurs inside the "
                             'outcome list, not as a branch-level label.'},
                {'predicate': 'in his sign of debilitation, or associated with a '
                              'debilitated planet, or in the 6th or the 8th',
                 'houses': '6,8',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'quarrels with kinsmen, headache, eye troubles, heart '
                            'disease, defamation, loss of wealth and distress to '
                            'cattle and wife',
                 'source': 'sloka',
                 'quote': 'If Venus be in his sign of debilitation or be '
                          'associated with a debilitated planet, or be in the 6th '
                          'or the 8th from the Ascendant, there will be quarrels '
                          'with kinsmen, headache, eye troubies, heart disease, '
                          "defamation' loss of wealth and distress to cattle and "
                          'wife.',
                 'pdf_page': '229',
                 'ocr_flag': "'troubies'=troubles. Note this branch uses 6th/8th "
                             'only (no 12th), unlike the from_dasa_lord branch '
                             'above which uses 6/8/12.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress and mental agony',
                 'source': 'sloka',
                 'quote': '15. Physical distress and mental agony will be caused '
                          'if Venus be the lord of the 2nd or the 7th.',
                 'pdf_page': '229',
                 'ocr_flag': 'Clean OCR. NO frame stated — contrast Mars vv.43-44, '
                             'Jupiter vv.59-60, Saturn vv.67-68 and Mercury '
                             "vv.77-79, which all say 'from the Ascendant' for the "
                             'same lordship test. No valence word: '
                             "'distress'/'agony' are not on the valence list."}],
 'maraka': '15. Physical distress and mental agony will be caused if Venus be the '
           'lord of the 2nd or the 7th. NOTE: no frame stated for the lordship, '
           'and this clause names physical distress/mental agony, NOT death — '
           'unlike the Sun, Moon, Mars, Jupiter, Saturn and Mercury cells, which '
           "all say 'fear of premature death'.",
 'remedy': 'The remedial measures to obtain relief fronn tle abc cvil effects, are '
           'performance of Durga Patha and giving a taw.coloured cow or female '
           'buffalo in charity. (PDFPAGE 229) — sits after BOTH branches; not a '
           'polarity marker.'},
    ('mars', 'jupiter'): {'verses': '15-22',
 'conditions': [{'predicate': 'in the 9th, the 5th, a kendra, the 11th or the 2nd '
                              'from the Ascendant',
                 'houses': '9,5,kendra,11,2',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'good reputation and renown, honours by government, '
                            'increase in wealth and grains, happiness at home, '
                            'gain of property, happiness from wife and children '
                            'etc.',
                 'source': 'sloka',
                 'quote': '15-16- Effects like good re;rtation and renown, honours '
                          "by government,' increase in wealth and grains, "
                          'happiness at hom€, gain of property, happitress from '
                          'wife and chiltlren ets., will be realised in the '
                          'Antardasa of Jupiter in the Dasa of Mars, if Jupiter be '
                          'in the 9th, the 5th, kendra, the llth or the 2nd from '
                          'the Ascendant, or be in his exalted or own Navamsa.',
                 'pdf_page': '163',
                 'ocr_flag': "'re;rtation'=reputation, 'happitress'=happiness, "
                             "'chiltlren ets.'=children etc."},
                {'predicate': 'in his exalted or own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be in his exalted or own Navamsa.',
                 'pdf_page': '163',
                 'ocr_flag': 'none'},
                {'predicate': 'in a kendra, trikona or the 11th from the lord of '
                              'the Dasa (Mars)',
                 'houses': 'kendra,trikona,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the ord of the Dasa (Mars)',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'acquisition of a house, land, well being, gain of '
                            'property, sound health, good reputation, gains of '
                            'cattle, success in business, happiness to wife and '
                            'children, reverence from government, gain of wealth '
                            'etc.',
                 'source': 'sloka',
                 'quote': 'll-lgt. Acquisition of a house, land, well being, gain '
                          'lf property, sound health, good reputation, gains of '
                          'cattle, ruccess in business, happiness to wife and '
                          'children, reverence iom government, gaiil of wealth '
                          'etc., will be beneficial :ffects, if Jupiter be in '
                          'kendra, trikona or the llth from the ord of the Dasa '
                          '(Mars), or be associated with the lord of the )th, the '
                          'l0th, the 4th or the Ascendant or being a benefic '
                          'rlavamsa etc.',
                 'pdf_page': '164',
                 'ocr_flag': 'SEVERE left-margin loss on pdf 164 — leading letters '
                             "stripped ('ll-lgt.'=17-19½, 'lf property'=of "
                             "property, ':ffects'=effects, 'ord of the Dasa'=lord "
                             "of the Dasa, ')th'=9th, 'rlavamsa'=Navamsa). Frame "
                             'words survive legibly.'},
                {'predicate': 'associated with the lord of the 9th, the 10th, the '
                              '4th or the Ascendant, or being in a benefic Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be associated with the lord of the )th, the l0th, '
                          'the 4th or the Ascendant or being a benefic rlavamsa '
                          'etc.',
                 'pdf_page': '164',
                 'ocr_flag': "')th' read as 9th — UNCERTAIN, could be 5th; margin "
                             'loss'},
                {'predicate': 'in the 5th, the 8th or the 12th',
                 'houses': '5,8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'danger from thieves, snakes, wrath of the king '
                            '(government), bilious diseases, oppression by '
                            'goblins, loss of servants and co-borns',
                 'source': 'sloka',
                 'quote': '20-22. Danger from thieves, snakes, wrath of the king '
                          "'government), bilious diseases, oppression by goblins "
                          "(fr6)' loss rf servants and co-forns, will be evil "
                          'effects, if Jupiter be in the 5th, the 8th or the l2th, '
                          'or be in his sign of debilitation, be msociated with or '
                          "aspected by rialefics or be otherwise weak'",
                 'pdf_page': '164',
                 'ocr_flag': "'the 5th' is PRINTED as 5th but the parallel "
                             'dusthana formula everywhere else in this chapter is '
                             "6/8/12 — possible OCR of '6th'. FLAGGED, not "
                             "silently corrected. Also 'co-forns'=co-borns, "
                             "'msociated'=associated, 'rialefics'=malefics."},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be in his sign of debilitation',
                 'pdf_page': '164',
                 'ocr_flag': 'none'},
                {'predicate': 'associated with or aspected by malefics, or '
                              'otherwise weak',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'be msociated with or aspected by rialefics or be '
                          "otherwise weak'",
                 'pdf_page': '164',
                 'ocr_flag': "'msociated', 'rialefics'"},
                {'predicate': 'Jupiter is lord of the 2nd',
                 'houses': '2',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'suffering from fever or danger of premature death',
                 'source': 'sloka',
                 'quote': 'Ihere will be suffering from fever or danger of '
                          'prenrature death if Jupiter be the lord of the 2nd.',
                 'pdf_page': '164',
                 'ocr_flag': "'Ihere'=There, 'prenrature'=premature. NOTE: only "
                             'the 2nd is named — the 7th is NOT mentioned, unlike '
                             'every other cell in this chapter.'}],
 'maraka': 'Ihere will be suffering from fever or danger of prenrature death if '
           'Jupiter be the lord of the 2nd. — NOTE: the 7th is absent here; the '
           'text names ONLY the 2nd for Jupiter.',
 'remedy': 'The remedial measure to be adopted to combat the rbove evil effects is '
           'recitation of Shiva Sahasranam (frtl e6e nw) (pdf 164)'},
    ('mars', 'ketu'): {'verses': '48-54',
 'conditions': [{'predicate': 'in a kendra, trikona, the 3rd or the 11th',
                 'houses': 'kendra,trikona,3,11',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the Ascendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'beneficence of the king (government), gain of wealth, '
                            'little gains of land at the commencement of the Dasa '
                            'and substantial later, birth of a son, conferment of '
                            'authority by government, gain of cattle etc.',
                 'source': 'sloka',
                 'quote': "4849+. Beneficence of the king (government)' gain of "
                          'wealth, Iittle gains of land at the commencement of the '
                          "Dasa and substantial later, birth of a son' confernment "
                          "of authority by gou.rn-ent, gain of cattle, etc', will "
                          'be the results in the Antirdusa of Ketu in the Dasa of '
                          'Mars, if Ketu be in kendra, trikona, the 3rd or the '
                          '1lth (from the Ascendant) or be associaied with or '
                          "aspected by benefics'",
                 'pdf_page': '168-169',
                 'ocr_flag': "'gou.rn-ent'=government, 'Antirdusa'=Antardasa, "
                             "'associaied'=associated; apostrophes substituted for "
                             'commas throughout. FRAME CAVEAT: the frame appears '
                             'ONLY in round brackets — translator-supplied gloss, '
                             'not words of the sloka. Low-confidence from_lagna.'},
                {'predicate': 'associated with or aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': "or be associaied with or aspected by benefics'",
                 'pdf_page': '169',
                 'ocr_flag': "'associaied'"},
                {'predicate': 'Ketu is a yogakaraka and is endowed with strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'birth of a son, increase in reputation, beneficence '
                            'of Goddess Lakshmi, gains of wealth from employees, '
                            'attainment of the position of a commander of army, '
                            'friendship with the king (cordial relations with high '
                            'government officials), performance of oblations, '
                            'gains of clothes and ornaments etc.',
                 'source': 'sloka',
                 'quote': "50-511. Birth of a son' increase in reputation, "
                          'beneficence of Goddess Ldkshmi, gains of wealth from '
                          "employees' attain-ment of the position of a commander "
                          'of army, friendship with the king (cordial relations '
                          "with high government officials)' performance of "
                          'oblations, gains of clothes and ornaments, etc\' t"itt '
                          'U" the.beneficial effects, if Ketu be a yogakaraka and '
                          'be endowed with strength.',
                 'pdf_page': '169',
                 'ocr_flag': '\'Ldkshmi\'=Lakshmi, \'t"itt U" the.beneficial '
                             "effects'=will be the beneficial effects. Verse order "
                             'is SCRAMBLED on pdf 169: the 52-54 translation block '
                             'is printed ABOVE the 50-51½ block in the OCR flow.'},
                {'predicate': 'Ketu assumes the role of a yogakaraka if he is '
                              'associated with a yogakaraka planet (lord of a '
                              'kendra and trikona)',
                 'houses': 'kendra,trikona',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "defines 'yogakaraka' for the preceding branch",
                 'source': 'note',
                 'quote': 'Notes : Ketu assumes the role of a yogakaraka if he is '
                          'associated with a yogakaraka planet (lord of a kendra '
                          'and trikona).',
                 'pdf_page': '169',
                 'ocr_flag': 'the note is split across the OCR page — its opening '
                             "('Notes : Ketu assumes the') appears mid-column "
                             'above the 52-54 block, its continuation below. '
                             "SANTHANAM'S NOTE, not mula. The sloka itself never "
                             'defines yogakaraka.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (Mars)',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Mars)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'quarrels, tooth trouble, distress from thieves and '
                            'tigers, fever, dysentry, leprosy and distress to wife '
                            'and children etc.',
                 'source': 'sloka',
                 'quote': '52-54. Effects like quarrels, tooth trouble, distress '
                          'from thieves and tigefs, fever, dysentry, leprosy and '
                          'distress to wjfe and children, etc., will be '
                          'experienced if Ketu be in the 6th, the 8th or the l2th '
                          'from the lord of the Dasa (Mars).',
                 'pdf_page': '169',
                 'ocr_flag': "'tigefs'=tigers, 'wjfe'=wife"},
                {'predicate': 'in the 2nd or the 7th from the Ascendant',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'diseases, disgrace, agony and loss of wealth',
                 'source': 'sloka',
                 'quote': 'If Ketu be in the 2nd or the ?th from the Ascendant '
                          'there will be diseases, disgrace, agony and loss of '
                          'wealth.',
                 'pdf_page': '169-170',
                 'ocr_flag': "'?th'=7th; the sentence is split across the page "
                             'break at PDFPAGE 170. NOTE: this is 2nd/7th '
                             'PLACEMENT from the Ascendant, NOT 2nd/7th lordship — '
                             'and it is the only such clause in the chapter that '
                             'carries an explicit frame.'}],
 'maraka': None,
 'remedy': 'Notes: No remedial measures have been prescribed here. Perhaps '
           'recitation of Vishnu Sahasranam and giving a goat in charity will give '
           "relief from the evil effecrs. — SANTHANAM'S NOTE; the text prescribes "
           "NO remedy for this cell and the commentator's suggestion is explicitly "
           "speculative ('Perhaps'). (pdf 170)",
 'absence_notes': {'maraka': 'NONE. This cell has no 2nd/7th-LORDSHIP clause at '
                             'all — the only 2nd/7th reference is a PLACEMENT '
                             "clause ('If Ketu be in the 2nd or the ?th from the "
                             'Ascendant there will be diseases, disgrace, agony '
                             "and loss of wealth.') and it does not mention death. "
                             'Ketu is the one antar lord in ch.54 for which the '
                             'maraka lordship formula is absent.'}},
    ('mars', 'mars'): {'verses': '1-8',
 'conditions': [{'predicate': 'in a kendra, the 5th, the 9th, the 11th, the 3rd or '
                              'the 2nd',
                 'houses': 'kendra,5,9,11,3,2',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of wealth by the beneficence of the king '
                            '(government), beneficence of Goddess Lakshmi, '
                            'recovery of lost kingdom (reinstatement in high '
                            'position) and wealth, birth of a son',
                 'source': 'sloka',
                 'quote': "1-2'1-. Effects like gains or wealth by the beneficence "
                          'of the king (government), beneficence of Goddess '
                          'Lakshmi, recovery of lost kingdorn (reinstatement in '
                          'high position) and weelth, birth of a son, will arise '
                          'in the Antardasa of Mars irr his dwn Dasa, if he be in '
                          'ken<ira, the 5th, the 9th, the l lth. the 3rcl or the '
                          '2nd or be associited with the lord of the .{scendant.',
                 'pdf_page': '161',
                 'ocr_flag': 'heavy OCR damage in verse-number and house list '
                             "('ken<ira'=kendra, 'l lth'=11th, '3rcl'=3rd, "
                             "'.{scendant'=Ascendant). NOTE: 'lord of the "
                             "Ascendant' appears only as an ASSOCIATION partner, "
                             'not as a counting frame — no frame is stated for the '
                             'house list.'},
                {'predicate': 'associated with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as above (alternative limb of the same '
                            'branch)',
                 'source': 'sloka',
                 'quote': 'or be associited with the lord of the .{scendant.',
                 'pdf_page': '161',
                 'ocr_flag': "'associited', '.{scendant'"},
                {'predicate': 'in his sign of exaltation, in his own sign, or in '
                              'his own Navamsa, and endowed with strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'fulfilment of ambitions by the beneficence of the '
                            'king (government) and acquisition of a house, land, '
                            'cow, buffalo etc.',
                 'source': 'sloka',
                 'quote': '3-4. Fuifilment of ambitions by the beneficence of the '
                          "ki'':i (gsyslnment) and acquisition of a house, land, "
                          'cow, truji;lo etc., will be the effects if Mars be in '
                          'his sign of exaltation, in his own sign or in his own '
                          'Navamsa, and be endowed with strength.',
                 'pdf_page': '161',
                 'ocr_flag': "'ki'':i (gsyslnment)'=king (government), "
                             "'truji;lo'=buffalo"},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'urinary troubles, wounds, danger from snakes and the '
                            'king (government)',
                 'source': 'sloka',
                 'quote': '5-5+. Urinary troubles, wounds, danger from snakesand '
                          'the king (government) will be the results, if Mars be '
                          'inthe 8th or the l2th or be associated with or aspected '
                          'bymalefics.',
                 'pdf_page': '162',
                 'ocr_flag': "line-break spaces lost ('snakesand', 'be inthe'); no "
                             'frame word anywhere in the clause'},
                {'predicate': 'associated with or aspected by malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'urinary troubles, wounds, danger from snakes and the '
                            'king (government)',
                 'source': 'sloka',
                 'quote': 'or be associated with or aspected bymalefics.',
                 'pdf_page': '162',
                 'ocr_flag': "'bymalefics'"},
                {'predicate': 'Mars is lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'mental agony and body pains',
                 'source': 'sloka',
                 'quote': '6-8. There will be mental agony and body pains if '
                          'Marsbe the lord of the 2nd or the 7th.',
                 'pdf_page': '162',
                 'ocr_flag': "'Marsbe'"}],
 'maraka': '6-8. There will be mental agony and body pains if Marsbe the lord of '
           'the 2nd or the 7th. — NOTE: this 2nd/7th-lordship clause states only '
           'agony and body pains; it does NOT state death for the Mars antar in '
           'the Mars dasa.',
 'remedy': 'Lord Shiva will give relief by restoring health and providing gains of '
           'wealrh and happiness, ,if the person concerned performs Rudra Japa and '
           'givcs a red coloured bull in charity. (vv.6-8, pdf 162)'},
    ('mars', 'mercury'): {'verses': '36-47',
 'conditions': [{'predicate': 'in a kendra or trikona from the Ascendant',
                 'houses': 'kendra,trikona',
                 'frame': 'from_lagna',
                 'frame_quote': 'frorn the r\\scendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'association with pious and holy persons, performance '
                            'of Ajapa Japa, charities, observance of religious '
                            'rites, gain of reputation, inclination towards '
                            'diplomacy, availability of sweetish preparations, '
                            'acquisition of conveyances, clothes and cattle etc., '
                            "conferment of authority in the king's retinue, "
                            'success in agricultural projects',
                 'source': 'sloka',
                 'quote': "36-371. Effects like associatiou n'ith pious and holy "
                          'pcrsons, performancc of Ajapa Japa (rreqt qq), '
                          "charities, '.rbservauce of religious rites, gain r:f "
                          'reputation, inclination towards diplomacy, availability '
                          'of srveetish preparations, rcquisition of conveyances, '
                          'clothes and cattle etc., confernment of authority in '
                          "the king's retinue (attainrnent of position of "
                          'tuthority in government), succcss in agricultural '
                          'projects, ctc., rvill be experienced in the Antardasa '
                          'of Mercury in the Dasa of Mars, if Mercury be in kendra '
                          'or trikona frorn the r\\scendant,',
                 'pdf_page': '167',
                 'ocr_flag': "'associatiou n'ith'=association with, "
                             "'r\\scendant'=Ascendant, 'succcss'=success. The "
                             'sentence ends with a comma — possible truncation of '
                             'a further limb.'},
                {'predicate': 'in his sign of debilitation, or combust',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'diseases of heart, imprisonment, loss of kinsmen, '
                            'distress to wife and children, destruction of wealth '
                            'and cattle etc.',
                 'source': 'sloka',
                 'quote': '38-39. Diseases of heart, imprisonment, loss of '
                          'kinsmen, distress to wife and children, destruction of '
                          'wealth and cattle ctc., will result, if Mercury be in '
                          'his sign of debilitation, combust . or be in the 6th, '
                          'the 8th or the l2th (from the \\sccndant).',
                 'pdf_page': '167',
                 'ocr_flag': "'ctc.'=etc., '\\sccndant'=Ascendant"},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the \\sccndant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'diseases of heart, imprisonment, loss of kinsmen, '
                            'distress to wife and children, destruction of wealth '
                            'and cattle etc.',
                 'source': 'sloka',
                 'quote': 'or be in the 6th, the 8th or the l2th (from the '
                          '\\sccndant).',
                 'pdf_page': '167',
                 'ocr_flag': 'FRAME CAVEAT: the frame appears ONLY inside round '
                             'brackets, which in this translation marks a '
                             'TRANSLATOR-SUPPLIED gloss rather than words of the '
                             'sloka. Treat as low-confidence from_lagna; a strict '
                             'reading would call it unstated.'},
                {'predicate': 'associated with the lord of the Dasa (Mars)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'journeys to foreign lands, increase in the number of '
                            'enemies, affliction with many kinds of ailments, '
                            'antagonism with the king (government), quarrels with '
                            'kinsmen etc.',
                 'source': 'sloka',
                 'quote': '40-40j. There will be journeys to lbrgien lands, '
                          'increase irt the rtrmber of cnemies, a{iiiction rvith '
                          'many kind of rtilmcnts, antagonism with the king '
                          '(govemment), quarrels with kinsmen etc., if Mercury be '
                          'associated rvith the lord of the I)astr (Mars).',
                 'pdf_page': '167',
                 'ocr_flag': "'lbrgien'=foreign, 'rtrmber of cnemies'=number of "
                             "enemies, 'I)astr'=Dasa"},
                {'predicate': 'in a kendra, trikona, or in his sign of exaltation, '
                              'from the lord of the Dasa (Mars)',
                 'houses': 'kendra,trikona',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from lord of the Dasa (Mars)',
                 'polarity': 'favourable',
                 'polarity_word': 'very auspicious',
                 'results': 'fulfilment of all ambitions, gain of wealth and '
                            'grains, recognition by the king (government), '
                            'acquisition of a kingdom (high position in '
                            'government), gain of clothes and ornaments, '
                            'attachment to many kinds of musical instruments, '
                            'attainment of the position of commander of army, '
                            'discussions on Shastras and Puranas, gain of riches '
                            'to wife and children, beneficence of Goddess Lakshmi',
                 'source': 'sloka',
                 'quote': '4143tr. Fulfilment of all ambitions, gain of wealth and '
                          'lins, recognition by the king (government), acquisition '
                          'of a lgdom (attainment of a high position in '
                          'government), gain of fhes and ornaments, attachment to '
                          'many kind of musical [ruments, attainment of the '
                          'position of a commander of hy, discussions on Shastras '
                          'and puranas (wrra-grrw-religious ipts), gain of riches '
                          'to wife and children and beneficence Goddess Lakshmi '
                          'will be the very auspicious results if rcury be in '
                          'kendra, trikona or in his sign of exaltation from lord '
                          'of the Dasa (Mars).',
                 'pdf_page': '168',
                 'ocr_flag': 'SEVERE left-margin loss on pdf 168 — leading letters '
                             "stripped from most lines ('lins'=grains, "
                             "'lgdom'=kingdom, 'fhes'=clothes, "
                             "'[ruments'=instruments, 'hy'=army, 'rcury'=Mercury, "
                             "'from lord'=from the lord). The frame phrase and the "
                             'valence phrase both survive.'},
                {'predicate': 'in the 6th, the 8th or the 12th from Mars',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from Mars',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'defamation, sinful thinking, harsh speech, danger '
                            'from thieves, fire and the king (government), '
                            'quarrels without reason, fear of attacks by thieves '
                            'and dacoits during travels',
                 'source': 'sloka',
                 'quote': 'U-45+. Effects like defamation, sinful thinking, harsh '
                          'rh, danger from the thieves, fire and the king '
                          '(government), rrels without reason, fear of attacks by '
                          'thieves and dacoits ing travels, will be derived if '
                          'Mercury be in the 6th, the gth, he l2th from Mars or be '
                          'associated with malefics.',
                 'pdf_page': '168',
                 'ocr_flag': "margin loss ('U-45+.'=44-45½, 'rh'=speech, "
                             "'rrels'=quarrels, 'ing travels'=during travels, 'he "
                             "l2th'=or the 12th); 'the gth'=the 8th. Frame is "
                             "'from Mars' — i.e. from the dasa lord, named "
                             "directly rather than by the usual 'lord of the Dasa' "
                             'formula.'},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be associated with malefics.',
                 'pdf_page': '168',
                 'ocr_flag': 'none'},
                {'predicate': 'Mercury is lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'possibility of critical illness',
                 'source': 'sloka',
                 'quote': '46-47. There will be possibility of critical illness in '
                          'the ardasa of Mercury if he be the lord of the 2nd or '
                          'the 7th.',
                 'pdf_page': '168',
                 'ocr_flag': "'ardasa'=Antardasa (margin loss)"}],
 'maraka': '46-47. There will be possibility of critical illness in the ardasa of '
           'Mercury if he be the lord of the 2nd or the 7th. — states critical '
           'illness, not death.',
 'remedy': 'Remedial measures to obtain relief from these evil effects [are] '
           'recitation of Vishnu Sahasranam and giving a horse in [char]ity. '
           '(vv.46-47, pdf 168)'},
    ('mars', 'moon'): {'verses': '70-76',
 'conditions': [{'predicate': 'in her sign of exaltation or in her own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of more kingdom (promotion to a high '
                            'position in government), gain of perfumes, clothes, '
                            'construction of reservoirs, shelters for cows etc., '
                            'celebrations of auspicious functions like marriage '
                            'etc., happiness to wife and children, good relations '
                            'with parents, acquisition of property by the '
                            'beneficence of the sovereign, success in the desired '
                            'projects',
                 'source': 'sloka',
                 'quote': '70-73. Acquisition of more kingdom(promotion to a higl '
                          'position in government), gain of perfumes, clothes, '
                          'construc-tio[n] reservoirs, shelters for cows etc., '
                          'celebrations of аurpi;i; functions like marriage etc., '
                          'happiness to wife and childr[en] good relations rvith '
                          'parents, acquisition of property by t[he] beneficence '
                          'ofthi sovereign, success in the-drsir"a prol,_.\' will '
                          'be the effects in the Antardasa of the [{oon in ttre '
                          'ij. of Mars if the Moon be in her sign of exaltation or '
                          'in ner o[wn] sign. or be in kendra or be in the 9th, '
                          'the 4th or the lOth or the Ascendant alongwith the '
                          'lords of those houses.',
                 'pdf_page': '172-173',
                 'ocr_flag': 'SEVERE right-margin truncation on pdf 173 — every '
                             "line loses its final characters ('higl'=high, "
                             '\'childr\'=children, \'by t\'=by the, \'the-drsir"a '
                             "prol,_.'=the desired projects, '[{oon in ttre ij. of "
                             "Mars'=Moon in the Dasa of Mars, 'ner o'=her own). "
                             "CAUTION: 'auspicious' appears here only as part of "
                             "the OUTCOME 'celebrations of auspicious functions "
                             "like marriage' — it is NOT a valence label on the "
                             'branch, so polarity is recorded as none.'},
                {'predicate': 'in a kendra, or in the 9th, the 4th or the 10th, or '
                              'in the Ascendant, along with the lords of those '
                              'houses',
                 'houses': 'kendra,9,4,10,1',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be in kendra or be in the 9th, the 4th or the lOth '
                          'orthe Ascendant alongwith the lords of those houses.',
                 'pdf_page': '173',
                 'ocr_flag': "'lOth'=10th, 'orthe'=or the, 'alongwith'=along with. "
                             "NO frame is stated: 'the Ascendant' here is one of "
                             'the LISTED HOUSES, not a reference point. Do not '
                             'read it as establishing a lagna frame.'},
                {'predicate': 'the Moon is waxing (full effects) vs waning '
                              '(reduced effects)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'good effects realised in full if waxing; waning Moon '
                            'reduces the impact of the effects to some extent',
                 'source': 'sloka',
                 'quote': 'The go[od] effects will be realised in full if the Moon '
                          'be waxing. Wini[ng] Moon will reduce the irnpact of the '
                          'effects to some extent.',
                 'pdf_page': '173',
                 'ocr_flag': "'go'=good, 'Wini'=Waning, 'irnpact'=impact "
                             '(right-margin truncation). This is a MAGNITUDE '
                             'modifier, not a favourable/adverse switch.'},
                {'predicate': 'in his sign of debilitation or in his enemy sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'death, distress to wife and children, loss of lands, '
                            'wealth and cattle and danger of a war etc.',
                 'source': 'sloka',
                 'quote': '74-76. The effects like death, distress to wife and '
                          'childre[n] loss oflands, wealth and cattle and danger '
                          "of a war etc., v[ill] be experie'ced, if the Moon be "
                          'irr his sign of debilitation or [in] his enemy sign',
                 'pdf_page': '173',
                 'ocr_flag': "right-margin truncation ('childre', 'v'=will, "
                             "'experie'ced'=experienced); 'oflands'=of lands. Note "
                             "the translation switches to masculine 'his' for the "
                             'Moon here.'},
                {'predicate': 'in the 6th, the 8th or the 12th — FRAME '
                              'UNRESOLVABLE',
                 'houses': '6,8,12',
                 'frame': 'unstated',
                 'frame_quote': 'from tAscendant of the lord of the Dasa (Mars)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'death, distress to wife and children, loss of lands, '
                            'wealth and cattle and danger of a war etc.',
                 'source': 'sloka',
                 'quote': 'or be in the 6th, the gth or the l2th from tAscendant '
                          'of the lord of the Dasa (Mars).',
                 'pdf_page': '173',
                 'ocr_flag': 'CRITICAL — DO NOT SHIP AS EITHER FRAME. The line '
                             "reads 'from t[he] Ascendant OF the lord of the Dasa "
                             "(Mars)', a construction used nowhere else in the "
                             'chapter. Right-margin truncation makes it impossible '
                             "to tell whether the original read 'from the "
                             "Ascendant OR the lord of the Dasa' (two alternative "
                             'frames) or a single garbled frame. Because the '
                             'recovered text does not settle it, frame is recorded '
                             "as unstated. Also 'the gth'=the 8th."},
                {'predicate': 'the Moon is lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'possibility of premature death, distress to the body '
                            'and mental agony',
                 'source': 'sloka',
                 'quote': 'There will be pos[si]bility of premature death, '
                          'distress to the body and men[tal] agony, if the Moon be '
                          'the lord of the 2nd or the ith"',
                 'pdf_page': '173',
                 'ocr_flag': "'pos'=possibility, 'men'=mental, 'the "
                             'ith"\'=the 7th (right-margin truncation)'}],
 'maraka': 'There will be pos[si]bility of premature death, distress to the body '
           'and men[tal] agony, if the Moon be the lord of the 2nd or the ith '
           '[7th].',
 'remedy': 'The remedial measures to be adopted to obtain rel[ief] from the above '
           'evil effects, are recitation of mantras of t[he] Coddess Durga and the '
           'Goddess Lakshmi. (vv.74-76, pdf 173)'},
    ('mars', 'rahu'): {'verses': '9-14',
 'conditions': [{'predicate': 'in his moolatrikona or in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'recognition from government, gain of house, land '
                            'etc., happiness from son, extraordinary profits in '
                            'business, bathing in holy rivers like Ganges and '
                            'foreign journeys',
                 'source': 'sloka',
                 'quote': '9-10+. Effects like recognition from government, gain '
                          'of house, land etc., happiness from son, extraordinary '
                          'profits in business, bathing in holy rivers like Ganges '
                          'and foreign jouri:eys, will be the auspicious effects '
                          'in the Antardasa of Rahu in the Dasa,of Mars, if Rahu '
                          'be in his moolatrikona, in his sign of exal{ation, in '
                          'kendra, the llth, the 5th or the 9th from the Ascendant '
                          'and be associated with benefics.',
                 'pdf_page': '162',
                 'ocr_flag': "'jouri:eys'=journeys, 'exal{ation'=exaltation"},
                {'predicate': 'in a kendra, the 11th, the 5th or the 9th from the '
                              'Ascendant',
                 'houses': 'kendra,11,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'recognition from government, gain of house, land '
                            'etc., happiness from son, extraordinary profits in '
                            'business, bathing in holy rivers, foreign journeys',
                 'source': 'sloka',
                 'quote': 'if Rahu be in his moolatrikona, in his sign of '
                          'exal{ation, in kendra, the llth, the 5th or the 9th '
                          'from the Ascendant and be associated with benefics.',
                 'pdf_page': '162',
                 'ocr_flag': "'llth'=11th"},
                {'predicate': 'associated with benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'and be associated with benefics.',
                 'pdf_page': '162',
                 'ocr_flag': 'none'},
                {'predicate': 'in the 8th or the 12th from the Ascendant',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'danger from snakes, wounds, destruction of cattle, '
                            'danger from animals, diseases due to imbalance of '
                            'bile and wind, imprisonment etc.',
                 'source': 'sloka',
                 'quote': '1l-14. Danger from snakes, wounds, destruction of I '
                          'cattle, danger from animals, diseases due to imbalance '
                          'of bile and wind, imprisonment, etc., will be the '
                          'results if Rahu be in the Sth or the l2th from the '
                          'Ascendant or be aspected by or associated with '
                          'malefics.',
                 'pdf_page': '163',
                 'ocr_flag': "'the Sth' is OCR for 'the 8th' (S/8 confusion); "
                             "'l2th'=12th. The valence word 'evil' appears only "
                             "later in the REMEDY sentence ('relief from the above "
                             "evil effects'), not in the sloka branch, so polarity "
                             'recorded as none.'},
                {'predicate': 'aspected by or associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be aspected by or associated with malefics.',
                 'pdf_page': '163',
                 'ocr_flag': 'none'},
                {'predicate': 'in the 2nd',
                 'houses': '2',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'loss of wealth',
                 'source': 'sloka',
                 'quote': 'There u,ill be loss of wealth if Rahu be in the 2nd and '
                          'great danger of premature death if he be in the 7th.',
                 'pdf_page': '163',
                 'ocr_flag': "'u,ill'=will. The preceding clause said 'from the "
                             "Ascendant' but this is a NEW sentence that does not "
                             'restate a frame — recorded as unstated rather than '
                             'inheriting.'},
                {'predicate': 'in the 7th',
                 'houses': '7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'great danger of premature death',
                 'source': 'sloka',
                 'quote': 'and great danger of premature death if he be in the '
                          '7th.',
                 'pdf_page': '163',
                 'ocr_flag': 'frame not restated; this is a PLACEMENT in the 7th, '
                             'not 7th-lordship'}],
 'maraka': 'There u,ill be loss of wealth if Rahu be in the 2nd and great danger '
           'of premature death if he be in the 7th. — NOTE: this is 2nd/7th '
           'PLACEMENT, not 2nd/7th lordship; it is the only death clause in this '
           'cell and it carries no frame.',
 'remedy': '.The remedial measure to be adopied to obtain relief from the above '
           'evil effects are Naga Puja, offering foo,l to Brahmins and Mrityunjaya '
           'Japa. They will help in the prolon;: tron cf Iongevity. (pdf 163)'},
    ('mars', 'saturn'): {'verses': '23-35',
 'conditions': [{'predicate': 'in a kendra or trikona',
                 'houses': 'kendra,trikona',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'recognition from the king (government), increase in '
                            'reputation, gain of wealth and grains, happiness from '
                            'children and grandchildren, increase in the number of '
                            'cows etc.',
                 'source': 'sloka',
                 'quote': '23-25. Effects like recognition from the king '
                          '(government) increase in reputation, gain of wealth and '
                          "graini, happiness from children and grand 'children, "
                          'increase in the number of cows etc., will be experinced '
                          'in the Antardasa of Saturn in the Dasa of Mars, if '
                          'Saturn be in kendra, trikona, in hismoolatrikona, in '
                          'exalted or own Navamsa or be associatedwith the lord of '
                          'the Ascendant or benefics. Results will generally '
                          'fructify on Saturdays in the month of Saturn.',
                 'pdf_page': '165',
                 'ocr_flag': "'graini'=grains, 'experinced'=experienced, "
                             "'hismoolatrikona', 'associatedwith' (spaces lost). "
                             "NO frame is given for kendra/trikona here — 'lord of "
                             "the Ascendant' is an association partner only."},
                {'predicate': 'in his moolatrikona, or in exalted or own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'in hismoolatrikona, in exalted or own Navamsa',
                 'pdf_page': '165',
                 'ocr_flag': "'hismoolatrikona'"},
                {'predicate': 'associated with the lord of the Ascendant or with '
                              'benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "as above; 'Results will generally fructify on "
                            "Saturdays in the month of Saturn.'",
                 'source': 'sloka',
                 'quote': 'or be associatedwith the lord of the Ascendant or '
                          'benefics. Results will generally fructify on Saturdays '
                          'in the month of Saturn.',
                 'pdf_page': '165',
                 'ocr_flag': "'associatedwith'"},
                {'predicate': 'in his sign of debilitation or in an enemy sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'danger from Yavana kings (foreign dignitaries), loss '
                            'of wealth, imprisonment, possibility of affliction '
                            'with diseases, loss in agricultural production',
                 'source': 'sloka',
                 'quote': '26-26rr. Danger from Yavana kings (foreign '
                          'dignitaries), loss of wealth, imprisonment, possibility '
                          'of affiiction with diseases, loss in agricultural '
                          'production, will result, if Saturh be in his sign of '
                          'debilitation or in an enemy sign or be in the gth or '
                          'the l2th.',
                 'pdf_page': '165',
                 'ocr_flag': "'Saturh'=Saturn, 'affiiction'=affliction"},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be in the gth or the l2th.',
                 'pdf_page': '165',
                 'ocr_flag': "'the gth' is OCR for 'the 8th' (g/8 confusion); "
                             "'l2th'=12th. No frame stated."},
                {'predicate': 'Saturn is lord of the 2nd or 7th AND associated '
                              'with malefics',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'great danger, loss of life, wrath of king '
                            '(government), mental agony, danger from thieves and '
                            'fire, punishment by the king, loss of co-borns, '
                            'dissensions amongst members of the family, loss of '
                            'cattle, fear of death, distress to wife and children, '
                            'imprisonment etc.',
                 'source': 'sloka',
                 'quote': '27-29t. Effects like great danger, loss of life, wrath '
                          'of king (government), mental agony, danger from thieves '
                          'and fire, punishment by the king (government), loss of '
                          'co-borns, dissensions amongst members of the family, '
                          'loss of cattle, fear of death, distress to wifC and '
                          'children, imprisonment etc., will be felt, if Saturn be '
                          'the lord of the 2nd or 7th and be associated with '
                          'malefics.',
                 'pdf_page': '165',
                 'ocr_flag': "'wifC'=wife. Conjunctive condition: lordship AND "
                             'malefic association.'},
                {'predicate': 'in a kendra, the 11th or the 5th from the lord of '
                              'the Dasa (Mars)',
                 'houses': 'kendra,11,5',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'frorr trre lor<i of tlie Drsa (Mars)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'journey to foreign lands, loss of reputation, violent '
                            'actions, loss from sale of agricultural lands, loss '
                            'of position, agony, defeat in battle, urinary '
                            'troubles etc.',
                 'source': 'sloka',
                 'quote': 'i0-32. There will be journcy to foreign lands. loss '
                          'o.orepuIiltioir, violent actions, loss from sale of '
                          'agriculturnl lands, Ioss of^ position, agony, defeat in '
                          'battle, urinary troublesetc" iisrturn be i\'kerrdra, '
                          'the llth or the 5th frorr trre lor<i of tlie Drsa '
                          '(Mars).',
                 'pdf_page': '165-166',
                 'ocr_flag': "BADLY damaged ('i0-32.'=30-32, 'o.orepuIiltioir'=of "
                             "reputation, 'iisrturn be i'kerrdra'=if Saturn be in "
                             "kendra, 'frorr trre lor<i of tlie Drsa'=from the "
                             "lord of the Dasa). THIS IS THE CHAPTER'S REVERSAL "
                             'CASE: the normally-good from-dasa-lord positions '
                             '(kendra/11/5) yield adverse RESULTS here, yet no '
                             'valence LABEL appears in the sloka — the '
                             "'inauspicious' label appears only in Santhanam's "
                             'note below.'},
                {'predicate': '(commentary on the preceding branch) a good '
                              'position of the antardasa lord relative to the dasa '
                              'lord normally gives auspicious results, but for '
                              'Saturn in the Dasa of Mars the effects are very '
                              'inauspicious',
                 'houses': 'kendra,11,5',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'with ret-erence to the Dasa lord',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'commentator flags the reversal as an important '
                            'exception',
                 'source': 'note',
                 'quote': '-r*otes : Normally a good position of tl.re '
                          'Antarclasalord with ret-erence to the Dasa lord brings '
                          "about ver1,ausp'icious results but in the case of "
                          "Saturn in the Dasa of Mars; tltr.'efiects lvill be very "
                          'inauspicious accorcling to sage parasara. Tiris '
                          'important fact is rvorth noting by the readers.',
                 'pdf_page': '166',
                 'ocr_flag': "heavy damage ('Antarclasalord', "
                             "'ver1,ausp'icious'=very auspicious, 'accorcling to "
                             "sage parasara'). SANTHANAM'S NOTE, not mula — the "
                             "valence word 'inauspicious' is the commentator's, "
                             "not the sloka's."},
                {'predicate': 'in the 8th or the 12th from the lord of the Dasa '
                              'AND associated with malefics',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'death, danger from the king (government) and thieves, '
                            'rheumatism, pains, danger from the enemy and members '
                            'of the family',
                 'source': 'sloka',
                 'quote': "33-35. Efl'ects like death, danger from the king "
                          '(government) and thieves, rheumatism, pains, danger '
                          'from the enenv and members of the family, will be '
                          'experierrced if Saturn bc irr the 8th or the l2th from '
                          'the lord of the Dasa and be associnted with rnalefics.',
                 'pdf_page': '166',
                 'ocr_flag': "'enenv'=enemy, 'experierrced'=experienced, 'bc "
                             "irr'=be in, 'associnted with rnalefics'"}],
 'maraka': '27-29t. Effects like great danger, loss of life, ... fear of death, '
           '... will be felt, if Saturn be the lord of the 2nd or 7th and be '
           'associated with malefics. — NOTE: unlike the other cells, the lordship '
           'trigger here is CONJOINED with malefic association.',
 'remedy': 'Thcre will be relief from the evil cffects by the bcnellcence of loid '
           'Shiva if Mrityunjaya Japa is performetl in the prescribed r11Anrler. '
           '(pdf 166)'},
    ('mars', 'sun'): {'verses': '64-69',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of conveyances, gain of reputation, birth '
                            'of a son, growth of wealth, amicable atmosphere in '
                            'the family, sound health, potency, recognition by the '
                            'king (government), extraordinary profits in business '
                            'and audience with the king (meeting with high '
                            'officials of government) etc.',
                 'source': 'sloka',
                 'quote': '(4.6(r. Effects like acquisition of conveyances, gain '
                          'of reputation, birth of a son, growth of wealth, '
                          'amicable atmos- . phere in the family, sound health, '
                          'potency, recognition bythe the hng (gov.:rnment); '
                          'extraordinary profits in business and audience with tbe '
                          "king (meeting ' with high officials of government) "
                          'etc., will be experienced in the Antardasa cif the Sun '
                          'in the Dasa of Mars, if the Sun be in his sign of '
                          'cxal:ation, in his own sign or be in kendra, trikona or '
                          'the llth along with the lords of the lOth and the I '
                          'lth.',
                 'pdf_page': '171-172',
                 'ocr_flag': "'(4.6(r.'=64-66½ (verse numbers badly mangled), "
                             "'bythe the hng (gov.:rnment)'=by the king "
                             "(government), 'cxal:ation'=exaltation, 'cif'=of. "
                             'Sentence spans the page break at PDFPAGE 172.'},
                {'predicate': 'in a kendra, trikona or the 11th along with the '
                              'lords of the 10th and the 11th',
                 'houses': 'kendra,trikona,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be in kendra, trikona or the llth along with the '
                          'lords of the lOth and the I lth.',
                 'pdf_page': '172',
                 'ocr_flag': "'llth'/'I lth'=11th, 'lOth'=10th. NO frame is stated "
                             'for kendra/trikona/11th — the 10th and 11th lords '
                             'are conjunction partners, not a frame.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (Mars)',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord i.r, the Dasa fMars)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'distress to the body, agony, failure in ventures, '
                            'possibilities of suffering from troubles in the '
                            'forehead, fever, dysentry etc.',
                 'source': 'sloka',
                 'quote': "67-671. Distress to the body, agony' failure in "
                          'ventures, possibilities of suffering from troubles in '
                          'the forehead, fever, dysentry etc., will be the '
                          'effects. if the Sun be in tire 6th, the 8th or the 12th '
                          'from the lord i.r, the Dasa fMars) or be asso-ciated '
                          'with malefics.',
                 'pdf_page': '172',
                 'ocr_flag': "'tire'=the, 'lord i.r, the Dasa fMars)'=lord of the "
                             'Dasa (Mars)'},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be asso-ciated with malefics.',
                 'pdf_page': '172',
                 'ocr_flag': 'hyphenated line break'},
                {'predicate': 'the Sun is lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'attacks of fever, danger from snakes and poison and '
                            'distress to son',
                 'source': 'sloka',
                 'quote': '68-69. There will be attacks of fever, danger from '
                          'snakes aod poision and distress to son if the Sun be '
                          'the lord of the 2nd or the 7th.',
                 'pdf_page': '172',
                 'ocr_flag': "'aod poision'=and poison"}],
 'maraka': '68-69. There will be attacks of fever, danger from snakes aod poision '
           'and distress to son if the Sun be the lord of the 2nd or the 7th. — no '
           'death stated.',
 'remedy': ', The rrrmg6l.t me!:.ure to gain good health and wealth is to perform '
           'worship of the Sun in the prescribed manner. (vv.68-69, pdf 172)'},
    ('mars', 'venus'): {'verses': '55-63',
 'conditions': [{'predicate': 'in a kendra to the Ascendant',
                 'houses': 'kendra',
                 'frame': 'from_lagna',
                 'frame_quote': 'in kendra to the Ac: crrtlant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of kingdom (attainment of a high position '
                            'in government), great enjoyment and comfort of '
                            'luxuries, gain of elephants, horses, clothes etc.',
                 'source': 'sloka',
                 'quote': '55-56j. Effects like acquisition of kingdom (artainment '
                          'of a high position in government), great enjoyment and '
                          'comfort of luxuries, gain of elephants, hn1sx5, clothes '
                          'etc., will be derived in the Antardasa of rr.,is in the '
                          'Dasa of Mars. ifVenus be in kendra to the Ac: crrtlant, '
                          'be in his sign of exaltation, or in his own sign or be '
                          'the lord of the Ascenclant, the 5th orthe 9th.',
                 'pdf_page': '170',
                 'ocr_flag': "'hn1sx5'=horses, 'rr.,is'=Venus, 'Ac: "
                             "crrtlant'=Ascendant, 'Ascenclant'=Ascendant, "
                             "'orthe'=or the. Frame reads 'in kendra TO the "
                             "Ascendant' (not the usual 'from')."},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'be in his sign of exaltation, or in his own sign',
                 'pdf_page': '170',
                 'ocr_flag': 'none'},
                {'predicate': 'Venus is lord of the Ascendant, the 5th or the 9th',
                 'houses': '1,5,9',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'or be the lord of the Ascenclant, the 5th orthe 9th.',
                 'pdf_page': '170',
                 'ocr_flag': "'Ascenclant', 'orthe'. This is a LORDSHIP condition, "
                             'not a placement.'},
                {'predicate': 'related to the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'happiness to wife and children, opulence and glory '
                            'and increased good fortune',
                 'source': 'sloka',
                 'quote': 'If Venus be related to the lord of the Ascendant, there '
                          'will be happiness to wife and children, opulence and '
                          'glory andincreased good fortune.',
                 'pdf_page': '170',
                 'ocr_flag': "'andincreased'"},
                {'predicate': 'in the 5th, the 9th, the 11th or the 2nd from the '
                              'lord of the Dasa (Mars)',
                 'houses': '5,9,11,2',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'lrom the lord of the Dasa (Mars)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of property, celebrations on the birth of a son, '
                            'gain of wealth from the employer, acquisition of a '
                            'house and villages etc. by the beneficence of the '
                            'sovereign; in the last part of the Dasa, functions of '
                            'songs and dances and bathing in holy waters',
                 'source': 'sloka',
                 'quote': '57-60. Gain of pioperty, celebrations on the birth of '
                          'alon, gain of wealth from the employer, acquisition of '
                          'a house,and. villages etc. by the beneficence of the '
                          'sovereign, will be :he results if Venusbe in the 5th, '
                          'the 9th, the llth 1r the 2nd lrom the lord of the Dasa '
                          '(Mars). In the last part of the Dasa there rvill be '
                          'functions of songs and dances and bathing in holy '
                          'waters.',
                 'pdf_page': '170-171',
                 'ocr_flag': "'alon'=a son, 'llth 1r the 2nd'=11th or the 2nd, "
                             "'Venusbe', ':he results'=the results. Sentence spans "
                             'the page break at PDFPAGE 171.'},
                {'predicate': 'connected with or related to the lord of the 10th',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'construction of wells, reservoirs etc., and '
                            'performance of religious, charitable and pious deeds',
                 'source': 'sloka',
                 'quote': 'If Venus be connected with or related to the lord of '
                          'the l0th, there witl be construction of wells, '
                          'reservoirs etc., and performance of religious, '
                          'charitable and pious deecls.',
                 'pdf_page': '171',
                 'ocr_flag': "'witl'=will, 'deecls'=deeds"},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (Mars), or associated with malefics',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa lMars)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'sorrows, physical distress, loss of wealth, danger '
                            'from thieves and the king (government), dissensions '
                            'in the family, distress to wife and children and '
                            'destruction of cattle',
                 'source': 'sloka',
                 'quote': '6l-62. There will be sorrows, physical distress, loss '
                          'of wealth, danger from thieves, and the king '
                          '(government), dissensions in the family, distress to '
                          'wife and children and destruction of cattle, if Venus '
                          'be in the 6th, the 8th or the 12th from the lord of the '
                          'Dasa lMars) or be associated with malefics.',
                 'pdf_page': '171',
                 'ocr_flag': "'lMars)'=(Mars)"},
                {'predicate': 'Venus is lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'pains in the body',
                 'source': 'sloka',
                 'quote': '63. IfVenus be the lord of the 2nd or the 7th, there '
                          'will be pains in the body in his Antardasa.',
                 'pdf_page': '171',
                 'ocr_flag': "'IfVenus'"}],
 'maraka': '63. IfVenus be the lord of the 2nd or the 7th, there will be pains in '
           'the body in his Antardasa. — states bodily pain only; NO death is '
           'stated.',
 'remedy': 'For regaining good health, the remedial measure to be edopted is '
           'giving a cow or female buffalo in charity. (v.63, pdf 171)'},
    ('mercury', 'jupiter'): {'verses': 'vv.56-66 (56-58.5, 59-61, 62-63.5, 64-64.5, 65-66)',
 'conditions': [{'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical felicity; gain of wealth; beneficence of the '
                            'king; celebration of auspicious functions like '
                            'marriage at home; availability of sweetish '
                            'preparations; increase in cattle wealth; attending '
                            'discourses on Puranas; devotion to deities and the '
                            'preceptor; interest in religion, charities; worship '
                            'of Lord Shiva.',
                 'source': 'sloka',
                 'quote': '56-58$. Effects like physical felicity, gain of wealth, '
                          'beneficence of the king, celebration of auspicious '
                          'functions like marriage etc., at home, availability of '
                          'sweetish preparations, increase in cattle wealth, '
                          'attending discourses on Puranas (religious scriptures) '
                          "etc., devotion to deities and the preceptor' interest "
                          'in religion, charities etc., worship of Lord Shiva '
                          'etc., will be derived in the Antardasa of Jupiter in '
                          'the Dasa of Mercury, if Jtrpiter be in kendra, trikona '
                          'or the llth from the Ascendant or bc in his sign of '
                          'exaltation or irr his own sign.',
                 'pdf_page': '224',
                 'ocr_flag': 'POLARITY TRAP: the word "auspicious" DOES occur in '
                             'this passage, but as an adjective describing the '
                             'EVENTS ("celebration of auspicious functions like '
                             'marriage"), NOT as a valence label on the branch. '
                             'Polarity therefore recorded as none; the apodosis '
                             'verb is the neutral "will be derived".'},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.56-58.5 above.',
                 'source': 'sloka',
                 'quote': 'or bc in his sign of exaltation or irr his own sign.',
                 'pdf_page': '224',
                 'ocr_flag': '"bc"=be, "irr"=in.'},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Discord with kings and kinsmen; danger from thieves; '
                            'death of parents; disgrace; punishment from '
                            'government; loss of wealth; danger from snakes and '
                            'poison; fever; losses in agricultural production; '
                            'loss of lands.',
                 'source': 'sloka',
                 'quote': '59-61. Discord with kings and kinsmett, danger from '
                          'thieves etc., death of parents, disgrace, punishment '
                          'from government, loss of wealth, danger froF snakes and '
                          'poison, fever, losses in agricultural production, loss '
                          'of lands etc., will be the results, if Jupiter be in '
                          'his sign of debilitation, be combust, or be in the 6th, '
                          'the 8th or the l2th from the Ascendant or be associated '
                          'with or aspected by Saturn and Mars.',
                 'pdf_page': '224-225',
                 'ocr_flag': 'The English apodosis is printed on PDFPAGE 224 and '
                             'the protasis continues onto 225 across an '
                             'interleaved Sanskrit block. "death" and "loss" also '
                             'present as valence words.'},
                {'predicate': 'be combust',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Same list as vv.59-61 above.',
                 'source': 'sloka',
                 'quote': 'if Jupiter be in his sign of debilitation, be combust, '
                          'or be in the 6th, the 8th or the l2th from the '
                          'Ascendant',
                 'pdf_page': '225',
                 'ocr_flag': 'The only explicit COMBUSTION condition in the '
                             'chapter.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Same list as vv.59-61 above.',
                 'source': 'sloka',
                 'quote': 'or be in the 6th, the 8th or the l2th from the '
                          'Ascendant or be associated with or aspected by Saturn '
                          'and Mars.',
                 'pdf_page': '225',
                 'ocr_flag': ''},
                {'predicate': 'associated with or aspected by Saturn and Mars',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Same list as vv.59-61 above.',
                 'source': 'sloka',
                 'quote': 'or be associated with or aspected by Saturn and Mars.',
                 'pdf_page': '225',
                 'ocr_flag': 'AMBIGUOUS: "Saturn and Mars" — the text does not '
                             'state whether BOTH are required or either suffices.'},
                {'predicate': 'in a kendra, trikona or the 11th AND be endowed '
                              'with strength',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Mercury)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Happiness from kinsmen and son; enthusiasm; increase '
                            'in wealth and name and fame; giving grains in '
                            'charity.',
                 'source': 'sloka',
                 'quote': '62-63I. There will be happiness from kinsmen and 8on, '
                          'enthusiasm, increase in wealth and name and fame, '
                          'giving grains etc., in charity, if Jupiter be in '
                          'kendra, trikona or the llth from the lord of the Dasa '
                          '(Mercury) and be endowed with strength.',
                 'pdf_page': '225',
                 'ocr_flag': '"8on"=son. Note the CONJUNCTIVE strength requirement '
                             '("and be endowed with strength") — this branch does '
                             'not fire on placement alone.'},
                {'predicate': 'be weak and be in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the loril 9f the Dasa (Mercury)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Agony; anxiety; danger from diseases; antagonism with '
                            'wife and kinsmen; wrath of the king (government); '
                            'quarrels; loss of wealth; danger from Brahmins (wrath '
                            'of Brahmins).',
                 'source': 'sloka',
                 'quote': '64-64t. Agony, anxiety, danger from diseases, '
                          'antagonisn with wife and kinsmen, wrath of the king '
                          '(government), quarrels, . loss of wealth, danger from '
                          'Brahmins (wrath of Brahmins), will be the iegults if '
                          'Jdpiter..be weik and be in the 6th, theSth on .. .. the '
                          'l2th from the loril 9f the Dasa (Mercury).',
                 'pdf_page': '225',
                 'ocr_flag': 'Heavy damage: "Jdpiter..be weik"=Jupiter be weak, '
                             '"theSth on .. .. the l2th"=the 8th or the 12th, '
                             '"loril 9f"=lord of. "loss" also present.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical distress.',
                 'source': 'sloka',
                 'quote': '65-66. There will be physical distress if Jupiter be '
                          "thq lord of'the Znd or the, ?th or be in the 2nd or the "
                          '7th.',
                 'pdf_page': '225',
                 'ocr_flag': '"thq lord of\'the Znd or the, ?th"=the lord of the '
                             '2nd or the 7th. FRAME: NO "from the Ascendant" gloss '
                             'appears here at all, parenthesised or otherwise — '
                             'unlike the Ketu/Venus/Sun/Moon/Mars/Saturn maraka '
                             'clauses. Recorded as unstated.'},
                {'predicate': 'be in the 2nd or the 7th (placement)',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical distress.',
                 'source': 'sloka',
                 'quote': 'or be in the 2nd or the 7th.',
                 'pdf_page': '225',
                 'ocr_flag': 'CRITICAL FRAME GAP: a bare placement condition with '
                             'no reference point stated. The immediately preceding '
                             'vv.62-64 both count FROM THE DASA LORD, while the '
                             'parallel lordship clause would count from the '
                             'Ascendant — either frame is arguable and the text '
                             'settles neither. Recorded as unstated — do NOT '
                             'infer.'}],
 'maraka': '"65-66. There will be physical distress if Jupiter be thq lord of\'the '
           'Znd or the, ?th or be in the 2nd or the 7th." — UNIQUE in this '
           'chapter: it adds a PLACEMENT alternative alongside the lordship one, '
           'and NO frame is stated for either.',
 'remedy': '"The lemedial measures to obtain relief from the above evil effects '
           'are recitation of Shiva Sahasranama and glving a cow and gol{ in '
           'charity." (PDFPAGE 225)'},
    ('mercury', 'ketu'): {'verses': 'vv.6-12 (6-8.5, 9-11, 12)',
 'conditions': [{'predicate': 'associated with benefics in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'in kendra or trikona from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical fitness; gain of wealth; affectionate '
                            'relations with kinsmen; increase in cattle wealth; '
                            'income from industries; success in educational '
                            'sphere; acquisition of name and fame; honours; '
                            'audience with the king and joining in a banquet with '
                            'him; comforts of clothes.',
                 'source': 'sloka',
                 'quote': '6-8$. Effects like physical fitness, *rle gain of '
                          'wealtlt, affectionate relations with kinsrnen. .ncrease '
                          'in cattle wealtb, income from industries, success i:, '
                          'educational sphere, acquisition of name and fame, '
                          'honours, audience with the king and joining in a '
                          'banquet with him, comforts of clothes etc., will be '
                          'experi- enced, if Ketu be a$sociated with benefics in '
                          'kendra or trikona from the Ascendant or be in '
                          'conjunction with the lord of the Ascendant or a '
                          'yogakaraka.',
                 'pdf_page': '216',
                 'ocr_flag': '"*rle gain of wealtlt" and "success i:, educational '
                             'sphere" OCR-damaged; apodosis verb is the neutral '
                             '"will be experienced".'},
                {'predicate': 'in conjunction with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.6-8.5 above.',
                 'source': 'sloka',
                 'quote': 'or be in conjunction with the lord of the Ascendant or '
                          'a yogakaraka.',
                 'pdf_page': '216',
                 'ocr_flag': ''},
                {'predicate': 'in conjunction with a yogakaraka (or: be a '
                              'yogakaraka)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.6-8.5 above.',
                 'source': 'sloka',
                 'quote': 'or be in conjunction with the lord of the Ascendant or '
                          'a yogakaraka.',
                 'pdf_page': '216',
                 'ocr_flag': 'AMBIGUOUS PARSE: "or a yogakaraka" may attach to "in '
                             'conjunction with" or be an independent predicate '
                             '(Ketu himself a yogakaraka). The text does not '
                             'settle it.'},
                {'predicate': 'in a kendra or the 11th',
                 'houses': '1,4,7,10,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Mercury)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.6-8.5 above.',
                 'source': 'sloka',
                 'quote': 'The same will be the results if Ketu be in kendra or '
                          'the llth from the lord of the Dasa (Mercury).',
                 'pdf_page': '216',
                 'ocr_flag': '"llth" = 11th.'},
                {'predicate': 'in association with malefics in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Mercury)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Fall from a conveyance; distress to son; danger from '
                            'the king; indulgence in sinful deeds; danger from '
                            'scorpions; quarrels with the menials; sorrow; '
                            'diseases; association with menials.',
                 'source': 'sloka',
                 'quote': '9-ll. Fall from a gonveyance, distress to son, danger '
                          'from the king, indulgence in sinful deeds, danger from '
                          'scorpions etc., quarrels with the menials, sorrow, '
                          'diseases and association with meanials etc., willtb* '
                          'the results, if Ketu be in association with malefics in '
                          'the 8th or the l2th from the lord of the Dasa '
                          '(Mercury).',
                 'pdf_page': '216-217',
                 'ocr_flag': '"gonveyance", "meanials", "willtb*" OCR damage; the '
                             'protasis is split across the PDFPAGE 217 break but '
                             'is legible.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the Ascendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical distress.',
                 'source': 'sloka',
                 'quote': '12. There will be physical distress if Ketu be the lord '
                          'of the 2nd or the 7th (from the Ascendant).',
                 'pdf_page': '217',
                 'ocr_flag': 'FRAME CAVEAT: "(from the Ascendant)" is '
                             "PARENTHESISED, i.e. very likely Santhanam's "
                             'editorial gloss rather than sloka words. Recorded as '
                             'from_lagna on the strength of the printed words, but '
                             'the parentheses are a hedge. No death word, so '
                             'polarity none.'}],
 'maraka': '"12. There will be physical distress if Ketu be the lord of the 2nd or '
           'the 7th (from the Ascendant)." — promises only physical distress, NOT '
           'death, unlike the Venus/Sun/Mars/Rahu/Saturn cells.',
 'remedy': '"The remedial measure to obtain relief from the above evil effects, is '
           'giving a goat in charity." (PDFPAGE 217)'},
    ('mercury', 'mars'): {'verses': 'vv.36-46 (36-38.5, 39-40.5, 41-42, 43-44.5, 45-46)',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Well being and enjoyments in the family by the '
                            'beneficence of the king (government); increase in '
                            'prosperity; recovery of lost kingdom (reinstatement '
                            'in a high position in government); birth of son; '
                            'satisfaction; acquisition of cattle, conveyances and '
                            'agricultural lands; happiness from wife.',
                 'source': 'sloka',
                 'quote': '36-38+. Effects like-well being and enjoyments in the '
                          'familyby.the beneficence of the king (government;, '
                          'increase i, or"p..iy, 11":u..t of lost kingdom etc., '
                          '(reinstatemenr in a high p*iri.iriln government), birth '
                          'of son, satisfaction, acquisition of cattle,coneyances '
                          'and asricultural lands, happiness from wife etc.,will '
                          'be derived ii ttre Antardasa of-Mars in the Dasa '
                          'ofMercury, if Mars be in his sign of exaltation, in his '
                          'own -sign, in kendra or trikona from thJ Ascendant or '
                          "be associat.o wTtnthe'lord of the Ascendant.",
                 'pdf_page': '221',
                 'ocr_flag': 'Badly de-spaced block ("increase i, or\\"p..iy", '
                             '"11\\":u..t of lost kingdom", "p*iri.iriln"); the '
                             'PROTASIS is nonetheless legible. Apodosis verb is '
                             'the neutral "will be derived".'},
                {'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from thJ Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.36-38.5 above.',
                 'source': 'sloka',
                 'quote': 'if Mars be in his sign of exaltation, in his own -sign, '
                          'in kendra or trikona from thJ Ascendant or be '
                          "associat.o wTtnthe'lord of the Ascendant.",
                 'pdf_page': '221',
                 'ocr_flag': '"thJ"=the.'},
                {'predicate': 'associated with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.36-38.5 above.',
                 'source': 'sloka',
                 'quote': "or be associat.o wTtnthe'lord of the Ascendant.",
                 'pdf_page': '221',
                 'ocr_flag': '"associat.o wTtnthe\'lord" = "associated with the '
                             'lord".'},
                {'predicate': 'associated with or aspected by malefics in the '
                              '8th(?) or the 12th',
                 'houses': '8?,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'Physical distress; mental agony; obstacles in '
                            'industrial ventures; loss of wealth; gout; distress '
                            'from wounds; danger from weapons and fever.',
                 'source': 'sloka',
                 'quote': "39'40+. Physical distress, mental agony, _ obstacles "
                          'inindustrial ventures, loss of wealth, gout, disirem '
                          'iro- *ounOiand danger from weapons and fevJr etc., will '
                          'be the results if Mars be associated with or aspected '
                          'by malefics in the g:.rr r: the l2th from the '
                          'Ascendant.',
                 'pdf_page': '221',
                 'ocr_flag': 'HOUSE LIST OCR-DAMAGED: printed "in the g:.rr r: the '
                             'l2th" — the first house number is unreadable. Most '
                             'likely "the 8th or the 12th" by analogy with the '
                             'rest of the chapter, but the glyphs do NOT support '
                             'it. FLAGGED. "danger" also present as a valence '
                             'word.'},
                {'predicate': 'aspected by benefics in a kendra, trikona or the '
                              '11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'fron the lord of the Dasa (Mercury)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Gain of wealth; physical felicity; birth of a son; '
                            'good reputation; affectionate relations with kinsmen.',
                 'source': 'sloka',
                 'quote': '4l-42, There will be gain of wealth, physical felicity, '
                          'birth of a son, good reputation, affectionate relations '
                          'etc., rviih [...] '
                          'kinsmenetc.,ifMarsbeaspectedbybeneficsinkendra,trikona '
                          'or the llth fron the lord of the Dasa (Mercury).',
                 'pdf_page': '221-222',
                 'ocr_flag': 'Protasis printed with all spaces lost '
                             '("ifMarsbeaspectedbybeneficsinkendra,trikona") and '
                             'split across the PDFPAGE 222 break; still '
                             'unambiguous.'},
                {'predicate': 'associated with malefics in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from ths lord *f the Dasa (Mercur,v.l',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'THREE-PART TIME SPLIT. (1) Commencement: distress, '
                            'danger from kinsmen, wrath of the king and fire, '
                            'antagonism with the son, loss of position. (2) MIDDLE '
                            'portion: enjoyments and gains of wealth. (3) End: '
                            'danger from the king (government) and loss of '
                            'position.',
                 'source': 'sloka',
                 'quote': "43-4+i. Il'Mars ite associated with malefies ru the 8th "
                          'or the l2th from ths lord *f the Dasa (Mercur,v.l, '
                          'there will be- (1) Distress, danger from kinsmen, '
                          'wr.ith oi the king and fire, antagonism with the son, '
                          'loss of positiol, at the commence- ment of the '
                          'Antardasa. (2) Enjoyments and gains of wealth in the '
                          'middle ponion of the Antardasa. (3) Danger from the '
                          'king (government) and loss of position at the end"of '
                          'the Antardasa.',
                 'pdf_page': '222',
                 'ocr_flag': '"Il\'Mars ite"=If Mars be; "malefies ru the '
                             '8th"=malefics in the 8th. POLARITY CAVEAT: the '
                             'explicit valence words ("danger", "loss") attach '
                             'only to the FIRST and THIRD sub-periods; the MIDDLE '
                             'sub-period is stated without any valence word and '
                             'lists gains. A single adverse verdict for the whole '
                             'antardasa would misreport the text.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'Fear of premature death.',
                 'source': 'sloka',
                 'quote': '45-46. There n:i!l be fear of premature death if Mars '
                          'bs the lord of the 2nd or th, 7th from the Ascendant.',
                 'pdf_page': '222',
                 'ocr_flag': '"n:i!l"=will, "th, 7th"=the 7th. Frame words are '
                             'UNparenthesised here.'}],
 'maraka': '"45-46. There n:i!l be fear of premature death if Mars bs the lord of '
           'the 2nd or th, 7th from the Ascendant." — here "from the Ascendant" is '
           'NOT parenthesised, i.e. it reads as part of the translated sloka.',
 'remedy': '"The remedial measures to be adopted to obtain relief from the '
           'above.evil effects are Mrityunjaya Japa and giving a cow in charity." '
           '(PDFPAGE 222)'},
    ('mercury', 'mercury'): {'verses': 'vv.1-5 (1-3.5, 4-5)',
 'conditions': [{'predicate': 'in his sign of exaltation "or otherwise"',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Gain of jewels like pearls; learning; increase in '
                            'happiness; performance of pious deeds; success in the '
                            'educational sphere; acquisition of name and fame; '
                            'meeting with new kings (high dignitaries); gain of '
                            'wealth; happiness from wife, children and parents.',
                 'source': 'sloka',
                 'quote': "Gain of jewels like pearls etc., 'learning, increase in "
                          'happiness and perforrnance of pious deeds, s rccess in '
                          'the cducational sphere, acquisition of. name and fame, '
                          'meeting with new kings(high dignitarics), gain of '
                          'wealth, happiness from wife, childrcn and parents will '
                          'bc the effects in the Antardasa of IVercury in lris '
                          "o'wh Dasa, if Mercury be placed in his sign of "
                          'exaltation or otherwise.',
                 'pdf_page': '215',
                 'ocr_flag': '"or otherwise" is vague/possibly damaged — the '
                             'protasis as printed does not delimit what the '
                             'alternative dignity is. Do not resolve.'},
                {'predicate': 'in his sign of debilitation "etc."',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'Loss of wealth and cattle; antagonism with kinsmen; '
                            'diseases like stomach pains; anxiety in discharging '
                            'duties as a government official.',
                 'source': 'sloka',
                 'quote': 'There will be loss of wealth and cattle, antagonism '
                          'with kinsmerr, diseases like stomach pains, anxiety in '
                          'discharging duties as a govcrnment official, if Mercury '
                          'be in his sign of debilitation etc., or be in the 6th, '
                          'the 8th or the l2th from the Ascendant ot be associated '
                          'with rnalefics.',
                 'pdf_page': '215',
                 'ocr_flag': '"debilitation etc." — the "etc." is unresolved in '
                             'the printed text.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'Loss of wealth and cattle; antagonism with kinsmen; '
                            'diseases like stomach pains; anxiety in discharging '
                            'duties as a government official.',
                 'source': 'sloka',
                 'quote': 'if Mercury be in his sign of debilitation etc., or be '
                          'in the 6th, the 8th or the l2th from the Ascendant ot '
                          'be associated with rnalefics.',
                 'pdf_page': '215',
                 'ocr_flag': '"ot be associated" = "or be associated"; "l2th" = '
                             '12th.'},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'Loss of wealth and cattle; antagonism with kinsmen; '
                            'diseases like stomach pains; anxiety in discharging '
                            'duties as a government official.',
                 'source': 'sloka',
                 'quote': 'ot be associated with rnalefics.',
                 'pdf_page': '215',
                 'ocr_flag': '"rnalefics" = malefics.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'Distress to wife; death of members of the family; '
                            'affliction with diseases like rheumatism and stomach '
                            'pains.',
                 'source': 'sloka',
                 'quote': '4-5. Distress to ;ife, death of members of the family, '
                          'afriction with diseases like rheumatism and stomach '
                          'pains etc., will result if the Mercury be the lord of '
                          'the 2nd or the 7th.',
                 'pdf_page': '216',
                 'ocr_flag': '";ife"=wife; "afriction"=affliction. FRAME: the '
                             'parenthetical "(from the Ascendant)" that most other '
                             'maraka clauses in this chapter carry is ABSENT here. '
                             'Recorded as unstated.'}],
 'maraka': '"Distress to ;ife, death of members of the family, afriction with '
           'diseases like rheumatism and stomach pains etc., will result if the '
           'Mercury be the lord of the 2nd or the 7th." — NOTE: unlike every other '
           'cell in this chapter, no "(from the Ascendant)" gloss is attached. '
           'Also note it predicts death of FAMILY MEMBERS, not of the native.',
 'remedy': '"Remedial measure to obtain relief from the above evil efrects, is '
           'recitation of Vishnu Sahasran4ma." (PDFPAGE 216)'},
    ('mercury', 'moon'): {'verses': 'vv.26-35 (26-27, 28-29.5, 30-31.5, 32-33, 34-35)',
 'conditions': [{'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'The yoga becomes very strong for beneficial effects: '
                            'marriage, birth of a son, gain of clothes and '
                            'ornaments.',
                 'source': 'sloka',
                 'quote': "26-27. The yoga becomes very strong for beneficial' "
                          'effects if in the Antardasa of the Moon in the Dasa of '
                          'Mercury" the Moon be in kendra or trikona from the '
                          'Ascendant or be in her sign of exaltation or in her own '
                          'sign associated with or aspected by Jupiter or be a '
                          'yogakaraka herself. Then there will be marriage, birth '
                          'of a Eon and gain of clothes and ornaments-',
                 'pdf_page': '219',
                 'ocr_flag': '"a Eon"=a son. POLARITY NOTE: "beneficial" is the '
                             'ONLY explicitly favourable valence word in the '
                             'entire chapter (it governs three conditions in this '
                             'cell). It is not one of the standard Sanskrit-gloss '
                             'terms (auspicious/subha) but it is an explicit '
                             'valence label in the apodosis, so recorded.'},
                {'predicate': 'in her sign of exaltation, or in her own sign, '
                              'associated with or aspected by Jupiter',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'The yoga becomes very strong for beneficial effects: '
                            'marriage, birth of a son, gain of clothes and '
                            'ornaments.',
                 'source': 'sloka',
                 'quote': 'or be in her sign of exaltation or in her own sign '
                          'associated with or aspected by Jupiter or be a '
                          'yogakaraka herself.',
                 'pdf_page': '219',
                 'ocr_flag': 'AMBIGUOUS SCOPE: "associated with or aspected by '
                             'Jupiter" may qualify only "in her own sign", or the '
                             'whole exaltation/own-sign pair. The printing does '
                             'not settle it.'},
                {'predicate': 'be a yogakaraka herself',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'The yoga becomes very strong for beneficial effects: '
                            'marriage, birth of a son, gain of clothes and '
                            'ornaments.',
                 'source': 'sloka',
                 'quote': 'or be a yogakaraka herself.',
                 'pdf_page': '219',
                 'ocr_flag': ''},
                {'predicate': '"in the circumstances mentioned above" — '
                              'back-reference to the whole vv.26-27 protasis',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Construction of a new house; availability of sweetish '
                            'preparations; enjoyment of music; study of Shastras; '
                            'journey to the South; gains of clothes from beyond '
                            'the seas; gain of gems like pearls.',
                 'source': 'sloka',
                 'quote': '28-29t. In the . circumstances nentioned above, therc '
                          'also be ,:onstruction of a new house, availability of '
                          "sweetish [...] preparation, etrjoyme't of music, study "
                          'of Shastras, journey to the South, gains of clothes '
                          'from beyond the seas, gain of gems like pealls etc.',
                 'pdf_page': '219-220',
                 'ocr_flag': 'An ADDITIVE result-clause with no protasis of its '
                             'own — it inherits whichever of the vv.26-27 '
                             'conditions fired. Frame recorded as unstated because '
                             'the inherited set MIXES from_lagna and not_a_house '
                             'predicates; do not attach a single frame to it. The '
                             'Sanskrit block is interleaved and the English is '
                             'split across the PDFPAGE 220 break.'},
                {'predicate': "in her sign of debilitation or in an enemy's sign",
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical distress.',
                 'source': 'sloka',
                 'quote': '30-31+. There will be physical distress if the Moon be '
                          "in her sign of debilitation or in an enemy's sigir.",
                 'pdf_page': '220',
                 'ocr_flag': '"sigir"=sign. No explicit valence word — "physical '
                             'distress" is a result description, not a valence '
                             'label; polarity left none.'},
                {'predicate': 'in a kendra, trikona, the 3rd or the 11th',
                 'houses': '1,4,7,10,5,9,3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'tiom the lord of the Dasa (l{ercury)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'At the COMMENCEMENT of the antardasa: visits to '
                            'sacred shrines; patience; enthusiasm; gains of wealth '
                            'from foreign countries.',
                 'source': 'sloka',
                 'quote': 'If the Moon be in keudra, trikona, the 3rd or the ilth '
                          'tiom the lord of the Dasa (l{ercury), there will be at '
                          'the conrrllencement of the Antardasa visits to sacred '
                          'shri,res, paticnce, enthusiasm and gains of wealth from '
                          'foreign countries.',
                 'pdf_page': '220',
                 'ocr_flag': '"keudra"=kendra, "ilth"=11th, "tiom"=from, '
                             '"shri,res"=shrines. Note the explicit TIMING '
                             'restriction to the commencement of the antardasa.'},
                {'predicate': 'be weak, and be in the 6th, the 6th[sic] or the '
                              '12th',
                 'houses': '6,8?,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Mcrcury)',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'Danger from the king, fire and thieves; defamation or '
                            'disgrace; loss of wealth on account of wife; '
                            'destruction of agricultural lands and cattle.',
                 'source': 'sloka',
                 'quote': '32-33. Danger from the king, fire and thieves, '
                          'defAmation or disgrace and loss of wealth on account of '
                          'rvife, destruction of a-ericultural lands and '
                          "cattle.etc., u'ill be the results if the Moon be weak, "
                          'anci be in the 6th, the 6th or the l2th from the lord '
                          'of the Dasa (Mcrcury).',
                 'pdf_page': '220',
                 'ocr_flag': 'OCR DAMAGE, HOUSE LIST UNRELIABLE: printed "the 6th, '
                             'the 6th or the l2th" — the second "6th" is almost '
                             'certainly a mis-scan of "8th" (the 6/8/12 dusthana '
                             'triad used everywhere else in this chapter), but the '
                             'printed text says 6th twice. FLAGGED, NOT SILENTLY '
                             'CORRECTED. "loss" is also present as a valence '
                             'word.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': '(frorn rhe Ascendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical distress.',
                 'source': 'sloka',
                 'quote': '34-35. There will be phrsical Cistress if the Moon b-e '
                          'the lord of the 2nd or the Ttir (frorn rhe Ascendant).',
                 'pdf_page': '220',
                 'ocr_flag': '"phrsical Cistress"=physical distress, "Ttir"=7th, '
                             '"frorn rhe"=from the (parenthesised-gloss caveat). '
                             'No death word here, so polarity none.'}],
 'maraka': '"34-35. There will be phrsical Cistress if the Moon b-e the lord of '
           'the 2nd or the Ttir (frorn rhe Ascendant)." — like the Ketu cell, '
           'promises distress, not death.',
 'remedy': '"There will be relief, prolongaticn of longevity and restor- ation of '
           'comforts by the beneiicence of Goddess Durga if the mantras of the '
           "Goddess are recited in the prescribed manner anC clothes are gil'en in "
           'charity." (PDFPAGE 220)'},
    ('mercury', 'rahu'): {'verses': 'vv.47-55 (47-49, 50, 51, 52-53, 54-55)',
 'conditions': [{'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Reverence from the king (government); good '
                            'reputation; gain of wealth; visits to sacred shrines; '
                            'performance of religious sacrifices and oblations; '
                            'recognition; gain of clothes.',
                 'source': 'sloka',
                 'quote': '47-49. Ffects like reversnce from the king '
                          '(government), good reputr.i":n, gain of wealth, visits '
                          'to sacred shrines, per- formance of religious '
                          'sacrifices alrd oblations, recognition, gain of clothes '
                          'etc., are derived in the Antardasa of Rahu in the Dasa '
                          'of Mercury if Rahu be in kendra or trikona from the '
                          'Ascendant or be in Aries, Aquarius, Virgo. or Taurus.',
                 'pdf_page': '223',
                 'ocr_flag': '"Ffects"=Effects, "reversnce"=reverence, '
                             '"reputr.i\\":n"=reputation. Apodosis verb is the '
                             'neutral "are derived".'},
                {'predicate': 'in Aries, Aquarius, Virgo or Taurus (rasi '
                              'placement, not a house)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.47-49 above.',
                 'source': 'sloka',
                 'quote': 'or be in Aries, Aquarius, Virgo. or Taurus.',
                 'pdf_page': '223',
                 'ocr_flag': 'One of very few RASI-specific (not house-specific, '
                             'not dignity-specific) conditions in the chapter.'},
                {'predicate': 'timing rider on the vv.47-49 conditions: the '
                              'commencement of the Antardasa versus later',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'Some evil effects at the commencement of the '
                            'antardasa; all well later.',
                 'source': 'sloka',
                 'quote': 'There will be some evil effects at the commencement of '
                          'the Antardasa but all will be well later.',
                 'pdf_page': '223',
                 'ocr_flag': 'This rider has no protasis of its own and modifies '
                             'the OTHERWISE-favourable-sounding vv.47-49 branch. '
                             'Frame recorded unstated because it inherits a mixed '
                             'from_lagna / not_a_house condition set. "evil" is '
                             'explicit and is the only valence word in the '
                             'vv.47-49 passage.'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from rhc Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss',
                 'results': 'Loss of wealth; rheumatic fever; indigestion.',
                 'source': 'sloka',
                 'quote': '50. Loss of wealth, rheumatic fever, and indigestion '
                          'will be the results if Rahu be in the 8th cr the l2th '
                          'from rhc Ascendant.',
                 'pdf_page': '223',
                 'ocr_flag': '"8th cr the l2th"=8th or the 12th.'},
                {'predicate': 'in the 3rd, the 8th, the 10th or the 11th',
                 'houses': '3,8,10,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'fromthe Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'An opportunity to have conversation or a meeting with '
                            'the king (high dignitaries).',
                 'source': 'sloka',
                 'quote': '51. There will be an opportunity to have conversation '
                          'or a meeting with the king (high dignitaries), if Rahu '
                          'be in the 3rd. the 8th, the 10th or the llth fromthe '
                          'Ascendant.',
                 'pdf_page': '223',
                 'ocr_flag': 'INTERNAL CONFLICT: the 8th from the Ascendant '
                             'appears in BOTH v.50 (loss of wealth, rheumatic '
                             'fever, indigestion) and v.51 (audience with the '
                             'king), with no tie-break stated. The text does not '
                             'resolve it — flag as contested, do not pick one.'},
                {'predicate': 'in that same position, associated with a benefic',
                 'houses': '3,8,10,11',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'A visit to a new king (dignitary).',
                 'source': 'sloka',
                 'quote': 'In this position if Rahu be associated with a benefic, '
                          'there will be a visit to a new king (dignitary).',
                 'pdf_page': '223',
                 'ocr_flag': '"In this position" back-references v.51\'s 3/8/10/11 '
                             'from the Ascendant; the ADDED predicate itself is a '
                             'conjunction condition, not a house condition.'},
                {'predicate': 'associated with a malefic or malefics in the 8th or '
                              'the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'froo the lord of the Dasa (Mercury)',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'Pressure of hard work as a government functionary; '
                            'loss of position; fears; imprisonment; diseases; '
                            'agony to self and kinsmen; heart disease; loss of '
                            'reputation and wealth.',
                 'source': 'sloka',
                 'quote': '52-53. Pressure of hard work as a govemment '
                          'functionary, loss of position, fears, imprisonment, '
                          'diseases, agony to self end kinrmen, heart disease, '
                          'loss of reputation and rvealth, will be the results if '
                          'Rahu be associated with a malefic or malefics foi the '
                          '8th or the l2th froo the lord of the Dasa (Mercury).',
                 'pdf_page': '223',
                 'ocr_flag': '"foi the 8th" = "in the 8th" (mis-scan); '
                             '"froo"=from; "end kinrmen"=and kinsmen.'},
                {'predicate': 'be IN the 2nd or the 6th (placement, not lordship)',
                 'houses': '2,6',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'Fear of premature death.',
                 'source': 'sloka',
                 'quote': '54-55. There will be fear of premature death if Rahu be '
                          'in the 2nd or the 6th from the Ascendant.',
                 'pdf_page': '224',
                 'ocr_flag': 'TWO ANOMALIES, BOTH FLAGGED NOT RESOLVED: (a) the '
                             'predicate is PLACEMENT ("be in"), whereas the other '
                             'maraka clauses in this chapter are LORDSHIP ("be the '
                             'lord of"); (b) the house pair is 2nd/6th, whereas '
                             'every other maraka clause here uses 2nd/7th. Both '
                             'readings are plausible as printed and both are '
                             'plausible as OCR corruption. The text as extracted '
                             'says 2nd and 6th.'}],
 'maraka': '"54-55. There will be fear of premature death if Rahu be in the 2nd or '
           'the 6th from the Ascendant." — STRUCTURALLY DIFFERENT from every other '
           'maraka clause in this chapter: it is a PLACEMENT ("be in"), not a '
           'LORDSHIP, and the second house is the 6th, not the 7th.',
 'remedy': '"The remedial measures to obtain relief from the above evil effects, '
           'are recitation of mantras of Goddess Durga and Goddess Lakshmi in the '
           'prescribed manner and giving a tawny coloured cow or female buffalo in '
           'charity." (PDFPAGE 224)'},
    ('mercury', 'saturn'): {'verses': 'vv.67-72 (67-68.5, 69-70.5, 71-72)',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Well being in the family; acquisition of a kingdom '
                            '(attainment of a high position in government); '
                            'enthusiasm; increase in cattle wealth; gain of '
                            'position; visits to sacred shrines.',
                 'source': 'sloka',
                 'quote': '!;7-65+. Effccts iike wel being in the family, '
                          'acquisition o{a kingdcir: (attainment of a bigh '
                          'position in government)o enthusiasm, increase in cattle '
                          'wealth, gain of positi,on, viSits tosacred shrines '
                          'ctc., rvill be deriled in the Antardasa of Saturn in '
                          'the Dasa of Mercury, if Saiurn be jn his sign of '
                          'exaltation, in his own sign, or in keqdra, trikona or '
                          'the llth from the Ascendant.',
                 'pdf_page': '226',
                 'ocr_flag': 'Verse label mis-scanned as "!;7-65+" — from context '
                             'this is 67-68.5. "Effccts iike wel being", "o{a '
                             'kingdcir:", "rvill be deriled" are OCR damage. '
                             'Apodosis verb is the neutral "will be derived".'},
                {'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Same list as vv.67-68.5 above.',
                 'source': 'sloka',
                 'quote': 'if Saiurn be jn his sign of exaltation, in his own '
                          'sign, or in keqdra, trikona or the llth from the '
                          'Ascendant.',
                 'pdf_page': '226',
                 'ocr_flag': '"keqdra"=kendra.'},
                {'predicate': 'in the 8th(?) or the 12th',
                 'houses': '8?,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa(Mercurl)',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'Danger from enemies; distress to wife and children; '
                            'loss of thinking power; loss of kinsmen; loss in '
                            'ventures; mental agony; journeys to foreign lands; '
                            'bad dreams.',
                 'source': 'sloka',
                 'quote': '69-70*. Danger from enemies, distress to wife and '
                          'children, loss of thinking power, loss of kinsmen, loss '
                          'in ventures, mental lgony, journeys to foreign lands, '
                          'bad dreams, will be the results,if Saturn be in the sth '
                          'or the l2th from the lord of the Dasa(Mercurl).',
                 'pdf_page': '226',
                 'ocr_flag': 'HOUSE NUMBER OCR-DAMAGED: printed "the sth or the '
                             'l2th". "sth" is most likely 8th (matching the 8/12 '
                             'dasa-lord pair used in the Ketu, Mars, Rahu and '
                             'Jupiter cells) but it could read 5th. FLAGGED, NOT '
                             'RESOLVED. "loss" also present as a valence word.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from tfr" ar"."nJunt- [= from the Ascendant]',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'Fear of premature death.',
                 'source': 'sloka',
                 'quote': '7l-72. There will be fear of prematore death if Saturn '
                          'be the lord of the 2nd or the Zth from tfr" ar"."nJunt- '
                          '\'i --\'-^" "\' .',
                 'pdf_page': '226',
                 'ocr_flag': '"prematore"=premature, "the Zth"=the 7th, "tfr\\" '
                             'ar\\".\\"nJunt-"=the Ascendant (the letter skeleton '
                             'matches). Frame recorded from_lagna on that '
                             'reconstruction; flagged.'}],
 'maraka': '"7l-72. There will be fear of prematore death if Saturn be the lord of '
           'the 2nd or the Zth from tfr\\" ar\\".\\"nJunt-" — i.e. "the lord of '
           'the 2nd or the 7th from the Ascendant", the last words badly '
           'OCR-mangled but reconstructible.',
 'remedy': '"The remedial rneasures to obtain relief from the above evil \'.I:rt '
           '::1 to regain. sountl health, are performanc of Mrityun- Jdva . Japa '
           'and giving a black cow and female buffalo in cnarltv." — i.e. '
           'Mrityunjaya Japa and giving a black cow and female buffalo in charity '
           '(PDFPAGE 226)'},
    ('mercury', 'sun'): {'verses': 'vv.20-25 (20-22, 23-24, 25)',
 'conditions': [{'predicate': 'in his own sign or sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Dawn of fortune by the beneficence of the king (high '
                            'government officials); happiness from friends.',
                 'source': 'sloka',
                 'quote': "2A'22. Effccts like dawn of fortune by thc beneficence "
                          "of' tltc king (higlr goveiltment officials),,happiness "
                          'from friends etc" will be derived in the Antardasa of '
                          'the Sun in the Dasa of Mercury, if the Sun is in his '
                          'own sign or sign of exaltation or in kendra, trikona, '
                          'the 2nd or the llth, in exalted or own Navamsai',
                 'pdf_page': '218',
                 'ocr_flag': '"Effccts", "goveiltment", "Navamsai" OCR damage.'},
                {'predicate': 'in a kendra, trikona, the 2nd or the 11th',
                 'houses': '1,4,7,10,5,9,2,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Dawn of fortune by the beneficence of the king (high '
                            'government officials); happiness from friends.',
                 'source': 'sloka',
                 'quote': 'if the Sun is in his own sign or sign of exaltation or '
                          'in kendra, trikona, the 2nd or the llth, in exalted or '
                          'own Navamsai',
                 'pdf_page': '218',
                 'ocr_flag': 'CRITICAL FRAME GAP: no reference point is printed '
                             'for "kendra, trikona, the 2nd or the llth". Neither '
                             '"from the Ascendant" nor "from the lord of the Dasa" '
                             'appears anywhere in vv.20-22. Recorded as unstated — '
                             'do NOT infer. This is the single most consequential '
                             'unstated frame in the chapter.'},
                {'predicate': 'in exalted or own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Dawn of fortune by the beneficence of the king (high '
                            'government officials); happiness from friends.',
                 'source': 'sloka',
                 'quote': 'in exalted or own Navamsai',
                 'pdf_page': '218',
                 'ocr_flag': 'AMBIGUOUS CONJUNCTION: not printed whether the '
                             'Navamsa clause is a further alternative in the "or" '
                             'chain or an added requirement conjoined to the '
                             'preceding clauses. Text does not settle.'},
                {'predicate': 'aspected by Mars',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Acquisition of land.',
                 'source': 'sloka',
                 'quote': 'There will be acquisition of land if the Sun is '
                          'aspected by Mars',
                 'pdf_page': '218',
                 'ocr_flag': ''},
                {'predicate': 'aspected by the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Comforts of good food and clothes.',
                 'source': 'sloka',
                 'quote': 'and comforts of good food and clothes if such a Sun be '
                          "aspected by the lord of the Ascendant'",
                 'pdf_page': '218',
                 'ocr_flag': '"such a Sun" back-references the vv.20-22 protasis; '
                             'the scope of that back-reference is not spelled '
                             'out.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascenclant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Fear or danger from thieves, fire and weapons; '
                            'bilious troubles; headaches; mental agony; separation '
                            'from friends.',
                 'source': 'sloka',
                 'quote': "23-24. Fear or danger from thieve!' fire and weepons, "
                          'bilio-is troubles, headaches, mental agony and '
                          'separation from friends ctc., will be the results if '
                          "the sun be in the 6th'-the 8tb or the 12th from the "
                          'Ascenclant or thc lord of the Dasa (Mcrcury), be weak '
                          'and be associated with Saturn, Mars and Rahu.',
                 'pdf_page': '219',
                 'ocr_flag': '"thieve!\'", "weepons", "bilio-is", "8tb", '
                             '"Ascenclant", "Mcrcury" OCR damage.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or thc lord of the Dasa (Mcrcury)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Fear or danger from thieves, fire and weapons; '
                            'bilious troubles; headaches; mental agony; separation '
                            'from friends.',
                 'source': 'sloka',
                 'quote': "will be the results if the sun be in the 6th'-the 8tb "
                          'or the 12th from the Ascenclant or thc lord of the Dasa '
                          '(Mcrcury), be weak and be associated with Saturn, Mars '
                          'and Rahu.',
                 'pdf_page': '219',
                 'ocr_flag': 'DUAL-FRAME clause: the SAME house set is offered '
                             'from EITHER the Ascendant OR the Dasa lord, '
                             'disjunctively, in one sentence. Recorded as two '
                             'conditions.'},
                {'predicate': 'be weak and be associated with Saturn, Mars and '
                              'Rahu',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Fear or danger from thieves, fire and weapons; '
                            'bilious troubles; headaches; mental agony; separation '
                            'from friends.',
                 'source': 'sloka',
                 'quote': 'be weak and be associated with Saturn, Mars and Rahu.',
                 'pdf_page': '219',
                 'ocr_flag': 'AMBIGUOUS: printed with a comma, so it is unsettled '
                             'whether weakness + malefic association are '
                             'ADDITIONAL REQUIREMENTS on the house placement or '
                             'further alternatives. Also unsettled whether '
                             '"Saturn, Mars and Rahu" is conjunctive (all three) '
                             'or a list of alternatives.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': '(lrom the Ascendant)',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'Fear of premature death.',
                 'source': 'sloka',
                 'quote': '25. There will be fear of premature death if the Sun be '
                          'the lord of the 2nd or the 7tb (lrom the Ascendant).',
                 'pdf_page': '219',
                 'ocr_flag': '"lrom"=from; parenthesised-gloss caveat as '
                             'elsewhere.'}],
 'maraka': '"25. There will be fear of premature death if the Sun be the lord of '
           'the 2nd or the 7tb (lrom the Ascendant)."',
 'remedy': '"Worship of the Sun is the remedial measure tr; obtain relief from the '
           'above evil effects." (PDFPAGE 219)'},
    ('mercury', 'venus'): {'verses': 'vv.13-19 (13-15.5, 16-17.5, 18-19)',
 'conditions': [{'predicate': 'in a kendra, the 11th, the 5th or the 9th',
                 'houses': '1,4,7,10,11,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Inclination to perform religious rites; fulfilment of '
                            'all ambitions through the help of the king '
                            '(government) and friends; gains of agricultural lands '
                            'and happiness.',
                 'source': 'sloka',
                 'quote': 'l3-15;. Effects like inclination to perforrn religious '
                          "rites, fulfilme't of all ambitions through the help of "
                          'the kin; (govern- ment) and friends, gains of '
                          'agricultural lands and happincss etc., will be derived '
                          'in the Antardasa of venus in the Dasa of Mercury, if '
                          'Venus be in kendra, the llth, the 5th or the 9th from '
                          'the Ascendant.',
                 'pdf_page': '217',
                 'ocr_flag': '"perforrn", "fulfilme\'t", "the kin;", "happincss" '
                             'OCR damage. Apodosis verb is the neutral "will be '
                             'derived".'},
                {'predicate': 'in a kendra, the 5th, the 9th or the 11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Mercury)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Acquisition of a kingdom (attainment of a high '
                            'position in government); gain of wealth and property; '
                            'construction of a reservoir; readiness to give '
                            'charities and performance of religious rites; '
                            'extraordinary gains of wealth and gains in business.',
                 'source': 'sloka',
                 'quote': 'There will be acquisition of a kingdom(attainment of a '
                          'high position in government), gain of w-ealth and '
                          'property, canstruction of a reservoir, readiness to '
                          'give charities and performance of religious rites, '
                          'extraordinary gains of wealth and gains in business, if '
                          'Venus be in kendra, the 5th, the 9th or the llth from '
                          'the lord of the Dasa (Mercury).',
                 'pdf_page': '217',
                 'ocr_flag': '"canstruction" = construction.'},
                {'predicate': 'be weak in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'fromthe lord ci the Dasa',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Heart disease; defamation; fevers; dysentery; '
                            'separation from kinsmen; physical distress and agony.',
                 'source': 'sloka',
                 'quote': '16-171. Heart disease, defamation, fevers, dysentry, '
                          "sep3ratioll from kinsmen, pltl'sicrl distless and agony "
                          "will result if Venus be u'eak rrt tite 6th, the Sth or "
                          'the 12th fromthe lord ci the Dasa.',
                 'pdf_page': '218',
                 'ocr_flag': 'Heavily damaged: "u\'eak rrt tite 6th, the '
                             'Sth"="weak in the 6th, the 8th"; "ci the Dasa"="of '
                             'the Dasa". This is the ONLY dasa-lord frame in the '
                             'chapter stated WITHOUT the "(Mercury)" gloss. '
                             'Despite the adverse-sounding outcome list, NO '
                             'explicit valence word appears — polarity left none.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the Ascendant)',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'Fear of premature death.',
                 'source': 'sloka',
                 'quote': 'iB-19. There uill be fear of premature death if Venus '
                          'be th* lord of the 2nd or the 7th (from the Ascendant).',
                 'pdf_page': '218',
                 'ocr_flag': 'FRAME CAVEAT: "(from the Ascendant)" is '
                             'parenthesised — likely an editorial gloss, not sloka '
                             'words.'}],
 'maraka': '"iB-19. There uill be fear of premature death if Venus be th* lord of '
           'the 2nd or the 7th (from the Ascendant)."',
 'remedy': '"The remeclial measure to obtain relief from the above evil effects is '
           'to recite mantras of Goddess Durga." (PDFPAGE 218)'},
    ('moon', 'jupiter'): {'verses': '22-31',
 'conditions': [{'predicate': 'in kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'to th€ Ascendant',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'Acquisition of a kingdom (attainment of a high '
                            'position in government), auspicious celebrations at '
                            'home, gains of clothes and ornaments, recognition '
                            'from the king (government), beneficence of the Ishta '
                            'lord, gains of wealth, land, conveyances, success in '
                            'all ventures by the beneficence of the king '
                            '(government)',
                 'source': 'sloka',
                 'quote': 'witl be the beneficial effects in the Antardasa ,f '
                          'Jupiter in the Dasa of the Moon . !f Jupiter be posited '
                          'in ... kendra or trikona to th€ Ascendant, be in his '
                          'own sign or in his slgn of exaltation.',
                 'pdf_page': '152-153',
                 'ocr_flag': 'The protasis is split across the page break at '
                             'PDFPAGE 153 with Sanskrit interleaved; the words '
                             '"kendra or trikona to the Ascendant" begin page 153. '
                             '"th€" for "the", "slgn" for "sign".'},
                {'predicate': 'in his own sign or in his sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'same beneficial list as above',
                 'source': 'sloka',
                 'quote': 'kendra or trikona to th€ Ascendant, be in his own sign '
                          'or in his slgn of exaltation.',
                 'pdf_page': '153',
                 'ocr_flag': ''},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'Destruction of preceptor (and father etc.) and '
                            'children, loss of position, mental agony, quarrels, '
                            'destruction of house, conveyances and agricultural '
                            'land',
                 'source': 'sloka',
                 'quote': 'will be the evil effects in his Antardasa, if Jupiter '
                          'be in the 6th, the 8th or the l2th, combust, in his '
                          'sign of debilitation or be associated with malefics.',
                 'pdf_page': '153',
                 'ocr_flag': 'No frame stated, in direct contrast to the '
                             'from-Ascendant frame stated two verses earlier.'},
                {'predicate': 'combust, in his sign of debilitation, or associated '
                              'with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'same evil list as above',
                 'source': 'sloka',
                 'quote': 'combust, in his sign of debilitation or be associated '
                          'with malefics.',
                 'pdf_page': '153',
                 'ocr_flag': ''},
                {'predicate': 'in the 3rd or 11th',
                 'houses': '3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'frdm the lord of the Dasa (the Moon)',
                 'polarity': 'favourable',
                 'polarity_word': 'favourable',
                 'results': 'Gains of cattle, grains, clothes and happiness from '
                            'brothers, acquisition of property, valour, patience, '
                            'oblations, celebrations like marriage etc., gain of a '
                            'kingdom (attainment of a high position in government)',
                 'source': 'sloka',
                 'quote': 'will be the favourable effects, if Jupiter be in 3rd or '
                          'llth frdm the lord of the Dasa (the Moon).',
                 'pdf_page': '153',
                 'ocr_flag': '"frdm" for "from"'},
                {'predicate': 'weak and in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_moon',
                 'frame_quote': 'from the Moon',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'unpalatable food, journeys to places away from the '
                            'homeland',
                 'source': 'sloka',
                 'quote': 'Effects like unpalatable food, journeys to places away '
                          'from the homeland,- will be derived, if Jupiter be weak '
                          'and be in the 6th, the 8th or the l2th from the Moon.',
                 'pdf_page': '153-154',
                 'ocr_flag': 'The chapter says "from the Moon" here but "from the '
                             'lord of the Dasa (the Moon)" elsewhere. Recorded as '
                             'from_moon on the literal wording; the two phrasings '
                             'are NOT collapsed by this pass even though the Dasa '
                             'lord is the Moon. Neutral verb "will be derived" — '
                             'no valence word.'},
                {'predicate': '(none — unconditional timing statement, no '
                              'protasis)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'good effects at the commencement, distress at the end',
                 'source': 'sloka',
                 'quote': 'There will be good effects at the @mmencement of the '
                          'Antardasa and distress at its end.',
                 'pdf_page': '153',
                 'ocr_flag': '"@mmencement". No condition attached — must never be '
                             'fired as a rule. Contains both a positive and a '
                             'negative term, so no single polarity is recorded.'},
                {'predicate': 'lord of the 2nd or 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'prematurc death',
                 'results': 'premature death',
                 'source': 'sloka',
                 'quote': 'There will be prematurc death if Jupiter be the lord of '
                          '2nd or ?th from the Ascendant.',
                 'pdf_page': '154',
                 'ocr_flag': '"prematurc", "?th" for "7th". This is the ONLY '
                             '2nd/7th-lordship clause in the chapter that states '
                             'its frame.'}],
 'maraka': 'There will be prematurc death if Jupiter be the lord of 2nd or ?th '
           'from the Ascendant.',
 'remedy': 'Remedial measures for obtaining relief from the above evil effects are '
           'recitation of Shiva Sahasranam Japa (fua iI(Fa ;ilrT wr) and giving '
           'gold iu charity.'},
    ('moon', 'ketu'): {'verses': '47-52',
 'conditions': [{'predicate': 'in a kendra, trikona or the 3rd, and endowed with '
                              'strength',
                 'houses': '1,4,7,10,5,9,3',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of wealth, enjoyment, happiness to wife and '
                            'children, religious inclination etc.; with some loss '
                            'of wealth at the commencement of the Antardasa, and '
                            'all well later',
                 'source': 'sloka',
                 'quote': 'will arise in the Antardasa of Ketu in the t)asa of the '
                          'Moon, if Ketu be in a kendra, trikona or the 3rd from '
                          'the Ascendant and be endowed rvith strength. There will '
                          'tre somp loss of wr ;i:a al the commencernent of the '
                          'Antardase. Later all will be weli.',
                 'pdf_page': '156-157',
                 'ocr_flag': '"t)asa", "rvith", "tre somp loss of wr ;i:a" for "be '
                             'some loss of wealth", "Antardase", "weli". Neutral '
                             'verb "will arise" — no valence word on the main '
                             'branch; the word "loss" appears only in the '
                             'unconditional commencement rider, not in the '
                             'protasis-governed result, so no polarity is '
                             'recorded.'},
                {'predicate': 'in kendra, the 9th, the 5th or the 11th, and '
                              'equipped with strength',
                 'houses': '1,4,7,10,9,5,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the loir! of the Dasa (the Moon)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Gain of wealth, cattle etc.; with loss of wealth at '
                            'the end of the Antardasa',
                 'source': 'sloka',
                 'quote': "Gain of u'ealth, cattle etc., will be the -,ieers if "
                          'Ketu be in kendra, gth, 5th or I lth from the loir! of '
                          'the Dasa (the Moon) and be equipped with strength. '
                          'There will be loss of wgalth at the end of thc '
                          'AntarCasa.',
                 'pdf_page': '157',
                 'ocr_flag': 'SEVERE: the result noun is destroyed — "will be the '
                             '-,ieers if". "gth" read as 9th, "I lth" as 11th, '
                             '"loir!" for "lord", "wgalth", "AntarCasa". An '
                             'UNNUMBERED fragment follows ("Effects like '
                             'acquisition of a kingdom..., gain of clothes, '
                             'ornaments, cattle,") with no protasis — not recorded '
                             'as a condition.'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (the Moou)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'obstacles in ventures due to interference by enemies, '
                            'and quarrels',
                 'source': 'sloka',
                 'quote': 'There will be obstacles in ventures due to '
                          'inter-ference by erremies and quarrels, if Ketri be in '
                          'the gttr or itre l2th from the lord of the Dasa (the '
                          "Moou) or be aspected by or'associated with malefics.",
                 'pdf_page': '157',
                 'ocr_flag': '"gttr" read as 8th and "itre l2th" as the 12th from '
                             'the parallel 8/12 pattern — the digits themselves '
                             'are destroyed. "erremies", "Ketri", "Moou". No '
                             'explicit valence word: "obstacles" is not one of the '
                             "chapter's valence labels."},
                {'predicate': 'aspected by or associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as above',
                 'source': 'sloka',
                 'quote': "or be aspected by or'associated with malefics.",
                 'pdf_page': '157',
                 'ocr_flag': ''},
                {'predicate': 'in the 2nd or 7th (placement, not lordship)',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger of affliction of the body with diseases',
                 'source': 'sloka',
                 'quote': 'If Ketu be in the 2nd or ?tn tu"." will be danger of '
                          'afriction of the body with diseases.',
                 'pdf_page': '157',
                 'ocr_flag': '"?tn tu\\".\\"" for "7th there"; "afriction" for '
                             '"affliction". Placement, not lordship.'}],
 'maraka': 'If Ketu be in the 2nd or 7th there will be danger of affliction of the '
           'body with diseases. — NOTE: PLACEMENT, not lordship, and the result is '
           'disease, not death.',
 'remedy': 'Mrityunjaya Japa will give relief in all the evil effects and will '
           'ensure gain of wealth and property with the beneficience of lord '
           'Shiva.'},
    ('moon', 'mars'): {'verses': '7-12',
 'conditions': [{'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'favourable',
                 'results': 'Advancement of fortune, recognition by government, '
                            'gain of clothes and ornaments, success in all '
                            'efforts, increase in agricultural production and '
                            'prosperity at home, profits in business',
                 'source': 'sloka',
                 'quote': 'will be the favourable effects of the Antardasa of Mals '
                          'in the Dasa o[ the Moon, if Mars be in a kendra dr '
                          'trikona.',
                 'pdf_page': '150',
                 'ocr_flag': '"Mals" for "Mars"; "kendra dr trikona" for "kendra '
                             'or trikona"'},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Great happiness and enjoyment of comforts',
                 'source': 'sloka',
                 'quote': 'Great happiness and enjoyrnent of comforts will be '
                          'derived if Mars be in his sign of exaltation or in his '
                          'cwn sign.',
                 'pdf_page': '150',
                 'ocr_flag': '"cwn" for "own". Neutral verb "will be derived" — no '
                             'valence word.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'Distress to body, losses at home and in agricultural '
                            'production, losses in business dealings, antagonism '
                            'or adverse relations with servants (employees) and '
                            'the king (government), separation from kinsmen and '
                            'hot temperament',
                 'source': 'sloka',
                 'quote': 'will be the evil efrects in the Antardasa of Mars, if '
                          'he be posited in the 6th, the Sth or the l2th from the '
                          'Ascendant.',
                 'pdf_page': '150-151',
                 'ocr_flag': '"Sth" for "8th", "l2th" for "12th", "efrects" for '
                             '"effects"'},
                {'predicate': 'associated with or aspected by malefics in the 6th, '
                              'the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the Iord of the Dasa (the Moon)',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'same evil list as above',
                 'source': 'sloka',
                 'quote': 'be associated with or aspected by malefics in the 6th, '
                          'the Sth or the l2th from the Iord of the Dasa (the '
                          'Moon).',
                 'pdf_page': '151',
                 'ocr_flag': 'CRITICAL: a stray full stop precedes "be associated" '
                             '— the printed text reads "...from the Ascendant. be '
                             'associated with...". Whether this is an alternative '
                             '(or) or a conjunctive (and) with the preceding '
                             'from-Ascendant condition is NOT settled by the '
                             'text.'}],
 'maraka': None,
 'remedy': None},
    ('moon', 'mercury'): {'verses': '39-46',
 'conditions': [{'predicate': 'in kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of wealth, recognition by the king '
                            '(government), gain of clothes etc., discussions on '
                            'Shastras (religious scriptures), gain of knowledge '
                            'from society with learned and holy people, '
                            'enjoyments, birth of children, satisfaction, profits '
                            'in business, acquisition of conveyances and ornaments '
                            'etc.',
                 'source': 'sloka',
                 'quote': "will be experienced i' the Antardasa of Mercury in the "
                          "Dasa of the Mo'n, if Mercury be in kendra or trikont, "
                          'in his own sign, in bis own Navamsa, in his sign or '
                          'exaiiat,,., cndowed with strength.',
                 'pdf_page': '155',
                 'ocr_flag': '"kendra or trikont", "Mo\'n", "in his sign or '
                             'exaiiat,,.," for "in his sign of exaltation", '
                             '"cndowed". Neutral verb "will be experienced" — no '
                             'valence word. NO frame stated here, in contrast to '
                             'the from-Ascendant frame stated in the Saturn cell '
                             'three verses earlier.'},
                {'predicate': 'in his own sign, in his own Navamsa, in his sign of '
                              'exaltation, endowed with strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as above',
                 'source': 'sloka',
                 'quote': 'in his own sign, in bis own Navamsa, in his sign or '
                          'exaiiat,,., cndowed with strength.',
                 'pdf_page': '155',
                 'ocr_flag': '"exaiiat,,.," — the word "exaltation" is materially '
                             'damaged.'},
                {'predicate': 'in kendra or trikona, the 11th or the 2nd',
                 'houses': '1,4,7,10,5,9,11,2',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (the Moon)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'marriage, oblations, charities, performance of '
                            'religious rites, close relations with the king '
                            '(government), social contacts with men of learning, '
                            'acquisition of pearls, corals, Mani (jewels), '
                            'conveyances, clothes, ornaments, good health, '
                            'affections, enjoyments, drinking of Soma rasa and '
                            'other tasty syrups etc.',
                 'source': 'sloka',
                 'quote': 'will be derived in the Antardasa of Mercury, if he be '
                          "in kendra or trikoti;', the llth or the 2nd from the "
                          'lord of the Dasa (the Moon).',
                 'pdf_page': '155-156',
                 'ocr_flag': '"trikoti;\'" for "trikona". Neutral verb "will be '
                             'derived". NOTE: the 2nd is a FAVOURABLE-listed house '
                             'here while the 2nd is an affliction house in the '
                             'Saturn cell — the chapter does not reconcile this.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'irom the lord of the Dasa (the Moon)',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'Pains in the body, loss in agricultural ventures, '
                            'imprisonment, distress to wife and children',
                 'source': 'sloka',
                 'quote': 'will be the inauspicious effects, if Mercury be in the '
                          '6th, the 8th or the 12th irom the lord of the Dasa (the '
                          'Moon) or be in his sign of debilitation.',
                 'pdf_page': '156',
                 'ocr_flag': '"irom" for "from", "ventureg" for "ventures", '
                             '"imprisonmen!" for "imprisonment"'},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'same inauspicious list as above',
                 'source': 'sloka',
                 'quote': 'or be in his sign of debilitation.',
                 'pdf_page': '156',
                 'ocr_flag': ''},
                {'predicate': 'lord of the 2nd or 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'fear of fever',
                 'source': 'sloka',
                 'quote': 'If Mercury be the lord of the 2nd or 7th, there will be '
                          'fear of fever.',
                 'pdf_page': '156',
                 'ocr_flag': '2nd/7th lordship form but NO death and NO valence '
                             'word — result is fever only. Frame not stated.'}],
 'maraka': 'If Mercury be the lord of the 2nd or 7th, there will be fear of fever. '
           '— NOTE: this is a 2nd/7th-lordship clause whose stated result is '
           'FEVER, not death. It must not be treated as a maraka death verdict.',
 'remedy': 'The remedial measures to be adopted for obtaining relief from the evil '
           'effects, are recitation of Vishnu Sahasra Nam and giving a goat in '
           'charity.'},
    ('moon', 'moon'): {'verses': '1-6',
 'conditions': [{'predicate': 'in her sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'Acquisition of horses, elephants and clothes, '
                            'devotion to deities and preceptor, recitation of '
                            'religious songs in praise of God, acquisition of a '
                            'kingdom (attainment of a high position in '
                            'government), extreme happiness and enjoyment and name '
                            'and fame',
                 'source': 'sloka',
                 'quote': 'will be the beneflcial results in the Antardasa of the '
                          'Moon in her own Dasa, if she be posited in her sigh of '
                          'exaltation, her own sign, in a kendra or trikona or bc '
                          'isso-ciated with the r..,rd of the 9th or the loth.',
                 'pdf_page': '149',
                 'ocr_flag': '"sigh of exaltation" for "sign"; "bc isso-ciated '
                             'with the r..,rd" for "be associated with the lord"'},
                {'predicate': 'in her own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'same beneficial list as above',
                 'source': 'sloka',
                 'quote': 'if she be posited in her sigh of exaltation, her own '
                          'sign, in a kendra or trikona or bc isso-ciated with the '
                          'r..,rd of the 9th or the loth.',
                 'pdf_page': '149',
                 'ocr_flag': ''},
                {'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'same beneficial list as above',
                 'source': 'sloka',
                 'quote': 'if she be posited in her sigh of exaltation, her own '
                          'sign, in a kendra or trikona or bc isso-ciated with the '
                          'r..,rd of the 9th or the loth.',
                 'pdf_page': '149',
                 'ocr_flag': ''},
                {'predicate': 'associated with the lord of the 9th or the 10th',
                 'houses': '9,10',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'same beneficial list as above',
                 'source': 'sloka',
                 'quote': 'or bc isso-ciated with the r..,rd of the 9th or the '
                          'loth.',
                 'pdf_page': '149',
                 'ocr_flag': '"loth" for "10th"; the house from which the 9th/10th '
                             'is reckoned is never stated'},
                {'predicate': 'in her sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'Loss of wealth, loss of position, lethargy, agony, '
                            'antagonism towards the king and ministers, distress '
                            'to mother, imprisonment and loss of kinsmen',
                 'source': 'sloka',
                 'quote': 'will be the evil effects in her Antardasa, if the Moon '
                          'be in her sign of debilitation, be associated with '
                          'malefics or be in the 6th, the 8th or the 12th.',
                 'pdf_page': '149-150',
                 'ocr_flag': ''},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'same evil list as above',
                 'source': 'sloka',
                 'quote': 'if the Moon be in her sign of debilitation, be '
                          'associated with malefics or be in the 6th, the 8th or '
                          'the 12th.',
                 'pdf_page': '149-150',
                 'ocr_flag': ''},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'same evil list as above',
                 'source': 'sloka',
                 'quote': 'if the Moon be in her sign of debilitation, be '
                          'associated with malefics or be in the 6th, the 8th or '
                          'the 12th.',
                 'pdf_page': '149-150',
                 'ocr_flag': 'no reference frame given for 6/8/12 anywhere in this '
                             'verse group'},
                {'predicate': 'lord of the 2nd or 7th, or associated with the lord '
                              'of the 8th or the 12th',
                 'houses': '2,7,8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger of premature death',
                 'results': 'pains in the body and danger of premature death',
                 'source': 'sloka',
                 'quote': 'If the Moon be the lord of the 2nd or 7th, or be '
                          'associated with the lord of the 8th or tne l2th, there '
                          'will be pains in the body and danger of premature '
                          'death.',
                 'pdf_page': '150',
                 'ocr_flag': '"tne l2th" for "the 12th"'}],
 'maraka': 'If the Moon be the lord of the 2nd or 7th, or be associated with the '
           'lord of the 8th or tne l2th, there will be pains in the body and '
           'danger of premature death.',
 'remedy': 'The remedial measures are giving in ctrarity of a tawny coloured cow '
           'or female buffalo.'},
    ('moon', 'rahu'): {'verses': '13-21',
 'conditions': [{'predicate': 'in a kendra or trikona — commencement phase',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'some auspicious results at the commencement of the '
                            'Antardasa',
                 'source': 'sloka',
                 'quote': 'There will be sorne auspicious results at the '
                          'Jommencement of the Antardasa of Rahu in the Dasa of '
                          'the Moon but later there will be danger from the king '
                          '(government), tirieves and snakes, distress to cattle, '
                          'loss of kinsmen and friends, loss of reputation and '
                          'mental agony, if Rahu be posited in a kendra or '
                          'trikona.',
                 'pdf_page': '151',
                 'ocr_flag': 'Same protasis as the next row — one condition with '
                             'two phases, split here only so neither polarity is '
                             'lost.'},
                {'predicate': 'in a kendra or trikona — later phase',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger from the king (government), thieves and '
                            'snakes, distress to cattle, loss of kinsmen and '
                            'friends, loss of reputation and mental agony',
                 'source': 'sloka',
                 'quote': 'but later there will be danger from the king '
                          '(government), tirieves and snakes, distress to cattle, '
                          'loss of kinsmen and friends, loss of reputation and '
                          'mental agony, if Rahu be posited in a kendra or '
                          'trikona.',
                 'pdf_page': '151',
                 'ocr_flag': '"tirieves" for "thieves"'},
                {'predicate': 'aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Success in all ventures, gain of conveyances, '
                            'garments etc., from the king (government) etc., in '
                            'the South-West direction',
                 'source': 'sloka',
                 'quote': 'will.be derived if Rahu in his Antardasa be aspected by '
                          'benefics, be in the 3rd, the 6th, the l0th, rhe llth or '
                          'be rssociated with a Yogakaraka planet.',
                 'pdf_page': '151',
                 'ocr_flag': 'Neutral verb "will be derived" — no valence word.'},
                {'predicate': 'in the 3rd, the 6th, the 10th or the 11th',
                 'houses': '3,6,10,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as above',
                 'source': 'sloka',
                 'quote': 'be in the 3rd, the 6th, the l0th, rhe llth or be '
                          'rssociated with a Yogakaraka planet.',
                 'pdf_page': '151',
                 'ocr_flag': '"l0th" / "rhe llth" / "rssociated". No frame '
                             'stated.'},
                {'predicate': 'associated with a Yogakaraka planet',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as above',
                 'source': 'sloka',
                 'quote': 'or be rssociated with a Yogakaraka planet.',
                 'pdf_page': '151',
                 'ocr_flag': ''},
                {'predicate': 'weak and in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa ( the Moon)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Loss of position, mental agony, distress to wife and '
                            'children, danger of diseases, danger from the king '
                            '(government), scorpions and snakes etc.',
                 'source': 'sloka',
                 'quote': 'Loss of position, . mental agony, distress to rivife '
                          'and children, danger of diseases, danger from the king '
                          '(government), scorpions and snakes etc., will bappen if '
                          'Rahu be weak and be in the 8th or the t2th from the '
                          'lord of the Dasa ( the Moon).',
                 'pdf_page': '151-152',
                 'ocr_flag': '"rivife" for "wife"; "bappen" for "happen"; "t2th" '
                             'for "12th". English text is split across a page '
                             'break with Sanskrit interleaved.'},
                {'predicate': 'in kendra, trikona, 3rd or 11th',
                 'houses': '1,4,7,10,5,9,3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (the Moon)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Pilgrimage to holy places, visits to sacred shrines, '
                            'beneficence, inclination towards charitable deeds '
                            'etc.',
                 'source': 'sloka',
                 'quote': 'will be the results, if Rahube in kendra, trikona,3rd '
                          'or llth from the lord of the Dasa (the Moon).',
                 'pdf_page': '152',
                 'ocr_flag': '"Rahube" run together. Neutral "will be the results" '
                             '— no valence word.'},
                {'predicate': 'in the 2nd or 7th (placement, not lordship)',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'body troubles (physical afflictions)',
                 'source': 'sloka',
                 'quote': 'There will be body troubles (physical affiictions), if '
                          'Rahu be in the 2nd or 7t|',
                 'pdf_page': '152',
                 'ocr_flag': 'House number truncated at line break: "7t|". Read as '
                             '7th from parallel clauses elsewhere in the chapter, '
                             'but the digit is not legible.'}],
 'maraka': None,
 'remedy': "Rahu Japa and giving a goat i. Jltarity, are the remedial measures' "
           'for obtaining relief rrom the evil effects in the Antardasa of Rahu.'},
    ('moon', 'saturn'): {'verses': '32-38',
 'conditions': [{'predicate': 'in kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'birth of a son, friendship, gain of wealth and '
                            'property, profits in business with the help of '
                            'Sudras, increase in agricultural production, gains '
                            'from son, riches and glory by the beneficence of the '
                            'king (government)',
                 'source': 'sloka',
                 'quote': 'will be experienced in the Antardasa of Saturn in the '
                          'Dasa of the Moon, if Saturn be in kendra or trikona '
                          'from the Ascendant, or be in his own sign, in his own '
                          'Navamsa in his sign of exaltation, aspected by or '
                          'associated with benefics, or be in the l lth with '
                          'strength.',
                 'pdf_page': '154',
                 'ocr_flag': 'Neutral verb "will be experienced" — no valence word '
                             'anywhere in this branch.'},
                {'predicate': 'in his own sign, in his own Navamsa, in his sign of '
                              'exaltation, or aspected by / associated with '
                              'benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as above',
                 'source': 'sloka',
                 'quote': 'or be in his own sign, in his own Navamsa in his sign '
                          'of exaltation, aspected by or associated with benefics',
                 'pdf_page': '154',
                 'ocr_flag': '"in his own Navamsa in his sign of exaltation" — the '
                             'comma between Navamsa and exaltation is missing, so '
                             'whether these are alternatives or a conjunction is '
                             'not fully legible.'},
                {'predicate': 'in the 11th with strength',
                 'houses': '11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as above',
                 'source': 'sloka',
                 'quote': 'or be in the l lth with strength.',
                 'pdf_page': '154',
                 'ocr_flag': '"l lth" for "11th". No frame stated for the 11th, '
                             'although the same sentence states "from the '
                             'Ascendant" for the kendra/trikona clause — the frame '
                             'is NOT carried over by this pass.'},
                {'predicate': 'in the 6th, the 8th, the 12th or the 2nd',
                 'houses': '6,8,12,2',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'visits to holy places, bathing in holy rivers etc., '
                            'creation of troubles by many people and distress from '
                            'enemies',
                 'source': 'sloka',
                 'quote': 'will be derived in the Antardasa of Saturn if Saturn be '
                          'lh the 6th, the 8th, the l2th or the 2nd or be in his '
                          'sign of debilitation.',
                 'pdf_page': '154',
                 'ocr_flag': '"lh" for "in". Neutral verb "will be derived". Note '
                             'the results MIX pleasant (holy pilgrimage) and '
                             'unpleasant (troubles, distress) items with no '
                             'valence word — a clear case where inferring polarity '
                             'would be wrong.'},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same mixed list as above',
                 'source': 'sloka',
                 'quote': 'or be in his sign of debilitation.',
                 'pdf_page': '154',
                 'ocr_flag': 'Debilitation here carries NO stated adverse '
                             'polarity, unlike the debilitation clauses in the '
                             'Moon, Jupiter, Mercury and Venus cells.'},
                {'predicate': 'in kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (the Moon)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'enjoyments, and gains of wealth sometimes, while '
                            'opposition or quarrels with wife and children at '
                            'other times',
                 'source': 'sloka',
                 'quote': 'will be realiscd, if Satuln be in kendra or trikona '
                          'from the lord of the Dasa (the Moon) or be eudowed '
                          'r.r:i., strength.',
                 'pdf_page': '155',
                 'ocr_flag': '"Satuln", "realiscd", "eudowed r.r:i., strength" for '
                             '"endowed with strength". Neutral verb "will be '
                             'realised"; results again mix good and bad.'},
                {'predicate': 'endowed with strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same mixed list as above',
                 'source': 'sloka',
                 'quote': 'or be eudowed r.r:i., strength.',
                 'pdf_page': '155',
                 'ocr_flag': '"eudowed r.r:i.," — OCR damage in the phrase '
                             'itself.'},
                {'predicate': 'in the 2nd, the 7th or the 8th (placement, not '
                              'lordship)',
                 'houses': '2,7,8',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': 'If Saturn be irr 2nd, the 7th or the gilr, there viill '
                          'bc physical distress.',
                 'pdf_page': '155',
                 'ocr_flag': '"irr" for "in", "gilr" for "8th" (read from the '
                             'parallel 2/7/8 pattern — the digit itself is '
                             'destroyed), "viill bc". This is a PLACEMENT, not a '
                             '2nd/7th lordship, and it adds the 8th — do not route '
                             'to maraka logic.'}],
 'maraka': None,
 'remedy': 'The remedial measures to :e adopted for obtaining relief from the evil '
           'effects, are Mrityunjaya Japa, giving in charity a black cow or female '
           'buffallo.'},
    ('moon', 'sun'): {'verses': '65-70',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'Recovery of the lost kingdom (high position in '
                            'government) and wealth, happiness in the family, '
                            'acquisition of villages and land with the kind '
                            'assistance of the friends and the king (government), '
                            'birth of a son, beneficence of Goddess Lakshmi',
                 'source': 'sloka',
                 'quote': 'will be the beneficial results in the Antardasa of the '
                          'Sun in the Dasa of the Moon, if the Sun be in his sign '
                          'of exaltation, in his own sign, in kendra or the sth, '
                          'the 9th, the llth, the 2nd or the 3rd.',
                 'pdf_page': '159-160',
                 'ocr_flag': ''},
                {'predicate': 'in kendra or the 5th, the 9th, the 11th, the 2nd or '
                              'the 3rd',
                 'houses': '1,4,7,10,5,9,11,2,3',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'same beneficial list as above, with a rider: at the '
                            'end of the Antardasa there is likelihood of attacks '
                            'of fever and lethargy',
                 'source': 'sloka',
                 'quote': 'in kendra or the sth, the 9th, the llth, the 2nd or the '
                          '3rd. At the end of the Antardasa, there is likelihood '
                          'of attacks of fever and lethargy.',
                 'pdf_page': '160',
                 'ocr_flag': '"sth" read as 5th, "llth" as 11th. NO frame stated. '
                             'The 2nd appears here as a FAVOURABLE house for the '
                             'Sun while the 2nd is an affliction house in the '
                             'Saturn cell of the same chapter — unreconciled.'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'Danger from the government, thieves and snakes, '
                            'affliction with fever, troubles in foreign journey',
                 'source': 'sloka',
                 'quote': 'Danger from the government, thieves and snakes, '
                          'affiiction with fever and troubles in foreign journey '
                          'are the likely results if the Sun be in the 8th or the '
                          '12th from the lord of the Dasa.',
                 'pdf_page': '160',
                 'ocr_flag': 'This is the ONLY from_dasa_lord instance in the '
                             'chapter with NO parenthetical gloss "(the Moon)" — '
                             'the identification is left implicit.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'sufferings from fever',
                 'source': 'sloka',
                 'quote': 'If the Sun be the lord of 2nd or the 7th, there will be '
                          'sufferings from fever in his Antardasa.',
                 'pdf_page': '160',
                 'ocr_flag': '2nd/7th lordship form but no death and no valence '
                             'word. Frame not stated.'}],
 'maraka': 'If the Sun be the lord of 2nd or the 7th, there will be sufferings '
           'from fever in his Antardasa. — NOTE: 2nd/7th-lordship form but the '
           'stated result is FEVER, not death. Must not be treated as a maraka '
           'death verdict.',
 'remedy': 'Worship of Lord Shiva is the remedial measure to obtain relief from '
           'the above evil effects.'},
    ('moon', 'venus'): {'verses': '53-64 (verse 56 MISSING from the text)',
 'conditions': [{'predicate': 'in a kendra, trikona, the 11th, the 4th or the 9th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of a kingdom (attainment of a high '
                            'position in government), gain of clothes, ornaments, '
                            'cattle, conveyances etc., happiness to wife and '
                            'children, construction of a new house, availability '
                            'of sweet preparations every day, use of perfumes, '
                            'affairs with beautiful women, sound health etc.',
                 'source': 'sloka',
                 'quote': 'will be experienced in the Antardasa of Venus iir the '
                          'Dasa of the Moon, if Venus be in a kendra, trikona, the '
                          'llth, th" 4th or the 9th from the Ascendant, or be in '
                          'his sign of exal-tation or in his own sign.',
                 'pdf_page': '157-158',
                 'ocr_flag': '"iir", "th\\"" for "the". Neutral verb "will be '
                             'experienced" — no valence word. Note 4 and 9 are '
                             'listed redundantly alongside kendra/trikona.'},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as above',
                 'source': 'sloka',
                 'quote': 'or be in his sign of exal-tation or in his own sign.',
                 'pdf_page': '158',
                 'ocr_flag': ''},
                {'predicate': 'conjunct the lord of the Dasa (the Moon)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Physical soundness, good reputation, acquisition of '
                            'more land and houses',
                 'source': 'sloka',
                 'quote': 'Physical soundness, good reputation, acquisition of '
                          'more land and houses, will result, if Vertrrs bp with '
                          "the lord of the Dasa (the l'Ioon).",
                 'pdf_page': '158',
                 'ocr_flag': '"Vertrrs bp" for "Venus be", "l\'Ioon". This is an '
                             'association with the Dasa lord, not a house count '
                             'from it. "good reputation" is part of the result '
                             'list, not a valence label on the branch, so polarity '
                             'is none.'},
                {'predicate': 'in his sign of debilitation, combust, or aspected '
                              'by / associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'loss of landed property, children, wife and cattle, '
                            'and opposition from government',
                 'source': 'sloka',
                 'quote': "There will be loss of landed property, children' wife "
                          'and cattle and opposition from government, if Venus be '
                          'in his sign of debilitation, combust or be aspected by '
                          'or associated with malefics.',
                 'pdf_page': '158',
                 'ocr_flag': 'Verse numbering jumps 55 -> 57-57t: VERSE 56 IS '
                             'ABSENT from the text entirely.'},
                {'predicate': 'in the 2nd, in his sign of exaltation or in his own '
                              'sign, or associated there with the lord of the 11th',
                 'houses': '2,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of an underground hidden treasure, gain '
                            'of land, enjoyment, birth of a son etc.',
                 'source': 'sloka',
                 'quote': 'If Venus be in the 2nd in his sign of exaltation or in '
                          'his own sign or be associated there with the lord of '
                          'the l lth, there will be acquisition of an underground '
                          'hidden treasure, gain of land, enjoyment, birth of a '
                          "son etc'",
                 'pdf_page': '158',
                 'ocr_flag': 'No frame stated for the 2nd or for the 11th '
                             'lordship.'},
                {'predicate': 'in conjunction with the lord of the 9th or 11th',
                 'houses': '9,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Advancement of good fortune, fulfilment of ambitions '
                            'with the beneficence of the king (government), '
                            'devotion to deities and Brahmins, gain of jewels like '
                            'pearls etc.',
                 'source': 'sloka',
                 'quote': 'will result if Venus be in conjunction with the lord of '
                          'the 9th or llth.',
                 'pdf_page': '158',
                 'ocr_flag': 'Neutral verb "will result". "good fortune" is inside '
                             'the result list, not a valence label.'},
                {'predicate': 'in kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (the Moon)',
                 'polarity': 'favourable',
                 'polarity_word': 'good',
                 'results': 'Acquisition of more house property and agricultural '
                            'land, gain of wealth and enjoyment',
                 'source': 'sloka',
                 'quote': 'gain of wealth and enjoym.nt *itt be the good effects '
                          'if Venus be in kendra or trikona from the lord of the '
                          'Dasa (the Moon).',
                 'pdf_page': '159',
                 'ocr_flag': '"enjoym.nt *itt be" for "enjoyment will be".'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (the Moon)',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'Deportation to foreign lands, sorrows, death, and '
                            'danger from thieves and snakes',
                 'source': 'sloka',
                 'quote': 'Deportation to foreign lands, sorrows, death and danger '
                          'from thieves and snakes will be the results, if Venus '
                          'be in the 6th, the 8th or the l2th from the lord of the '
                          'Dasa (the Moon).',
                 'pdf_page': '159',
                 'ocr_flag': 'The English of v.62 is printed OUT OF ORDER on the '
                             'page — the fragment "62. Deportation to" appears '
                             'BELOW the verse 63-64 text and the closing "(the '
                             'Moon)." sits above it. Reassembled from the '
                             'fragments; the reading is confident but the page '
                             'layout is scrambled.'},
                {'predicate': 'lord of the 2nd or 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'premature death',
                 'results': 'danger of premature death',
                 'source': 'sloka',
                 'quote': 'There will be danger of premature death, if Vernrg bc '
                          'the lord of the 2nd or Zth.',
                 'pdf_page': '159',
                 'ocr_flag': '"Vernrg bc" for "Venus be", "Zth" for "7th". No '
                             'frame stated, unlike the Jupiter maraka clause which '
                             'specifies "from the Ascendant".'}],
 'maraka': 'There will be danger of premature death, if Vernrg bc the lord of the '
           '2nd or Zth.',
 'remedy': 'The remedial measures to be addpted for obtaining relief from the evil '
           'effects, are Rudra Japa and giving in chirity a white cow and silver.'},
    ('rahu', 'jupiter'): {'verses': '8-20',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, in his '
                              'own Navamsa or exalted Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of position, patience, destruction of foes, '
                            'enjoyment, cordial relations with the king, regular '
                            'increase in wealth and property, gain of conveyance '
                            'and cows, audience with the king by performing '
                            'journey to the West or South East, success in the '
                            'desired ventures, return to homeland, doing good for '
                            'Brahmins, visit to holy places, gain of a village, '
                            'devotion to deities and Brahmins, happiness from '
                            'wife, children and grand children, availability of '
                            "sweetish preparations daily — 'will be Cerived'",
                 'source': 'sloka',
                 'quote': 'if Jupiter be in his sign of exaltation, in his own '
                          "sign' ir his own Navamsa or exalted Navamsa",
                 'pdf_page': '175-176',
                 'ocr_flag': "'ir' = 'in'; 'Cerived' = 'derived'. Verse span "
                             "printed as '8.12+' i.e. 8-12.5."},
                {'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'wifh reference to the Ascendani',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.8-12.5',
                 'source': 'sloka',
                 'quote': 'or be in kendra or trikona wifh reference to the '
                          'Ascendani.',
                 'pdf_page': '176',
                 'ocr_flag': "'wifh' = with; 'Ascendani' = Ascendant."},
                {'predicate': 'in his sign of debilitation, combust, in an enemy '
                              'sign, or associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss',
                 'results': 'Loss of wealth, obstacles in work, defamation, '
                            'distress to wife and children, heart disease, '
                            'entrustment of governmental authority etc.',
                 'source': 'sloka',
                 'quote': 'l3-141. Loss of.rrealth, obstacles in work, defamation, '
                          "distress to wife and 'children, heart disease, "
                          'entrustment of governmentai authority) etc., will '
                          'result if Jupiter be in his sign of debilitation, '
                          'cornbust, ... or in an enemy sign or be associated '
                          'rvith malefics.',
                 'pdf_page': '176',
                 'ocr_flag': "'rrealth'=wealth, 'cornbust'=combust, 'rvith'=with. "
                             "'Loss' is ITEM-level. Santhanam flags this result "
                             'list as probably corrupt (see note entry).'},
                {'predicate': 'in the 6th, 8th or 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss',
                 'results': 'same adverse list as vv.13-14.5',
                 'source': 'sloka',
                 'quote': 'in the 6th, the 8th or the l2th from the Ascendant',
                 'pdf_page': '176',
                 'ocr_flag': "'l2th' = 12th."},
                {'predicate': "Santhanam's note: the original text is probably "
                              'corrupt here because a favourable outcome sits in '
                              'an adverse list',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "Santhanam's conjecture: 'punishment by government' in "
                            "place of 'entrustment of governmental authority'. NOT "
                            'mula — conjecture only.',
                 'source': 'note',
                 'quote': 'Notes : With so manv cvil effects as a result of the '
                          'inauspicious position of Jupiter. it is difficult to '
                          'believe that a good effect like getting a position of '
                          'authority is possitrle. There is perhaps some rnistake '
                          'in the original text. It appears that there will . be '
                          'punishment by government in such c ircumstances.',
                 'pdf_page': '176',
                 'ocr_flag': "'cvil'=evil, 'possitrle'=possible, "
                             "'rnistake'=mistake. The words 'evil' and "
                             "'inauspicious' occur ONLY here, in the note, never "
                             'in the sloka.'},
                {'predicate': 'in a kendra, trikona, the 11th, the 2nd or the 3rd, '
                              'AND endowed with strength',
                 'houses': '1,4,7,10,5,9,11,2,3',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of land, good food, gains of cattle etc., '
                            'inclination towards charitable and religious work',
                 'source': 'sloka',
                 'quote': '15-17. There will be gains of land, good food, gains of '
                          'cattle etc., inclination towards charitable and '
                          'religious work, etc., if Jupiter be in kendra, trikona, '
                          'the 1lth, the 2nd or the 3rd from the lord of the Dasa '
                          '(Rahu) and be endowed with strength.',
                 'pdf_page': '176',
                 'ocr_flag': "'1lth' = 11th. Strength is a conjunctive requirement "
                             "('and be endowed with strength')."},
                {'predicate': 'in the 6th, 8th or 12th, or associated with '
                              'malefics',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss',
                 'results': 'Loss of wealth and distress to body',
                 'source': 'sloka',
                 'quote': '18-20. Loss of wealth, aud distress to body will result '
                          'if .Jupiter be in the 6th. the 8th ..rr the l2th from '
                          'the lord of the Dasa (Rahu) or be associated with '
                          'malefics.',
                 'pdf_page': '177',
                 'ocr_flag': "'aud'=and, '..rr'=or, 'l2th'=12th. 'Loss' is "
                             'ITEM-level.'},
                {'predicate': 'lord of the 2nd and the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'danger of premature death',
                 'source': 'sloka',
                 'quote': 'There will be danger of premature death if Jupiter be '
                          'the Ioid of the 2nd and the 7th.',
                 'pdf_page': '177',
                 'ocr_flag': "'Ioid' = lord. Conjunctive 'and' where all siblings "
                             "read 'or' — undecidable. Polarity 'none' per "
                             'ch.34.'}],
 'maraka': '18-20. ... There will be danger of premature death if Jupiter be the '
           "Ioid of the 2nd and the 7th. (PDFPAGE 177) — NOTE: reads 'AND the "
           "7th', unlike every sibling clause which reads 'or'.",
 'remedy': 'The person will get relief from the above evil effects .and enjoy good '
           'hua tir the, beneficence of the lord Shiva if he worships His idol '
           'made of gold. (PDFPAGE 177)'},
    ('rahu', 'ketu'): {'verses': '40-45',
 'conditions': [{'predicate': 'UNCONDITIONAL — no condition stated; the effects '
                              'are attached to the antardasa itself',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'journeys to foreign countries, danger from the king '
                            '(government), rheumatic fever etc., and loss of '
                            'cattle',
                 'source': 'sloka',
                 'quote': '40-41. During the Antardasa of . Ketu in the Dasa of '
                          'Rahu, there will be journeys to foreign countries, '
                          'danger from the king (government), rheumatic fever '
                          'etc., and loss of cattle.',
                 'pdf_page': '180',
                 'ocr_flag': 'The ONLY unconditional branch in ch.55. Whether it '
                             'is a default overridden by the following conditional '
                             'branches, or an always-on overlay, is not stated. '
                             "'danger' and 'loss' are both ITEM-level."},
                {'predicate': 'in conjunction with the lord of the 8th',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'distress to the body and mental tension',
                 'source': 'sloka',
                 'quote': 'If Ketu be in conjunction with thp lord of the 8th, '
                          'there will be distress to the body and mental tension.',
                 'pdf_page': '180',
                 'ocr_flag': "'thp' = the. This is a lordship-conjunction, not a "
                             'placement — the 8th is not a house Ketu occupies.'},
                {'predicate': 'associated with or aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Enjoyment, gain of wealth, recognition by the king '
                            '(government), acquisition of gold',
                 'source': 'sloka',
                 'quote': 'Enjoyment, gain of wealth, recognition by the king '
                          '(government), acquisition of gold etc., will be the '
                          'results if Ketu be associated with or aspected by '
                          'benefics.',
                 'pdf_page': '180',
                 'ocr_flag': 'none'},
                {'predicate': 'related to the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Isht Siddhi',
                 'source': 'sloka',
                 'quote': '42-42t. There will be Isht Siddhi (coa fqla) if Ketu be '
                          'related to the lord of the Ascendant.',
                 'pdf_page': '180',
                 'ocr_flag': "'related to' vs the next clause's 'associated with' "
                             '— the text draws a distinction it never defines.'},
                {'predicate': 'associated with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'definitely gain of wealth',
                 'source': 'sloka',
                 'quote': 'If he be associated with the lord of the Ascendant '
                          'there will definitely be gain of wealth.',
                 'pdf_page': '180',
                 'ocr_flag': 'none'},
                {'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the Ascendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'definitely increase in the number of cattle',
                 'source': 'sloka',
                 'quote': 'There will also definitely be increase in the number of '
                          'cattle, if Ketu be in a kendra or trikona (from the '
                          'Ascendant).',
                 'pdf_page': '180',
                 'ocr_flag': "FLAG: the frame appears ONLY inside the translator's "
                             "parentheses. Under the project rule that Santhanam's "
                             'supplied material is not mula, this reverts to '
                             "'unstated'."},
                {'predicate': 'without strength, in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger from thieves and snakes, distress from wounds, '
                            'separation from parents, antagonistic relations with '
                            'kinsmen, mental agony',
                 'source': 'sloka',
                 'quote': '43-45. Effects like danger from thieves, and snakes, '
                          'distress from wounds, separation from parents, '
                          'antagonistic relations with kinsmen, mental agony etc., '
                          'will be derived if Ketu be without strength in the 8th '
                          'or the l2th from the Ascendant.',
                 'pdf_page': '181',
                 'ocr_flag': "'l2th'=12th. 'without strength' is conjunctive with "
                             "the placement. 'danger' is ITEM-level. Note 6th "
                             'absent.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'distress to the body',
                 'source': 'sloka',
                 'quote': 'If Ketu be lord of the 2nd or the Zth, there will be '
                          'distress to the body.',
                 'pdf_page': '181',
                 'ocr_flag': "'Zth' = 7th (OCR). Result is NOT death, unlike most "
                             "sibling clauses. Polarity 'none' per ch.34."}],
 'maraka': 'If Ketu be lord of the 2nd or the Zth, there will be distress to the '
           "body. (PDFPAGE 181) — 'Zth' = 7th (OCR). NOTE: the stated result is "
           'distress to the body, NOT death.',
 'remedy': 'The remedial measure to obtain relief from the above evil effects is '
           'giving a goat in charity. (PDFPAGE 181)'},
    ('rahu', 'mars'): {'verses': '76-83',
 'conditions': [{'predicate': 'in the [HOUSE LOST TO OCR], the 5th, the 9th, or a '
                              'kendra',
                 'houses': '?,5,9,1,4,7,10',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'recovery of lost kingdom (reinstatement in a high '
                            'position in government) and lost wealth, prosperity '
                            'at home and increase in agricultural production, gain '
                            'of wealth, blessings by the household deity, '
                            'happiness from children, enjoyment of good food — '
                            "'will be derived'",
                 'source': 'sloka',
                 'quote': '{,ntardasa of Mars in the Dasa of Rahu if Mars be in '
                          'the , the 5th, the 9th or kendra from the Ascendant, be',
                 'pdf_page': '186',
                 'ocr_flag': 'SEVERE: PDFPAGE 186 is left-margin-truncated on '
                             'every English line. The FIRST house number is '
                             "entirely missing ('in the , the 5th'). Not guessed. "
                             'Re-OCR required before this ships.'},
                {'predicate': 'aspected by benefics, or in his sign of exaltation, '
                              'or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as vv.76-77.5',
                 'source': 'sloka',
                 'quote': 'cted by henefics, or be in his sign of exaltation, or '
                          'in his sign.',
                 'pdf_page': '186',
                 'ocr_flag': "SEVERE left-truncation: 'cted by henefics' = "
                             "'[aspe]cted by benefics'; 'or in his sign' = 'or in "
                             "his [own] sign'."},
                {'predicate': 'in a kendra, the 5th, [HOUSE LOST TO OCR], the 3rd '
                              'or the 11th',
                 'houses': '1,4,7,10,5,?,3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of red coloured garments, jewels, '
                            'audience with the king (meetings with high officials '
                            'of government), well being of children and employer, '
                            'attainment of the position of commander of the army, '
                            'enthusiasm, and gain of wealth through kinsmen',
                 'source': 'sloka',
                 'quote': 'of wealth through kinsmen, if Mars be in kendra, the '
                          '5th / th, the 3rd or the llth from the lord of the Dasa '
                          '(Rahu).',
                 'pdf_page': '186',
                 'ocr_flag': "SEVERE: the line break leaves an orphan 'th' — a "
                             "lost ordinal between '5th' and 'the 3rd' (plausibly "
                             '9th by the pattern of sibling cells, but '
                             'UNVERIFIABLE from this text). Not guessed.'},
                {'predicate': 'in the 6th, the 8th or the [HOUSE LOST TO OCR], '
                              'aspected by malefics',
                 'houses': '6,8,?',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rairu)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Distress to wife, children and co-borns, tor[?] '
                            'position, antagonistic relations with children, wife '
                            'and [other] close relations, danger from thieves, '
                            'wounds and pain in the body',
                 'source': 'sloka',
                 'quote': 'body, etc., will result if Mars be in the 6th. the 8th '
                          'or the / from the lord of the Dasa (Rairu) aspected by '
                          'malefics.',
                 'pdf_page': '187',
                 'ocr_flag': 'SEVERE: the third house is lost at the line break '
                             "('the 8th or the ___ from the lord'). 12th by "
                             'pattern, but the text as extracted does not say it. '
                             "'Rairu'=Rahu. Result string also truncated ('tor "
                             "position' = probably 'torture'/'loss of position' — "
                             "unrecoverable). 'danger' is ITEM-level. CONJUNCTIVE "
                             'with the malefic aspect.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'lethargy and danger of death',
                 'source': 'sloka',
                 'quote': '83. There will be lethargy and danger of death, if J / '
                          'be the lord of the 2nd or the 7th.',
                 'pdf_page': '187',
                 'ocr_flag': "Graha name truncated to the glyph 'J'; context "
                             'requires Mars but the text does not print it. '
                             "Polarity 'none' per ch.34."}],
 'maraka': '83. There will be lethargy and danger of death, if J / be the lord of '
           'the 2nd or the 7th. (PDFPAGE 187) — the graha name is truncated by OCR '
           "to the glyph 'J'; within the Mars antardasa it must be Mars, but the "
           'extracted text does not say so.',
 'remedy': "Remedial measure to obtain relief 'from the above [evil] effects is "
           'giving a cow. or a bull in charity. (PDFPAGE 187)'},
    ('rahu', 'mercury'): {'verses': '30-39',
 'conditions': [{'predicate': 'in his sign of exaltation, endowed with strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Auspicious',
                 'results': 'Raja yoga, well being in the family, profits and gain '
                            'of wealth in business, comforts of conveyances, '
                            'marriage and other auspicious functions, increase in '
                            'the number of cattle, gain of perfumes, comforts of '
                            'bed and women',
                 'source': 'sloka',
                 'quote': "30-33. Auspicious effects like Raja yoga' well being in "
                          "thc amily, profits an-d and gain of wealth in business' "
                          'comlbrts or ,onuayon"rr, marriage and other auspicious '
                          "functions' increase n the number of cattle, gain of "
                          "perfumes' comfo-rts of bed ilornen, etc. will be "
                          'derivid in the Antardasa of Mercury rn lhe Dasa of '
                          'Rahu, if--M"r"u\'y be in his sign of exaltation\'',
                 'pdf_page': '179',
                 'ocr_flag': "Heavy OCR: 'thc amily'=the family, 'comlbrts or "
                             ',onuayon"rr\'=comforts of conveyances, '
                             "'ilornen'=women, 'derivid'=derived, "
                             '\'M"r"u\'y\'=Mercury. This is ONE OF ONLY TWO '
                             'branch-LEVEL valence labels in the chapter '
                             "('Auspicious effects like...')."},
                {'predicate': 'in a kendra or in the 5th, and endowed with '
                              'strength',
                 'houses': '1,4,7,10,5',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Auspicious',
                 'results': "same list as vv.30-33, plus: 'Good results like Raja "
                            'Vogu,-f"ntn"ence of the king and gain-of wealth and '
                            'reputation, *iff be realised particularly on '
                            "wednesday in the month of MercurY.'",
                 'source': 'sloka',
                 'quote': "in kendra or in the Stn anA be endowed with strength'",
                 'pdf_page': '179',
                 'ocr_flag': "CRITICAL: NO frame word. 'Stn'=5th, 'anA'=and. Note "
                             'the immediately following branch (vv.34-35) IS '
                             'glossed from the Dasa lord, so adjacency supplies no '
                             'default here.'},
                {'predicate': 'in a kendra, the 11th, the 3rd, the 9th or the 10th',
                 'houses': '1,4,7,10,11,3,9',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Sound health, Ishta Siddhi, attending discourse on '
                            'Puranas and ancient history, marriage, offering of '
                            'oblations, charities, religious inclination and '
                            'sympathetic attitude towards others',
                 'source': 'sloka',
                 'quote': '34.35.Soundhealth,IshtaSiddhi,attendingdiscourseon '
                          '?uranas and ancient history, marriage, offering of '
                          "oblations' charities, religious inclination and "
                          'sympathetic attitude towards others, will result if '
                          "Mercury be ln kendra' the llth'the 3rd the 9th or the "
                          "10th from the lord of the Dasa (Rahu)'",
                 'pdf_page': '179',
                 'ocr_flag': 'Word-spacing destroyed in the verse number run-in; '
                             "'?uranas'=Puranas, 'ln'=in. The 10th is listed "
                             'separately though kendra already includes it — '
                             'printed as-is.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'opprobrium of deities and Brahmins by the native, '
                            'loss of fortune, speaking lies, unwise actions, fear '
                            'from snakes, thieves and the government, quarrels, '
                            'distress to wife and children',
                 'source': 'sloka',
                 'quote': '36-38.Therewillbeopprobrium(|fiEr)ofdeitiesand Brahmins '
                          "by the native, loss of fortune, speaking lies' unwise "
                          'actions, fear from snakes, thieves and the governmentn '
                          "quarrels' distress to wife and children, etc., if "
                          "Mercury be in the 6th' the 8th or the 12th, or be "
                          "aspected by Saturn'",
                 'pdf_page': '179',
                 'ocr_flag': 'CRITICAL: NO frame word for 6/8/12 — the phrase '
                             "'from the Ascendant' / 'from the lord of the Dasa' "
                             'is simply absent, unlike the parallel clauses in '
                             "every other cell. 'governmentn'=government. 'loss' "
                             'is ITEM-level.'},
                {'predicate': 'aspected by Saturn',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss',
                 'results': 'same adverse list as vv.36-38',
                 'source': 'sloka',
                 'quote': "or be aspected by Saturn'",
                 'pdf_page': '179',
                 'ocr_flag': 'Valence word carried from the shared result list; '
                             'ITEM-level.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'fear of premature death',
                 'source': 'sloka',
                 'quote': '39. If Mercury be the lord of the 2nd or the 7th, there '
                          'will be fear of premature death.',
                 'pdf_page': '180',
                 'ocr_flag': "Polarity 'none' per ch.34."}],
 'maraka': '39. If Mercury be the lord of the 2nd or the 7th, there will be fear '
           'of premature death. (PDFPAGE 180)',
 'remedy': 'Remedial measure to obtain relief from the above evil effects is '
           'recitation of Vishnu Sahasranam. (PDFPAGE 180)'},
    ('rahu', 'moon'): {'verses': '68-75',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of kingdom (high position in government), '
                            'respect from the king, gains of wealth, sound health, '
                            'gains of garments and ornaments, happiness from '
                            'children, comforts of conveyances, increase in house '
                            'and landed property',
                 'source': 'sloka',
                 'quote': '.68-70. Effects like acquisition of kingdom (attainment '
                          'of a high position in government), respect from the '
                          'king (high ofrcials of government), gains of wealth, '
                          'sound health, gains of garments and ornaments, '
                          'happiness from children, comforts ofconveyances, '
                          'increase in house and landed property etc., will be '
                          'derived, in the Antradasa of the Moon in the Dasa of '
                          'Rahu, if the Moon be in his sign of exaltation, in his '
                          'own sign,',
                 'pdf_page': '185',
                 'ocr_flag': "'ofrcials'=officials, 'Antradasa'=Antardasa. NOTE: "
                             'no waxing/waning qualifier here, unlike ch.54 v.73 '
                             "which added 'The good effects will be realised in "
                             "full if the Moon be waxing'. ch.55 states no such "
                             'qualifier for the Moon.'},
                {'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as vv.68-70',
                 'source': 'sloka',
                 'quote': 'kendra, trikona or the llth,',
                 'pdf_page': '185',
                 'ocr_flag': "CRITICAL: NO frame word. 'llth'=11th. The very next "
                             "branch (vv.71-72) IS glossed 'from the lord of the "
                             "Dasa (Rahu)', so adjacency supplies no default."},
                {'predicate': 'in a friendly sign and aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as vv.68-70',
                 'source': 'sloka',
                 'quote': 'or in a friendly sign aspected by benefics.',
                 'pdf_page': '185',
                 'ocr_flag': 'Conjunctive: friendly sign AND benefic aspect, as '
                             'printed.'},
                {'predicate': 'in the 5th, the 9th, a kendra or the 11th',
                 'houses': '5,9,1,4,7,10,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Beneficence of the Goddess Lakshmi, success all '
                            'round, increase in wealth and grains, good '
                            'reputation, worship of deities',
                 'source': 'sloka',
                 'quote': '7l-72. Beneficence of the Goddess l-akshmi, success all '
                          'round, increase in wealth and grains, good reputation, '
                          'worship of deities, will be the lresults, if the Moon '
                          'be in the 5th, the 9th, kendra or the llth from the '
                          'lord of the Dasa (Rahu).',
                 'pdf_page': '185',
                 'ocr_flag': "'l-akshmi'=Lakshmi, 'lresults'=results, "
                             "'llth'=11th."},
                {'predicate': 'bereft of strength in the 6th, 8th or 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'disturbances at home and in agricultural activities '
                            'by evil spirits, leopards and other wild animals; '
                            'danger from thieves during journeys; stomach '
                            'disorders',
                 'source': 'sloka',
                 'quote': '73-75. There will be creation of disturbances at home '
                          'and in the agricultural activities by evil spirits, '
                          'leoparis and other wild animals, danger from thieves '
                          'during journeys and stomach disordcrs, if the Moon be '
                          'bereft of strength in the 6th, the 8th or the l2th from '
                          'the lord of the Dasa (Rahu).',
                 'pdf_page': '185',
                 'ocr_flag': "'leoparis'=leopards, 'disordcrs'=disorders, "
                             "'l2th'=12th. 'bereft of strength' is conjunctive "
                             "with the placement. 'danger' is ITEM-level; 'evil "
                             "spirits' is a noun in the result list, NOT a valence "
                             'word.'},
                {'predicate': 'lord of the 2nd or the 12th',
                 'houses': '2,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'possibility of premature death',
                 'source': 'sloka',
                 'quote': 'There will be possibility of premature death if the '
                          'Moon be the lord of the 2nd or the l2th.',
                 'pdf_page': '185',
                 'ocr_flag': 'ANOMALY: 12th, not 7th — unique in this chapter. '
                             "'l2th'=12th. Do NOT silently normalise to 7th. "
                             "Polarity 'none' per ch.34."}],
 'maraka': 'There will be possibility of premature death if the Moon be the lord '
           'of the 2nd or the l2th. (PDFPAGE 185) — ANOMALY: reads 2nd or TWELFTH. '
           'Every other cell in ch.55 reads 2nd or 7th. Recorded as printed; may '
           "be an OCR corruption of '7th' or a genuine variant. FLAGGED, not "
           'resolved.',
 'remedy': 'The remedial measure to obtain relief from the abovs evil effects is '
           'to give in charity a white cow or female buffalo. (PDFPAGE 185)'},
    ('rahu', 'rahu'): {'verses': '1-7',
 'conditions': [{'predicate': 'in Cancer, Scorpio, Virgo or Sagittarius (raw sign '
                              'placement, not a dignity)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Effects like acquisition of a kingdom (attainment of '
                            'a high position in government), enthusiasm, cordial '
                            'relations with the king (government), happiness from '
                            'wife and children and increase in properi.1,, will be '
                            'derived',
                 'source': 'sloka',
                 'quote': 'if Rahu be in Cancer, Scorpio, Virgo or Sagittarius',
                 'pdf_page': '174',
                 'ocr_flag': 'none'},
                {'predicate': 'in the 3rd, 6th, 10th or 11th',
                 'houses': '3,6,10,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as above; joined to the sign '
                            "condition by 'and'",
                 'source': 'sloka',
                 'quote': 'and be in the 3rd, qhe 6th, the 10th or the I lth from '
                          'the Ascendant',
                 'pdf_page': '174',
                 'ocr_flag': "'qhe 6th' = 'the 6th'; 'I lth' = '11th'"},
                {'predicate': 'associated with a yogakaraka planet in his sign of '
                              'exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as above',
                 'source': 'sloka',
                 'quote': 'or be associated with yogakaraka planet in his sign of '
                          'exaltation.',
                 'pdf_page': '174',
                 'ocr_flag': "Ambiguous whether 'in his sign of exaltation' "
                             'qualifies Rahu or the yogakaraka — text does not '
                             'settle it.'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger from thieves, distress from wounds, antagonism '
                            'with government officials, destruction of kinsmen, '
                            'distress to wife and children',
                 'source': 'sloka',
                 'quote': "There will be danger from thieves, distress from' "
                          'wounds, antagonism with government officials, '
                          "destructiot'i cf kinsmen, distress to wife and "
                          'children, if Rahu be in the 8ih or the 12th from the '
                          'Ascendant',
                 'pdf_page': '174',
                 'ocr_flag': "'8ih' = 8th; 'destructiot'i cf' = 'destruction of'. "
                             "Valence word 'danger' is ITEM-level ('danger from "
                             "thieves'), not a branch label."},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'same adverse list as vv.5-6',
                 'source': 'sloka',
                 'quote': "or be associated with malefics'",
                 'pdf_page': '174',
                 'ocr_flag': 'Valence word is ITEM-level, carried over from the '
                             'shared result list.'},
                {'predicate': 'lord of the 2nd or the 7th, or posited in the 2nd '
                              'or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'distress and diseases',
                 'source': 'sloka',
                 'quote': '7. If Rahu be the lord of the 2nd or the 7th or be in '
                          'any of those hottses, there will be distress and '
                          "diseases'",
                 'pdf_page': '175',
                 'ocr_flag': "'hottses' = houses. No frame word for the placement "
                             "limb. Polarity left 'none' per ch.34 (maraka verdict "
                             'must not be mixed with a benefic/malefic nature).'}],
 'maraka': '7. If Rahu be the lord of the 2nd or the 7th or be in any of those '
           "hottses, there will be distress and diseases' (PDFPAGE 175) — NOTE: "
           'the stated result is distress and disease, NOT death.',
 'remedy': 'To otrtain relief from the above evil effects Rahu should be '
           'worshipped (by recitation of his mantras) and by givirig in charity '
           "things connecied with or ruled by Rahu' (PDFPAGE 175)"},
    ('rahu', 'saturn'): {'verses': '21-29',
 'conditions': [{'predicate': 'in a kendra, trikona, the 3rd or the 11th',
                 'houses': '1,4,7,10,5,9,3,11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'pleasure of the king for devotion in his service, '
                            'auspicious functions like celebration of marriage '
                            'etc. at home, construction of a garden, reservoir '
                            'etc., gain of wealth and cattle from well to do '
                            'persons belonging to Sudra class, loss of wealth '
                            'caused by the king (government officials) during '
                            'journey to the West, reduction in income due to '
                            "lethargy, return to homeland — 'will be derived'",
                 'source': 'sloka',
                 'quote': 'if Saturn be in kendra, trikona in his sign bf '
                          'exiiir.ation, in his orvn sign, in iris moolatrikona, '
                          'the 3rd or . the I lth.',
                 'pdf_page': '177',
                 'ocr_flag': "CRITICAL: NO frame word anywhere in this branch. 'bf "
                             "exiiir.ation'=of exaltation, 'orvn'=own, 'iris'=his, "
                             "'I lth'=11th. Polarity deliberately 'none': the SAME "
                             "result list contains both 'auspicious functions' and "
                             "'loss of wealth', so no branch valence is readable."},
                {'predicate': 'in his sign of exaltation, in his own sign, or in '
                              'his moolatrikona',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same mixed result list as vv.21-24',
                 'source': 'sloka',
                 'quote': 'in his sign bf exiiir.ation, in his orvn sign, in iris '
                          'moolatrikona',
                 'pdf_page': '177',
                 'ocr_flag': 'Same OCR corruptions as above.'},
                {'predicate': "in his sign of debilitation or an enemy's sign",
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'Danger from menials, king and enemies, distress to '
                            'wife and children, distress to kinsmen, disputes with '
                            'co-parceners, disputes in dealings with others, BUT '
                            'sudden gain of ornaments',
                 'source': 'sloka',
                 'quote': '25-2.6. Danger from menials, king and enemies, '
                          'distress. to wife anll children, distress to kinsmen, '
                          'disputes with the co-parceners, disputes in dealirigs '
                          'with others, but sudden gain of ornaments, will result '
                          "if Saturn be in his sign of debilitation, enemy's sign",
                 'pdf_page': '178',
                 'ocr_flag': "'anll'=and, 'dealirigs'=dealings. 'Danger' is "
                             'ITEM-level. Result list is internally mixed (adverse '
                             "items + 'sudden gain of ornaments') — Santhanam "
                             'notes this, see note entry.'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'same result list as vv.25-26',
                 'source': 'sloka',
                 'quote': 'or be in the 8th, or the l2th from the Ascendant.',
                 'pdf_page': '178',
                 'ocr_flag': "'l2th' = 12th. Note only 8th and 12th here — the 6th "
                             'is absent, unlike the parallel clauses in the other '
                             'cells.'},
                {'predicate': "Santhanam's note: the favourable item inside the "
                              'adverse list is unexplained',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'No conjecture offered — the note simply records that '
                            'the text is unclear.',
                 'source': 'note',
                 'quote': 'Note : It is not clear how there can be strdden gain of '
                          "ornaments when the Antardasa lord is badly placed'",
                 'pdf_page': '178',
                 'ocr_flag': "'strdden' = sudden. NOT mula."},
                {'predicate': 'in the 6th, 8th or 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'heart disease, defamation, quarrels, danger from '
                            'enemies, foreign journeys, affliction with Gulma, '
                            'unpalatable food and sorrows',
                 'source': 'sloka',
                 'quote': '27-29. There will be heart disease, defamation, '
                          'quarrels, danger from enemies, foreign journeys, '
                          'affiiction with.[Gulma (enlargement of skin), '
                          'unpalatable food and sorrows etc., rf Saturn be in the '
                          '6th, tire 8th or the l2th from the lord of the Dasa '
                          '(Rahu).',
                 'pdf_page': '179',
                 'ocr_flag': "'affiiction'=affliction, 'rf'=if, 'tire'=the, "
                             "'l2th'=12th. 'danger' is ITEM-level."},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'premature death is likely',
                 'source': 'sloka',
                 'quote': 'Premature death is likely if Saiurn be iord of the 2nd '
                          'or the 7th.',
                 'pdf_page': '179',
                 'ocr_flag': "'Saiurn'=Saturn, 'iord'=lord. Polarity 'none' per "
                             'ch.34.'}],
 'maraka': '27-29. ... Premature death is likely if Saiurn be iord of the 2nd or '
           'the 7th. (PDFPAGE 179)',
 'remedy': 'Remedial measure to obtain relief from the above evrl effects and to '
           'regain good health, is giving a black cow or she-buffaio in charity. '
           '(PDFPAGE 179)'},
    ('rahu', 'sun'): {'verses': '60-67',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, or in '
                              'his exalted or own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'cordial relations with the king (government), '
                            'increase in wealth and grains, some popularity and '
                            'respect, some possibility of becoming head of a '
                            'village',
                 'source': 'sloka',
                 'quote': "60-61]'. Effects like cordial relations with the king "
                          '(government), increase in wealth and grains, some '
                          'popularity rispect, some possibility of becoming head '
                          "of a village, etc', will be experienced in the "
                          'Antardasa of the Sun in the Dasa of Rahu, if the Sun be '
                          'in his sign of exaltation, in his own sign, ... or be '
                          'in his exalted or own Navamsa.',
                 'pdf_page': '183',
                 'ocr_flag': "'rispect'=respect. Section heading on this page "
                             "misreads 'in the Antardasa of Rahu' — should be 'in "
                             "the Dasa of Rahu'. 'will be experienced' — neutral "
                             'verb.'},
                {'predicate': 'in the 11th, a kendra or a trikona',
                 'houses': '11,1,4,7,10,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the Ascendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same list as vv.60-61.5',
                 'source': 'sloka',
                 'quote': "the l lth' .a kendra or trikona (from the Ascendant)",
                 'pdf_page': '183',
                 'ocr_flag': "FLAG: the frame appears ONLY inside the translator's "
                             "parentheses. Under the project rule that Santhanam's "
                             'supplied material is not mula, this reverts to '
                             "'unstated'. 'l lth'=11th."},
                {'predicate': 'associated with or aspected by the lords of the '
                              'Ascendant, the 9th, or the 10th',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'good reputation, encouragement and assistance by '
                            'government, journeys to foreign countries, '
                            'acquisition of the sovereignty of the country, gains '
                            'of elephants, horses, clothes, ornaments, fulfilment '
                            'of ambitions, happiness to children',
                 'source': 'sloka',
                 'quote': '62-631. There will be good reputation and encouragement '
                          'and assistance by government, journeys to foreign '
                          'countries, acquisition of the Sovereignty of the '
                          "country, gains of elephants' horses, clgthes, "
                          'ornaments, fulfilment of ambitions, happiness to '
                          'children etc., if the Sun be associated with or '
                          "'aspected by thc lords of the Ascendant, the 9th, or "
                          'the lOth.',
                 'pdf_page': '183-184',
                 'ocr_flag': "'clgthes'=clothes, 'thc'=the, 'lOth'=10th. "
                             'Lordship-association, not placement.'},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'Fevers, dysentery, other diseases, quarrels, '
                            'antagonism with the king (government), travels, '
                            'danger from foes, thieves, fire',
                 'source': 'sloka',
                 'quote': '64-65. Fevers, dysentry, other diseases, quarrels, '
                          'anta-gonism with the king (government), travels, danger '
                          'from foes thieves, fire etc., will be the results if '
                          'the Sun be in his Sign of debilitation',
                 'pdf_page': '184',
                 'ocr_flag': "'dysentry'=dysentery. 'danger' is ITEM-level."},
                {'predicate': 'in the 6th, 8th or 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'same list as vv.64-65',
                 'source': 'sloka',
                 'quote': 'or be in the 6th, the 8th or the 12th from the lord of '
                          'the Dasa (Rahu).',
                 'pdf_page': '184',
                 'ocr_flag': 'none'},
                {'predicate': 'in a kendra, trikona, the 3rd or the 11th',
                 'houses': '1,4,7,10,5,9,3,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the Iord of the Dasa (Rahu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Well being in every way and recognition from the '
                            'kings (high dignitaries) in foreign countries',
                 'source': 'sloka',
                 'quote': '66. Well being in every way anb recognition from the '
                          'kings (high dignitaries) in foreign -.runtries, will be '
                          'the results, if the Sun bein a kendra, tril...ina, the '
                          '3rd or the tlth from the Iord of the Dasa (Rahu).',
                 'pdf_page': '184',
                 'ocr_flag': "'anb'=and, '-.runtries'=countries, "
                             "'tril...ina'=trikona, 'tlth'=11th, 'bein'=be in."},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'danger of critical illness',
                 'source': 'sloka',
                 'quote': '67. There will be danger of critical illnesy if Sun be '
                          'the lord of the 2nd or the 7th.',
                 'pdf_page': '184',
                 'ocr_flag': "'illnesy'=illness. Result is critical ILLNESS, not "
                             "death. Polarity 'none' per ch.34."}],
 'maraka': '67. There will be danger of critical illnesy if Sun be the lord of the '
           '2nd or the 7th. (PDFPAGE 184) — NOTE: the stated result is critical '
           "ILLNESS, not death. 'illnesy' = illness (OCR).",
 'remedy': 'Worship of the Sun is the remedial measure recommended to obtain '
           'relief from the above evil effects. (PDFPAGE 184)'},
    ('rahu', 'venus'): {'verses': '46-59',
 'conditions': [{'predicate': 'with strength in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of wealth through Brahmins, increase in the '
                            'number of cattle, celebrations for the birth of a '
                            'son, well being, recognition from government, '
                            'acquisition of a kingdom, great enjoyment and '
                            'comforts',
                 'source': 'sloka',
                 'quote': '46-47tr. Effects like gains of wealth through Brahmins, '
                          'increase in the number of cattle, celebrations for the '
                          'birth of a son, well being, recognition from '
                          'government, acquisition of akingdom (attainment of a '
                          'high poritioo in government), great enjoyment and '
                          'co{brts etc,, will be experienced in the Antar-dasa of '
                          'Venus in the Dasa of Rahu if Venus be with strength in '
                          'a kendra, trikona or the ltth from the Ascendant.',
                 'pdf_page': '181',
                 'ocr_flag': "'poritioo'=position, 'co{brts'=comforts, "
                             "'ltth'=11th. 'will be experienced' — neutral verb, "
                             'no valence.'},
                {'predicate': 'in his sign of exaltation, own sign, exalted '
                              'Navamsa or own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'Construction of a new house, availability of sweet '
                            'preparations, happiness from wife and children, '
                            'association with friends, giving of grains etc. in '
                            'charity, beneficence of the king (government), gain '
                            'of conveyances and clothes, extraordinary profits in '
                            'business, celebration of upanayana ceremony of '
                            'wearing the sacred thread',
                 'source': 'sloka',
                 'quote': '...etc., will be the auspicious results, if Venus be in '
                          "his sign of exaltation, in his own sign' in his exalted "
                          'Navamsa, or in his own Navamsa.',
                 'pdf_page': '181-182',
                 'ocr_flag': "'sweer preparations'=sweet, 'lriends'=friends. This "
                             'is the SECOND (and last) branch-LEVEL valence label '
                             'in the chapter.'},
                {'predicate': 'in the 6th, 8th or 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'danger of death',
                 'results': 'diseases, quarrels, separation from son or father, '
                            'distress to kinsmen, disputes with co-parceners, '
                            'danger of death to self or employer, unhappiness to '
                            'wife and children, pain in the stomach',
                 'source': 'sloka',
                 'quote': '5l-53+. There will be diseases, quarrels, separation '
                          'from the son or father, distress to kinsmen, disputes '
                          "with co'parceners' danger of death to self or employer, "
                          'unhappiness to wife and children, pain in the stomach '
                          'etc., if Venus be in the 6th, the 8th or the l2th from '
                          'the Ascendant',
                 'pdf_page': '182',
                 'ocr_flag': "'l2th'=12th. Both 'danger' and 'death' present but "
                             'ITEM-level, inside the enumeration. NOTE: this is a '
                             'death statement that is NOT tied to 2nd/7th '
                             'lordship.'},
                {'predicate': "in his sign of debilitation or an enemy's sign, or "
                              'associated with Saturn, Mars or Rahu',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger of death',
                 'results': 'same list as vv.51-53.5',
                 'source': 'sloka',
                 'quote': "be in his sign of debilit'ation or an enemy's sign, or "
                          'be associated with Satrun, Mars or Rahu.',
                 'pdf_page': '182',
                 'ocr_flag': "'Satrun'=Saturn. Note Rahu here is the MAHADASA lord "
                             '— association with the dasa lord itself is a '
                             'condition.'},
                {'predicate': 'in a kendra, trikona, the 11th or the 10th',
                 'houses': '1,4,7,10,5,9,11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Enjoyments from perfumes, bed, music etc., gain of a '
                            'desired object, fulfilment of desires',
                 'source': 'sloka',
                 'quote': '54-55;, Enjoyments from perfumes, bed\' music etc" gain '
                          'of a dlsired object, fuinf.tnt of desires, will be the '
                          "results' if Venusbe in a kendra, trikona, the llth "
                          'orthe lOthfromthe lord of the Dasa (Rahu).',
                 'pdf_page': '182',
                 'ocr_flag': "'dlsired'=desired, 'fuinf.tnt'=fulfilment; "
                             "word-spacing lost ('Venusbe', 'orthe lOthfromthe'). "
                             'The 10th is listed separately though kendra already '
                             'includes it.'},
                {'predicate': 'associated with malefics AND in the 6th, 8th or '
                              '12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Rahu)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger from the wrath of Brahmins, snakes and the '
                            'king; possible affliction with diseases like stoppage '
                            'of urine, diabetes, pollution of blood, anaemia; '
                            'availability of only coarse food, nervous disorder, '
                            'imprisonment, loss of wealth from penalties or fines '
                            'imposed by government',
                 'source': 'sloka',
                 'quote': "56-59. Effects like danger from the wrath of Brahmins' "
                          'snakes and the king (government), possibility of '
                          'affiiction with .diseases like stoppage of urine, '
                          'diabetes, pollution of blood, .anaemia, availability of '
                          'only coarse food, nervous disorder, imprisonment, loss '
                          'of wealth as a result of penalties or fines imposed by '
                          'government, will be derived if Venus be associated wiih '
                          'malefics in the 6th, the 8th or the 12th from the lord '
                          'of the Dasa (Rahu).',
                 'pdf_page': '183',
                 'ocr_flag': "'affiiction'=affliction, 'wiih'=with. CONJUNCTIVE: "
                             'the malefic association and the 6/8/12 placement are '
                             "required jointly. 'danger' and 'loss' are "
                             'ITEM-level.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'distress to wife and children, danger of premature '
                            'death to self',
                 'source': 'sloka',
                 'quote': "There will be distress to wife and children' danger of "
                          'premature death to self if Venus be lord of the 2nd or '
                          'the 7th.',
                 'pdf_page': '183',
                 'ocr_flag': "Polarity 'none' per ch.34."}],
 'maraka': "There will be distress to wife and children' danger of premature death "
           'to self if Venus be lord of the 2nd or the 7th. (PDFPAGE 183)',
 'remedy': 'Remedial measures to obtain relief from the above evil effects are '
           "worship of Goddess Durga and Goddess Lakshmi' (PDFPAGE 183)"},
    ('saturn', 'jupiter'): {'verses': '71-82',
 'conditions': [{'predicate': 'in kendra or trikona',
                 'houses': 'kendra/trikona — not enumerated in the text',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'success all round, well being in the family, gain of '
                            'conveyances, ornaments and clothes by the beneficence '
                            'of the king (government), reverence, devotion to '
                            'deities and the preceptor, association with men of '
                            'learning, happiness from wife and children etc., will '
                            'be derived',
                 'source': 'sloka',
                 'quote': '7l-731. Effects like success all round, well being in '
                          'the family, gain of conveyances, ornaments and clothes '
                          'by the bene- ficence of the king (government), ... will '
                          'be derived in the Antardasa of Jupiter in the Dasa of '
                          'Saturn, if Jupiter be in kendra or trikona, be '
                          'associated with the lord of the Ascendant, or be in his '
                          'own sign or sign of exaltation.',
                 'pdf_page': '212',
                 'ocr_flag': "CRITICAL: NO REFERENCE FRAME STATED for 'kendra or "
                             "trikona'. The 'lord of the Ascendant' in the NEXT "
                             'clause is an association test, not a frame for this '
                             'one — do not borrow it.'},
                {'predicate': 'associated with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.71-73 1/2',
                 'source': 'sloka',
                 'quote': 'be associated with the lord of the Ascendant, or be in '
                          'his own sign or sign of exaltation.',
                 'pdf_page': '212',
                 'ocr_flag': ''},
                {'predicate': 'in his own sign or sign of exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.71-73 1/2',
                 'source': 'sloka',
                 'quote': 'or be in his own sign or sign of exaltation.',
                 'pdf_page': '212',
                 'ocr_flag': ''},
                {'predicate': 'in his sign of debilitation, or associated with '
                              'malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'death of the near relations, loss of wealth, '
                            'antagonism with the government officials, failure in '
                            'projects, journeys to foreign lands, affliction with '
                            'diseases like leprosy etc.',
                 'source': 'sloka',
                 'quote': '74-75+. Results like death of the near relations, loss '
                          'of wealth, antagonism with the government officials, '
                          'failure in projects, journeys to foreign lands, '
                          'affiiction with diseases like laprosy etc., will be '
                          'experienced if Jupiter be in his sign of debilitation, '
                          'be associated with malefics, or be in the 6th, the 8th '
                          'or the 12th from the Ascendant.',
                 'pdf_page': '213',
                 'ocr_flag': "'laprosy'=leprosy, 'affiiction'=affliction"},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.74-75 1/2',
                 'source': 'sloka',
                 'quote': 'or be in the 6th, the 8th or the 12th from the '
                          'Ascendant.',
                 'pdf_page': '213',
                 'ocr_flag': ''},
                {'predicate': 'in the 5th, the 9th, the 11th, the 2nd or kendra',
                 'houses': '5(?),9,11,2,kendra (not enumerated)',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'opulence and glory, happiness to wife, gains through '
                            'the king (government), comforts of good food and '
                            'clothes, religious mindedness, name and fame in the '
                            'country, interest in Vedas and Vedanta, performance '
                            'of religious sacrifices, giving grains etc. in '
                            'charity',
                 'source': 'sloka',
                 'quote': '76-78. There will be opulence and glory, happiness to '
                          'rvife, gains through the king (government), comforts of '
                          "good food and clothes, ... ir Jupiter be in the'Sth, "
                          'the 9th, the llth, the 2nd or kendra from the lord of '
                          'the Dasa (Saturn).',
                 'pdf_page': '213',
                 'ocr_flag': 'OCR AMBIGUITY UNRESOLVED: "the\'Sth" could be 5th or '
                             '8th on the glyph alone. Read as 5th only because 8th '
                             'would contradict vv.79-80 (which makes the 8th from '
                             'the Dasa lord adverse) — but that is inference, not '
                             'the text. FLAG for verification against the printed '
                             "book. 'ir'=if, 'rvife'=wife."},
                {'predicate': 'be weak AND in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of thc Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Antagonism with kinsmen, mental agony, quarrels, loss '
                            'of position, losses in ventures, loss of wealth as a '
                            'result of imposition of fines or penalties by '
                            'government, imprisonment, distress to wife and son',
                 'source': 'sloka',
                 'quote': '79-80. Antagonism with kinsmen, mental agony, quarrels, '
                          'loss of position, losses in ventures, loss of wealth as '
                          'a result of imposition of fines or penalties by '
                          "government, imprison'ment, distress to wife and son, "
                          'will be the results if Jupiter be weak and be in the '
                          '6th, the 8th or the l2th from the lord of thc Dasa '
                          '(Saturn).',
                 'pdf_page': '213',
                 'ocr_flag': "CONJUNCTIVE 'weak and' — weakness is not defined in "
                             'this chapter'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the Ascendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress, agony, death of the native or any '
                            'member of family',
                 'source': 'sloka',
                 'quote': '8l-82. Thcre will be physical distress, agony, death of '
                          'the native or any member offarnily, ifJupiter.be the '
                          'lord of the 2nd ol the 7th (from the Ascendant).',
                 'pdf_page': '214',
                 'ocr_flag': 'FRAME IS PARENTHESISED — translator interpolation, '
                             "not sloka text. 'offarnily'=of family, 'ol'=or. One "
                             'of only three cells whose maraka clause names death. '
                             'Per ch.34 no polarity attached.'}],
 'maraka': '8l-82. Thcre will be physical distress, agony, death of the native or '
           'any member offarnily, ifJupiter.be the lord of the 2nd ol the 7th '
           '(from the Ascendant).',
 'remedy': 'Remedial measures to obtain relief from the above evil effects are '
           'recitation of Shiva Sahasranama and giving gold in charity.'},
    ('saturn', 'ketu'): {'verses': '16-23',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, or in a '
                              'benefic sign (CONCESSIVE — the evil result follows '
                              'EVEN IF this holds)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Evil effects',
                 'results': 'loss of position, dangers, poverty, distress, foreign '
                            'journeys etc., will be derived',
                 'source': 'sloka',
                 'quote': "16.18.Evileffectslikelossofposition,dangers,poverty' "
                          'distress, foreign journeys etc., will be derived in the '
                          'Antardasa ;ii;i; in thJ 6uru oi Saturn even if Ketu be '
                          'in his sien of exaltation, in his own sign, in a '
                          'benefic sign or in kendra or ;tik.;" or be associated '
                          "wittr or aspected by benefics'",
                 'pdf_page': '204',
                 'ocr_flag': 'Heavy OCR damage: word-spacing collapsed in the '
                             "first line; ';ii;i;'=of Ketu, '6uru'=Dasa, "
                             '\'sien\'=sign, \';tik.;"\'=trikona. CONCESSIVE '
                             "structure ('even if') — good placements yield the "
                             'evil result.'},
                {'predicate': 'in kendra or trikona',
                 'houses': 'kendra/trikona — not enumerated in the text',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Evil effects',
                 'results': 'loss of position, dangers, poverty, distress, foreign '
                            'journeys etc.',
                 'source': 'sloka',
                 'quote': 'even if Ketu be in his sien of exaltation, in his own '
                          'sign, in a benefic sign or in kendra or ;tik.;" or be '
                          "associated wittr or aspected by benefics'",
                 'pdf_page': '204',
                 'ocr_flag': "CRITICAL: NO REFERENCE FRAME STATED for 'kendra or "
                             "trikona'. Do not infer one. The following verse (19) "
                             'supplies a frame for a different rule, which is not '
                             'licence to import it here.'},
                {'predicate': 'associated with or aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Evil effects',
                 'results': 'loss of position, dangers, poverty, distress, foreign '
                            'journeys etc.',
                 'source': 'sloka',
                 'quote': "or be associated wittr or aspected by benefics'",
                 'pdf_page': '204',
                 'ocr_flag': "still inside the 'even if' concessive"},
                {'predicate': 'related to the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of wealth and enjoyment and bathing in holy '
                            'places and visit to a sacred shrine at the '
                            'commencement of the Antardasa',
                 'source': 'sloka',
                 'quote': 'If Kett: be related to the lord of the Ascendant, there '
                          'will be garn or wealth and enjoyment and bathing in '
                          'holy places and vi:iir to a sacred shrine at tlte '
                          "commencement of the Antarda*sa'",
                 'pdf_page': '204',
                 'ocr_flag': "'Kett:'=Ketu, 'garn or wealth'=gain of wealth, "
                             "'vi:iir'=visit. 'related to' is undefined in this "
                             'chapter.'},
                {'predicate': 'in kendra, trikona, the 3rd or the 11th',
                 'houses': 'kendra/trikona (not enumerated), 3, 11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Gain of physical strength and courage, religious '
                            'thoughts, audience with the king (high dignitaries in '
                            'government — like president, prime minister, '
                            'governor, ministers), and all kinds of enjoyments, '
                            'will be experienced',
                 'source': 'sloka',
                 'quote': "19'19+. Gain of physical strength and courage' "
                          'rcligious thoughts, audience with the king {high '
                          'dignitaries. ... and all kinds of enjoyments, will be '
                          'experienced if Ketu be in *rOt", trikona, the 3rd or '
                          'the llth from the lord of the Dasa (Saturn).',
                 'pdf_page': '204',
                 'ocr_flag': '\'*rOt"\' = kendra (badly damaged); the gloss in '
                             "braces is the translator's, the frame words are not"},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Fear of premature death, coarse food, cold fever, '
                            'dysentry, wounds, danger from thieves, separation '
                            'from wife and children etc.',
                 'source': 'sloka',
                 'quote': '20-21+. Fear of premature death, coarse fool, cold '
                          'fever, ,dysentry, wounds, danger from thieves, '
                          'separation from -wife .and children etc., will be the '
                          'rpsults if Ketu be iri the 8th or the l2th from the '
                          'Ascendant or the lord of the Dasa (Saturn).',
                 'pdf_page': '204',
                 'ocr_flag': "'coarse fool'=coarse food, 'rpsults'=results. "
                             'DISJUNCTIVE FRAME — split into two rows.'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as the from-Ascendant row',
                 'source': 'sloka',
                 'quote': 'if Ketu be iri the 8th or the l2th from the Ascendant '
                          'or the lord of the Dasa (Saturn).',
                 'pdf_page': '204',
                 'ocr_flag': 'second half of the disjunction in vv.20-21 1/2'},
                {'predicate': 'be IN the 2nd or the 7th (placement, NOT lordship)',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'frqm the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '22-23. There will be physical distress, if Ketu be in '
                          'the 2nd or the 7th frqm the Ascendant.',
                 'pdf_page': '204',
                 'ocr_flag': "'frqm'=from. UNIQUE: the only maraka-slot clause in "
                             'the chapter phrased as PLACEMENT in the 2nd/7th '
                             'rather than LORDSHIP of them. Do not normalise to '
                             'the lordship form. Per ch.34 no polarity attached.'}],
 'maraka': '22-23. There will be physical distress, if Ketu be in the 2nd or the '
           '7th frqm the Ascendant.',
 'remedy': 'Remedial measures to obtain relief from the above evil effects and to '
           'regain enjoyments of life by the beneficence of Ketu is giving a goat '
           'in charity.'},
    ('saturn', 'mars'): {'verses': '55-62',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'enjoyments, gain of wealth, reverence from the king '
                            '(government), gain of conveyances, clothes and '
                            'ornaments, attainment of the position of a Commander '
                            'of the Army, increase in agricultural and cattle '
                            'wealth, construction of a new house, happiness to '
                            'kinsmen, will be derived from the very commencement '
                            'of the Antardasa',
                 'source': 'sloka',
                 'quote': '55-57. Effects like enjoyments, gain of wealth, '
                          'reverence from the king (governnrent), ... will be '
                          'derived from the very commencement of the Antardasa of '
                          'Mars in the Dasa of Saturn, if Mars be in his sign of '
                          'exaltation, in bis own sign or be associated with the '
                          'lord of thc Ascendant or the Dasa lord (Saturn).',
                 'pdf_page': '209-210',
                 'ocr_flag': "'bis'=his, 'thc'=the; sentence spans the p.209/p.210 "
                             'boundary'},
                {'predicate': 'associated with the lord of the Ascendant or with '
                              'the Dasa lord (Saturn)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.55-57',
                 'source': 'sloka',
                 'quote': 'or be associated with the lord of thc Ascendant or the '
                          'Dasa lord (Saturn).',
                 'pdf_page': '210',
                 'ocr_flag': 'ASSOCIATION with the Dasa lord, not a house count '
                             'from it — do not classify as from_dasa_lord'},
                {'predicate': 'in his sign of debilitation or combust',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'loss of wealth, danger of wounds, danger from '
                            'thieves, snakes, weapons, gout and other similar '
                            'diseases, distress to father and brothers, quarrels '
                            'with co-partners, loss of kinsmen, coarse food, going '
                            'away to foreign lands, unnecessary expenditure, etc.',
                 'source': 'sloka',
                 'quote': '58-60. There will be loss. of wealth, danger of wounds, '
                          'danger from thieves, snakes, weapons, gout and other '
                          'similar diseases, ... if Mars be iu his sign of '
                          'debilitation or combust, or bc in the 8th or the l2th '
                          'from the Ascendant and be associated with or aspected '
                          'by malefics.',
                 'pdf_page': '210',
                 'ocr_flag': 'THIS BLOCK IS PRINTED AFTER vv.61-62 on p.210 '
                             "(column scrambling). 'iu'=in, 'bc'=be."},
                {'predicate': 'in the 8th or the 12th AND associated with or '
                              'aspected by malefics',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.58-60',
                 'source': 'sloka',
                 'quote': 'or bc in the 8th or the l2th from the Ascendant and be '
                          'associated with or aspected by malefics.',
                 'pdf_page': '210',
                 'ocr_flag': "CONJUNCTIVE 'and' — the malefic association appears "
                             'required here, unlike the parallel Sun/Ketu clauses '
                             'where the 8th/12th alone suffices. Flagged, not '
                             'normalised.'},
                {'predicate': 'be IN the 2nd (placement)',
                 'houses': '2',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Great distress, dependence on others and fear of '
                            'premature death, may be expected',
                 'source': 'sloka',
                 'quote': '61.62. Great distress, dependence on others and fear of '
                          "prematurg death, may be expected if Mars be in'the 2nd "
                          'or be ths lord of the 7th or the 8th from the '
                          'Ascendant.',
                 'pdf_page': '210',
                 'ocr_flag': "'prematurg'=premature, 'ths'=the. HYBRID CLAUSE — "
                             "'be in the 2nd' (placement) vs 'be the lord of the "
                             "7th or the 8th' (lordship). The trailing 'from the "
                             "Ascendant' most naturally governs both, but the "
                             'split is unresolved. Per ch.34 no polarity '
                             'attached.'},
                {'predicate': 'be the LORD of the 7th or the 8th (lordship)',
                 'houses': '7,8',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as the 2nd-placement row',
                 'source': 'sloka',
                 'quote': "if Mars be in'the 2nd or be ths lord of the 7th or the "
                          '8th from the Ascendant.',
                 'pdf_page': '210',
                 'ocr_flag': 'THE ONLY maraka-slot clause in the chapter that '
                             'brings in the 8th house; every other cell uses '
                             '2nd/7th only. Flagged as a genuine textual outlier, '
                             'not OCR.'}],
 'maraka': '61.62. Great distress, dependence on others and fear of prematurg '
           "death, may be expected if Mars be in'the 2nd or be ths lord of the 7th "
           'or the 8th from the Ascendant.',
 'remedy': 'The remedial measures to obtain relief from the above evil effects are '
           'performance of Havana and giving a bull in charity.'},
    ('saturn', 'mercury'): {'verses': '8-15',
 'conditions': [{'predicate': 'in a kendra or trikona',
                 'houses': 'kendra/trikona — not enumerated in the text',
                 'frame': 'from_lagna',
                 'frame_quote': '(from the tscendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'reverence from the people, good reputation, gain of '
                            'wealth, comforts of conveyances etc., inclination '
                            'towards performance of religious sacrifices, '
                            'Rajayoga, bodily felicity, enthusiasm, well being in '
                            'the family, pilgrimage to holy places, performance of '
                            'religious rites, listening to Puranas, charities, '
                            'availability of sweetish preparations, etc., will be '
                            'derived',
                 'source': 'sloka',
                 'quote': '8-11. Effects like reverence from the people, good '
                          'reput- ation, gain of wealth, ... will be derived in '
                          'the Antardasa of Mercury in the Dasa of Saturn, if '
                          'Mercury be in a kendra or trikona (from the tscendant).',
                 'pdf_page': '202',
                 'ocr_flag': "FRAME IS PARENTHESISED — '(from the Ascendant)' is "
                             'translator interpolation in this edition, not sloka '
                             "text; 'tscendant' = Ascendant. Weaker frame evidence "
                             'than the unbracketed cases.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Acquisition of a kingdom (attainment of a high '
                            'position in Government), gain of wealth, headship of '
                            'a village at the commencement of the Dasa; affliction '
                            'with diseases, failure in all ventures, anxiety and '
                            'feeling of danger etc. in the middle portion and last '
                            'part',
                 'source': 'sloka',
                 'quote': 'l2-13t. Acquisition of a kingdom (attainment of a high '
                          'position in Government), gain of wealth, headship of.a '
                          'village, will be the effects at the commencemeitt of '
                          'the Dasa, if Mercury be in the 6th, the 8th or the '
                          'l2th, from the Ascendant or the iord of the Dasa '
                          '(Saturn) or be associated with the Sun, Mars and Rahu.',
                 'pdf_page': '203',
                 'ocr_flag': 'DISJUNCTIVE FRAME — one sentence states two frames; '
                             "split into two rows. 'iord' = lord."},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the iord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as the from-Ascendant row: good effects at '
                            'commencement, affliction with diseases, failure in '
                            'all ventures, anxiety and feeling of danger in the '
                            'middle and last part',
                 'source': 'sloka',
                 'quote': 'if Mercury be in the 6th, the 8th or the l2th, from the '
                          'Ascendant or the iord of the Dasa (Saturn) or be '
                          'associated with the Sun, Mars and Rahu.',
                 'pdf_page': '203',
                 'ocr_flag': 'second half of the disjunction in vv.12-13 1/2'},
                {'predicate': 'associated with the Sun, Mars and Rahu',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.12-13 1/2',
                 'source': 'sloka',
                 'quote': 'or be associated with the Sun, Mars and Rahu.',
                 'pdf_page': '203',
                 'ocr_flag': 'text does not say whether all three or any one '
                             'suffices — unresolved'},
                {'predicate': 'editorial doubt about vv.12-13 1/2 — the translator '
                              'disbelieves that good effects follow from this '
                              'placement, but declines to alter it',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'no rule stated; commentary only',
                 'source': 'note',
                 'quote': 'Note : It is difficult for us to believe that very good '
                          "cffects at the comlencement of the Dasa can be' "
                          'expected with Mercury so i2a.uspiciously placed. But we '
                          'dare no[ question Parasara.',
                 'pdf_page': '203',
                 'ocr_flag': "'i2a.uspiciously' = inauspiciously. SANTHANAM NOTE — "
                             'must never be promoted to mula; it contradicts the '
                             'sloka it comments on.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '14-15. There will be physical distress if Mercury be '
                          'the lord of the 2nd or the 7th.',
                 'pdf_page': '203',
                 'ocr_flag': "NO frame given — omits 'from the Ascendant' unlike "
                             'five other cells. No death stated, only physical '
                             'distress.'}],
 'maraka': '14-15. There will be physical distress if Mercury be the lord of the '
           '2nd or the 7th.',
 'remedy': 'The remedial measures to obtain relief from the above evil effects and '
           'to regain enjoyment in life are recitation of Vishnu Sahasranam and '
           'giving grams in charity.'},
    ('saturn', 'moon'): {'verses': '43-54',
 'conditions': [{'predicate': 'be full',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gains of conveyance, garments, ornaments, betterment '
                            'of fortune and enjoyments, taking care of brothers, '
                            'happiness in both maternal and paternal homes, '
                            'increase in cattle wealth etc., will be derived',
                 'source': 'sloka',
                 'quote': '43-45. Effects like gains of conveyance, garments, '
                          'orrril- ments, betetrment of fortune and enjoyments, '
                          '... will be derived in the Antardasa of the Moon iu the '
                          'Dasa of Saturn, if the Moon be full, in her sign of '
                          'exaltation, in her own sign or in kendra, trikona or '
                          'the llth from the Dasa lord or aspected by benefics.',
                 'pdf_page': '208',
                 'ocr_flag': "'orrril-ments'=ornaments, 'betetrment'=betterment"},
                {'predicate': 'in her sign of exaltation or in her own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.43-45',
                 'source': 'sloka',
                 'quote': 'if the Moon be full, in her sign of exaltation, in her '
                          'own sign or in kendra, trikona or the llth from the '
                          'Dasa lord or aspected by benefics.',
                 'pdf_page': '208',
                 'ocr_flag': ''},
                {'predicate': 'in kendra, trikona or the 11th',
                 'houses': 'kendra/trikona (not enumerated), 11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the Dasa lord',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.43-45',
                 'source': 'sloka',
                 'quote': 'or in kendra, trikona or the llth from the Dasa lord or '
                          'aspected by benefics.',
                 'pdf_page': '208',
                 'ocr_flag': "phrased 'from the Dasa lord' — the only place in the "
                             "chapter using this shorter form instead of 'from the "
                             "lord of the Dasa (Saturn)'"},
                {'predicate': 'aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.43-45',
                 'source': 'sloka',
                 'quote': 'or aspected by benefics.',
                 'pdf_page': '208',
                 'ocr_flag': ''},
                {'predicate': 'be waning, or associated with/aspected by malefics, '
                              'or in his sign of debilitation, or in cruel '
                              'Navamsa, or in the sign of a cruel (malefic) planet',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'great distress, wrath, separation from parents, ill '
                            'health of children, losses in business, irregular '
                            'meals, administration of medicines',
                 'source': 'sloka',
                 'quote': '46-48+. There will Qe great distress, wrath, separation '
                          'from parents ill, health of children, losses in '
                          'business, irregular meals, administration of medicines, '
                          'if the Moon be waning, be associated with or aspected '
                          'by malefics, be in his sign of debilitation, in cruel '
                          'Navamsa or in the sign of a cruel (malefic) planet.',
                 'pdf_page': '208',
                 'ocr_flag': "'Qe'=be. 'cruel Navamsa' (krura navamsa) is not "
                             "defined in this chapter. Text says 'his' for the "
                             "Moon here but 'her' in vv.43-45."},
                {'predicate': 'same placement as vv.46-48 1/2 — at the '
                              'commencement of the Antardasa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'good effects',
                 'results': 'There will, however, be good effects and some gains '
                            'of wealth at the commencement of the Antardasa.',
                 'source': 'sloka',
                 'quote': "There will, however, be good effects' and some gains of "
                          'lvealth at the commencement of the Antardasa.',
                 'pdf_page': '208',
                 'ocr_flag': "'lvealth'=wealth. A timing sub-clause reversing the "
                             'branch it sits in — one of only four explicit '
                             'valence labels in the chapter.'},
                {'predicate': 'general editorial claim that an ill-placed '
                              'Antardasa lord yields nothing good — no sloka basis '
                              'given',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'no rule stated; commentary only',
                 'source': 'note',
                 'quote': "Note :'Our belief-is nothing good may be expected if "
                          'the. Antardasa lord is ill placed.',
                 'pdf_page': '208',
                 'ocr_flag': "SANTHANAM NOTE — directly qualifies the sloka's "
                             "'good effects at the commencement' concession. Must "
                             'never be promoted to mula.'},
                {'predicate': 'in kendra, trikona or the 11th',
                 'houses': 'kendra/trikona (not enumerated), 11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Srturrr)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Enjoyment of conveyances and garments, happiness from '
                            'kinsmen, happiness from parents, wife, employer etc.',
                 'source': 'sloka',
                 'quote': "49-501. Errjoyment of conve)'ances and garmetRts' "
                          "ha;lpiness fi'om kinsmen, happineds from parellts, "
                          'lvife, emplol-er etc., will be the results if the Moon '
                          'be in kendra, trikona or the llth from the lord of the '
                          'Dasa (Srturrr).',
                 'pdf_page': '209',
                 'ocr_flag': "'(Srturrr)'=(Saturn). Duplicates the house set of "
                             'the vv.43-45 clause with a different result list — '
                             'the text does not reconcile them.'},
                {'predicate': 'be weak AND in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'sleepiness, lethargy, loss of position, loss of '
                            'enjoyments, increase in the number of enemies, '
                            'antagonism with kinsmen, will be experienced',
                 'source': 'sloka',
                 'quote': '51-52. Effects like sleepiness, lethargy, loss of '
                          "position,loss of enjol'ments, iucrease in the number of "
                          'enemies, autlgonism rvith kiusmen, will be experienced, '
                          'if the Moon be weak and be in thr 6th. the Sth or the '
                          'l2th from the lord of the Dasa (Saturn).',
                 'pdf_page': '209',
                 'ocr_flag': "'the Sth'=the 8th; 'thr'=the. Note the CONJUNCTIVE "
                             "'weak AND' — weakness is not defined in this "
                             'chapter.'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'lethargy and physical distress',
                 'source': 'sloka',
                 'quote': '53-54. There will be lethargy and physical distress if '
                          'the Moo.n be the lord of the 2nd or the 7th from the '
                          'Ascendant.',
                 'pdf_page': '209',
                 'ocr_flag': 'Per ch.34 no polarity attached.'}],
 'maraka': '53-54. There will be lethargy and physical distress if the Moo.n be '
           'the lord of the 2nd or the 7th from the Ascendant.',
 'remedy': 'The remedial measures to obtain relief from the above evil effects and '
           'prolongation of longevity are Havana and giving jaggery, ghee, rice '
           'mixed with curd, a cow or a female buffalo in charity.'},
    ('saturn', 'rahu'): {'verses': '63-70',
 'conditions': [{'predicate': 'NOT in his house of exaltation or any other '
                              'auspicious position (negative condition)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'quarrels, mental agony, physical distress, agony, '
                            'antagonism with the sons, danger from diseases, '
                            'unnecessary expenditure, discord with close '
                            'relations, danger from the government, foreign '
                            'journeys, loss of house and agricultural lands, will '
                            'be derived',
                 'source': 'sloka',
                 'quote': '63-64.Effects I re quarrels, mental agony. physical '
                          'distress, agony, antagonism with the sons, danger from '
                          'diseases, unecessary expenditure, discord with close '
                          'relations,:danger from the government, foreign '
                          'journeys, loss of house and agricultural Iands, will be '
                          'derived in the Antardasa of Rahu in the Dasa of Saturn, '
                          'if Rahu not be in his house of exaltation or any other '
                          'ruspicious position.',
                 'pdf_page': '211',
                 'ocr_flag': "'ruspicious'=auspicious, 'unecessary'=unnecessary, "
                             "'Effects I re'=Effects like. NEGATIVELY stated "
                             "condition; 'any other auspicious position' is left "
                             'undefined — the text does not settle it. '
                             "'auspicious' here qualifies the CONDITION, not the "
                             'result — NOT a polarity marker.'},
                {'predicate': 'associated with the lord of the Ascendant or a '
                              'yogakaraka planet',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Enjoyment, gains of wealth, increase in agricultural '
                            'production, devotion to deities and Brahmins, '
                            'pilgrimage to holy places, increase in cattle wealth, '
                            'well being in the family at the commencement of the '
                            'Antardasa; cordiality with the king and happiness '
                            'from friends in the middle portion',
                 'source': 'sloka',
                 'quote': '65-67. Ilnjoyment, gains of wealth, increase in '
                          'agricultural productioir. devotion io ileities and '
                          'Brahmins, ... will be the results at the commencement '
                          'of the Antardasa, if Rahu be associated with the lord '
                          'of tlre Ascendant r or a yogakaraka planet, be in his '
                          'sign of exaltatio! , or in his. own sign or be in '
                          'kendra or the llth from the Ascendant or the lord of '
                          "the Dasa (Saturn). There will be cordiality'rruith the "
                          'king and happiness from friEnds in the middle portion '
                          'of the Antardasa.',
                 'pdf_page': '211',
                 'ocr_flag': "'exaltatio!'=exaltation, 'rruith'=with, "
                             "'friEnds'=friends"},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.65-67',
                 'source': 'sloka',
                 'quote': 'be in his sign of exaltatio! , or in his. own sign or '
                          'be in kendra or the llth from the Ascendant or the lord '
                          'of the Dasa (Saturn).',
                 'pdf_page': '211',
                 'ocr_flag': "Rahu's exaltation/own sign are not specified "
                             'anywhere in this chapter'},
                {'predicate': 'in kendra or the 11th',
                 'houses': 'kendra (not enumerated), 11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.65-67',
                 'source': 'sloka',
                 'quote': 'or be in kendra or the llth from the Ascendant or the '
                          'lord of the Dasa (Saturn).',
                 'pdf_page': '211',
                 'ocr_flag': 'DISJUNCTIVE FRAME — split into two rows'},
                {'predicate': 'in kendra or the 11th',
                 'houses': 'kendra (not enumerated), 11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.65-67',
                 'source': 'sloka',
                 'quote': 'or be in kendra or the llth from the Ascendant or the '
                          'lord of the Dasa (Saturn).',
                 'pdf_page': '211',
                 'ocr_flag': 'second half of the disjunction in vv.65-67'},
                {'predicate': 'in Aries, Virgo, Cancer, Taurus, Pisces or '
                              'Sagittarius (rasi placement)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of elephants, opulence and glory, cordial '
                            'relations with the king (government), gains of '
                            'valuable clothes',
                 'source': 'sloka',
                 'quote': '68-68-,rr. There will be acquisition of elephants, '
                          'opulence and glory, cordial relations with the king '
                          '(government), gains of valuable clothes, if Rahu be in '
                          'Aries, Virgo, Cancer, Taurus Pisces or Sagittarius.i',
                 'pdf_page': '212',
                 'ocr_flag': 'The ONLY rasi-based (sign, not house) condition in '
                             'the chapter; no frame is involved.'},
                {'predicate': 'qualifies vv.68-68 1/2 by adding a house/frame '
                              'requirement the sloka does not state',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "no independent rule; the note imposes 'well placed "
                            'with reference to the Ascendant or the lord of the '
                            "dasa and unafflicted' as a precondition",
                 'source': 'note',
                 'quote': 'Notes : Even in these signs Rahu has to be well placed '
                          'with reference to the Ascendant or the lord of the dasa '
                          'and be unaffiicted for attaining capability of giving '
                          'results mentioned above.',
                 'pdf_page': '212',
                 'ocr_flag': "'unaffiicted'=unafflicted. SANTHANAM NOTE that ADDS "
                             'a condition absent from the sloka — must never be '
                             'merged into the mula rule.'},
                {'predicate': 'be ASSOCIATED WITH the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '69-70. There will be physical distress, if Rahu be '
                          'associ- ated with the lord of the 2nd or the 7th.',
                 'pdf_page': '212',
                 'ocr_flag': 'TWO departures from the chapter norm: no frame is '
                             'stated, and the test is ASSOCIATION WITH the 2nd/7th '
                             'lord rather than being that lord (Rahu owns no sign, '
                             'so the lordship form is unavailable). Per ch.34 no '
                             'polarity attached.'}],
 'maraka': '69-70. There will be physical distress, if Rahu be associ- ated with '
           'the lord of the 2nd or the 7th.',
 'remedy': 'The remedial measures to obtain relief from the above evil effects are '
           'Mrityunjaya Japa and giving a goat in charity.'},
    ('saturn', 'saturn'): {'verses': '1-7',
 'conditions': [{'predicate': 'in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquidtion of a kingdom (attainment of a high '
                            "positibn in government), happiness from rl'ife and "
                            'children, acquisition of conveyances like elephants, '
                            'gain of clothes, attainment of the position of a '
                            'connmander. of the armyby the beneficence of the '
                            "king, acquisition'cf cattle, villages and land etc., "
                            'will be derived',
                 'source': 'sloka',
                 'quote': 'l-3. Effects like acquidtion of a kingdom ... will be '
                          "derived in' .the Antardasa of Saturn in the Dasa of "
                          'Saturn, if Saturn be in his own sign, in his sign of '
                          'exaltation or in deep exaltation, or be in kendta or '
                          'trikona from the Ascendant, or be a yogakaraka.',
                 'pdf_page': '201',
                 'ocr_flag': "'acquidtion', 'kendta' = OCR noise for acquisition / "
                             'kendra'},
                {'predicate': 'in his sign of exaltation or in deep exaltation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.1-3',
                 'source': 'sloka',
                 'quote': 'if Saturn be in his own sign, in his sign of exaltation '
                          'or in deep exaltation, or be in kendta or trikona from '
                          'the Ascendant, or be a yogakaraka.',
                 'pdf_page': '201',
                 'ocr_flag': "'deep exaltation' (paramocca) is not defined in this "
                             'chapter'},
                {'predicate': 'in a kendra or trikona',
                 'houses': 'kendra/trikona — not enumerated in the text',
                 'frame': 'from_lagna',
                 'frame_quote': 'or be in kendta or trikona from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.1-3',
                 'source': 'sloka',
                 'quote': 'if Saturn be in his own sign, in his sign of exaltation '
                          'or in deep exaltation, or be in kendta or trikona from '
                          'the Ascendant, or be a yogakaraka.',
                 'pdf_page': '201',
                 'ocr_flag': "'kendta' = kendra"},
                {'predicate': 'be a yogakaraka',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.1-3',
                 'source': 'sloka',
                 'quote': 'or be a yogakaraka.',
                 'pdf_page': '201',
                 'ocr_flag': 'yogakaraka is not defined in this chapter'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'if Saturn be in the 8th or the l2th from the '
                                'Ascen- dant',
                 'polarity': 'adverse',
                 'polarity_word': 'evil effects',
                 'results': 'Fear or danger from the king (government), getting '
                            'inflicted with injuries with some weapon, bleeding '
                            'gulms, dysentry etc., at the commencement of the '
                            'Dasa; danger from thieves etc., going away from the '
                            'house land, mental agony etc. in the middle portion; '
                            'the last part will yield beneficial results',
                 'source': 'sloka',
                 'quote': "4-5{.'Fear or danger from the' king (government) "
                          'getting inflicted with injuries with some weapon, '
                          'bleeding gulms, ... dysentry etc., will be the evil '
                          'effects at ths commencement of the Dasa, if Saturn be '
                          'in the 8th or the l2th from the Ascen- dant or be '
                          'associated with malefics in his sign of debilitation.',
                 'pdf_page': '201-202',
                 'ocr_flag': "verse number renders '4-5{' = 4-5 1/2; sentence "
                             'broken across the p.201/p.202 boundary'},
                {'predicate': 'associated with malefics in his sign of '
                              'debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil effects',
                 'results': 'same as the 8th/12th branch — evil effects at '
                            'commencement, danger from thieves etc. in the middle '
                            'portion',
                 'source': 'sloka',
                 'quote': 'will be the evil effects at ths commencement of the '
                          'Dasa, if Saturn be in the 8th or the l2th from the '
                          'Ascen- dant or be associated with malefics in his sign '
                          'of debilitation.',
                 'pdf_page': '202',
                 'ocr_flag': ''},
                {'predicate': 'same placement (8th/12th from Ascendant, or '
                              'malefic-associated in debilitation) — the last part '
                              'of the Dasa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'The last part of the Dasa will yield beneficial '
                            'results.',
                 'source': 'sloka',
                 'quote': 'There will be danger from thieves etc., going away from '
                          'the house land, mental agony etc. in the middle portion '
                          'of thc Dasa. The last part of the Dasa will yield '
                          'beneficial results.',
                 'pdf_page': '202',
                 'ocr_flag': 'a timing sub-clause of the vv.4-5 1/2 branch; no '
                             'separate placement condition is given for it'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'danger of premature death',
                 'source': 'sloka',
                 'quote': '6-7. There will be danger of premature death, if Saturn '
                          'be the lord of the 2nd or the 7th.',
                 'pdf_page': '202',
                 'ocr_flag': 'NO frame given — unlike the Venus/Sun/Moon/Mars '
                             "cells this clause omits 'from the Ascendant'. Maraka "
                             'clause: per ch.34 no benefic/malefic polarity '
                             'attached.'}],
 'maraka': '6-7. There will be danger of premature death, if Saturn be the lord of '
           'the 2nd or the 7th.',
 'remedy': 'Lord Shiva will afford protection and render relief if Mrityunjaya '
           'Japa is performed in the prescribed manner.'},
    ('saturn', 'sun'): {'verses': '37-42',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'good relations with employer, well being in the '
                            'family, happiness from children, gain of conveyances '
                            'and cattle, etc. will be derived',
                 'source': 'sloka',
                 'quote': "3?-381. Effe,:'- :ike good relations with employer, "
                          'well bcing in thc famity, happiness fronr children, '
                          'gain of conveya- nces and cattle, etc. will be derived '
                          'in the Antardasa of the Sun in the Dasa of Saturn, if '
                          'thc Sun be in his sign of exaltation, in his own sign '
                          'or be associated with the lord of the 9th or be in '
                          'kendra or trikona from the Ascendant associated with or '
                          'a:nccted by bcnefics.',
                 'pdf_page': '207',
                 'ocr_flag': "'Effe,:'- :ike'=Effects like; 'a:nccted'=aspected"},
                {'predicate': 'associated with the lord of the 9th',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.37-38 1/2',
                 'source': 'sloka',
                 'quote': 'or be associated with the lord of the 9th',
                 'pdf_page': '207',
                 'ocr_flag': 'this is a LORDSHIP association, not a house '
                             'placement of the Sun'},
                {'predicate': 'in kendra or trikona',
                 'houses': 'kendra/trikona — not enumerated in the text',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.37-38 1/2',
                 'source': 'sloka',
                 'quote': 'or be in kendra or trikona from the Ascendant '
                          'associated with or a:nccted by bcnefics.',
                 'pdf_page': '207',
                 'ocr_flag': ''},
                {'predicate': 'associated with or aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.37-38 1/2',
                 'source': 'sloka',
                 'quote': 'associated with or a:nccted by bcnefics.',
                 'pdf_page': '207',
                 'ocr_flag': 'unclear from the text whether this attaches only to '
                             'the kendra/trikona clause or to all four'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'heart disease, defamation, loss of position, mental '
                            'agony, separation from close relatives, obstacles in '
                            'industrial ventures, fevers, fears, loss of kinsmen, '
                            'loss of articles dear to the person',
                 'source': 'sloka',
                 'quote': '3941. Thcre will bc heart disease, defamation, loss of '
                          'position, mental agony, separation from close '
                          'relatives, obstacles in industrial v€ntures, fevers,. '
                          'fears, loss of kinsmen, loss of articles dear tb thc '
                          'person, if the Sun be in the 8th or the l2th from the '
                          "ascendant or tbe lord of the Dasa (Saturn)'",
                 'pdf_page': '207',
                 'ocr_flag': "verse number renders '3941' = 39-41. DISJUNCTIVE "
                             'FRAME — split into two rows.'},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or tbe lord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as the from-Ascendant row',
                 'source': 'sloka',
                 'quote': 'if the Sun be in the 8th or the l2th from the ascendant '
                          "or tbe lord of the Dasa (Saturn)'",
                 'pdf_page': '207',
                 'ocr_flag': 'second half of the disjunction in vv.39-41'},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Asce:rdant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '42. There will be physical distress if the Sun be the '
                          'lord of the 2nd or rhe 7th from the Asce:rdant.',
                 'pdf_page': '207',
                 'ocr_flag': "'Asce:rdant'=Ascendant, 'rhe'=the. Per ch.34 no "
                             'polarity attached.'}],
 'maraka': '42. There will be physical distress if the Sun be the lord of the 2nd '
           'or rhe 7th from the Asce:rdant.',
 'remedy': 'The worship of the Sun is the remedial measure to obtain relief from '
           'the above evil effects.'},
    ('saturn', 'venus'): {'verses': '24-36',
 'conditions': [{'predicate': 'in kendra, trikona or the 11th',
                 'houses': 'kendra/trikona (not enumerated), 11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'marriage, birth of a son, gain of wealth, sound '
                            'health, well being in the family, acquisition of a '
                            'kingdom (attainment of high position in government), '
                            'enjoyments by the beneficence of the king '
                            '(government), honours, gain of clothes, ornaments, '
                            'conveyance and other desired objects, will be derived',
                 'source': 'sloka',
                 'quote': '24-27*. Effects like marriage, birth of a son, gain of '
                          'wealth, sound health\';\'win"\'b\'eing in the family, '
                          'acquisition of a kingdom ... ivill be derive<l in the '
                          'Anfardasa of Venus in the Dasa of Saturn, if Venus be '
                          'in kendra, trikona or the llth associated with or. '
                          'aspected by benefics.',
                 'pdf_page': '205',
                 'ocr_flag': 'CRITICAL: NO REFERENCE FRAME STATED. Note also that '
                             'this section is COLUMN-SCRAMBLED on p.205 — vv.28-29 '
                             'are printed above this heading.'},
                {'predicate': 'associated with or aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.24-27 1/2',
                 'source': 'sloka',
                 'quote': 'if Venus be in kendra, trikona or the llth associated '
                          'with or. aspected by benefics.',
                 'pdf_page': '205',
                 'ocr_flag': 'the text gives no conjunction — unclear whether this '
                             'is additive to the house condition or an '
                             'alternative'},
                {'predicate': 'Jupiter favourable in transit during the period of '
                              'the Antardasa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'dawn of fortune and growth of property',
                 'source': 'sloka',
                 'quote': 'If duiing the period of Antardasa, Jupiter be '
                          'favourable in transit, there will de dawn of fortune '
                          'and growth ofproperty.',
                 'pdf_page': '205',
                 'ocr_flag': "'favourable' here qualifies the CONDITION (the "
                             'transit), not the result — NOT a polarity marker. '
                             "'favourable in transit' is undefined in this "
                             'chapter.'},
                {'predicate': 'Saturn favourable in transit',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Rajayoga or accomplishment of yoga rites',
                 'source': 'sloka',
                 'quote': 'If Saturn be favourable in transit, there rrill be '
                          'Rajayoga !ftsl; ol::A€cf?mplishmelt of yoga ri.tes',
                 'pdf_page': '205',
                 'ocr_flag': "badly damaged mid-clause; again 'favourable' "
                             'qualifies the transit condition, not the result'},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Distress to wife, loss of position, mental agony, '
                            'quarrels with close relations etc.',
                 'source': 'sloka',
                 'quote': "28-'19. Distress tb wife, loss of position, 'mental "
                          'alony, quarrels with close relations etc., will be the '
                          'results, if Venus be in his sign of debiliiation, '
                          'combust or bQ in the 6th, the 8th oithe 12th (fiorn the '
                          'Ascendant).',
                 'pdf_page': '205',
                 'ocr_flag': "verse number renders '28-\\'19' = 28-29; "
                             "'debiliiation'=debilitation, 'bQ'=be. THIS BLOCK IS "
                             'PRINTED OUT OF ORDER on p.205, before the Venus '
                             'heading — assignment to Venus rests on the verse '
                             'numbers, not the layout.'},
                {'predicate': 'combust',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.28-29',
                 'source': 'sloka',
                 'quote': 'if Venus be in his sign of debiliiation, combust or bQ '
                          'in the 6th, the 8th oithe 12th (fiorn the Ascendant).',
                 'pdf_page': '205',
                 'ocr_flag': 'combustion orb not defined in this chapter'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': '(fiorn the Ascendant)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same result list as vv.28-29',
                 'source': 'sloka',
                 'quote': 'or bQ in the 6th, the 8th oithe 12th (fiorn the '
                          'Ascendant).',
                 'pdf_page': '205',
                 'ocr_flag': 'FRAME IS PARENTHESISED — translator interpolation, '
                             "not sloka text. 'fiorn'=from, 'oithe'=or the."},
                {'predicate': 'in the 9th, the 11th or kendra',
                 'houses': '9,11,kendra (not enumerated)',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Fulfilment of ambitions by the beneficence of the '
                            'king, charities, performance of religious rites, '
                            'creation of interest in the study of Shastras, '
                            'composition of poems, interest in Vedanta etc., '
                            'listening to Puranas, happiness from wife and '
                            'children, will be experienced',
                 'source': 'sloka',
                 'quote': "30-31+. Fulfilment of ambitions by the bene{rc':nce of "
                          'the king, cl.arities, performance of religious ritbs, '
                          'r;rea.tion of inte- rest in the study of Shastras, ... '
                          "will be experienced, if Venus be in tire 9tl'!, the "
                          'llth or kendra from the lord of the Dasa (Saturn).',
                 'pdf_page': '206',
                 'ocr_flag': "'9tl'!'=9th, 'tire'=the"},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Daea (Saturn)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'eye trouble, fevers, loss of good conduct, dental '
                            'problems, heart disease, pain in arms, danger from '
                            'drowning or falling from a tree, antagonism towards '
                            'relations, with the officials of government and '
                            'brothers',
                 'source': 'sloka',
                 'quote': '32-34. There will be eye trouble, fevers,.loss of good '
                          'conduct, dental problems, heart disease, pain in arms, '
                          'danger from drowning or felling from a tree, entagonism '
                          'towards relations, with the officials of government and '
                          'brothers, if Venus be in the 6th, the Sth or the l2th '
                          'from the lord of the Daea (Saturn).',
                 'pdf_page': '206',
                 'ocr_flag': "'the Sth' = the 8th (confirmed by the 6/8/12 "
                             "pattern); 'felling'=falling, "
                             "'entagonism'=antagonism, 'Daea'=Dasa"},
                {'predicate': 'be the lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '35-36. There will be physical distress if Venus be thc '
                          'lord of the 2nd or ihe 7th from the Ascendant.',
                 'pdf_page': '206',
                 'ocr_flag': "'thc'=the, 'ihe'=the. Frame IS stated here, unlike "
                             'the Saturn/Mercury/Rahu cells. Per ch.34 no polarity '
                             'attached.'}],
 'maraka': '35-36. There will be physical distress if Venus be thc lord of the 2nd '
           'or ihe 7th from the Ascendant.',
 'remedy': 'The remedial measures to obtain relief from the above evil effects and '
           'to regain enjoyment and good health by the beneficence of Goddess '
           'Durga and performance of Durga Saptashati Patha and giving a cow or a '
           'female buffalo in charity.'},
    ('sun', 'jupiter'): {'verses': '32-39',
 'conditions': [{'predicate': 'in a kendra or trikona to the Ascendant',
                 'houses': 'kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'to the Ascendant',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'Marriage of the native, favours by the King '
                            '(government), gain of wealth and grains, birth of a '
                            'son, fulfilment of the ambitions by the beneficience '
                            'of the sovereign and gain of clothes',
                 'source': 'sloka',
                 'quote': 'Marriage of the native, favours by the King '
                          '(governmerrt) gain of wealth and grains, birth of a '
                          'son, fulfil- ment of the ambitions by the beneficience '
                          "of the sovereign and gain of clothes, u'ili i:,r the "
                          "auspicious effects derived in the' Antardasa of Jupiter "
                          'in t;\\r Dasa of the Sun if Jupiter be in kendra or '
                          'trikona to the Ascendant, in his sign of exaltation in '
                          'his own sign or in his ornn Yarga.',
                 'pdf_page': '143',
                 'ocr_flag': '"u\'ili i:,r" = will be; "ornn Yarga" = own Varga. '
                             'Note the frame preposition here is "to the '
                             'Ascendant", not "from" — recorded from_lagna.'},
                {'predicate': 'in his sign of exaltation, in his own sign, or in '
                              'his own Varga',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'Marriage of the native, favours by the King, gain of '
                            'wealth and grains, birth of a son, fulfilment of '
                            'ambitions, gain of clothes',
                 'source': 'sloka',
                 'quote': 'if Jupiter be in kendra or trikona to the Ascendant, in '
                          'his sign of exaltation in his own sign or in his ornn '
                          'Yarga.',
                 'pdf_page': '143',
                 'ocr_flag': '"in his own Varga" — WHICH varga is not specified. '
                             'GAP.'},
                {'predicate': 'lord of the 9th or 10th',
                 'houses': '9,10',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Acquisition of a kingdom (attainment of a high '
                            'position in government), comforts of conveyance like '
                            'palanquin, gain of position etc.',
                 'source': 'sloka',
                 'quote': "Acquisitiorr of a kingdom (attainment of a high' "
                          'positiorr in government), comforts of conveyance like '
                          'palat" luin (motor car in the present times), gain of '
                          'position etc., wili result if Jupiter be the lord of '
                          'the 9th or l0th.',
                 'pdf_page': '143',
                 'ocr_flag': '"palat" luin" = palanquin. "(motor car in the '
                             'present times)" is unmistakably Santhanam\'s '
                             'modernising gloss, not the sloka. Neutral verb, no '
                             'valence word.'},
                {'predicate': 'well placed with reference to the lord of the Dasa '
                              '(the Sun)',
                 'houses': '',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'with reference to rhe lord of the Dasa (the Sun)',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'Better fortune, charities, religious inclinations, '
                            'worship of deities, devotion to preceptor, fulfilment '
                            'of ambitions',
                 'source': 'sloka',
                 'quote': "Better fortunr,. pharities, reli: ., :'$ inclinations, "
                          'worship of deities, devotion to preceptor, ,u:iiimei,t. '
                          "of ambitions will be the auspicious effectg if'Jupiter "
                          'be well placed with reference to rhe lord of the Dasa '
                          '(the Sun).',
                 'pdf_page': '144',
                 'ocr_flag': '"pharities" = charities; ",u:iiimei,t." = '
                             'fulfilment. CRITICAL GAP: "well placed" is never '
                             'enumerated — no house list is given. The frame is '
                             'explicit but the predicate is not testable as '
                             'stated.'},
                {'predicate': 'in the 6th or the 8th[?] from the lord of the Dasa',
                 'houses': '6, and one further house DAMAGED (printed "6rh")',
                 'frame': 'from_dasa_lord',
                 'frame_quote': "f'om the lord of the Dasa",
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Distress to wife and children, pains in the body, '
                            'displeasure of the King, non-achievement of desired '
                            'goals, loss of wealth due to sinful deeds, mental '
                            'worries etc.',
                 'source': 'sloka',
                 'quote': 'Distress to wife and children, pains in the body, '
                          'displeasure of the King (government), non-achievement '
                          'of dcs:ired g-t als, loss of wealth due to sinful '
                          'deects, mentai worries etc.. *rir iesult in his '
                          "Antardasa if the Jupiter be in the 6th or the6rh f'om "
                          'the lord of the Dasa or be associated with marefics.',
                 'pdf_page': '144',
                 'ocr_flag': 'OCR DAMAGE ON A HOUSE NUMBER — printed "in the 6th '
                             'or the6rh from the lord of the Dasa". The second '
                             'house is unreadable; by parallel with other cells it '
                             'is most likely the 8th or the 12th, but ch.52 does '
                             'NOT settle it. FLAGGED, not resolved. Do not '
                             'implement the second house.'},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Distress to wife and children, pains in the body, '
                            'displeasure of the King, non-achievement of desired '
                            'goals, loss of wealth due to sinful deeds, mental '
                            'worries etc.',
                 'source': 'sloka',
                 'quote': '*rir iesult in his Antardasa if the Jupiter be in the '
                          "6th or the6rh f'om the lord of the Dasa or be "
                          'associated with marefics.',
                 'pdf_page': '144',
                 'ocr_flag': '"marefics" = malefics; "*rir iesult" = will '
                             'result.'}],
 'maraka': None,
 'remedy': 'Givirlg in charity gord, a tawny coroured cow (afrol rnr) wor- ship of '
           'lshta lord (era te), arc the remedial measures to obtain alleviation '
           'of the evil effr:cts and to achieve good health and happiness. '
           '(PDFPAGE 144)',
 'absence_notes': {'maraka': 'NONE. The Jupiter cell of ch.52 contains NO '
                             '2nd/7th-lordship death clause — the only cell that '
                             'omits any maraka verdict entirely. Recorded as '
                             'absent, not inferred.'}},
    ('sun', 'ketu'): {'verses': '58-64',
 'conditions': [{'predicate': 'UNCONDITIONAL — no condition of any kind is '
                              'attached',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Body pains, mental agony, loss of wealth, danger from '
                            'the king (government), quarrels with the kinsmen',
                 'source': 'sloka',
                 'quote': 'Body Pains, mental agony, loss of wealth, danger from '
                          'the king (govcrnment), quarrels with the kinsmen, will '
                          'be the effects of the Antardasa of Ketu in the Dasa of '
                          'the Sun.',
                 'pdf_page': '146',
                 'ocr_flag': 'STRUCTURALLY NOTABLE: the only opening clause in '
                             'ch.52 with NO condition — the Ketu antardasa in a '
                             'Sun mahadasa is given these effects flatly, with no '
                             'dignity or house qualifier. Every other cell opens '
                             "with an 'if'. Neutral verb, no valence label — "
                             'polarity none.'},
                {'predicate': 'associated with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'some happiness at the commencement, distress in the '
                            'middle part, and receipt of the news of death at the '
                            'end of the antardasa',
                 'source': 'sloka',
                 'quote': 'If Ketu be associated with the lord of the Ascendant, '
                          'there wilt bc some happiness at the commencement, '
                          'distress in the middlc part and receipt of the news of '
                          'death, at the eud of the Antar- dasa.',
                 'pdf_page': '146',
                 'ocr_flag': '"wilt bc" = will be; "eud" = end. A CONDITIONAL '
                             "timed clause (unlike Saturn's and Mercury's "
                             "unconditional ones). Internally mixed; 'death' here "
                             "is news of another's death, not a death verdict on "
                             'the native — polarity none.'},
                {'predicate': 'in the 8th or the 12th from the lord of the Dasa '
                              '(Sun)',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Sun)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Diseases of teeth or cheeks, urinary troubles, loss '
                            'of position, loss of friends and wealth, death of '
                            'father, foreign journey and troubles from enemies',
                 'source': 'sloka',
                 'quote': 'Diseases of teeth or cheeks, urinary troubles,loss of '
                          'position, loss of friends and wealth, death of father, '
                          'fgrcisn journey and troubres from enemies wil be the '
                          'i.csults ifKetu be in the 8th or the l2th from the lord '
                          'of the Dasa (Sun).',
                 'pdf_page': '147',
                 'ocr_flag': '"fgrcisn" = foreign; "i.csults" = results. Neutral '
                             "verb; 'death of father' is an outcome item, not a "
                             'valence label on the branch — polarity none.'},
                {'predicate': 'in the 3rd, the 6th[?], the 10th or the 11th from '
                              'the Ascendant',
                 'houses': '3, 6[?], 10, 11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'favourable',
                 'polarity_word': 'Beneficial',
                 'results': 'happiness from wife and children, satisfaction, '
                            'increase of friends, gain of clothes etc. and renown',
                 'source': 'sloka',
                 'quote': 'Beneficial effects like happiness from wife '
                          'andchildren, satisfaction, increase of frienjs, gain of '
                          'clothes etc.and renown, will be derived if Ketu be in '
                          'the 3rd, the fth, the 10th or the llth from the '
                          'Ascendant.',
                 'pdf_page': '147',
                 'ocr_flag': 'OCR DAMAGE ON A HOUSE NUMBER: printed "the fth". '
                             'Context strongly suggests 6th (yielding the upachaya '
                             'set 3,6,10,11 — the set the Rahu section spells out '
                             'on PDFPAGE 141) but the glyph is destroyed. FLAGGED. '
                             '"frienjs" = friends.'},
                {'predicate': 'lord of the 2nd or 7th (or, per the parenthetical, '
                              'placed in either)',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger of premature death',
                 'source': 'sloka',
                 'quote': 'If Ketu be lord.of the2nd or 7th (or be in any of thosc '
                          'houses), there will be dangerof premature dlath.',
                 'pdf_page': '147',
                 'ocr_flag': '"dlath" = death. The parenthetical "(or be in any of '
                             'those houses)" is an editorial extension — Ketu owns '
                             'no sign in the classical scheme, so lordship is '
                             'inapplicable and the bracket supplies occupancy '
                             'instead. Treat the bracketed limb as EDITORIAL, not '
                             'mula.'}],
 'maraka': 'If Ketu be lord.of the2nd or 7th (or be in any of thosc houses), there '
           'will be dangerof premature dlath. (PDFPAGE 147) — the parenthetical '
           'occupancy limb is editorial, since Ketu holds no lordship.',
 'remedy': 'The remedial mcasures for obtaining relief from the evil effects are '
           'recitation of mantras of Goddess Durga (Shat Chandi Patha vrosu-dl wo1 '
           'unC giving a goat in charity. (PDFPAGE 147)'},
    ('sun', 'mars'): {'verses': '15-22',
 'conditions': [{'predicate': 'in his sign of exaltation, or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Auspicious',
                 'results': 'acquisition of land, gain of wealth and grains, '
                            'acquisition of a house etc.',
                 'source': 'sloka',
                 'quote': 'Auspicious effects like acquisition of land, gain of '
                          'wealth and grains, acquisition of a house etc., will br '
                          'cierived in the Antardasa of Mars in the Dasa of the '
                          'S.,ii if Mars be in his sign of exaltation, in his own '
                          'sign, i,, kendra or trikona.',
                 'pdf_page': '140',
                 'ocr_flag': '"br cierived" = be derived; "S.,ii" = Sun; "i,," = '
                             'in.'},
                {'predicate': 'in a kendra or trikona',
                 'houses': 'kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Auspicious',
                 'results': 'acquisition of land, gain of wealth and grains, '
                            'acquisition of a house etc.',
                 'source': 'sloka',
                 'quote': 'if Mars be in his sign of exaltation, in his own sign, '
                          'i,, kendra or trikona.',
                 'pdf_page': '140',
                 'ocr_flag': 'No frame word — recorded unstated.'},
                {'predicate': 'in conjunction with the lord of the Ascendant',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'All round gains, attainment of the position of a '
                            'commander of the army, destruction of enemies, peace '
                            'of mind, family comforts, and increase in the number '
                            'of new-borns',
                 'source': 'sloka',
                 'quote': 'All round gains, attaiument of the position of a '
                          'commander of the army, destruction of enemies. peace cf '
                          'mind, [amil,"" comforts, and increase in the .number oi '
                          ',::-borns will be the effects if Mars be in conjunction '
                          'wiih .!\'\'": icrd of the Ascendant.',
                 'pdf_page': '140',
                 'ocr_flag': '"wiih .!\'\'": icrd of the Ascendant" = with the '
                             'lord of the Ascendant — recoverable from context. '
                             'Neutral verb, no valence word.'},
                {'predicate': 'in the 8th or the 12th from the lord of the Dasa',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Brutality, mental ailment, imprisonment, loss of '
                            'kinsmen, disputes with brothers and failure in '
                            'ventures',
                 'source': 'sloka',
                 'quote': "Brutality, rnen'al ailment, imprisonment, loss of "
                          'kinsmen. disputes with brothers and failure in ventures '
                          'will result if Mars be in the 8th or the l2th from the '
                          'lord of the Dasa, be associated with malefics or be '
                          'without dignity and itrength.',
                 'pdf_page': '140',
                 'ocr_flag': '"rnen\'al" = mental; "itrength" = strength. Note '
                             'this set is 8/12 only — NOT 6/8/12 as in the Moon '
                             'and Mercury cells. Do not normalise.'},
                {'predicate': 'associated with malefics, or without dignity and '
                              'strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Brutality, mental ailment, imprisonment, loss of '
                            'kinsmen, disputes with brothers and failure in '
                            'ventures',
                 'source': 'sloka',
                 'quote': 'will result if Mars be in the 8th or the l2th from the '
                          'lord of the Dasa, be associated with malefics or be '
                          'without dignity and itrength.',
                 'pdf_page': '140',
                 'ocr_flag': '"without dignity and strength" is not operationally '
                             'defined in ch.52. GAP.'},
                {'predicate': 'in his sign of debilitation, or weak',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Destruction of wealth by the displeasure of the King '
                            '(government)',
                 'source': 'sloka',
                 'quote': 'Destruction of wealth by the displeasure of the King '
                          '(governrnent) will be the effect if Mars be in his sign '
                          'if debilitation or be weak.',
                 'pdf_page': '140',
                 'ocr_flag': '"in his sign if debilitation" — "if" is an OCR error '
                             'for "of".'},
                {'predicate': 'lord of the 2nd or 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Diseases of the mind and body',
                 'source': 'sloka',
                 'quote': "Diseases of the mind and body will 'esult if Mars be "
                          'the tord of the 2nd or 7th.',
                 'pdf_page': '140',
                 'ocr_flag': 'NOTABLE: this is the 2nd/7th-lordship clause but the '
                             'stated result is DISEASE, not death — unlike the '
                             'Sun, Moon, Rahu, Saturn and Ketu cells. Do not '
                             'upgrade it to a death verdict.'}],
 'maraka': "Diseases of the mind and body will 'esult if Mars be the tord of the "
           '2nd or 7th. (PDFPAGE 140) — the 2nd/7th lordship clause is present but '
           'yields DISEASE, not premature death. A genuine divergence from the '
           'other cells; must not be normalised.',
 'remedy': 'Recovery from ll health, inc;ease in lbngevity and success in '
           'adventures are :ossible if remedial measure like recitation of Vedas, '
           'Japa, Vrashotsarga (Et}ewrt) are perforrned in the prescribed nanner. '
           '(PDFPAGE 140)'},
    ('sun', 'mercury'): {'verses': '48-57',
 'conditions': [{'predicate': 'in a kendra or trikona from the Ascendant',
                 'houses': 'kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from thc Ascendant',
                 'polarity': 'favourable',
                 'polarity_word': 'good',
                 'results': 'Acquisition of a kingdom (attainment of a high '
                            'position in government), enthusiasm and vivacity, '
                            'happiness from wife and children, acquisition of '
                            'conveyance through the beneficience of the Sovereign, '
                            'gain of clothes, ornaments, pilgrimage to holy '
                            'places, acquisition of a cow etc.',
                 'source': 'sloka',
                 'quote': 'Acquisition of a kingdom (attainment of a high position '
                          'in government), enthusiasm and vivacity, happiness '
                          "'from wife and children, acquisition of conveyance "
                          'through the beneficience of the Sovereign, gain of '
                          'clothes, ornaments, pil- grimage to holy Dlaces, '
                          'acquisition of a cow, etc., will be the good effects in '
                          'ih: Antardasa of Mercury in the Dasa of thc Sun, if '
                          'Mercury be in a kcndra or trikona from thc Ascendant.',
                 'pdf_page': '145',
                 'ocr_flag': '"Dlaces" = places; "ih:" = the; "kcndra" = kendra.'},
                {'predicate': 'associated with the lord of the 9th',
                 'houses': '9',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'beneficial',
                 'results': 'Mercury becomes very beneficial',
                 'source': 'sloka',
                 'quote': 'Mercury bccomes very beneficial if he gets asso- ciated '
                          'with the lord of the 9th.',
                 'pdf_page': '145',
                 'ocr_flag': 'This branch states a QUALITY of the graha, not an '
                             'outcome list — the only such clause in the chapter.'},
                {'predicate': 'in the 9th, the 5th[?] or the 10th',
                 'houses': '9, 5[?], 10',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'Reverence from and popularity amongst people, '
                            'performance of pious deeds and religious rites, '
                            'devotion to the preceptor and deities, increase in '
                            'wealth and grains, birth of a son',
                 'source': 'sloka',
                 'quote': 'Reverence from and popu- larity amongst people, '
                          'performance of pious deeds and religious rites, '
                          'devotion to the preceptor and deities, increase in '
                          'riealth and grians, birth of a son, will be auspicious '
                          "effects, if Mercury be in the 9th, the Sth or the l0th'",
                 'pdf_page': '145',
                 'ocr_flag': 'OCR DAMAGE ON A HOUSE NUMBER: printed "the Sth" — '
                             'almost certainly 5th (giving the 5/9/10 set) but '
                             'conceivably 8th. NOT resolved. Also: NO frame word — '
                             'recorded unstated. "riealth and grians" = wealth and '
                             'grains.'},
                {'predicate': 'in an auspicious house like trikona etc., from the '
                              'lord of the Dasa (the Sun)',
                 'houses': 'trikona 1,5,9 ("etc." left open)',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (The sun)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Marriage, offering of oblations, charity, performance '
                            'of religious rites, name and fame, becoming famous by '
                            'assuming another name, good food, becoming happy like '
                            'Indra by acquiring wealth, robes and ornaments',
                 'source': 'sloka',
                 'quote': "Marriage, offering of toblations, charity, per' "
                          'formance of religious rites, narle and fame, becoming '
                          "famous by assuming another natrle' good food, becoming "
                          'happy like Indra by acquiring wealth, robu and '
                          'ornaments, will be the effects if Mercury be in an '
                          "auspicious house like trikona etc'' from the lord of "
                          'the Dasa (The sun).',
                 'pdf_page': '145',
                 'ocr_flag': '"toblations" = oblations; "robu" = robes. GAP: "an '
                             'auspicious house like trikona etc." is open-ended — '
                             "the 'etc.' is never enumerated, so the predicate is "
                             "only partially testable. The word 'auspicious' "
                             'qualifies the PREDICATE (which house), not the '
                             'result — polarity none.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the Lord nf the Dasa',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'Body distress, disturbance of peace of mind, distress '
                            'to wife and children',
                 'source': 'sloka',
                 'quote': 'Body distress, disburbance of peace of mind, distress '
                          'to wife and children, will be the evil effects in the '
                          'Antardasa of Mercury, if he be in the 6th, the gth or '
                          'the l2th from the Lord nf the Dasa',
                 'pdf_page': '146',
                 'ocr_flag': '"disburbance" = disturbance; "the gth" = the 8th; '
                             '"nf" = of.'},
                {'predicate': 'editorial observation that this branch is partly '
                              'unreachable — Mercury is never more than one sign '
                              'from the Sun',
                 'houses': '6,8',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the Sun',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'n/a — commentary, not a prediction',
                 'source': 'note',
                 'quote': '(Mercury cannot be in the 6th or 8th from the Sun)',
                 'pdf_page': '146',
                 'ocr_flag': "SANTHANAM'S NOTE, not mula — it appears as a "
                             'parenthesis inside the running English translation. '
                             'It is a correct astronomical observation and it '
                             'means the 6th/8th limbs of the preceding sloka can '
                             'never fire in a Sun mahadasa; only the 12th-from-Sun '
                             'limb is reachable. Recorded as a note; the sloka '
                             'itself is unamended.'},
                {'predicate': 'UNCONDITIONAL — timed thirds of the antardasa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'evil effects at the commencement, some good effects '
                            'in the middle part, possibility of displeasure of the '
                            'king and exile to foreign country at the end',
                 'source': 'sloka',
                 'quote': 'There will be evil effects at the commence- ment of the '
                          'Antardasa, some good effects in the middle part of the '
                          'Antardasa and possibility of displeasure of the king '
                          'and exile to foreign country at the end,',
                 'pdf_page': '146',
                 'ocr_flag': 'No condition attached. Internally MIXED (explicit '
                             "'evil' at the start, explicit 'good' in the middle) "
                             'so polarity is recorded none rather than collapsed. '
                             'Note this timed pattern is similar to but NOT '
                             "identical with Saturn's — do not share an "
                             'implementation.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'pains in the body and attacks of fever',
                 'source': 'sloka',
                 'quote': 'If Mercury be the lord of thc 2nd or the 7th, there '
                          'will be pains in the body and attacks offever.',
                 'pdf_page': '146',
                 'ocr_flag': 'Like Mars, the 2nd/7th-lordship clause here yields '
                             'ILLNESS, not death. Do not upgrade.'}],
 'maraka': 'If Mercury be the lord of thc 2nd or the 7th, there will be pains in '
           'the body and attacks offever. (PDFPAGE 146) — 2nd/7th lordship is '
           'present but produces bodily affliction, NOT a death verdict. Per ch.34 '
           'the maraka axis is separate from benefic/malefic nature; here the text '
           'does not even reach a death verdict.',
 'remedy': 'Forrelieffromthe evil effects and to regain good hcalth and happiness '
           'the remedial measures are racitation of Vishnu Sahasranam (fngqW nr) '
           'and giving in charity grains and an idol made of silver. (PDFPAGE 146)'},
    ('sun', 'moon'): {'verses': '4-14',
 'conditions': [{'predicate': 'in a kendra or trikona',
                 'houses': 'kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Functions like marriage etc., gain of wealth and '
                            'property, acquisition of house, land, cattle and '
                            'conveyance etc.',
                 'source': 'sloka',
                 'quote': 'Functions like marriage etc., gain of wealth '
                          'andproperty, acquisition ofhouse, land, cattle and '
                          'conveyance etc.will be the effects of the Antardasa of '
                          'the Moon in the Dasaof the Sun, if the Moon be in a '
                          'kendra or trikona.',
                 'pdf_page': '138',
                 'ocr_flag': 'Word-spacing collapsed in OCR ("andproperty", '
                             '"ofhouse", "Dasaof"); no frame word present — '
                             'recorded unstated. Neutral verb "will be the '
                             'effects", no valence word.'},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'marriage of the native, birth of children, '
                            'beneficience of and favours from Kings (government) '
                            'and fulfilment of all ambitions',
                 'source': 'sloka',
                 'quote': 'Therewill be marriage of the native, birth of children, '
                          'beneficience ofand favours from Kings (government) and '
                          'fulfilment of allambitions, if the Moon be in his '
                          'sign,of exaltation or in hisown sign.',
                 'pdf_page': '138',
                 'ocr_flag': 'Spacing collapsed; "sign,of" stray comma. No valence '
                             'word.'},
                {'predicate': 'waning, or associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Distress to wife and children, failures in ventures, '
                            'disputes with others, loss of servants, antagonism '
                            'with the King (government) and destructions of wealth '
                            'and grains',
                 'source': 'sloka',
                 'quote': 'Distress to wife ancl children, failures in '
                          'ventures,disputes with others, loss of servants, '
                          'antagonism with the Kinj(government) and destructions '
                          'of wealth and grains, will bithe effects if the Moon be '
                          'w,-ining or be associated with mele-fics.',
                 'pdf_page': '138',
                 'ocr_flag': '"w,-ining" = waning; "mele-fics" = malefics; "Kinj" '
                             '= King. Outcomes sound bad but NO branch-level '
                             'valence label — polarity none by the cautious rule.'},
                {'predicate': 'in the 6th, the 8th or the 12th house',
                 'houses': '6,8,12',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'danger from water, mental agony, imprisonment, danger '
                            'from diseases, loss of position, journeys to '
                            'difficult places, disputes with coparceners, bad '
                            'food, trouble from thieves etc., displeasure of the '
                            'King, urinary troubles, pains in the body',
                 'source': 'sloka',
                 'quote': 'Effects like danqer from water, mental agony, '
                          "imprison-ment, danger Jrorn-diseases, tors'oi-fosition, "
                          'journeys todifficult places, disputes with coparceners, '
                          'bad food, troublefrom thieves etc., displeasure of the '
                          'King (government), ur inary troubles, pains in the body '
                          'will be experienced, if theMoon be in the 6th, rhe gth '
                          'or the l2th house.',
                 'pdf_page': '138',
                 'ocr_flag': '"rhe gth" = the 8th; "tors\'oi-fosition" = loss of '
                             'position. CRITICAL: the sentence says "house" with '
                             'NO frame — recorded unstated. Contrast vv.13-14 '
                             'below, which DOES say "from the lord of the Dasa" '
                             'for the same 6/8/12 set; the two clauses are NOT the '
                             'same rule.'},
                {'predicate': 'benefics in the 1st, 9th, or a kendra from the lord '
                              'of the Dasa',
                 'houses': '1,9; kendra 1,4,7,10',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'Luxuries, comforts, pleasures, dawn of fortune, '
                            'increase in enjoyment from wife and children, '
                            'acquisition of kingdom, performance of marriage and '
                            'religious functions, gain of garments, land and '
                            'conveyance and birth of children and grand children',
                 'source': 'sloka',
                 'quote': 'Luxuries, comforts, pleasures, dar."\'n of fot\'tune '
                          '(rrrd<r), increase inthe cnjoyment from wife and '
                          'child,,-*n, acquisition of kingdom, performance of '
                          'marriage anri reli;i..., .; functions, gain of '
                          "garnlents, land and conveyauce and t'. -rr of chidren "
                          'and grand children will be the auspicious effects if '
                          'there be benefics in the lst, 9th, kendra from the lord '
                          'of the Dasa.',
                 'pdf_page': '139',
                 'ocr_flag': 'Heavy OCR damage in the result list but the '
                             'CONDITION clause is clean and legible. Note this '
                             'condition is about BENEFICS being so placed, not the '
                             'Moon itself.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the I)asa',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Unpalatable food or coarse food, exile to outside '
                            'places etc.',
                 'source': 'sloka',
                 'quote': 'Unpalatable food or course food, exilc to outside '
                          'placcs etc. will be thc efTects in the Antardasa, if '
                          'the N{oon be in thc 6th, the 8th or the l2th from the '
                          'lord of the I)asa or be weak.',
                 'pdf_page': '139',
                 'ocr_flag': '"N{oon" = Moon; "I)asa" = Dasa; "course" = coarse. '
                             'Neutral verb, no valence word.'},
                {'predicate': 'weak',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Unpalatable food or coarse food, exile to outside '
                            'places etc.',
                 'source': 'sloka',
                 'quote': 'if the N{oon be in thc 6th, the 8th or the l2th from '
                          'the lord of the I)asa or be weak.',
                 'pdf_page': '139',
                 'ocr_flag': '"weak" is undefined in ch.52 — no strength metric is '
                             'given. GAP.'},
                {'predicate': 'lord of a maraka house (2nd or 7th)',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'premature death',
                 'source': 'sloka',
                 'quote': 'Thcre will be premature death if the Moon be the lord '
                          'of a maraka house (2nd or 7th).',
                 'pdf_page': '139',
                 'ocr_flag': '"(2nd or 7th)" is a parenthetical gloss on \'maraka '
                             "house' — likely Santhanam's expansion rather than "
                             "the sloka's own words."}],
 'maraka': 'Thcre will be premature death if the Moon be the lord of a maraka '
           'house (2nd or 7th). (PDFPAGE 139)',
 'remedy': 'To acquire peace and cornlbrt, the renedial measure is giving in '
           "charity ot' a white cow and a fcmale buffalo (qfqfr). (PDFPAGE 139)"},
    ('sun', 'rahu'): {'verses': '23-31',
 'conditions': [{'predicate': 'in a kendra or trikona from the Ascendant (first '
                              'two months of the antardasa)',
                 'houses': 'kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'in the first two months, loss of wealth, danger from '
                            'thieves, snakes, infliction of wounds and distress to '
                            'wife and children; after 2 months these effects '
                            'disappear',
                 'source': 'sloka',
                 'quote': 'In the Antardasa of Rahu in the Dasa of the Sun, if '
                          'Rahu be in kqndra or trikona from the Ascendant, there '
                          'will be in the first two months loss of wealth, danger '
                          "from thieves snakes, infliction of wounds'and distress "
                          "to wife and children. ' After 2 months inauspicious "
                          'effects will disappear',
                 'pdf_page': '141',
                 'ocr_flag': '"kqndra" = kendra. Polarity recorded adverse because '
                             'the following sentence explicitly names these same '
                             'effects "inauspicious effects" — the label is in the '
                             'sloka clause, though attached retrospectively. This '
                             'branch is TIME-SPLIT (first two months vs after), '
                             'which the engine must preserve.'},
                {'predicate': 'in conjunction with benefics, or in the Navamsa of '
                              'a benefic (after the first two months)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'favourable',
                 'results': 'enjoyment and comforts, sound health, satisfaction, '
                            'favours from the King and government etc.',
                 'source': 'sloka',
                 'quote': 'After 2 months inauspicious effects will disappear and '
                          'enjoy- ment and comforts, sound health, satisfaction, '
                          'favours from the King and government etc. will be the '
                          'favourable effects, if Rahu be in conjunction with '
                          'benefics or be in the Navamsa of a benefic.',
                 'pdf_page': '141',
                 'ocr_flag': ''},
                {'predicate': 'in an upachaya house (3,6,10,11) from the Ascendant',
                 'houses': '3,6,10,11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Recognition from the King (government), good fortune, '
                            'name and fame, some distress to wife and children, '
                            'birth of son, happiness in the family etc.',
                 'source': 'sloka',
                 'quote': 'Recognition from the King (government), good fortune, '
                          'name and fame, some distress to wife and children, '
                          'birth of son, happiness in the family etc., will be '
                          'derived if Rahu be in an upachaya house (3,6,10,11) '
                          'from the Ascendant, be associated with a yogakarka or '
                          'be placed auspiciously fron the loro of the l)asa.',
                 'pdf_page': '141',
                 'ocr_flag': '"yogakarka" = yogakaraka. "(3,6,10,11)" is a '
                             "bracketed enumeration — probably Santhanam's gloss "
                             "on 'upachaya'. Neutral verb; the result list MIXES "
                             'good and bad ("name and fame" alongside "some '
                             'distress to wife and children") — polarity none.'},
                {'predicate': 'associated with a yogakaraka',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Recognition from the King, good fortune, name and '
                            'fame, some distress to wife and children, birth of '
                            'son, happiness in the family etc.',
                 'source': 'sloka',
                 'quote': 'will be derived if Rahu be in an upachaya house '
                          '(3,6,10,11) from the Ascendant, be associated with a '
                          'yogakarka or be placed auspiciously fron the loro of '
                          'the l)asa.',
                 'pdf_page': '141',
                 'ocr_flag': 'ch.52 does not define who the yogakaraka is. GAP.'},
                {'predicate': 'placed auspiciously from the lord of the Dasa',
                 'houses': '',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'fron the loro of the l)asa',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Recognition from the King, good fortune, name and '
                            'fame, some distress to wife and children, birth of '
                            'son, happiness in the family etc.',
                 'source': 'sloka',
                 'quote': 'will be derived if Rahu be in an upachaya house '
                          '(3,6,10,11) from the Ascendant, be associated with a '
                          'yogakarka or be placed auspiciously fron the loro of '
                          'the l)asa.',
                 'pdf_page': '141',
                 'ocr_flag': '"placed auspiciously" is NOT enumerated — which '
                             'houses count as auspicious from the dasa lord is '
                             "never stated in ch.52. The word 'auspiciously' "
                             'qualifies the PREDICATE, not the result, so it is '
                             'not a polarity marker. GAP: unimplementable as '
                             'stated.'},
                {'predicate': 'weak, or in the 8th or 12th from the lord of the '
                              'Dasa (the Sun)',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': "from the lc.'rd of the Dasa (the Sun)",
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Imprisonment, loss of position, danger from thieves '
                            'and snakes, infliction of wounds, happiness to wife '
                            'and children, destruction of cattle, house, '
                            'agricultural fields, diseases, consumption, dysentry '
                            'etc.',
                 'source': 'sloka',
                 'quote': 'Imprisonment, loss of position, tianger fr*rm thieves '
                          'and snakes, inflection of wounds, happiness to wife and '
                          'chilciren, clestruction of cattle, house, agricultural '
                          'fields, diseases, consumption (get-enlargement of the '
                          'skin), dysentry etc.n wiil be the results, if Rahu be '
                          "weak or be in the 8th or l2th from the lc.'rd of the "
                          'Dasa (the Sun).',
                 'pdf_page': '141',
                 'ocr_flag': 'ANOMALY: "happiness to wife and chilciren" sits '
                             'inside an otherwise wholly afflictive list. Either '
                             'an OCR corruption of a negative phrase or a genuine '
                             'textual oddity — cannot be resolved from this '
                             'edition. Also "consumption (get-enlargement of the '
                             'skin)" is an incoherent gloss. Neutral verb, no '
                             'valence word.'},
                {'predicate': 'in the 2nd or 7th, or associated with the lords of '
                              'either of these houses',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Adverse',
                 'results': 'premature death, and danger from snakes',
                 'source': 'sloka',
                 'quote': "Adverse effects like premature deatl'1, antl cla:lger "
                          'from snakes, nvill be derived if Rahu be in the 2nd o/ '
                          'iih or be associeied with the lords of either of these '
                          "hy'ous^:*,",
                 'pdf_page': '142',
                 'ocr_flag': 'Badly damaged: "deatl\'1" = death; "cla:lger" = '
                             'danger; "o/ iih" = or 7th; "hy\'ous^:*," = houses. '
                             'Worst OCR in the chapter. NOTE: unlike other cells, '
                             "Rahu's maraka clause triggers on OCCUPYING the "
                             '2nd/7th as well as on association with their lords — '
                             'Rahu owns no sign, so lordship is not available. No '
                             'frame stated for "in the 2nd or 7th".'}],
 'maraka': "Adverse effects like premature deatl'1, antl cla:lger from snakes, "
           'nvill be derived if Rahu be in the 2nd o/ iih or be associeied with '
           "the lords of either of these hy'ous^:*, (PDFPAGE 142). Rahu-specific "
           'form: occupancy or association with the 2nd/7th lords, not lordship.',
 'remedy': "'l';medial measurcs — worship cf (]r,di!err,Ilurga [Goddess Durga], "
           'Jat;r [Japa], giving in charity rif a bllck c)w or femair bull.:la [a '
           'black cow or female buffalo] (PDFPAGE 142). Heavy OCR damage; items '
           'recoverable but the sentence is not cleanly quotable.'},
    ('sun', 'saturn'): {'verses': '40-47',
 'conditions': [{'predicate': 'in a kendra or trikona from the Ascendant',
                 'houses': 'kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascen-dant',
                 'polarity': 'favourable',
                 'polarity_word': 'good',
                 'results': 'Destruction of foes, full enjoyment, some gain of '
                            'grains, auspicious functions like marriage etc., at '
                            'home',
                 'source': 'sloka',
                 'quote': 'Destruction of foes, full enjoyment, some gain '
                          'ofgrains, auspicious functions like marriage etc., at '
                          "home, will bo the good effects derived in the An'ardasa "
                          'of saturn in the Dasrtof the sun, if saturn be in a '
                          'kendra or trikona from the Ascen-dant.',
                 'pdf_page': '144',
                 'ocr_flag': '"will bo" = will be; "Dasrtof" = Dasa of. '
                             "Lower-cased 'saturn'/'sun' throughout this passage."},
                {'predicate': 'in his sign of exaltation, in his own sign, in a '
                              'friendly sign, and in conjunction with a friendly '
                              'planet',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Well being, acquisition of more property, recognition '
                            'by the King (government), achievement of renown in '
                            'the country, gain of wealth from many sources',
                 'source': 'sloka',
                 'quote': 'Well ireing, acquisition r:i more property, recognition '
                          'bythe King (government), achievement of renown in tnJ '
                          'country, ... gain of wealth frorn rnany sources, will '
                          'be the effects if Saturn be in h.is sign of exaltation, '
                          'in his own sign, in a friendly sign and in conjunction '
                          'with a friendly planet.',
                 'pdf_page': '142 and 144',
                 'ocr_flag': 'PAGE-ORDER SCRAMBLE: this single sentence is split '
                             'across the OCR — the result clause opens at the foot '
                             'of PDFPAGE 144 and its condition clause is printed '
                             'at the TOP of PDFPAGE 142 (out of sequence). The '
                             'join is confident on grammar and content but IS a '
                             'reconstruction across a page break. Also note the '
                             'conjunction "and" (not "or") before the final clause '
                             '— read literally it requires all four '
                             'simultaneously; likely a translation artifact but '
                             'the text does NOT settle it. FLAGGED. Neutral verb, '
                             'no valence word.'},
                {'predicate': 'in the 8th or the 12th from the lord of the Dasa',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Rheumatism, pains, fever, dysentry like disease, '
                            'imprisonment, loss in ventures, loss of wealth, '
                            'quarrels, disputes with coparceners, claimants etc.',
                 'source': 'sloka',
                 'quote': 'Rheumatism, pains, fever, dysentry like disease, '
                          'imprisonment, loss in ventures, loss of wealth, '
                          'quarrels. disputes with coparceners, claimants etc. '
                          'will be the effects in the Antardasa if Saturn be in '
                          'the 8th or the 12th from the lord of the Dasa or be '
                          'associated with malefics.',
                 'pdf_page': '142',
                 'ocr_flag': 'Sits on PDFPAGE 142 owing to the page-order scramble '
                             'noted above. Clean OCR. Neutral verb, no valence '
                             'word.'},
                {'predicate': 'associated with malefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Rheumatism, pains, fever, dysentry like disease, '
                            'imprisonment, loss in ventures, loss of wealth, '
                            'quarrels, disputes with coparceners, claimants etc.',
                 'source': 'sloka',
                 'quote': 'will be the effects in the Antardasa if Saturn be in '
                          'the 8th or the 12th from the lord of the Dasa or be '
                          'associated with malefics.',
                 'pdf_page': '142',
                 'ocr_flag': ''},
                {'predicate': 'UNCONDITIONAL — timed thirds of the period',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'loss of friends at the commencement, good effects '
                            'during the middle part, distress at the end',
                 'source': 'sloka',
                 'quote': 'There will be loss of frien,Js at the commencement, '
                          'good effects during the middle part and distress at the '
                          'end of the Dasa.',
                 'pdf_page': '142',
                 'ocr_flag': 'No condition attached — fires unconditionally. '
                             'Polarity none because the clause is internally MIXED '
                             "(explicit 'good' for the middle third, "
                             "'loss'/'distress' at the ends); collapsing it to one "
                             'sign would misreport it. NOTE the text says "at the '
                             'end of the Dasa" — Dasa, not Antardasa — so it is '
                             'ambiguous whether the thirds are of the Saturn '
                             'antardasa or of the Sun mahadasa. UNRESOLVED.'},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'separation from parents and wandering, in addition to '
                            'other evil effects',
                 'source': 'sloka',
                 'quote': 'In addition to other evil effects, there will be sepa- '
                          'ration from parents and wandering, if Saturn be in his '
                          'sign of debilitation.',
                 'pdf_page': '142',
                 'ocr_flag': ''},
                {'predicate': 'lord of the 2nd or 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger of premature death',
                 'source': 'sloka',
                 'quote': 'If Saturn be the lord of the 2nd or 7th, there will be '
                          'danger of premature death.',
                 'pdf_page': '142',
                 'ocr_flag': ''}],
 'maraka': 'If Saturn be the lord of the 2nd or 7th, there will be danger of '
           'premature death. (PDFPAGE 142)',
 'remedy': 'Giving in charity black cow, buffalo, goat and Mrityunjaya Japa, are '
           'the remedial measures for obtaining relief from the evil effects of '
           'the Antardasa. These measures help to achieve happiness and gain of '
           'wealth and property. (PDFPAGE 142)'},
    ('sun', 'sun'): {'verses': '1-3',
 'conditions': [{'predicate': 'exalted, or in his own house',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Good',
                 'results': 'Good effects like acquisition of wealth and grains '
                            'etc.',
                 'source': 'sloka',
                 'quote': 'Good effects like acquisition of wealth and grains '
                          'etc., are derived in the Antardasa of the Sun in his '
                          'own Dpsa, if the Sun be exalted, in his own house, the '
                          'llth, Ke4dra or trikona.',
                 'pdf_page': '137',
                 'ocr_flag': '"Dpsa" = Dasa; "Ke4dra" = Kendra; "llth" = 11th — '
                             'routine OCR letterforms, meaning unambiguous.'},
                {'predicate': 'in the 11th, a kendra or a trikona',
                 'houses': '11; kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Good',
                 'results': 'Good effects like acquisition of wealth and grains '
                            'etc.',
                 'source': 'sloka',
                 'quote': 'Good effects like acquisition of wealth and grains '
                          'etc., are derived in the Antardasa of the Sun in his '
                          'own Dpsa, if the Sun be exalted, in his own house, the '
                          'llth, Ke4dra or trikona.',
                 'pdf_page': '137',
                 'ocr_flag': 'NO frame word anywhere in the sentence — houses are '
                             'given bare. Recorded unstated.'},
                {'predicate': 'debilitated',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Adverse',
                 'results': 'Adverse results will be experienced',
                 'source': 'sloka',
                 'quote': 'Adverse results will be experienced if the Sun be '
                          'debilitated or be in an in auspicious house or sign.',
                 'pdf_page': '137',
                 'ocr_flag': '"in auspicious" split across a space = '
                             'inauspicious.'},
                {'predicate': 'in an inauspicious house or sign',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Adverse',
                 'results': 'Adverse results will be experienced',
                 'source': 'sloka',
                 'quote': 'Adverse results will be experienced if the Sun be '
                          'debilitated or be in an in auspicious house or sign.',
                 'pdf_page': '137',
                 'ocr_flag': 'The text never enumerates WHICH houses are '
                             "'inauspicious' here, and states no frame. "
                             'Unresolvable from ch.52 alone — GAP.'},
                {'predicate': 'in other houses (i.e. houses not named above)',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Medium effects will be realised',
                 'source': 'sloka',
                 'quote': 'Medium effects will be realised if the Sun be in other '
                          'houses.',
                 'pdf_page': '137',
                 'ocr_flag': '"Medium" is a magnitude grade, not a valence word — '
                             'polarity recorded none.'},
                {'predicate': 'lord of the 2nd or 7th',
                 'houses': '2,7',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger',
                 'results': 'danger of premature death or death like sufferings',
                 'source': 'sloka',
                 'quote': 'If the Sun be the lord of the 2nd or 7th, there will be '
                          'danger of premature death or death like sufferings,',
                 'pdf_page': '137',
                 'ocr_flag': ''}],
 'maraka': 'If the Sun be the lord of the 2nd or 7th, there will be danger of '
           'premature death or death like sufferings, (PDFPAGE 137). Per ch.34 '
           'this maraka verdict must NOT be combined with a benefic/malefic nature '
           'verdict — it is a separate axis.',
 'remedy': 'The remedial measures to be adopted are Mrityunjaya Japa or the '
           'worship of the Sun (by recitation of appropriate mantras, charity '
           'etc.). (PDFPAGE 137) — sits after ALL branches; not a polarity marker.'},
    ('sun', 'venus'): {'verses': '65-73',
 'conditions': [{'predicate': 'posited in a kendra or trikona',
                 'houses': 'kendra 1,4,7,10; trikona 1,5,9',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'Marriage and happiness as desired from wife, gain of '
                            'property, travels to other places, meeting with '
                            'Brahmins and the king, acquisition of kingdom, '
                            'riches, magnanimity and majesty, auspicious functions '
                            'at the home, sweet preparations, acquisition of '
                            'pearls and other jewels, clothes, cattle, wealth and '
                            'grains and conveyances, enthusiasm, good reputation '
                            'etc.',
                 'source': 'sloka',
                 'quote': 'are the auspicious effects of the Antardasa of Venus in '
                          'the Dasa of the Sun, if Venus be posited in a kendra '
                          'trikona, be in his sign of exaltation, in his own sign, '
                          'in his own Varga or in a friendly sign.',
                 'pdf_page': '148',
                 'ocr_flag': 'Printed "in a kendra trikona" — the conjunction '
                             "between 'kendra' and 'trikona' is missing in the OCR "
                             "(elsewhere the chapter reads 'kendra or trikona'). "
                             'NO frame word — recorded unstated. Like the Sun and '
                             'Mars cells, this omits the frame that the '
                             'Jupiter/Saturn/Mercury/Ketu cells state.'},
                {'predicate': 'in his sign of exaltation, in his own sign, in his '
                              'own Varga, or in a friendly sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'auspicious',
                 'results': 'as above — marriage, gain of property, travels, '
                            'acquisition of kingdom, riches, jewels, clothes, '
                            'cattle, conveyances, good reputation etc.',
                 'source': 'sloka',
                 'quote': 'if Venus be posited in a kendra trikona, be in his sign '
                          'of exaltation, in his own sign, in his own Varga or in '
                          'a friendly sign.',
                 'pdf_page': '148',
                 'ocr_flag': '"his own Varga" unspecified as to which varga. GAP.'},
                {'predicate': 'in the 6th, the 8th or the 12th from the lord of '
                              'the Dasa (the Sun)',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord ofthe Dasa (the Sun)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'Displeasure of the king, mental agony and distress to '
                            'wife and children',
                 'source': 'sloka',
                 'quote': 'Displeasure of the king mental agony and distress to '
                          'wife and children, will be the -effects in tFe '
                          'Antardasa ofVenus if he be in the 6th, the 8th or the '
                          'l2th from the lord ofthe Dasa (the Sun).',
                 'pdf_page': '148',
                 'ocr_flag': '"tFe" = the; spacing collapsed. Neutral verb, no '
                             "valence word. (Venus's elongation limit from the Sun "
                             'makes the 6th and 8th limbs unreachable in a Sun '
                             'mahadasa — but unlike the Mercury cell the text '
                             'offers NO note saying so, and I do not supply one.)'},
                {'predicate': 'UNCONDITIONAL — timed thirds of the antardasa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'moderate at commencement, good during the middle '
                            'portion, and at the end evil effects like disrepute, '
                            'loss of position, inimical relations with kinsmen and '
                            'loss of comforts',
                 'source': 'sloka',
                 'quote': 'The effects of the Antardasa would be moderate at its '
                          'commencement, good during the middle portion and evil '
                          'effects like disrepute, loss of position, inimical '
                          'r6lations with kinsmen and losi of comforti. will be '
                          'derived at the end.',
                 'pdf_page': '148',
                 'ocr_flag': '"r6lations" = relations; "losi of comforti" = loss '
                             'of comforts. No condition attached. Internally MIXED '
                             "— explicit 'good' for the middle third and explicit "
                             "'evil' for the last third — so branch polarity is "
                             'none; an implementation must keep the three thirds '
                             'separate rather than assign one sign.'},
                {'predicate': 'lord of the 7th (and 2nd)',
                 'houses': '7, and 2 per the parenthetical',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'pains in the body and possibility of suffering from '
                            'diseases',
                 'source': 'sloka',
                 'quote': 'If Venus be the lord of the 7th (and 2nd) there will '
                          'bep?ins in.the body and possibility of suffering from '
                          'diseases.',
                 'pdf_page': '148',
                 'ocr_flag': 'The running text names only the 7TH; "(and 2nd)" is '
                             'a bracketed editorial completion to match the usual '
                             'maraka pair. Treat the 2nd as EDITORIAL, not mula. '
                             'Result is illness, not death — do not upgrade.'},
                {'predicate': 'associated with the lord of the 6th or 8th',
                 'houses': '6,8',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'death',
                 'results': 'premature death',
                 'source': 'sloka',
                 'quote': 'There will be premature death if Venus be as-sociated '
                          'with thelord of the 6th or 8th.',
                 'pdf_page': '148',
                 'ocr_flag': 'NOTABLE: in this cell the DEATH verdict hangs on '
                             'association with the 6th/8th lords, while the '
                             '2nd/7th-lordship clause yields only illness — the '
                             'reverse of the pattern in the Sun, Moon, Saturn and '
                             'Ketu cells. Preserve as written.'}],
 'maraka': "Two separate clauses, which do NOT follow the chapter's usual pattern: "
           '(a) "If Venus be the lord of the 7th (and 2nd) there will bep?ins '
           'in.the body and possibility of suffering from diseases." — illness '
           'only, and the \'2nd\' is an editorial bracket; (b) "There will be '
           'premature death if Venus be as-sociated with thelord of the 6th or '
           '8th." — the death verdict attaches to the 6th/8th lords, not the '
           '2nd/7th. (PDFPAGE 148)',
 'remedy': 'The remedial measures for obtainine relief from the evil effects are '
           'Mrityunjaya Japa, Rudra Japa] and giving in charity a tawny cow or '
           'female bu-ffalo. (PDFPAGE 148)'},
    ('venus', 'jupiter'): {'verses': '45-48 to 51 (PDFPAGE 247-248)',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'recovery of the lost kingdom (reinstatement in a high '
                            'position in government); acquisition of desired '
                            'grains, clothes and property; reverence from friends '
                            'and the king; gain of wealth; recognition from the '
                            'king; good reputation; gain of conveyances; '
                            'association with employer and men of learning; '
                            'industriousness in the study of Shastras; birth of a '
                            'son; satisfaction; visits of close friends; happiness '
                            'to parents and son',
                 'source': 'sloka',
                 'quote': '45-48. Effects like recovery of the lost kingdom '
                          "(reinstate' ment) in a high pqsition in (government), "
                          'acquisition of desired grains, clothes arid property '
                          'etc., reverence from the friends and the king '
                          '(govcrnrnent) and gain of wealth, recognition from the '
                          'king, good reputation, gain of conveyances, association '
                          "with employer and men ol' learniug, industriorrsness in "
                          'the study of Shastras, birth of a son, satisfaction, '
                          'visits of close friends, happiness to parents and son '
                          'etc., rvill be derived in tlre Antardasa of Jupiter in '
                          'the Dasa of Venus, if Jupiter be in his sign of '
                          'exaltation, in tris own sign or in kendra or trikona to '
                          'the Ascendant or the lord of the Dasa (Venus).',
                 'pdf_page': '247',
                 'ocr_flag': "'tris'=his; 'rvill'=will; "
                             "'industriorrsness'=industriousness"},
                {'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona)',
                 'frame': 'from_lagna',
                 'frame_quote': 'to the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.45-48 above',
                 'source': 'sloka',
                 'quote': 'or in kendra or trikona to the Ascendant or the lord of '
                          'the Dasa (Venus).',
                 'pdf_page': '247',
                 'ocr_flag': "Preposition is 'to' here rather than 'from' — same "
                             'sense. DUAL FRAME.'},
                {'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona)',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lord of the Dasa (Venus)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.45-48 above',
                 'source': 'sloka',
                 'quote': 'or in kendra or trikona to the Ascendant or the lord of '
                          'the Dasa (Venus).',
                 'pdf_page': '247',
                 'ocr_flag': ''},
                {'predicate': 'in the 6th, the 8th or the 12th AND associated with '
                              'a malefic',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Venus)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger (from the king and thieves); loss (of '
                                  'position)',
                 'results': 'danger from the king (government) and thieves; '
                            'distress to self and kinsmen; quarrels; mental agony; '
                            'loss of position; going away to foreign lands; danger '
                            'of many kinds of diseases',
                 'source': 'sloka',
                 'quote': '49-50. There will be danger from the king (government), '
                          'tnd thieves, distress to sel . arrd kinsmen, quarrels, '
                          'mental agony, oss of position, going away to foreign '
                          'lands and danger of nany kinds of diseases, if Jupiter '
                          'be in the 6th, the gth or the l2th from the lord of the '
                          'Dasa (Venus) and be associated with a nalefic.',
                 'pdf_page': '248',
                 'ocr_flag': "'gth'=8th; 'nalefic'=malefic; 'nany'=many; "
                             "'oss'=loss; 'tnd'=and; 'sel .'=self. CONJUNCTIVE "
                             "('AND be associated with a malefic'), not "
                             'disjunctive — unlike the Ketu parallel (vv.70-72) '
                             "which uses 'or'."},
                {'predicate': 'lord of the 2nd and the 7th',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '51. There will be physical distress if Jupiter be the '
                          'lc"rrd of the 2nd and the 7th.',
                 'pdf_page': '248',
                 'ocr_flag': '\'lc"rrd\'=lord. TWO FLAGS: (1) NO anchor stated — '
                             "'from the Ascendant' is missing here although "
                             'present in the Venus, Sun, Mars, Rahu, Saturn, '
                             'Mercury and Ketu parallels. Frame recorded UNSTATED. '
                             "(2) 'the 2nd AND the 7th' — conjunctive where every "
                             "parallel reads 'or'. Possibly typesetting, but not "
                             'corrected here.'}],
 'maraka': '"51. There will be physical distress if Jupiter be the lc"rrd of the '
           '2nd and the 7th." (PDFPAGE 248). TWO ANOMALIES vs every other section: '
           "(a) NO anchor is stated — the words 'from the Ascendant' are ABSENT; "
           "(b) it reads 'the 2nd AND the 7th', not 'or'. Both flagged, neither "
           'corrected.',
 'remedy': '"The remedial measure to obtri^ ":lief from the above rvil effects is '
           'Mrityunjaya Japa." (PDFPAGE 248; OCR-damaged = \'to obtain relief from '
           "the above evil effects')"},
    ('venus', 'ketu'): {'verses': '67-68 to 73-74 (PDFPAGE 250-251)',
 'conditions': [{'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Auspicious',
                 'results': 'auspicious effects like availability of sweetish '
                            'preparations, abnormal gains in profession and '
                            'increase in cattle wealth, from the very commencement '
                            'of the Antardasa',
                 'source': 'sloka',
                 'quote': '67-68. Auspicious effects like availability of sweetish '
                          'preparations, abnormal gains in profession and increase '
                          'in cattle wealth, will be derived from the vcry '
                          'commencement of rhe Antardasa of Ketu in the Dasa of '
                          "Venus, if Ketu be' in his ... sign cf exaltation, in "
                          'his own sign or be related to a yogakarak:r planet or '
                          'be possesscd of positional strcngth.',
                 'pdf_page': '250-251',
                 'ocr_flag': "'vcry'=very; 'rhe'=the; 'yogakarak:r'=yogakaraka; "
                             "'possesscd'=possessed; 'strcngth'=strength. Verse "
                             "straddles the page break. 'Auspicious' is a genuine "
                             'BRANCH-LEVEL label here.'},
                {'predicate': 'related to a yogakaraka planet, or possessed of '
                              'positional strength',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'favourable',
                 'polarity_word': 'Auspicious',
                 'results': 'as vv.67-68 above',
                 'source': 'sloka',
                 'quote': 'or be related to a yogakarak:r planet or be possesscd '
                          'of positional strcngth.',
                 'pdf_page': '251',
                 'ocr_flag': 'NOT COMPUTABLE as stated — see the Notes condition '
                             'below.'},
                {'predicate': "(the translator flags that 'positional strength' "
                              'for Ketu is never defined anywhere in the text)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'unavailable — the condition cannot be evaluated',
                 'source': 'note',
                 'quote': 'Notes : It is not laid down any where in which house '
                          'does Ketu get positional strength.',
                 'pdf_page': '251',
                 'ocr_flag': 'EXPLICIT GAP acknowledged by the translator. The '
                             "'positional strength' disjunct of vv.67-68 must "
                             "render 'unavailable', never be evaluated."},
                {'predicate': "(continuation — 'In the above circumstances', i.e. "
                              'the vv.67-68 condition set)',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': 'In the o.bove circumstanc.es',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'definite victory in the war at the end of the '
                            'Antardasa; moderate results in the middle portion; '
                            'feeling of distress sometimes',
                 'source': 'sloka',
                 'quote': '69-69i. In the o.bove circumstanc.es there wiil be '
                          'definjte victory in the war at the end of the '
                          'Antardasa. Morierate results will be experienced in the '
                          'middle portion of the Antrr- dasa and there will also '
                          'be {beling of distress scmctimes.',
                 'pdf_page': '251',
                 'ocr_flag': "'69-69i'=69-69½; 'definjte'=definite; "
                             "'Morierate'=Moderate; '{beling'=feeling; "
                             "'scmctimes'=sometimes; 'Antrr-dasa'=Antardasa"},
                {'predicate': 'in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Venus)',
                 'polarity': 'adverse',
                 'polarity_word': 'danger (from snakes, thieves, wounds); loss (of '
                                  'power of thinking); loss (in ventures)',
                 'results': 'danger from snakes, thieves, wounds; loss of power of '
                            'thinking; headache; agony; quarrels without any cause '
                            'or reason; diabetes; excessive expenditure; '
                            'antagonism with wife and children; going away to '
                            'foreign land; loss in ventures',
                 'source': 'sloka',
                 'quote': "' 70-72. Thergwill be danger from snakes, thieves, "
                          'wounds, loss of power of thinking, headache, agony, '
                          'qurrels without any cause or reason, diabetes, '
                          'excessive expenditure, antagonism with wifc and '
                          'children, going away to. foreign land, loss irr '
                          'vcntures, if Ketu be in tbe 8th or the l2th from the '
                          'lord of the Dasa (Venus) or be associated with a '
                          'malefic.',
                 'pdf_page': '251',
                 'ocr_flag': "'Thergwill'=There will; 'qurrels'=quarrels; "
                             "'wifc'=wife; 'irr vcntures'=in ventures; 'tbe'=the. "
                             'House-set is 8/12 only — the 6th is ABSENT, matching '
                             'the Rahu adverse branch (vv.42-44) and unlike most '
                             'others in this chapter.'},
                {'predicate': 'associated with a malefic',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'danger (from snakes, thieves, wounds); loss (in '
                                  'ventures)',
                 'results': 'as vv.70-72 above',
                 'source': 'sloka',
                 'quote': 'or be associated with a malefic.',
                 'pdf_page': '251',
                 'ocr_flag': "Disjunctive ('or'), unlike the Jupiter parallel "
                             "(vv.49-50) which is conjunctive ('and')."},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': '73-74. Tbere will be physical distress if Ketu be the '
                          'lord of the 2nd or the 7th from the Ascendant.',
                 'pdf_page': '251',
                 'ocr_flag': "'Tbere'=There. MARAKA position; no listed valence "
                             'word — polarity none.'}],
 'maraka': '"73-74. Tbere will be physical distress if Ketu be the lord of the 2nd '
           'or the 7th from the Ascendant." (PDFPAGE 251). Result is physical '
           'distress, not death.',
 'remedy': '"Thc remedial measures to obtain relief from the above cffects are '
           'Mrityun jaya Japa ond giving a goat in charity. Remedial measures for '
           'appeasing Venus will also prove beneficiai." (PDFPAGE 251). '
           'Chapter-closing remedy; also names the Mahadasa lord Venus. Sits after '
           'BOTH branches.'},
    ('venus', 'mars'): {'verses': '30-31½ to 35 + Note (PDFPAGE 245)',
 'conditions': [{'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of kingdom (high position in government); '
                            'property; clothes; ornaments; land; desired objects',
                 'source': 'sloka',
                 'quote': '30-31t. Effects iike acquisition of kingdom (attainment '
                          'of a high position in government), property, clothes, '
                          "ornaments, land and desired o'rjects, will be derive<i "
                          'in the Anpardasa of Mars in the Dasa of Venus, if Mars '
                          'be in kendra, trikona or the llth from the Ascendant or '
                          'be in his sign of exaltation or his own signs or be '
                          'associated with the lord of tbe Ascendant, 9th or the '
                          'l0rh.',
                 'pdf_page': '245',
                 'ocr_flag': "'30-31t'=30-31½; 'o'rjects'=objects; "
                             "'derive<i'=derived; 'Anpardasa'=Antardasa; "
                             "'l0rh'=10th"},
                {'predicate': 'in his sign of exaltation or in his own signs',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.30-31½ above',
                 'source': 'sloka',
                 'quote': 'or be in his sign of exaltation or his own signs',
                 'pdf_page': '245',
                 'ocr_flag': ''},
                {'predicate': 'associated with the lord of the Ascendant, the 9th '
                              'or the 10th',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.30-31½ above',
                 'source': 'sloka',
                 'quote': 'or be associated with the lord of tbe Ascendant, 9th or '
                          'the l0rh.',
                 'pdf_page': '245',
                 'ocr_flag': 'A lordship (association) condition, not a placement '
                             'condition. The anchor for the 9th/10th is not '
                             'repeated.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'loss (of position)',
                 'results': 'fever from cold; diseases like fever to parents; loss '
                            'of position; quarrels; antagonism with the king and '
                            'government officials; extravagant expenditure',
                 'source': 'sloka',
                 'quote': '32-34. There wili be fever from cold, diseases like '
                          'fever tr: parents,.loss of position, quarrels, '
                          'antagnrism with the king (government) and government '
                          "offficials, extravegant expenditure etc.,'if Mars be in "
                          'the 6th, the Sth or the t2th from the Ascendant ur the '
                          'lord of the Dasa.',
                 'pdf_page': '245',
                 'ocr_flag': "'Sth'=8th; 't2th'=12th; 'ur'=or; "
                             "'antagnrism'=antagonism; 'extravegant'=extravagant. "
                             'DUAL FRAME.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'ur the lord of the Dasa',
                 'polarity': 'adverse',
                 'polarity_word': 'loss (of position)',
                 'results': 'as vv.32-34 above',
                 'source': 'sloka',
                 'quote': 'if Mars be in the 6th, the Sth or the t2th from the '
                          'Ascendant ur the lord of the Dasa.',
                 'pdf_page': '245',
                 'ocr_flag': "Here the gloss '(Venus)' after 'lord of the Dasa' is "
                             'ABSENT, unlike the '
                             'Sun/Moon/Rahu/Jupiter/Saturn/Mercury/Ketu sections '
                             'which all gloss it. Same referent by context; '
                             'recorded as the text reads.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'losses (in profession); loss (of village)',
                 'results': 'physical distress; losses in profession; loss of '
                            'village, land etc.',
                 'source': 'sloka',
                 'quote': "35. Physical distress, losses in prot'ession, loss of "
                          'villagc, land etc., will be the rcsults, if Mars be thc '
                          'lord of the 2nd or the 7th from the Ascendant.',
                 'pdf_page': '245',
                 'ocr_flag': "'prot'ession'=profession; 'villagc'=village; "
                             "'rcsults'=results; 'thc'=the. MARAKA position, "
                             'non-death result.'},
                {'predicate': '(no remedial measure is stated in the sloka; the '
                              'translator supplies one on his own authority)',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'conjectured remedy: giving a bull in charity',
                 'source': 'note',
                 'quote': '/ Notes : Though remedial measure is not mentioned, we '
                          'trelieve that giving a bull in charity rvill enable the '
                          'native to obtain relief from the evil effects.-',
                 'pdf_page': '245',
                 'ocr_flag': "'trelieve'=believe; 'rvill'=will. Explicitly "
                             "conjectural ('we believe') — NOT mula."}],
 'maraka': '"35. Physical distress, losses in prot\'ession, loss of villagc, land '
           'etc., will be the rcsults, if Mars be thc lord of the 2nd or the 7th '
           'from the Ascendant." (PDFPAGE 245). Stated result is physical distress '
           'and losses — NOT death. Per ch.34, keep separate from any '
           'benefic/malefic nature verdict.',
 'remedy': 'NOT STATED IN THE SLOKA. Only a note: "/ Notes : Though remedial '
           'measure is not mentioned, we trelieve that giving a bull in charity '
           'rvill enable the native to obtain relief from the evil effects.-" '
           "(PDFPAGE 245) — the translator's own conjecture ('we believe')."},
    ('venus', 'mercury'): {'verses': '60-62 to 66 (PDFPAGE 249-250)',
 'conditions': [{'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'dawn of fortune; birth of a son; gain of wealth '
                            'through judgement of court; listening to stories from '
                            'Puranas; association with persons competent in '
                            'poetry; visits of close friends; happiness from '
                            'employer; availability of sweetish preparations',
                 'source': 'sloka',
                 'quote': '60-62. Effects like dawn of fortune, birth of a son, '
                          'gain of wealth through judgement of court, listening to '
                          'stories from Puranas, association with persons '
                          'competent in poetry etc., ... visits of close friends, '
                          'happiness from employer, availability of sleetish '
                          'preparations etc., will be derived in the Antardasa of '
                          'Mercury in the Dasa\\of Venirs, if Mercury be in '
                          "kenbra, trikona or the'l lth from the Ascendant, (or "
                          'from the lord of the Dasa Venus) in his sign of '
                          'exaltation or in his own sign.',
                 'pdf_page': '249-250',
                 'ocr_flag': "'sleetish'=sweetish; 'kenbra'=kendra; "
                             "'Venirs'=Venus. Verse straddles the page break."},
                {'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': '(or from the lord of the Dasa Venus)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.60-62 above',
                 'source': 'sloka',
                 'quote': "if Mercury be in kenbra, trikona or the'l lth from the "
                          'Ascendant, (or from the lord of the Dasa Venus) in his '
                          'sign of exaltation or in his own sign.',
                 'pdf_page': '250',
                 'ocr_flag': 'FLAG: this second frame is set in PARENTHESES in the '
                             'printed English. Elsewhere in the chapter the dual '
                             "frame is unparenthesised running text ('from the "
                             "Ascendant or the lord of the Dasa (Venus)'). The "
                             "parentheses may mark a TRANSLATOR'S insertion rather "
                             'than mula. Verify against the Devanagari before '
                             "treating this frame as mula. Recorded source 'sloka' "
                             'only because it stands inside the numbered verse '
                             'translation, not in a Notes block.'},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.60-62 above',
                 'source': 'sloka',
                 'quote': 'in his sign of exaltation or in his own sign.',
                 'pdf_page': '250',
                 'ocr_flag': ''},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of Dasa (Venus)',
                 'polarity': 'adverse',
                 'polarity_word': 'loss (of cattle); losses (in business)',
                 'results': "agony; loss of cattle; residence in other people's "
                            "houses; losses in business. TIME-SPLIT: 'some good "
                            'effects at the commencement, moderate in the middle '
                            'portion and distress from fever etc., at the end of '
                            "the Antardasa'",
                 'source': 'sloka',
                 'quote': '63-65. If Mercury be in the 6th, the 8th or the l2th '
                          'from the lord of Dasa (Venus) or be weak or-be '
                          'associated with a malefic, there will be agony, loss of '
                          "cattle, residence in othcr people's houses, and losses "
                          'in business. There will be some good effects at the '
                          "commencement, mi..' . ate in the middle portion and "
                          'distress from fever etc., 21 rire end of the Antardasa.',
                 'pdf_page': '250',
                 'ocr_flag': "'othcr'=other; 'mi..' . ate'=moderate; '21 rire "
                             "end'=at the end. Only 'from the lord of Dasa "
                             "(Venus)' is stated here — NO Ascendant alternative, "
                             'unlike the favourable branch above.'},
                {'predicate': 'weak, or associated with a malefic',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss (of cattle); losses (in business)',
                 'results': 'as vv.63-65 above',
                 'source': 'sloka',
                 'quote': 'or be weak or-be associated with a malefic',
                 'pdf_page': '250',
                 'ocr_flag': "'weak' is undefined — the text does not say by which "
                             'strength measure. FLAG.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': "66. 'Ihere will be physical distress if Merctrry be the "
                          'lord of the 2nd or the 7th from the Ascendant.',
                 'pdf_page': '250',
                 'ocr_flag': "'Merctrry'=Mercury. MARAKA position; no listed "
                             'valence word — polarity none.'}],
 'maraka': '"66. \'Ihere will be physical distress if Merctrry be the lord of the '
           '2nd or the 7th from the Ascendant." (PDFPAGE 250). Result is physical '
           'distress, not death.',
 'remedy': '"The remedial measure to obtain relief from the above evil efttcts, is '
           'recitation of Vishnu Sahasranama." (PDFPAGE 250)'},
    ('venus', 'moon'): {'verses': '21-22 to 27-29 + closing Note (PDFPAGE 243-244)',
 'conditions': [{'predicate': 'in her sign of exaltation or in her own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of wealth, conveyances, clothes by the '
                            'beneficence of the king; happiness in the family; '
                            'great opulence and glory; devotion to deities and '
                            'Brahmins',
                 'source': 'sloka',
                 'quote': "' 21-22. Effects like gain of wealth, conveyances, "
                          "clothes'by the beneficence of the king, happiness in "
                          'the family, great opulence and glory, devotion to '
                          'dcities and Brahmins, will , be derived in the '
                          'Antardasa of the Moon in the Dasa of Venus if the N{oon '
                          'be in her sign of exlltation, in her own sign, be '
                          'associated with the lord of the 9th, benefics or the '
                          'lord of the 10th or be in a kendra. trikona or the '
                          'llth.',
                 'pdf_page': '243-244',
                 'ocr_flag': "'dcities'=deities; 'N{oon'=Moon; "
                             "'exlltation'=exaltation"},
                {'predicate': 'associated with the lord of the 9th, with benefics, '
                              'or with the lord of the 10th',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.21-22 above',
                 'source': 'sloka',
                 'quote': 'be associated with the lord of the 9th, benefics or the '
                          'lord of the 10th',
                 'pdf_page': '243',
                 'ocr_flag': 'Lordship of the 9th/10th is itself reckoned from an '
                             'unstated anchor — the verse does not say. FLAG.'},
                {'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.21-22 above',
                 'source': 'sloka',
                 'quote': 'or be in a kendra. trikona or the llth.',
                 'pdf_page': '243',
                 'ocr_flag': "CRITICAL FRAME GAP: the sentence ENDS at 'the 11th' "
                             "with NO 'from the Ascendant' and NO 'from the lord "
                             "of the Dasa'. Contrast the Sun (v.15), Mars (v.31) "
                             'and Mercury (v.62) sections, which do state the '
                             'anchor. Frame is UNSTATED — do not infer.'},
                {'predicate': "(continuation — 'In the above circumstances', i.e. "
                              'the vv.21-22 condition set)',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': 'Inthe above circumstances',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'association with musicians and men of learning; '
                            'receiving of decorations; gain of cows, buffaloes and '
                            'other cattle; abnormal profits in business; dining '
                            'with brothers',
                 'source': 'sloka',
                 'quote': '23-231. Inthe above circumstances, there will also be '
                          'association with musicians and men of learning and '
                          'receiving of decorations, gain of cows, buffaloes and '
                          'other cattle, abnormal profits in business, dining with '
                          "brothers etc'",
                 'pdf_page': '244',
                 'ocr_flag': "'23-231'=23-23½. Inherits whichever of the vv.21-22 "
                             'disjuncts fired, including the frame-less '
                             'kendra/trikona/11th one.'},
                {'predicate': 'in her sign of debilitation, or combust',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss (of wealth)',
                 'results': 'loss of wealth; fears; physical distress; agony; '
                            'wrath of the king; journeys to foreign lands or '
                            'pilgrimage; distress to wife and children; separation '
                            'from kinsmen',
                 'source': 'sloka',
                 'quote': "24-26+. Loss of wealth, fears, physical distress' "
                          "agony' wrath of the king (government), journeys to "
                          'foreign lands or pilgrimage, distreis to wife and '
                          'childrn and separation from ii"ro,.n, w.ill be the '
                          "results if the Moon be in her sign of debilit'ation, "
                          'combust or be in the 6th, the 8th or the l2th from the '
                          'Ascendant or the lord of the Dasa (Venus).',
                 'pdf_page': '244',
                 'ocr_flag': "'24-26+'=24-26½; 'distreis'=distress; "
                             '\'childrn\'=children; \'ii"ro,.n\'=kinsmen'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss (of wealth)',
                 'results': 'as vv.24-26½ above',
                 'source': 'sloka',
                 'quote': 'or be in the 6th, the 8th or the l2th from the '
                          'Ascendant or the lord of the Dasa (Venus).',
                 'pdf_page': '244',
                 'ocr_flag': 'DUAL FRAME — recorded as two conditions.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lord of the Dasa (Venus)',
                 'polarity': 'adverse',
                 'polarity_word': 'Loss (of wealth)',
                 'results': 'as vv.24-26½ above',
                 'source': 'sloka',
                 'quote': 'or be in the 6th, the 8th or the l2th from the '
                          'Ascendant or the lord of the Dasa (Venus).',
                 'pdf_page': '244',
                 'ocr_flag': ''},
                {'predicate': 'in a kendra, trikona, the 3rd or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 3; 11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Venus)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'sovereignty over a province or village by the '
                            'beneficence of the king; gain of clothes etc.; '
                            'construction of a reservoir; increase in wealth; '
                            'physical fitness at the commencement of the Antardasa '
                            'and physical distress in its last portion',
                 'source': 'sloka',
                 'quote': "27-29.'There will be sovereigniy on,, a province or "
                          'village by the beneficence of the king (government), of '
                          "clothes etc'', construction of a reservoir, increase in "
                          "wealth erc:' if the Moon be in a kendra, trikona, the "
                          '3rd or the llth from the lord of the Dasa (Venus). '
                          'There will be physical fitness at the commencement of '
                          'the Antardasa and physiial distress in its last '
                          'portion.',
                 'pdf_page': '244',
                 'ocr_flag': "'sovereigniy'=sovereignty; 'physiial'=physical. "
                             'Internal time-split (fit at start, distress at end) '
                             'with no valence word — polarity none.'},
                {'predicate': 'lord of the 2nd and the 7th (SUPPLIED BY THE '
                              'TRANSLATOR — the sloka does not state it)',
                 'houses': '2,7',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': "Santhanam asserts the effects would be 'the same as "
                            "predicted for other planets earlier in every case' — "
                            'i.e. physical distress / fear of death. This is NOT '
                            'in the mula.',
                 'source': 'note',
                 'quote': 'Notes : Though it is not mentioned, it is but natural '
                          'that the efrects of the M6on being lord of the 2nd and '
                          'the 7th will be thc same as predicted for other planets '
                          "earlier in every case'",
                 'pdf_page': '244',
                 'ocr_flag': "'efrects'=effects; 'M6on'=Moon; 'thc'=the. The note "
                             "itself concedes 'it is not mentioned'. GAP — do not "
                             'ship as a rule.'}],
 'maraka': None,
 'remedy': None,
 'absence_notes': {'maraka': 'NO SLOKA MARAKA CLAUSE FOR THE MOON. Santhanam '
                             'supplies it only as a note: "Notes : Though it is '
                             'not mentioned, it is but natural that the efrects of '
                             'the M6on being lord of the 2nd and the 7th will be '
                             'thc same as predicted for other planets earlier in '
                             'every case\'" (PDFPAGE 244). The mula is SILENT — '
                             'flag, do not apply.',
                   'remedy': 'NONE STATED. No remedial measure is given for the '
                             'Moon antardasa in either sloka or note.'}},
    ('venus', 'rahu'): {'verses': '36-37½ to 42-44 (PDFPAGE 246-247)',
 'conditions': [{'predicate': 'in a kendra or trikona or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 11',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'great enjoyment; gain of wealth; visits of friends; '
                            'successful journeys; gain of cattle and land',
                 'source': 'sloka',
                 'quote': '36-37*. Effects tike great enjoynetrt, gain of wtalth, '
                          'visitg of friends, succcssful journcys, gein of cattle '
                          'and land etc., will be derived in the Antardasa of Rahu '
                          'in the Desa of Venus, if Rahubeinkendra ortrikona or '
                          'the llth, bcin his ei3uof exaltation or in his own sign '
                          'or b,s aasociated with or arpectcd by benefics.',
                 'pdf_page': '246',
                 'ocr_flag': "This is the worst-OCR'd page in the chapter. "
                             "'Rahubeinkendra ortrikona'=Rahu be in kendra or "
                             "trikona; 'bcin his ei3uof'=be in his sign of; 'b,s "
                             "aasociated'=be associated; 'arpectcd'=aspected. "
                             "CRITICAL FRAME GAP: the clause runs 'or the llth, be "
                             "in his sign of exaltation' — NO anchor stated for "
                             'the house-set. Frame UNSTATED.'},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.36-37½ above',
                 'source': 'sloka',
                 'quote': 'bcin his ei3uof exaltation or in his own sign',
                 'pdf_page': '246',
                 'ocr_flag': 'OCR-mangled but recoverable'},
                {'predicate': 'associated with or aspected by benefics',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.36-37½ above',
                 'source': 'sloka',
                 'quote': 'or b,s aasociated with or arpectcd by benefics.',
                 'pdf_page': '246',
                 'ocr_flag': "'b,s aasociated'=be associated; 'arpectcd'=aspected"},
                {'predicate': 'in the 3rd, the 6th, the ?10th or the 11th',
                 'houses': '3, 6, ?10 (OCR-uncertain), 11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from thc Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'enjoyments; destruction of enemy; enthusiasm; '
                            "beneficence of the king. TIME-SPLIT: 'Good effects "
                            'will be experienced up to 5 months from the '
                            'commencement of the Antardasa but at the end of the '
                            'Dasa there will be danger from fevers and '
                            "indigestion.'",
                 'source': 'sloka',
                 'quote': '3&39. Enjoymcnts, destnrction of encmy, athusiasm, '
                          'beneficcnce of tbe king, *ill bo the rcoulo, if Rahu bc '
                          'in thc 3rd, the 6th, the lfth or tbe llth from thc '
                          'Ascendant. Good effeccts will be expcricnced up to 5 '
                          'months from the comsens€t ment of thc Antardasa but at '
                          'the cnd of tbc Drss thcrc will bo danger from fcvers '
                          'and indigcstion.',
                 'pdf_page': '246',
                 'ocr_flag': "'lfth' is UNREADABLE — most plausibly '10th' but DO "
                             "NOT assume; a '6th' inside a favourable list is "
                             'itself anomalous for this chapter and may also be '
                             "corrupt. FLAG both. 'Drss'=Dasa (the text says Dasa, "
                             'not Antardasa — possible corruption). POLARITY CALL: '
                             "'danger' appears, but only in the end-of-period tail "
                             "of an otherwise favourable list headed by 'Good "
                             "effects' (not a listed valence word); recorded "
                             'polarity none rather than stamp a branch-level '
                             'verdict the text does not pronounce.'},
                {'predicate': "(continuation — 'In the above circumstances', i.e. "
                              'the vv.38-39 condition)',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '/n tnc abow circurutalccs',
                 'polarity': 'favourable',
                 'polarity_word': 'erspicirru (= auspicious)',
                 'results': 'except for obstacles in ventures and journeys, and '
                            'worries, all enjoyments like those of a king; '
                            'journeys to foreign lands bring success and safe '
                            'return home; blessings from Brahmins; auspicious '
                            'results consequent to visits to holy places',
                 'source': 'sloka',
                 'quote': '40-411. /n tnc abow circurutalccs €*c@t fbr obetrck in '
                          'vcnturts and journcp, and wo6rics, tbere ryill bc etl '
                          'cnjoyneatc like those of a king. Journoys to forcign '
                          'landr will bring succtss and the pcrson will rctBrn '
                          'safcly to his hodrld. Therc will also be bhssings fron '
                          'Bnhmins rnd erspicirru results consequent to visits to '
                          'holy plrcm.',
                 'pdf_page': '246',
                 'ocr_flag': "SEVERE OCR throughout. 'erspicirru'=auspicious — "
                             'legible enough to be certain from the surrounding '
                             "phrase 'results consequent to visits to holy "
                             "places'. '€*c@t fbr obetrck'=except for obstacles; "
                             "'hodrld'=homeland."},
                {'predicate': 'associated with a malefic in the 8th or the 12th',
                 'houses': '8,12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'from the lord of the Dasa (Venus)',
                 'polarity': 'adverse',
                 'polarity_word': 'inauspicious',
                 'results': 'inauspicious effects on self and parents; antagonism '
                            'with people',
                 'source': 'sloka',
                 'quote': '42-44. There will be inauspicious effects on self and '
                          'parents and antagonism with people, if Rahu be '
                          'associated with a malefic in thc 8th or the l2th from '
                          'the lord of the Dasa (Venus).',
                 'pdf_page': '247',
                 'ocr_flag': "'thc'=the. The house-set is 8/12 only — the 6th is "
                             'ABSENT, unlike most adverse branches in this '
                             'chapter. Recorded as the text has it.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from tfie Asccndant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': 'Physical distress will be caused if Rahu be the lord of '
                          'the 2nd or the 7th from tfie Asccndant.',
                 'pdf_page': '247',
                 'ocr_flag': "'tfie'=the; 'Asccndant'=Ascendant. MARAKA position; "
                             'stated result is physical distress with no listed '
                             'valence word — polarity none.'}],
 'maraka': '"Physical distress will be caused if Rahu be the lord of the 2nd or '
           'the 7th from tfie Asccndant." (within vv.42-44, PDFPAGE 247). Stated '
           'result is physical distress, NOT death.',
 'remedy': '"Remedial measure to obtain relief from the above evil cffects is '
           'Mrityunjaya Japa." (PDFPAGE 247). Sits after both the favourable '
           '(vv.36-41½) and adverse (vv.42-44) branches.'},
    ('venus', 'saturn'): {'verses': '52-54 to 58-59 (PDFPAGE 248-249)',
 'conditions': [{'predicate': 'in his sign of exaltation, in his own sign, or in '
                              'his own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'great enjoyments; visits of friends and kinsmen; '
                            'recognition from the king; birth of a daughter; '
                            'visits to holy places and sacred shrines; conferment '
                            'of authority by the king',
                 'source': 'sloka',
                 'quote': '52-54. Effects like great enjoyments, visits of friends '
                          'anrl insmen recognition from the king (governmcnt) '
                          'birth of a laughter, visits to holy places and sacred '
                          'shrines, confernment rf authority by the king '
                          '(government), will bc derived in the \\ntardasa of '
                          'Saturn in the Dasa of Venus, if Saturn be in his igo of '
                          'exaltation, in his own sign in kendra, trikona or in '
                          'his. rwn Navamsa.',
                 'pdf_page': '248',
                 'ocr_flag': "Left margin clipped throughout: 'anrl insmen'=and "
                             "kinsmen; 'laughter'=daughter; 'rf'=of; "
                             "'\\ntardasa'=Antardasa; 'igo'=sign; 'rwn'=own"},
                {'predicate': 'in a kendra or trikona',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona)',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.52-54 above',
                 'source': 'sloka',
                 'quote': 'if Saturn be in his igo of exaltation, in his own sign '
                          'in kendra, trikona or in his. rwn Navamsa.',
                 'pdf_page': '248',
                 'ocr_flag': 'CRITICAL FRAME GAP: no anchor stated. The clause '
                             "runs '...in his own sign in kendra, trikona or in "
                             "his own Navamsa' and never says from what. Frame "
                             'UNSTATED — do not infer. Compare the parallel Sun '
                             "verse (v.15), which DOES supply 'from the Ascendant "
                             "or the lord of the Dasa (Venus)'."},
                {'predicate': 'in his sign of debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'lethargy; more expenditure than income',
                 'source': 'sloka',
                 'quote': '55-57. There will be lethargy and more expenditure than '
                          'income, if Saturn be in his sign of debilitation.',
                 'pdf_page': '249',
                 'ocr_flag': 'No listed valence word — polarity none despite the '
                             'plainly unpleasant content.'},
                {'predicate': 'in the 8th, the 11th(?) or the 12th',
                 'houses': '8, 11(?), 12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'losses (in profession)',
                 'results': 'many kinds of distresses and troubles at the '
                            'commencement of the Antardasa; distress to parents, '
                            'wife and children; going away to foreign lands; '
                            'losses in profession; destruction of cattle',
                 'source': 'sloka',
                 'quote': 'Many kinds of distresses and troubles at the '
                          'commencement of the Antardasa, distress to parents, '
                          'wife and children, going away to foreign lands, losses '
                          'in profession, destruction of cattle, etc., will , be '
                          'the results, if Saturn be in the 8th, the llth or the '
                          'l2th from the Ascendant or the lord of the Dasa '
                          '(Venus).',
                 'pdf_page': '249',
                 'ocr_flag': "MAJOR FLAG: the middle house reads 'llth' (11th). "
                             'Every other adverse branch in this chapter uses '
                             '6/8/12, and the 11th is elsewhere in this very '
                             'chapter a FAVOURABLE house. Very likely OCR '
                             "corruption of '6th', but the text as extracted says "
                             '11th and is NOT corrected here. Verify against the '
                             'Devanagari before shipping. DUAL FRAME.'},
                {'predicate': 'in the 8th, the 11th(?) or the 12th',
                 'houses': '8, 11(?), 12',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lord of the Dasa (Venus)',
                 'polarity': 'adverse',
                 'polarity_word': 'losses (in profession)',
                 'results': 'as above',
                 'source': 'sloka',
                 'quote': 'if Saturn be in the 8th, the llth or the l2th from the '
                          'Ascendant or the lord of the Dasa (Venus).',
                 'pdf_page': '249',
                 'ocr_flag': "Same 'llth' flag as the preceding condition."},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'physical distress',
                 'source': 'sloka',
                 'quote': 'There wlll be physical distress if Saturn be the lord '
                          'of the 2nd or the 7th from the Ascendant.',
                 'pdf_page': '249',
                 'ocr_flag': "'wlll'=will. MARAKA position; no listed valence word "
                             '— polarity none.'}],
 'maraka': '"There wlll be physical distress if Saturn be the lord of the 2nd or '
           'the 7th from the Ascendant." (within vv.55-57, PDFPAGE 249). Result is '
           'physical distress, not death.',
 'remedy': '"58-59.The rernedial measures to obtain relief from the above evil '
           'effects, are Havana with sesamun seeds (fire), Mritvunjaya iapa, '
           'Durga-saptashati Patha (by self or through a Brahmin)." (PDFPAGE 249)'},
    ('venus', 'sun'): {'verses': '12 to 19-20 (PDFPAGE 242-243)',
 'conditions': [{'predicate': 'in any sign other than his sign of exaltation or '
                              'debilitation',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'a period of agony; wrath of the king (government); '
                            'quarrels with the coparceners',
                 'source': 'sloka',
                 'quote': '12. There will be a period of agony, wrath of the king '
                          '(government), quarrels with the coparceners etc., in '
                          'the Antar- dasa of the Sun in tbe Dasa of Venus if the '
                          'Sun be in any sign other than his sign of exaltaion or '
                          'debilitation.',
                 'pdf_page': '242',
                 'ocr_flag': "'tbe'=the; 'exaltaion'=exaltation. 'agony' is NOT "
                             'one of the listed valence words — polarity none. SEE '
                             'THE NOTE BELOW: this verse is repudiated by the '
                             'translator.'},
                {'predicate': '(Santhanam disputes the wording of v.12 and cites a '
                              'different Chowkhamba reading, printed ONLY in '
                              'Devanagari and NOT translated)',
                 'houses': '',
                 'frame': 'unstated',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'unavailable — the alternative reading is not rendered '
                            'into English anywhere in the text',
                 'source': 'note',
                 'quote': 'Notes : This verse does not appear to be correctly '
                          'worded because the Sun does produce good effects in '
                          'position other than exaltation or debilitation. The '
                          'position is correctiy stated in the Chowkambha version '
                          'of this verse which reads as under, Page 433',
                 'pdf_page': '242',
                 'ocr_flag': 'The Devanagari of the substitute verse follows and '
                             'is unreadable in this OCR. MAJOR GAP: v.12 is '
                             'flagged as probably corrupt and the correction is '
                             'unavailable. Treat v.12 as unusable pending the '
                             'Sanskrit.'},
                {'predicate': 'in his sign of exaltation or in his own sign',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of a kingdom and wealth; happiness from '
                            'wife and children; happiness from employer; meeting '
                            'with friends; happiness from parents; marriage; name '
                            'and fame; betterment of fortune; birth of a son',
                 'source': 'sloka',
                 'quote': '13-15, Effecis like acquisition of a kingdom '
                          '(attainment of a high position in government) and '
                          'wealth, happiness from wife and children, happiness '
                          'from employer, meeting wilh friends, happinc-s from '
                          'parents, marrige, name and fame, betterment of fortune, '
                          'birth of a son etc., will be experien cd if the Sun be '
                          'in his sign of exaltation, in his own sign in ker.dra '
                          'tritrona, the 2nd or the llth from the Ascendant or the '
                          'lord of the Dasa (Venus).',
                 'pdf_page': '242',
                 'ocr_flag': "'ker.dra tritrona'=kendra, trikona; 'experien "
                             "cd'=experienced. Neutral verb 'will be experienced' "
                             '— no valence word.'},
                {'predicate': 'in a kendra, trikona, the 2nd or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 2; 11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.13-15 above',
                 'source': 'sloka',
                 'quote': 'if the Sun be in his sign of exaltation, in his own '
                          'sign in ker.dra tritrona, the 2nd or the llth from the '
                          'Ascendant or the lord of the Dasa (Venus).',
                 'pdf_page': '242',
                 'ocr_flag': 'DUAL FRAME: the same house-set is offered from the '
                             'Ascendant OR from the Dasa lord (Venus); recorded as '
                             'two conditions, not collapsed.'},
                {'predicate': 'in a kendra, trikona, the 2nd or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 2; 11',
                 'frame': 'from_dasa_lord',
                 'frame_quote': 'or the lord of the Dasa (Venus)',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'as vv.13-15 above',
                 'source': 'sloka',
                 'quote': 'in ker.dra tritrona, the 2nd or the llth from the '
                          'Ascendant or the lord of the Dasa (Venus).',
                 'pdf_page': '242',
                 'ocr_flag': "The phrase 'from the Ascendant or the lord of the "
                             "Dasa (Venus)' distributes the preposition 'from' "
                             'over both anchors.'},
                {'predicate': 'in the 6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'loss (of kinsmen); danger (at home)',
                 'results': 'distress; agony; distress to members of the family; '
                            'harsh language; distress to father; loss of kinsmen; '
                            'wrath of the king; danger at home; many diseases; '
                            'destruction of agricultural production',
                 'source': 'sloka',
                 'quote': '16-18. Distress, agony, distress to members of the '
                          'family, harsh language, distress to father, loss of '
                          'kinsmen. wrath of the king (government), danger at '
                          'home, many diseases, destruction of agricultural '
                          'production, etc., will be the results, if the Sun be in '
                          'the 6th, the 8th or the l2th from the Ascendant, or be '
                          "in his sign of debilitation or in an enemy's sign.",
                 'pdf_page': '243',
                 'ocr_flag': 'Valence words appear inside outcome items, not as a '
                             'branch label.'},
                {'predicate': "in his sign of debilitation or in an enemy's sign",
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'adverse',
                 'polarity_word': 'loss (of kinsmen); danger (at home)',
                 'results': 'as vv.16-18 above (same results clause)',
                 'source': 'sloka',
                 'quote': 'if the Sun be in the 6th, the 8th or the l2th from the '
                          'Ascendant, or be in his sign of debilitation or in an '
                          "enemy's sign.",
                 'pdf_page': '243',
                 'ocr_flag': ''},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Asccndant',
                 'polarity': 'adverse',
                 'polarity_word': 'evil',
                 'results': 'evil influence of the planets',
                 'source': 'sloka',
                 'quote': '19-20. There will be evil influence of the planets if '
                          'the Sun be the lcrd of the 2nd or the 7th from the '
                          'Asccndant.',
                 'pdf_page': '243',
                 'ocr_flag': "'lcrd'=lord; 'Asccndant'=Ascendant. MARAKA position "
                             'but the stated result is NOT death — the text says '
                             "'evil influence of the planets'. Do not silently "
                             'upgrade to a death verdict.'}],
 'maraka': '"19-20. There will be evil influence of the planets if the Sun be the '
           'lcrd of the 2nd or the 7th from the Asccndant." (PDFPAGE 243). NOTE: '
           'unlike every other section in this chapter, the stated result of '
           "2nd/7th-lordship is NOT death or physical distress but 'evil influence "
           "of the planets' — recorded as the text has it, not normalised.",
 'remedy': '"Worship of the Sun is the renrcdial measure to obtain relief from the '
           'above evil effects." (PDFPAGE 243)'},
    ('venus', 'venus'): {'verses': '1-2½ to 11 (PDFPAGE 240-241)',
 'conditions': [{'predicate': 'in a kendra, trikona or the 11th',
                 'houses': '1,4,7,10 (kendra); 1,5,9 (trikona); 11',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'gain of wealth, cattle etc., through Brahmins; '
                            'celebrations in connection with the birth of a son; '
                            'well being; recognition from the king (government); '
                            'acquisition of a kingdom (attainment of a high '
                            'position in government)',
                 'source': 'sloka',
                 'quote': '1-2*. Effects like gain of wealth, cati,le etc., '
                          'through " Srahmins, celebrations in connection witL the '
                          'birth of a son, well being, recognition from ttrc king '
                          "(government), acquisition 'of a kingdom (attainment of "
                          'a high position in government), will be derived in the '
                          'Antardasa of Venus in hjs own Dasan if Venus be in '
                          'kendra, trikona or the llth from the Ascendant and be '
                          'endowed with streirgth.',
                 'pdf_page': '240',
                 'ocr_flag': "'cati,le'=cattle; 'Srahmins'=Brahmins; 'ttrc'=the; "
                             "'Dasan'=Dasa,; 'llth'=11th; 'streirgth'=strength"},
                {'predicate': 'endowed with strength (conjunctive with the house '
                              "condition above — 'and be endowed with strength')",
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'same as vv.1-2½ above',
                 'source': 'sloka',
                 'quote': 'if Venus be in kendra, trikona or the llth from the '
                          'Ascendant and be endowed with streirgth.',
                 'pdf_page': '240',
                 'ocr_flag': "'streirgth'=strength. Text does not define which "
                             'strength measure is meant — FLAG.'},
                {'predicate': 'in his sign of exaltation, in his own sign, or in '
                              'exalted or own Navamsa',
                 'houses': '',
                 'frame': 'not_a_house',
                 'frame_quote': '',
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'construction of a new house; sweet preparations; '
                            'happiness to wife and children; companionship with a '
                            'friend; giving grains in charity; beneficence of the '
                            'king; gain of clothes, conveyances and ornaments; '
                            'success in business; increase in cattle; gain of '
                            'garments by journeys in the western direction',
                 'source': 'sloka',
                 'quote': '3-6. Construction of a new house, availability oi sweet '
                          "preparations, happiness' to wife and children, "
                          'companionship ... with a frieird, giving grains etc. in '
                          'charity, beneficence of the king (Government) gain of '
                          'clothes, conveyances and ornaments, success in '
                          'business, increase in the number of cattle, gain of '
                          'garments by performing journeys in the western '
                          'direction, etc., will be the results, if Venus be in '
                          "his sign of exaltation, in bis 'own sign or be in "
                          'exalted or own Navamsa.',
                 'pdf_page': '240-241',
                 'ocr_flag': 'Devanagari block heavily garbled across the page '
                             "break; English body legible. 'frieird'=friend; "
                             "'bis'=his"},
                {'predicate': 'associated with or aspected by a benefic AND in a '
                              'friendly Navamsa AND in the 3rd, the ?th or the '
                              '11th',
                 'houses': '3, ? (OCR-destroyed), 11',
                 'frame': 'from_lagna',
                 'frame_quote': "t'rom the Ascendant",
                 'polarity': 'none',
                 'polarity_word': '',
                 'results': 'acquisition of a kingdom (high position in '
                            'government); enthusiasm; beneficence of the king; '
                            'well being in the family; increase in the number of '
                            'wives, children and wealth',
                 'source': 'sloka',
                 'quote': '7-8. There will be acquisition of a kingdom (high '
                          'position in gov-rnment), enthu$iasm, beneficencE of the '
                          'king (govern- meriS] ."cil being in the family, '
                          "increase in the number of *ives. ..r'rldren and wealth, "
                          "etc., if Venus be associated with or aspi'.i'i )y a "
                          'benefic and be in a friendly Navarisa, in the 3rd, thd: '
                          ";,ti: or the llth t'rom the Ascendant.",
                 'pdf_page': '241',
                 'ocr_flag': "SEVERE: the middle house of the triplet reads 'thd: "
                             ";,ti:' — UNREADABLE. Do not guess. 'aspi'.i'i "
                             ")y'=aspected by; 'Navarisa'=Navamsa. The second "
                             'house number is a GAP.'},
                {'predicate': 'associated with or aspected by a malefic in the '
                              '6th, the 8th or the 12th',
                 'houses': '6,8,12',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendant',
                 'polarity': 'adverse',
                 'polarity_word': 'Danger',
                 'results': 'danger from thieves etc.; antagonistic relations with '
                            'government officials; destruction of friends and '
                            'kinsmen; distress to wife and children',
                 'source': 'sloka',
                 'quote': '9-10. Danger from thieves etc., antagonistic relations '
                          'with governrrent officials, desrruction of friends and '
                          'kinsmen, . distress to wife and children, firay be '
                          'expected if Venus be associated with or aspected by a '
                          'malefic in the 6th, the 8th or the l2th from the '
                          'Ascendant.',
                 'pdf_page': '241',
                 'ocr_flag': "'governrrent'=government; 'desrruction'=destruction; "
                             "'firay'=may. The valence word 'Danger' sits inside "
                             'an outcome item, not as a branch label.'},
                {'predicate': 'lord of the 2nd or the 7th',
                 'houses': '2,7',
                 'frame': 'from_lagna',
                 'frame_quote': 'from the Ascendal:t',
                 'polarity': 'adverse',
                 'polarity_word': 'de, ih (= death)',
                 'results': 'fear of death',
                 'source': 'sloka',
                 'quote': "I1.,' fhere will be fear of de, ih, if Venus be the "
                          'lord of the 2nd or the ?th from the Ascendal:t.',
                 'pdf_page': '241',
                 'ocr_flag': "'de, ih'=death; '?th'=7th; 'Ascendal:t'=Ascendant. "
                             'MARAKA clause.'}],
 'maraka': '"I1.,\' fhere will be fear of de, ih, if Venus be the lord of the 2nd '
           'or the ?th from the Ascendal:t." (v.11, PDFPAGE 241). OCR-damaged: '
           "'fear of de, ih' = 'fear of death'; '?th' = '7th'. Per ch.34 this "
           'maraka verdict must not be merged with a benefic/malefic nature '
           'verdict.',
 'remedy': '"Remedial meesures to obtain relief from the above evil "cffects are, '
           'Durga Patha and gviog a cow in charity." (PDFPAGE 241). Remedy sits '
           'AFTER both the favourable (vv.1-8) and adverse (vv.9-11) branches — '
           'not a polarity marker.'},
}


def cell(maha_lord, antar_lord):
    """The mined cell for one (mahādaśā, antardaśā) pair, or None."""
    return MATRIX.get((maha_lord, antar_lord))
