#!/usr/bin/env python3
"""
Concatenate a Parsnp XMFA into a core alignment that Gubbins can consume.

WHY THIS EXISTS
---------------
harvesttools cannot read Parsnp 2.1.1 output. On every group tried it aborts
with "LCB N extends beyond reference" and writes only the reference sequence,
so the documented parsnp -> harvesttools -> Gubbins route is broken with the
installed versions. This reads the XMFA directly instead.

WHAT IT PRODUCES
----------------
Only locally collinear blocks present in EVERY genome are kept, concatenated in
file order. That is the core alignment proper. Invariant sites are retained,
which is mandatory: Gubbins estimates recombination from SNP density along the
alignment and silently produces nonsense when handed a variant-sites-only
alignment.

Sequence names come from the XMFA ##SequenceFile records with the .fasta and
.ref suffixes stripped, so tips match the isolate identifiers used elsewhere.
"""

import os
import sys


def parse_xmfa(path):
    """Return (index -> sequence name, list of {index: aligned string})."""
    names = {}
    blocks = []
    cur = {}
    idx = None
    buf = []
    pending_index = None

    with open(path) as fh:
        for line in fh:
            if line.startswith("##SequenceIndex"):
                pending_index = int(line.split()[1])
            elif line.startswith("##SequenceFile"):
                raw = line.split(None, 1)[1].strip()
                if raw.endswith(".ref"):
                    raw = raw[:-4]
                if raw.endswith(".fasta"):
                    raw = raw[:-6]
                names[pending_index] = raw
            elif line.startswith("#"):
                continue
            elif line.startswith(">"):
                if idx is not None:
                    cur[idx] = "".join(buf)
                idx = int(line[1:].split(":")[0].strip())
                buf = []
            elif line.startswith("="):
                if idx is not None:
                    cur[idx] = "".join(buf)
                if cur:
                    blocks.append(cur)
                cur, idx, buf = {}, None, []
            else:
                buf.append(line.strip())
    if idx is not None:
        cur[idx] = "".join(buf)
    if cur:
        blocks.append(cur)
    return names, blocks


def build_core(names, blocks):
    wanted = set(names)
    parts = {i: [] for i in wanted}
    kept = dropped = 0
    for block in blocks:
        if set(block) != wanted:
            dropped += 1
            continue
        lengths = {len(v) for v in block.values()}
        if len(lengths) != 1:
            # Ragged block, cannot be concatenated safely.
            dropped += 1
            continue
        kept += 1
        for i in wanted:
            parts[i].append(block[i].upper())
    return {names[i]: "".join(parts[i]) for i in wanted}, kept, dropped


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: xmfa_to_core_bp.py <parsnp.xmfa> <out.fasta>")
    xmfa, out = sys.argv[1], sys.argv[2]
    names, blocks = parse_xmfa(xmfa)
    core, kept, dropped = build_core(names, blocks)
    length = len(next(iter(core.values()))) if core else 0
    with open(out, "w") as fh:
        for name in sorted(core):
            fh.write(">%s\n" % name)
            seq = core[name]
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i + 60] + "\n")
    variable = 0
    if core:
        cols = zip(*core.values())
        variable = sum(1 for col in cols if len(set(col) - {"-"}) > 1)
    sys.stderr.write(
        "%s: %d genomes, %d/%d blocks kept, core %d bp, %d variable sites\n"
        % (os.path.basename(xmfa), len(core), kept, kept + dropped,
           length, variable))


if __name__ == "__main__":
    main()
