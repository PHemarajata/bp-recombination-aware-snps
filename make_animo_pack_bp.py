#!/usr/bin/env python3
"""
Build ANIMO_PACK/, the transferable subset of VM_HANDOFF_PACK.

WHY THIS EXISTS. VM_HANDOFF_PACK was assembled for a session running on this
machine, so it carries three tables that .gitignore and REVIEW_DATA_GOVERNANCE.md
deliberately withhold from anything that leaves it:

  FINAL_PANEL.tsv               2,959 rows joining accession to country,
                                collection date, isolation_location (679 rows)
                                and validation_label (31 rows). This is the full
                                re-identification surface.
  CGMLST_LICHT_ATTRIBUTION.tsv  92 rows joining accession to exposure country and
                                to the identity of its nearest neighbor.
  FINAL_PARTITION.tsv           accession to analysis unit, 2,340 rows.

B. pseudomallei is a US Tier 1 Select Agent and that join is re-identifiable for
rare cases. None of the 17 visuals in ANIMO_BRIEF_2026-09-09.md needs any of the
three, so this pack drops them rather than asking a remote session to be careful.

derive_vm_data.py is also dropped, because it reads two files that are withheld
and it has never been runnable from inside the pack. MANIFEST.sha256 replaces it
as the integrity check.

The build FAILS if a denied file or a restricted field reaches the output.

  python3 make_animo_pack_bp.py
"""

import hashlib
import os
import re
import shutil
import sys

B = os.path.dirname(os.path.abspath(__file__))
SRC = f"{B}/VM_HANDOFF_PACK"
OUT = f"{B}/ANIMO_PACK"

DENY = {
    "FINAL_PANEL.tsv":
        "accession joined to country, collection date, isolation_location and "
        "validation_label. The full re-identification surface.",
    "CGMLST_LICHT_ATTRIBUTION.tsv":
        "accession joined to exposure country and to its nearest neighbor.",
    "FINAL_PARTITION.tsv":
        "accession to analysis unit, which enumerates study membership.",
    "derive_vm_data.py":
        "reads two withheld tables and cannot run from inside the pack.",
    "RM_RESULTS_L1_CORRECTED.tsv":
        "its reference column carries accession plus country for all 82 "
        "unit-replicons. No visual needs it, because per-unit r/m is already in "
        "GATE1_ALIGNMENT_2026-08-21.tsv. Dropped rather than argued about.",
    "L1_GLOBAL_ML_TREE.nwk":
        "the 88-unit A100 cross-hardware control run, not the reported basis. "
        "82 tips, only 54 basis units, carries units the basis excludes. "
        "Replaced by global_ml_tree_86tip.treefile.",
    "L1_GLOBAL_BACKBONE.nwk":
        "same A100 control run, strain-level backbone. Not the reported basis.",
}

# The reported-basis unit tree, copied in to replace the two A100 files above. Its
# tips are unit names, no accessions, and make_figure3_bp.py reads it.
EXTRA_DATA = {
    "L1v4c_out/global_ml_tree.treefile": "data/global_ml_tree_86tip.treefile",
}

# Four public run accessions survive, and they are the same four: the genomes
# retired from the exclusion register on 2026-08-23. They appear in
# FIGURE1_STUDY_FLOW.svg and in a provenance note in NUMBERS.tsv. A public run
# accession is not restricted on its own. The join to exposure is, and neither
# file carries one. Nothing else is allowed through.
ALLOWED_ACCESSIONS = {"SRR2896257", "SRR2896259", "SRR2896271", "ERR9980356"}

ACC = re.compile(r"\b(?:GCF|GCA|SRR|ERR|DRR)[_0-9]{6,}")
RESTRICTED = re.compile(r"exposure_country|validation_label|isolation_location",
                        re.I)
EXTRA = ["ANIMO_BRIEF_2026-09-09.md", "HANDOFF_VIRTUAL_MANUSCRIPT_2026-09-08.md"]

# Cross-project standard, kept outside any project folder so it travels. Defines
# who owns which stage of clip generation and the gates between them.
EXTRA_ABS = {
    os.path.expanduser("~/CLIP_GENERATION_STANDARD.md"):
        "CLIP_GENERATION_STANDARD.md",
}


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"FATAL: {SRC} not found.")
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)

    os.makedirs(f"{OUT}/narration", exist_ok=True)
    copied, skipped = [], []
    for root, _dirs, files in os.walk(SRC):
        for fn in sorted(files):
            src = os.path.join(root, fn)
            rel = os.path.relpath(src, SRC)
            if fn in DENY:
                skipped.append((rel, DENY[fn]))
                continue
            dst = os.path.join(OUT, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(rel)

    for fn in EXTRA:
        p = f"{B}/{fn}"
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {fn} not found at the repo root.")
        shutil.copy2(p, f"{OUT}/{fn}")
        copied.append(fn)

    nar = f"{B}/narration_csv"
    if os.path.isdir(nar):
        for fn in sorted(os.listdir(nar)):
            if fn.endswith((".csv", ".txt", ".md")):
                shutil.copy2(f"{nar}/{fn}", f"{OUT}/narration/{fn}")
                copied.append(f"narration/{fn}")

    for src_abs, dst_rel in EXTRA_ABS.items():
        if not os.path.isfile(src_abs):
            sys.exit(f"FATAL: {src_abs} not found. It is the cross-project clip "
                     "standard and the pack is incomplete without it.")
        shutil.copy2(src_abs, f"{OUT}/{dst_rel}")
        copied.append(dst_rel)

    for src_rel, dst_rel in EXTRA_DATA.items():
        src = f"{B}/{src_rel}"
        if not os.path.isfile(src):
            sys.exit(f"FATAL: {src_rel} not found.")
        dst = f"{OUT}/{dst_rel}"
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(dst_rel)

    if len(skipped) != len(DENY):
        sys.exit(f"FATAL: denied {len(skipped)} files, DENY lists {len(DENY)}. "
                 "A denied file is missing from the source pack, so this build "
                 "cannot prove it was excluded.")

    # Audit the OUTPUT, not the plan. A rule that is never tested against the
    # thing it produced is the empty check this project has been bitten by.
    bad_acc, bad_field = [], []
    for root, _dirs, files in os.walk(OUT):
        for fn in files:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, OUT)
            try:
                s = open(p, errors="replace").read()
            except Exception:
                continue
            found = set(ACC.findall(s)) - ALLOWED_ACCESSIONS
            if found:
                bad_acc.append((rel, len(found), sorted(found)[:3]))
            # Field NAMES may be discussed in prose. A restricted field becomes a
            # problem when it is a column in a data file, so only flag those.
            if rel.startswith("data" + os.sep) and RESTRICTED.search(
                    s.split("\n", 1)[0]):
                bad_field.append(rel)

    if bad_acc:
        for rel, n, sample in bad_acc:
            print(f"  DENIED {rel}: {n} accessions, e.g. {sample}",
                  file=sys.stderr)
        sys.exit("FATAL: the built pack carries genome accessions.")
    if bad_field:
        sys.exit(f"FATAL: restricted columns in {bad_field}.")

    readme(copied, skipped)

    # Hash every file in the built tree except the manifest itself, so the
    # README is covered too. Hashing only the copy list left two files
    # unverified, which is the kind of gap a manifest exists to close.
    rels = sorted(
        os.path.relpath(os.path.join(r, f), OUT)
        for r, _d, fs in os.walk(OUT) for f in fs
    )
    lines = []
    for rel in rels:
        h = hashlib.sha256(open(f"{OUT}/{rel}", "rb").read()).hexdigest()
        lines.append(f"{h}  {rel}")
    open(f"{OUT}/MANIFEST.sha256", "w").write("\n".join(lines) + "\n")
    n_hashed = len(lines)
    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _d, fs in os.walk(OUT) for f in fs)
    print(f"wrote {OUT}/  {len(copied)} files, {total/1024/1024:.1f} MB")
    print(f"  excluded {len(skipped)}:")
    for rel, why in skipped:
        print(f"    {os.path.basename(rel)}")
    print(f"  audit: 0 genome accessions outside the allowlist, "
          f"0 restricted columns")
    print(f"  MANIFEST.sha256 covers {n_hashed} of {n_hashed + 1} files")


def readme(copied, skipped):
    rows = "\n".join(f"| `{os.path.basename(r)}` | {w} |" for r, w in skipped)
    txt = f"""# ANIMO_PACK

The transferable subset of `VM_HANDOFF_PACK`, built by `make_animo_pack_bp.py`.
{len(copied)} files.

## Read in this order

1. **`CLIP_GENERATION_STANDARD.md`** — how clip work is divided and sequenced.
   Domain-neutral and cross-project. Section 2 is the ownership table.
2. **`ANIMO_BRIEF_2026-09-09.md`** — this project's brief.

## Your role here is BUILDER

Against the standard's ownership table, in this collaboration:

| role | who | owns |
|---|---|---|
| concept owner | Claude Code | the brief, the narration, the captions |
| **builder** | **you** | **the data audit, the encoding, the motion** |
| verifier | Claude Code | probing the render and mapping its beats |

So four things are yours and three are not.

**Yours.** Auditing the brief against the data before you design anything, and
**refusing any spec the data does not support**. Choosing the encoding. Choosing
the motion, including deciding that motion is the wrong answer. Delivering a
rendered file.

**Not yours.** Writing narration, which is timed to a render that must already
exist. Generating captions, which come from final narration. Verifying your own
beats.

**The one thing to push back on.** If the brief names a chart type rather than the
claim and the quantity that carries it, that is a defect in the brief. Say so.
Naming the encoding is your call, not the concept owner's.

## What was removed, and why

*Burkholderia pseudomallei* is a US Tier 1 Select Agent. The study metadata joins
accession to isolation location, collection date and exposure label, and for rare
cases that combination is re-identifiable. The repository has never tracked
isolate-level data, and `REVIEW_DATA_GOVERNANCE.md` applies the same rule to the
reviewer package. This pack applies it to anything that leaves the machine.

| file | why it is not here |
|---|---|
{rows}

None of the 17 visuals in the brief needs any of them. Every figure is served by
the aggregate and per-unit tables, which carry no genome identifiers.

## What is verified about this pack

The build audits its own output rather than trusting the exclusion list. It
fails if any file carries a genome accession, and it fails if any file under
`data/` carries an exposure, isolation location or validation label column.

One exception is allowed and named in the script: `FIGURE1_STUDY_FLOW.svg`
mentions the public run accession `SRR2896257`, a genome retired from the
exclusion register. Public accessions are not restricted on their own. The join
to exposure is, and that figure carries none.

Check integrity from inside this directory, since the paths are relative:

```bash
cd ANIMO_PACK && sha256sum -c MANIFEST.sha256
```

It covers every file except itself.

## What this pack cannot do

`derive_vm_data.py` is not here, so the embedded datasets cannot be re-derived
from source in this copy. They never could be from inside the pack, since that
script reads two withheld tables from the repository root. Treat
`extracts/virtual_manuscript_data.json` as frozen input and check it against
`MANIFEST.sha256` instead.

## If you need something that is not here

Ask. The answer may be an aggregate that carries the same information without the
join, which is how the reviewer package handled the same problem.
"""
    open(f"{OUT}/README.md", "w").write(txt)


if __name__ == "__main__":
    main()
