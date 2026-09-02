#!/usr/bin/env python3
"""
Relapse vs reinfection calls for the Nakhon Phanom recurrence series, on
genome-wide distance instead of MLST identity.

WHY THIS EXISTS
---------------
The previous table (C29_recurrence_pairwise.csv) classified every pair on
same-ST and carried a `patristic` column with two defects:

  1. NOT REPRODUCIBLE. None of the 1,217 trees in this workspace produce the
     listed values. For 17 of 20 rows, 14 trees contain both isolates and none
     agree; the ratio of the listed value to the true chromosome 1 distance
     scatters 0.00x-7.50x, so it is not a unit conversion. One row
     (IP-0185-9 vs IP-0216-2) is listed as 0.0, implying identical genomes,
     where the trees give 3.09e-4 and 3.18e-4, among the largest in the table.

  2. NO SOURCE TREE FOR 3 ROWS. Patient 9's isolates sit in different clusters
     (strain_2_L1_10 and strain_2_L1_9) and patients 7 and 10's four isolates
     are not in the curated panel at all, so no single cluster tree contains
     those pairs. Patient 9's 0.1153 is ~500x any other value in the column.

Same-ST is also too weak a criterion to state. Within this collection there are
18 pairs of isolates from DIFFERENT patients carrying byte-identical seven-locus
profiles (ST10 and ST538) at mash 5.1e-4 to 1.0e-3. Chance ST sharing is common
in an endemic setting, so same-ST carries no margin on its own. What actually
separates the two classes is genome-wide distance, so that is what this script
computes and states.

THE RULE
--------
Two separate questions, reported in two separate columns. Conflating them is
what made the previous table overclaim.

`classification` answers "are these two isolates the same strain?":

  RELAPSE      mash distance < REL_MAX
  REINFECTION  mash distance >= REL_MAX

REL_MAX = 0.001 is CHOSEN, not calibrated. This series carries no clinically
adjudicated truth set, so nothing here calibrates a cutoff. It is placed inside
an empirical gap in these same 20 pairs: 19 pairs span 1.9e-5 to 2.5e-4 and one
(patient 9) sits at 2.6e-3, roughly 10x above the rest with nothing in between.
Any cutoff in 2.6e-4 to 2.5e-3 gives identical calls, which is why the exact
value does not matter. Because the gap is observed in the data being classified,
this column describes the data; it does not validate itself. Treat it as
descriptive.

`exclusive` answers the harder question, "does that rule out reinfection?":

  True   no other local genome is within MARGIN_X of this pair's distance, so a
         persisting strain is the only close explanation.
  False  at least one genome from the local collection sits about as close to
         one of these isolates as they sit to each other. Same-strain still
         holds, but reinfection from a locally circulating near-identical clone
         cannot be excluded on genome-wide distance alone.

`exclusive` is False for several pairs here, which is a real limitation of this
collection rather than a defect in a given pair. IP-0227-9, for instance, sits
2.9e-5 from patient 13's first isolate, closer than that patient's own next
episode at 3.2e-5. IP-0227-9 is a lab-only row with no StudyID, so it cannot be
attributed to a patient at all. Genome-wide distance therefore bounds how
confident a relapse call can be; it does not settle it.

MARGIN_X = 3 is likewise chosen, and the raw `margin` is reported per pair so a
reader can apply their own threshold.

Distances are mash, k=21, s=100000. The large sketch is for resolution at the
relapse scale; the default s=1000 cannot separate 2e-5 from 2e-4. Mash is a
whole-genome k-mer distance, so unlike the tree columns it does not depend on a
reference, a core alignment, a cluster assignment or a recombination filter,
which is what made the previous column unreproducible.

CAVEATS
-------
  - Patient, episode and collection date are carried over verbatim from the
    input CSV. No local metadata file carries a patient, episode or date column,
    so those fields are unverifiable here and patient 11's absence from the
    series could not be confirmed as deliberate.
  - The background set is every IP- genome present locally. Patient identity is
    unknown for all but the 29 recurrence isolates, so a background genome could
    in principle belong to the same patient. That would understate a margin, and
    so is conservative for relapse calls.
  - Assemblies must come from one assembler. SKESA and SPAdes shift mash by ~27%
    on the same reads, so mixing them would corrupt these distances. All IP-
    genomes in ASSEMBLY_DIR are from the same collection and pipeline.
"""

import csv
import os
import subprocess
import sys
import urllib.request
from datetime import date

REPO = os.path.dirname(os.path.abspath(__file__))
NOTES = ("/home/phemarajata/Insync/Peera.Hemarajata@tha.aphl.org/OneDrive Biz/"
         "Bioinformatics Support by Country/Thailand/"
         "Burkholderia_pseudomallei_genomics/claude notes")

IN_CSV = os.path.join(NOTES, "C29_recurrence_pairwise.csv")
OUT_CSV = os.path.join(NOTES, "C29_recurrence_pairwise_mash.csv")
ALLELES = os.path.join(REPO, "MLST_ALLELES_WIDE.tsv")
PROFILES = os.path.join(REPO, "mlst_profiles_bpseudomallei.tsv")
ASSEMBLY_DIR = "/home/phemarajata/Downloads/320_isolates"
WORKDIR = os.environ.get("RECURRENCE_WORKDIR", "/tmp/recurrence_mash_bp")

PROFILES_URL = ("https://rest.pubmlst.org/db/pubmlst_bpseudomallei_seqdef"
                "/schemes/1/profiles_csv")
LOCI = ["ace", "gltB", "gmhD", "lepA", "lipA", "narK", "ndh"]

MASH_K = 21
MASH_S = 100000
REL_MAX = 0.001
MARGIN_X = 3.0
THREADS = 8


def load_profiles():
    """Map a seven-locus allele tuple to its PubMLST ST."""
    if not os.path.exists(PROFILES):
        sys.stderr.write("fetching PubMLST profiles\n")
        urllib.request.urlretrieve(PROFILES_URL, PROFILES)
    prof = {}
    with open(PROFILES) as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            prof[tuple(row[locus] for locus in LOCI)] = row["ST"]
    return prof


def load_alleles():
    with open(ALLELES) as fh:
        return {row["FILE"]: tuple(row[locus] for locus in LOCI)
                for row in csv.DictReader(fh, delimiter="\t")}


def mash_matrix(names):
    """All-pairs mash distances over the named assemblies."""
    os.makedirs(WORKDIR, exist_ok=True)
    listfile = os.path.join(WORKDIR, "genomes.txt")
    sketch = os.path.join(WORKDIR, "genomes")
    with open(listfile, "w") as fh:
        for name in names:
            fh.write(os.path.join(ASSEMBLY_DIR, name + ".fasta") + "\n")
    subprocess.run(["mash", "sketch", "-p", str(THREADS), "-k", str(MASH_K),
                    "-s", str(MASH_S), "-o", sketch, "-l", listfile],
                   check=True, capture_output=True)
    out = subprocess.run(["mash", "dist", "-p", str(THREADS),
                          sketch + ".msh", sketch + ".msh"],
                         check=True, capture_output=True, text=True).stdout
    dist = {}
    for line in out.splitlines():
        a, b, d = line.split("\t")[:3]
        a = os.path.basename(a)[:-6]
        b = os.path.basename(b)[:-6]
        dist[(a, b)] = float(d)
    return dist


def classify(pair_d, nn_a, nn_b):
    """Same strain or not, on absolute distance; separately, whether any other
    local genome is close enough to leave reinfection open."""
    call = "Relapse" if pair_d < REL_MAX else "Reinfection"
    margin = float("inf") if pair_d <= 0 else min(nn_a, nn_b) / pair_d
    # Only meaningful for a relapse call. On a reinfection call a margin below 1
    # is the expected signature, not a weakness: it says the two isolates are
    # each closer to other local genomes than to each other.
    exclusive = (margin >= MARGIN_X) if call == "Relapse" else "n/a"
    return call, margin, exclusive


def main():
    prof = load_profiles()
    alleles = load_alleles()

    with open(IN_CSV) as fh:
        rows = list(csv.DictReader(fh))

    patient_of = {}
    for row in rows:
        patient_of.setdefault(row["isolate_A"], row["patient"])
        patient_of.setdefault(row["isolate_B"], row["patient"])

    background = sorted(
        f[:-6] for f in os.listdir(ASSEMBLY_DIR)
        if f.startswith("IP-") and f.endswith(".fasta"))
    missing = [i for i in patient_of if i not in set(background)]
    if missing:
        sys.exit("assemblies missing for: " + ", ".join(sorted(missing)))
    sys.stderr.write("sketching %d genomes (k=%d s=%d)\n"
                     % (len(background), MASH_K, MASH_S))
    dist = mash_matrix(background)

    def nearest_other(iso):
        """Closest genome not known to belong to the same patient."""
        best, best_d = None, float("inf")
        for other in background:
            if other == iso:
                continue
            if patient_of.get(other) is not None and \
               patient_of.get(other) == patient_of.get(iso):
                continue
            d = dist[(iso, other)]
            if d < best_d:
                best, best_d = other, d
        return best, best_d

    nn_cache = {iso: nearest_other(iso) for iso in patient_of}

    fields = ["patient", "episode_A", "isolate_A", "date_A",
              "episode_B", "isolate_B", "date_B",
              "interval_days", "interval_months",
              "ST_A", "ST_B", "profile_A", "profile_B", "same_profile",
              "mash_dist", "nn_A", "nn_A_dist", "nn_B", "nn_B_dist",
              "margin", "exclusive", "consecutive", "classification"]

    out_rows = []
    for row in rows:
        a, b = row["isolate_A"], row["isolate_B"]
        pa, pb = alleles[a], alleles[b]
        st = lambda p: ("ST" + prof[p]) if p in prof else "novel"
        d = dist[(a, b)]
        nn_a, nn_a_d = nn_cache[a]
        nn_b, nn_b_d = nn_cache[b]
        call, margin, exclusive = classify(d, nn_a_d, nn_b_d)

        # Recompute the interval from the dates rather than trusting the input.
        da = date.fromisoformat(row["date_A"])
        db = date.fromisoformat(row["date_B"])
        days = (db - da).days

        out_rows.append({
            "patient": row["patient"],
            "episode_A": row["episode_A"], "isolate_A": a, "date_A": row["date_A"],
            "episode_B": row["episode_B"], "isolate_B": b, "date_B": row["date_B"],
            "interval_days": days,
            "interval_months": round(days / 30.44, 1),
            "ST_A": st(pa), "ST_B": st(pb),
            "profile_A": "-".join(pa), "profile_B": "-".join(pb),
            # Compare allele profiles, not ST labels. Two different novel
            # profiles both render as "novel" and must not count as a match.
            "same_profile": pa == pb,
            "mash_dist": f"{d:.6f}",
            "nn_A": nn_a, "nn_A_dist": f"{nn_a_d:.6f}",
            "nn_B": nn_b, "nn_B_dist": f"{nn_b_d:.6f}",
            "margin": f"{margin:.2f}" if margin != float("inf") else "inf",
            "exclusive": exclusive,
            "consecutive": row["consecutive"],
            "classification": call,
        })

    with open(OUT_CSV, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    # Summary: the empirical gap the chosen margin sits inside.
    rel = sorted(float(r["mash_dist"]) for r in out_rows
                 if r["classification"] == "Relapse")
    rei = sorted(float(r["mash_dist"]) for r in out_rows
                 if r["classification"] == "Reinfection")
    print("wrote %s (%d rows)" % (OUT_CSV, len(out_rows)))
    if rel:
        print("relapse      n=%2d  mash %.5f - %.5f"
              % (len(rel), rel[0], rel[-1]))
    if rei:
        print("reinfection  n=%2d  mash %.5f - %.5f"
              % (len(rei), rei[0], rei[-1]))
    if rel and rei:
        print("gap between the two classes: %.5f to %.5f (%.0fx), cutoff %.5f"
              % (rel[-1], rei[0], rei[0] / rel[-1], REL_MAX))

    rel_rows = [r for r in out_rows if r["classification"] == "Relapse"]
    weak = [r for r in rel_rows if r["exclusive"] is False]
    print("relapse calls a local genome could also explain (exclusive=False):"
          " %d of %d" % (len(weak), len(rel_rows)))
    for r in weak:
        print("  patient %-3s %s/%s  pair=%s  nearest other=%s (%s)  margin=%s"
              % (r["patient"], r["isolate_A"], r["isolate_B"], r["mash_dist"],
                 min(r["nn_A_dist"], r["nn_B_dist"]),
                 r["nn_A"] if r["nn_A_dist"] <= r["nn_B_dist"] else r["nn_B"],
                 r["margin"]))

    disagree = [(r["patient"], r["isolate_A"], r["isolate_B"],
                 old["classification"], r["classification"])
                for r, old in zip(out_rows, rows)
                if r["classification"] != old["classification"]]
    print("changed calls vs the ST-based table: %d" % len(disagree))
    for row in disagree:
        print("  patient %s %s/%s  %s -> %s" % row)


if __name__ == "__main__":
    main()
