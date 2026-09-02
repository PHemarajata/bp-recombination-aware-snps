#!/usr/bin/env python3
"""
Positive species identification for Burkholderia pseudomallei.

WHY THIS EXISTS
---------------
Distance methods cannot do this job. B. mallei sits 0.0101 from K96243 by mash,
INSIDE this project's <=0.012 species gate, so mash (and ANI, and any k-mer
method) admits B. mallei as B. pseudomallei. That is not a tuning problem: the two
taxa are ~99.3% ANI, which is why GTDB merges them and why GAMBIT v3.0.0 reports
B. pseudomallei genomes as B. mallei.

B. mallei is separated from B. pseudomallei by GENE CONTENT, not similarity: it is
a host-restricted clone that deleted ~1.4 Mb. This script tests for that directly.

THE TEST
--------
Three independent criteria, in increasing order of what they establish:

  1. COMPLEX MEMBERSHIP  mash distance to K96243 <= 0.012.
     Excludes B. thailandensis (0.064), B. humptydooensis (0.066) and
     B. oklahomensis (0.081), which sit ~7x further out than anything in this
     collection. Does NOT exclude B. mallei.

  2. NOT B. MALLEI       fraction of 540 diagnostic cgMLST loci that are called.
     These are loci present in both B. pseudomallei reference genomes and absent
     from all eight complete B. mallei genomes tested. Held-out validated: define
     the set on 4 B. mallei and score the other 4, over all 70 splits, and the
     worst held-out B. mallei scores 0.061 while the worst of 3,033 real
     B. pseudomallei scores 0.685. Threshold 0.50 sits in a 62-point gap.

  3. SIZE SANITY         6.3 Mb <= assembly <= 7.6 Mb.
     B. mallei complete genomes span 5.23-5.91 Mb; this collection spans
     6.55-10.63 Mb. A coarse assembly-quality bound, not a species test.

  4. NOT REDUNDANT       NIPHEM (locus found in multiple EXACT copies) <= 300.
     Detects an assembly that carries part of the genome twice. Panel median is
     29 and p99 is 41; the two known-defective genomes score 1,395 and 1,444,
     and the highest legitimate genome is 131, so 300 sits in a wide gap.
     This is strictly better than criterion 3 for finding redundant assemblies:
     it flags exactly the 2 real cases where the size bound flags 20. BUSCO does
     NOT detect them (duplicated-BUSCO score 4.1%, against 4.3% for a normal
     genome), because B. pseudomallei's core BUSCOs sit on chromosome 1 and it is
     chromosome 2 that is duplicated.

Criterion 2 is the one that does the work no other tool does. Criteria 1 and 3 are
cheap and catch different failure modes.

USAGE
-----
  python3 species_id_bp.py \
      --alleles cgmlst_lichtenegger/results/results_alleles.tsv \
      --loci    rapid_id_2026-08-28/BP_DIAGNOSTIC_LOCI.txt \
      --mash    rapid_id_2026-08-28/RAPID_ID_BPC_3033.tsv \
      --out     SPECIES_ID.tsv

--mash is optional; without it criteria 1 and 3 are skipped and only the
B. mallei test is reported.

REGENERATING THE LOCUS SET
--------------------------
See RAPID_ID_RESULT_2026-08-28.md §8. Briefly: run chewBBACA AlleleCall on the
B. pseudomallei references and a set of complete B. mallei genomes against the
same schema, then keep loci called in every B. pseudomallei and LNF in every
B. mallei. Re-derive it if the cgMLST schema changes.
"""
import argparse, csv, sys

MALLEI_MAX = 0.50      # below this, the genome lacks the B. pseudomallei-specific loci
NIPHEM_MAX = 300       # above this, part of the genome is present twice (panel p99 = 41)
MASH_MAX   = 0.012     # complex membership, the project's existing gate
SIZE_MIN   = 6_300_000
SIZE_MAX   = 7_600_000


def is_called(v: str) -> bool:
    """chewBBACA marks an absent locus LNF. Everything else is a call."""
    return bool(v) and v != "LNF" and not v.startswith("LNF")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alleles", required=True, help="chewBBACA results_alleles.tsv")
    ap.add_argument("--loci", required=True, help="BP_DIAGNOSTIC_LOCI.txt, one locus per line")
    ap.add_argument("--mash", help="table with sample_id, d_B_pseudomallei_K96243, total_bp")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    want = {l.strip() for l in open(a.loci) if l.strip()}
    fh = open(a.alleles)
    rd = csv.reader(fh, delimiter="\t")
    hdr = next(rd)[1:]
    idx = [i for i, l in enumerate(hdr) if l in want]
    if not idx:
        sys.exit("ERROR: none of the diagnostic loci are present in the allele table. "
                 "Wrong schema, or the locus set needs re-deriving.")
    if len(idx) < len(want):
        print(f"WARNING: {len(want) - len(idx)} of {len(want)} diagnostic loci are absent "
              f"from this allele table; scoring on the {len(idx)} present.", file=sys.stderr)

    aux = {}
    if a.mash:
        for r in csv.DictReader(open(a.mash), delimiter="\t"):
            try:
                aux[r["sample_id"]] = (float(r["d_B_pseudomallei_K96243"]), int(r["total_bp"]))
            except (KeyError, ValueError):
                pass

    out, counts = [], {}
    for r in rd:
        sid, vals = r[0], r[1:]
        n = sum(1 for i in idx if is_called(vals[i]))
        frac = n / len(idx)
        niphem = sum(1 for v in vals if v.startswith("NIPHEM"))
        d, bp = aux.get(sid, (None, None))

        fail = []
        if frac < MALLEI_MAX:
            fail.append("NOT_B_PSEUDOMALLEI:lacks_diagnostic_loci")
        if d is not None and d > MASH_MAX:
            fail.append("OUTSIDE_COMPLEX:mash")
        if bp is not None and not (SIZE_MIN <= bp <= SIZE_MAX):
            fail.append("SIZE_OUT_OF_RANGE:" + ("low" if bp < SIZE_MIN else "high"))
        if niphem > NIPHEM_MAX:
            fail.append("REDUNDANT_ASSEMBLY:niphem")

        verdict = "B_pseudomallei" if not fail else ";".join(fail)
        counts[verdict.split(":")[0]] = counts.get(verdict.split(":")[0], 0) + 1
        out.append(dict(sample_id=sid, diagnostic_loci_called=n,
                        diagnostic_frac=round(frac, 4), niphem=niphem,
                        mash_K96243="" if d is None else f"{d:.6f}",
                        total_bp="" if bp is None else bp, verdict=verdict))

    out.sort(key=lambda r: r["diagnostic_frac"])
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter="\t",
                           lineterminator="\n")  # NOT the csv default \r\n: CRLF breaks awk/cut downstream
        w.writeheader(); w.writerows(out)

    print(f"scored {len(out)} genomes on {len(idx)} diagnostic loci -> {a.out}")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {v:>6}  {k}")


if __name__ == "__main__":
    main()
