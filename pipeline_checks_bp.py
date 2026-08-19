#!/usr/bin/env python3
"""
pipeline_checks_bp.py -- runnable checks for Gap 3 of the B. pseudomallei SNP
strategy review. Companion to GAP3_pipelines_and_scale.md.

Four independent checks, each a subcommand. Standard library only; no BioPython,
no pandas. FASTA parsing is deliberately simple-minded and assumes an aligned
FASTA (equal record lengths), which every step here also verifies.

    A  fconst      Verify the snp-sites -C / snp-sites -c accounting closes.
    B  split       Split a concatenated multi-replicon alignment, and report
                   per-replicon callable fraction.
    C  junction    Flag Gubbins recombination calls that straddle a replicon
                   junction in a concatenated alignment.
    D  cost        Report distinct site patterns and an IQ-TREE memory estimate.

K96243 replicon lengths are built in as the default boundary set:
    BX571965.1 / NC_006350.1  chromosome I   4,074,542 bp
    BX571966.1 / NC_006351.1  chromosome II  3,173,005 bp
                                     total   7,247,547 bp

Run `pipeline_checks_bp.py <subcommand> -h` for per-check usage.
"""

import argparse
import collections
import sys

# --------------------------------------------------------------------------
# K96243 reference geometry. Order matters: it is the order the replicons are
# concatenated in by snippy-core / vcf2pseudogenome, i.e. reference FASTA order.
# --------------------------------------------------------------------------
K96243 = [
    ("BX571965.1", 4_074_542),   # chromosome I,  NC_006350.1
    ("BX571966.1", 3_173_005),   # chromosome II, NC_006351.1
]

# Base composition of K96243, computed from the RefSeq records. Recorded here
# because a flat 25/25/25/25 assumption is wrong by >2x in both directions at
# 68.06% GC, which is the whole argument for -fconst over +ASC.
K96243_BASE_COUNTS = {"A": 1_155_449, "C": 2_474_268, "G": 2_458_320, "T": 1_159_510}


def read_fasta(path):
    """Yield (name, sequence) pairs. Sequence is upper-cased."""
    name, chunks = None, []
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n\r")
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(chunks)
                name, chunks = line[1:].split()[0], []
            elif line:
                chunks.append(line.upper())
    if name is not None:
        yield name, "".join(chunks)


def load_alignment(path):
    """Read a FASTA and assert every record is the same length."""
    records = list(read_fasta(path))
    if not records:
        sys.exit(f"ERROR: no records read from {path}")
    lengths = {len(s) for _, s in records}
    if len(lengths) != 1:
        by_len = collections.Counter(len(s) for _, s in records)
        sys.exit(
            f"ERROR: {path} is not an alignment -- {len(lengths)} distinct record "
            f"lengths: {dict(by_len)}\n"
            "       This is exactly the backbone-fallback failure mode the main "
            "review flags. Fix it before interpreting anything downstream."
        )
    return records, lengths.pop()


# ==========================================================================
# A. fconst accounting
# ==========================================================================
def cmd_fconst(args):
    """
    The arithmetic that must close:

        len(SNP alignment) + sum(fconst counts) == len(full-length alignment)

    A shortfall means one of the two documented snp-sites leaks:

      1. `-C` silently ignores `-c` (it hardcodes pure_mode=0). Columns that are
         variable AND contain an N are dropped by `-c` but not added to the
         constant counts, so they vanish from the accounting entirely.

      2. `-C` reads base identity off the FIRST sequence only, via is_pure(),
         which accepts only ACGT. Wherever taxon #1 carries a gap or N at an
         otherwise-constant column, that column is not counted. With a
         Gubbins-masked alignment this undercounts in proportion to the first
         taxon's masked fraction -- so order the least-masked genome first.

    This check also recomputes the counts independently, under the strict
    definition the IQ-TREE author states ("fA should only count the number of
    AAAAA sites"), so you can see how far snp-sites' answer is from it.
    """
    _, full_len = load_alignment(args.full)
    records, snp_len = load_alignment(args.snps)

    fconst = [int(x) for x in args.fconst.replace(" ", "").split(",")]
    if len(fconst) != 4:
        sys.exit(f"ERROR: --fconst needs 4 comma-separated integers (A,C,G,T), got {len(fconst)}")

    total = snp_len + sum(fconst)
    print(f"full-length alignment   : {full_len:>12,} columns   ({args.full})")
    print(f"SNP alignment           : {snp_len:>12,} columns   ({args.snps})")
    print(f"fconst A,C,G,T          : {','.join(f'{c:,}' for c in fconst)}")
    print(f"fconst sum              : {sum(fconst):>12,}")
    print(f"SNP + fconst            : {total:>12,}")
    shortfall = full_len - total
    print(f"shortfall               : {shortfall:>12,}  ({100.0 * shortfall / full_len:.3f}% of the alignment)")

    if shortfall == 0:
        print("\nOK: accounting closes exactly.")
    else:
        print(
            "\nWARNING: accounting does not close. Every missing column is a site "
            "that\n         contributes to neither the likelihood nor the constant-site "
            "correction.\n         See the two leak modes in this function's docstring."
        )

    # Independent recount under the strict all-taxa-unambiguous definition.
    if args.recount:
        print("\nRecounting constant sites from the full-length alignment (strict definition)...")
        recs, _ = load_alignment(args.full)
        seqs = [s for _, s in recs]
        strict = collections.Counter()
        ambiguous_constant = 0
        for col in zip(*seqs):
            bases = set(col)
            if len(bases) == 1 and next(iter(bases)) in "ACGT":
                strict[next(iter(bases))] += 1
            elif bases <= set("ACGT-N") and len(bases & set("ACGT")) == 1:
                # one real base plus gaps/Ns: constant to snp-sites' first-taxon
                # heuristic sometimes, and "ambiguous constant" to IQ-TREE always.
                # This is the column class that trips +ASC after Gubbins masking.
                ambiguous_constant += 1
        strict_list = [strict[b] for b in "ACGT"]
        print(f"  strict constant (all taxa ACGT, identical) : {','.join(f'{c:,}' for c in strict_list)}"
              f"   sum {sum(strict_list):,}")
        print(f"  ambiguous-constant (1 base + gaps/Ns)      : {ambiguous_constant:,}")
        print(f"  supplied fconst                            : {','.join(f'{c:,}' for c in fconst)}"
              f"   sum {sum(fconst):,}")
        delta = sum(fconst) - sum(strict_list)
        print(f"  supplied - strict                          : {delta:+,}")
        if ambiguous_constant:
            print(
                f"\n  NOTE: {ambiguous_constant:,} ambiguous-constant columns exist. These are "
                "what make\n        IQ-TREE reject +ASC, and what get silently deleted if you "
                "rerun on\n        .varsites.phy. They are a further reason to use -fconst instead."
            )

    # Composition sanity check against the reference.
    ref_total = sum(K96243_BASE_COUNTS.values())
    ref_frac = [K96243_BASE_COUNTS[b] / ref_total for b in "ACGT"]
    obs_total = sum(fconst) or 1
    obs_frac = [c / obs_total for c in fconst]
    print("\nBase composition of the supplied constant sites vs K96243 reference:")
    print("        supplied    K96243    flat")
    for b, o, r in zip("ACGT", obs_frac, ref_frac):
        print(f"  {b}      {o:7.4f}   {r:7.4f}   0.2500")
    if max(abs(o - 0.25) for o in obs_frac) < 0.02:
        print(
            "\n  WARNING: supplied counts are near-flat. At 68.06% GC that is almost "
            "certainly\n           wrong, and it discards exactly the information -fconst "
            "exists to preserve."
        )
    return 0


# ==========================================================================
# B. replicon split and per-replicon callable fraction
# ==========================================================================
def replicon_bounds(spec):
    """Turn [(name, length), ...] into [(name, start, end_exclusive), ...] 0-based."""
    out, offset = [], 0
    for name, length in spec:
        out.append((name, offset, offset + length))
        offset += length
    return out, offset


def parse_replicon_spec(text):
    if not text:
        return K96243
    spec = []
    for item in text.split(","):
        name, _, length = item.partition(":")
        spec.append((name.strip(), int(length)))
    return spec


def cmd_split(args):
    """
    snippy-core joins reference contigs end to end, in reference-FASTA order,
    with no separator, no N-padding and no boundary record (verified in source:
    `join '', map { $seq{$id}{$_} } @$chrom_list`). bactmap's vcf2pseudogenome.py
    does the same, flattening every contig into one SeqRecord.

    So a two-chromosome K96243 alignment has BX571965.1 at columns 1..4,074,542
    and BX571966.1 at 4,074,543..7,247,547, adjacent in the alignment and ~3 Mb
    plus an origin of replication apart in reality.

    This splits the concatenation back into per-replicon alignments so Gubbins
    can be run once per replicon, and reports the per-replicon callable fraction
    -- a number nobody has published for this organism.
    """
    spec = parse_replicon_spec(args.replicons)
    bounds, expected = replicon_bounds(spec)

    records, aln_len = load_alignment(args.alignment)
    print(f"alignment: {len(records)} taxa x {aln_len:,} columns")
    print(f"expected from replicon spec: {expected:,} columns")
    if aln_len != expected:
        sys.exit(
            f"\nERROR: alignment length {aln_len:,} != expected {expected:,}.\n"
            "       Do NOT split on these boundaries. Either the reference differs\n"
            "       from the spec, or the alignment is not a plain concatenation.\n"
            "       Pass --replicons NAME:LEN,NAME:LEN to override."
        )
    print("length matches the replicon spec exactly -- safe to split.\n")

    for name, start, end in bounds:
        sub_len = end - start
        called = collections.Counter()
        per_taxon_called = []
        for _, seq in records:
            piece = seq[start:end]
            n_called = sum(1 for c in piece if c in "ACGT")
            per_taxon_called.append(n_called)
            called[name] += n_called
        mean_frac = (sum(per_taxon_called) / len(per_taxon_called)) / sub_len
        min_frac = min(per_taxon_called) / sub_len
        max_frac = max(per_taxon_called) / sub_len
        print(f"{name}: columns {start + 1:,}-{end:,}  ({sub_len:,} bp)")
        print(f"    callable fraction  mean {mean_frac:6.2%}   min {min_frac:6.2%}   max {max_frac:6.2%}")

        if args.outdir:
            out = f"{args.outdir.rstrip('/')}/{name.replace('.', '_')}.aln"
            with open(out, "w") as fh:
                for tname, seq in records:
                    fh.write(f">{tname}\n{seq[start:end]}\n")
            print(f"    written -> {out}")
        print()

    print(
        "Run Gubbins separately on each output. Do not run it on the concatenation:\n"
        "its spatial scanning statistic uses a 0.1-10 kb sliding window, so any window\n"
        "straddling the junction spans both chromosomes across a step change in\n"
        "polymorphism density. Use `junction` below to see whether that has happened."
    )
    return 0


# ==========================================================================
# C. junction artefact detection in Gubbins output
# ==========================================================================
def cmd_junction(args):
    """
    If Gubbins has already been run on a concatenated alignment, this reports how
    many recombination blocks touch the junction region -- i.e. how much of the
    output is potentially an artefact of the false adjacency rather than biology.

    A block that *spans* the junction is unambiguously an artefact: no single
    recombination event covers the end of chromosome I and the start of
    chromosome II. Blocks merely *near* the junction are suspect because the
    background substitution density used for the null on that branch is a
    mixture of two regimes.
    """
    spec = parse_replicon_spec(args.replicons)
    bounds, total = replicon_bounds(spec)
    junctions = [end for _, _, end in bounds[:-1]]  # 0-based, exclusive
    if not junctions:
        sys.exit("ERROR: replicon spec has only one replicon; there is no junction.")

    window = args.window
    spanning, nearby, n_blocks = [], [], 0
    with open(args.gff) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 5:
                continue
            try:
                start, end = int(f[3]), int(f[4])   # GFF is 1-based inclusive
            except ValueError:
                continue
            n_blocks += 1
            s0, e0 = start - 1, end                 # to 0-based half-open
            for j in junctions:
                if s0 < j < e0:
                    spanning.append((start, end, j))
                elif abs(s0 - j) <= window or abs(e0 - j) <= window:
                    nearby.append((start, end, j))

    print(f"recombination blocks in {args.gff}: {n_blocks:,}")
    print(f"replicon junction(s) at 1-based column(s): {', '.join(f'{j:,}' for j in junctions)}")
    print(f"window for 'nearby': +/- {window:,} bp (Gubbins' max window size is 10,000)\n")

    print(f"blocks SPANNING a junction : {len(spanning):,}   <- artefacts by construction")
    for start, end, j in spanning[:20]:
        print(f"    {start:,}-{end:,}  (length {end - start + 1:,}) crosses {j:,}")
    if len(spanning) > 20:
        print(f"    ... and {len(spanning) - 20:,} more")

    print(f"\nblocks NEAR a junction     : {len(nearby):,}   <- suspect")
    for start, end, j in nearby[:20]:
        print(f"    {start:,}-{end:,}  (length {end - start + 1:,}) near {j:,}")
    if len(nearby) > 20:
        print(f"    ... and {len(nearby) - 20:,} more")

    if spanning:
        print(
            "\nA junction-spanning block cannot be a real recombination event. Its presence\n"
            "means Gubbins was run on a concatenation and the result should be regenerated\n"
            "per replicon (see the `split` subcommand)."
        )
    elif nearby:
        print("\nNo spanning blocks, but blocks abut the junction. Regenerate per replicon.")
    else:
        print("\nNo junction artefacts detected.")
    return 0


# ==========================================================================
# D. cost: distinct site patterns and an IQ-TREE memory estimate
# ==========================================================================
def cmd_cost(args):
    """
    IQ-TREE and RAxML-NG compress identical alignment columns before computing
    likelihoods, so runtime and conditional-likelihood memory scale with the
    number of DISTINCT SITE PATTERNS, not raw columns:

        memory ~ n_internal_nodes * n_patterns * n_states * n_rate_cats * 8 bytes

    This matters because it cuts both ways. In a clean full-length core alignment,
    constant sites collapse to ~4 extra patterns, so retaining them costs almost
    nothing. But mask_gubbins_aln.py gives every taxon a different gap pattern,
    which fragments previously-identical constant columns into many distinct
    patterns -- masking actively destroys pattern compression, and the penalty
    scales with recombination load.

    No published benchmark exists at ~500 taxa x 3.8 Mb, so measuring this on a
    real masked cluster is both the cheapest way to settle the full-length-vs-SNP
    question and a genuine contribution. `raxml-ng --parse` gives the same number.
    """
    records, aln_len = load_alignment(args.alignment)
    n_taxa = len(records)
    seqs = [s for _, s in records]

    patterns = collections.Counter()
    const_strict = 0
    const_ambiguous = 0
    for col in zip(*seqs):
        patterns[col] += 1
        bases = set(col)
        real = bases & set("ACGT")
        if len(bases) == 1 and real:
            const_strict += 1
        elif len(real) == 1 and bases <= set("ACGTN-"):
            const_ambiguous += 1

    n_patterns = len(patterns)
    print(f"alignment      : {n_taxa:,} taxa x {aln_len:,} columns   ({args.alignment})")
    print(f"distinct patterns : {n_patterns:,}")
    print(f"compression       : {aln_len / n_patterns:.1f}x  "
          f"({100.0 * n_patterns / aln_len:.2f}% of columns are distinct)")
    print(f"strictly constant columns    : {const_strict:,}")
    print(f"ambiguous-constant columns   : {const_ambiguous:,}   <- these trip +ASC")

    # Rough CLV memory. Order-of-magnitude only; use raxml-ng --parse for real numbers.
    n_states, n_cats = 4, args.rate_categories
    internal = max(n_taxa - 2, 1)
    clv_bytes = internal * n_patterns * n_states * n_cats * 8
    scale_bytes = internal * n_patterns * n_cats
    est = (clv_bytes + scale_bytes) / (1024 ** 3)
    print(f"\nCLV memory estimate ({n_states} states, {n_cats} rate categories):")
    print(f"    ~{est:,.2f} GB for one tree; budget 2-3x for search overhead and retained trees")
    print("    (Order of magnitude only. `raxml-ng --parse --msa ... --model ...` gives")
    print("     the authoritative figure and the same pattern count.)")

    if const_ambiguous > const_strict and const_strict:
        print(
            "\nNOTE: ambiguous-constant columns outnumber strictly-constant ones. That is the\n"
            "      signature of heavy masking, and it is why this alignment compresses poorly."
        )
    return 0


# ==========================================================================
def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("fconst", help="verify the snp-sites -C / -c accounting closes")
    a.add_argument("--full", required=True, help="full-length (masked) alignment FASTA")
    a.add_argument("--snps", required=True, help="snp-sites -c output FASTA")
    a.add_argument("--fconst", required=True, help="constant-site counts, 'A,C,G,T'")
    a.add_argument("--recount", action="store_true",
                   help="independently recount constant sites under the strict definition")
    a.set_defaults(func=cmd_fconst)

    b = sub.add_parser("split", help="split a concatenated multi-replicon alignment")
    b.add_argument("--alignment", required=True, help="concatenated alignment FASTA")
    b.add_argument("--outdir", help="write per-replicon alignments here (optional)")
    b.add_argument("--replicons", help="NAME:LEN,NAME:LEN (default: K96243 two chromosomes)")
    b.set_defaults(func=cmd_split)

    c = sub.add_parser("junction", help="flag Gubbins blocks straddling a replicon junction")
    c.add_argument("--gff", required=True, help="*.recombination_predictions.gff")
    c.add_argument("--replicons", help="NAME:LEN,NAME:LEN (default: K96243 two chromosomes)")
    c.add_argument("--window", type=int, default=10_000,
                   help="'nearby' window in bp (default 10000 = Gubbins max window)")
    c.set_defaults(func=cmd_junction)

    d = sub.add_parser("cost", help="distinct site patterns and an IQ-TREE memory estimate")
    d.add_argument("--alignment", required=True, help="alignment FASTA")
    d.add_argument("--rate-categories", type=int, default=4)
    d.set_defaults(func=cmd_cost)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
