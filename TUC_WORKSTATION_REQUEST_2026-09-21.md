# Request to the Linux workstation session (TUC briefing)

Paste this whole file into a Claude session on the **old Linux workstation** that
holds the full `bp-recombination-aware-snps` working tree and the Kawang closeout
deck. It asks for seven values and three judgements. It does **not** ask you to
send any table.

---

## Why you are being asked

Four narrated films (the "TUC briefing") were finished on a Mac. Their standing
rule is that every number is reproduced from source before it is drawn. Seven
numbers cannot be checked on the Mac, because two tables and the closeout deck
were never migrated. Nothing is known to be wrong. The point is to confirm or
correct them before the films go to the lab chief.

**Do not send the tables themselves.** `FINAL_PANEL.tsv` is on the restricted
list, the repo's GitHub remote is public, and the repo `.gitignore` denies by
default. Return **only the counts and the read-off values**, pasted back as
text. Nothing to Drive, nothing to rclone, nothing committed, no `git add -f`.

---

## A. Counts that need recomputing

Absent on the Mac: **`FINAL_PANEL.tsv`** and **`FINAL_PARTITION.tsv`**.
Present on the Mac and already checked: `NUMBERS.tsv`, `TABLES.md`,
`GATE1_ALIGNMENT_2026-08-21.tsv`, `GROUPING_LADDER.tsv`,
`CGMLST_LICHT_ATTRIBUTION.tsv`, `EXPOSURE_OVERRIDES.tsv`.

Report each figure with **the command you used**, so the arithmetic is
auditable. Check the real column names first: the "claimed source" column is the
Mac's record of provenance, not a verified schema.

| # | figure as drawn | where it appears | claimed source |
|---|---|---|---|
| A1 | **312** funded isolates | clip 1 act 1, clip 4 act 9 | `FINAL_PANEL.tsv`, IP/IE prefixes |
| A2 | **259** from patients, **53** from the environment | clip 1 act 1 | same; IP = patient, IE = environmental |
| A3 | **276** of the 312 enter the analysed set | clip 4 act 4 | `FINAL_PANEL` joined to `FINAL_PARTITION` |
| A4 | they land in **56 of the 85** units | clip 4 act 4 | same join |
| A5 | **36** did not enter | clip 4 act 4 | same join; should be 312 − 276 |
| A6 | **34 of 47** in-window units contain funded isolates | clip 4 act 7, clip 3 act 7 | that join, then `GATE1_ALIGNMENT_2026-08-21.tsv` |
| A7 | **10** of those 34 fall below the 7-member floor without their funded isolates | clip 4 act 7, clip 3 act 7 | recomputed from the same join |

Two cautions carried over from earlier work on this dataset:

- **Use the frozen basis.** 85 units / 2,340 genomes, `FINAL_BASIS_2026-08-22`.
  Validate with `freeze_basis_bp.py` before quoting anything. An 88-unit A100
  control basis also exists and is *not* what the films report.
- **Do not glob a Clusters directory to get unit counts.** `L1v4c_out/Clusters`
  is a hybrid holding 88 directories, not 86, and globbing it has already
  double-counted 153 genomes and corrupted two summary tables.

---

## B. Values that exist only in the closeout deck

The films label these on screen as cited, not computed here. There is **no copy
of the deck on the Mac and no table in the repo that reproduces them**, so they
have never been checked against their source.

### B1. Association index by trait — Kawang closeout deck, **slide 25**

Drawn in clip 4 act 7 as five rows on a 0-to-1 axis, "lower means more
structured", on the 2,773-genome / 35-country framework:

| trait | value as drawn | labelled |
|---|---|---|
| Region | **0.193** | strongly structured |
| Country | **0.236** | strongly structured |
| Collection decade | **0.581** | well mixed |
| Isolation source | **0.710** | well mixed |
| Thai province | **0.721** | well mixed |

Please read slide 25 and report: the five values, the exact trait labels, and
**what the slide calls the metric** (association index, or something else).

### B2. **Region's 0.193 is the one to look at hardest**

In the same film, `0.193` is also **country's attribution kappa** (clip 4 act 5,
nearest-neighbour, 22% correct against a 26% baseline, on our own 46-genome
validation set). Two unrelated quantities, on two different frameworks,
identical to three decimal places.

That may be a coincidence. It may also be a transcription slip when the deck was
read. **Please confirm region's association index on slide 25 digit by digit.**
If it is not 0.193, say so and give the real value.

### B3. Nine nominated pairs, six evaluable — deck **slide 23**

Clip 4 act 2 draws nine nominated patient-and-environment pairs and says six are
evaluable. Confirm both counts from slide 23, and say in one line what
"evaluable" meant there.

### B4. What is the framework actually called?

Clip 4 act 7 says **"the Kawang framework"** on screen and **"the closeout
framework"** in the narration, for the same thing. Only one should survive.
Tell us what the deck itself calls it, and whether "Kawang" is appropriate to
put on screen in a film going to the funder.

---

## C. While you are in there

Two things that are cheap to answer on that machine and awkward on the Mac.

- **C1.** Does `FINAL_PANEL.tsv` still match the films' basis, or has it moved
  since 2026-08-22? Give its row count and mtime. If it has changed, say so
  loudly: every figure in section A would then be against a different table
  than the films were built on.
- **C2.** Is there anything else in that tree that the films cite and the Mac
  lacks? The Mac has the four scene sources, the briefs, `NUMBERS.tsv`,
  `TABLES.md`, `GATE1_ALIGNMENT_2026-08-21.tsv`, `GROUPING_LADDER.tsv`,
  `CGMLST_LICHT_ATTRIBUTION.tsv` and `EXPOSURE_OVERRIDES.tsv`. A one-line list
  of anything else the film sources name is enough.

---

## How to reply

Paste back a plain block like this. No files, no attachments.

```
A1  312      <command>        CONFIRMED | ACTUAL: <n>
A2  259/53   <command>        CONFIRMED | ACTUAL: <n>/<n>
A3  276      <command>        CONFIRMED | ACTUAL: <n>
A4  56/85    <command>        CONFIRMED | ACTUAL: <n>
A5  36       <command>        CONFIRMED | ACTUAL: <n>
A6  34/47    <command>        CONFIRMED | ACTUAL: <n>
A7  10       <command>        CONFIRMED | ACTUAL: <n>

B1  region <v>  country <v>  decade <v>  source <v>  province <v>
    metric is called: "<as printed on slide 25>"
B2  region's index digit by digit: <value>   coincidence | TRANSCRIPTION SLIP
B3  nominated <n>, evaluable <n>.  evaluable meant: <one line>
B4  the deck calls it: "<name>".  safe to show the funder: yes | no

C1  FINAL_PANEL.tsv  rows <n>  mtime <date>   unchanged since 2026-08-22 | CHANGED
C2  also missing on the Mac: <list, or "nothing">
```

**If a figure does not reproduce, do not fix anything.** Just report the real
value. Several of these numbers appear in two films and in the manuscript, and
changing one has to be done in one pass across all of them.
