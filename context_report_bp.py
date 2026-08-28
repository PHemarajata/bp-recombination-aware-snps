#!/usr/bin/env python3
"""
Turn the per-group Gubbins output into recurrence answers: recombination-filtered
SNP distances, a per-pair exclusivity check, and annotated context trees.

WHAT THE TWO NUMBERS MEAN
-------------------------
`snp` is the number of differences between two episodes at sites that survived
Gubbins' recombination filter, so imported tracts are excluded. This is the
number that answers "is this the same strain persisting".

`nearest_other_snp` is the distance from either isolate to the closest genome in
the same local context group that is NOT from the same patient. It answers the
question the SNP distance alone cannot: whether a locally circulating clone
could explain the second episode just as well. A relapse call is only exclusive
when the pair is much closer to each other than either is to anything else
circulating locally.

Both are computed on the whole-genome alignment (snippy-core against the group
medoid), not per replicon, so each pair gets one number.

OUTPUTS
-------
  CONTEXT_RECURRENCE_SNPS.tsv   per-pair distances and exclusivity
  trees/<group>.annotated.tre   Newick with recurrence tips relabelled
  trees/<group>.itol_*.txt      iTOL colorstrip and label annotation
"""

import csv
import json
import os
import re

REPO = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("CTX_WORK", "/tmp/recurrence_ctx")
GROUPS_JSON = "/tmp/recurrence_mash_bp/context_groups.json"
NOTES = ("/home/phemarajata/Insync/Peera.Hemarajata@tha.aphl.org/OneDrive Biz/"
         "Bioinformatics Support by Country/Thailand/"
         "Burkholderia_pseudomallei_genomics/claude notes")
IN_CSV = os.path.join(NOTES, "C29_recurrence_pairwise.csv")
OUT_TSV = os.path.join(REPO, "CONTEXT_RECURRENCE_SNPS.tsv")
TREEDIR = os.path.join(REPO, "context_trees")

ACGT = set("ACGT")
MARGIN_X = 3.0

# Distinct colours for the 13 patients, plus grey for context genomes.
PALETTE = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#42d4f4",
           "#f032e6", "#bfef45", "#fabed4", "#469990", "#dcbeff", "#9a6324",
           "#800000"]
GREY = "#cccccc"


def read_fasta(path):
    """Sequences are upper-cased on read. snippy writes low-confidence calls in
    lowercase, and those positions are concentrated exactly at variant sites: on
    ctx07 a case-sensitive ACGT comparison scored 787 SNPs between two genomes
    where the correct answer is 15,390."""
    seqs, name, buf = {}, None, []
    for line in open(path):
        if line.startswith(">"):
            if name:
                seqs[name] = "".join(buf)
            name, buf = line[1:].strip().split()[0], []
        else:
            buf.append(line.strip().upper())
    if name:
        seqs[name] = "".join(buf)
    return seqs


def snp_dist(sa, sb):
    n = 0
    comp = 0
    for x, y in zip(sa, sb):
        if x in ACGT and y in ACGT:
            comp += 1
            if x != y:
                n += 1
    return n, comp


def main():
    state = json.load(open(GROUPS_JSON))
    rows = list(csv.DictReader(open(IN_CSV)))

    patient, episode = {}, {}
    for r in rows:
        patient.setdefault(r["isolate_A"], r["patient"])
        patient.setdefault(r["isolate_B"], r["patient"])
        episode.setdefault(r["isolate_A"], r["episode_A"])
        episode.setdefault(r["isolate_B"], r["episode_B"])

    group_of, alns, rm = {}, {}, {}
    ready = []
    for g in state["groups"]:
        name = g["name"]
        f = os.path.join(WORK, name, "gubbins",
                         name + ".filtered_polymorphic_sites.fasta")
        if not os.path.exists(f):
            continue
        alns[name] = read_fasta(f)
        ready.append(g)

    # A genome can sit in two groups, because small groups were padded to a
    # workable size with their nearest neighbours. Always evaluate a genome in
    # the group it actually belongs to, never in one it was borrowed into:
    # patient 14 was padded into ctx06 (12 genomes) and would otherwise be
    # scored there instead of in its own ctx02 (43 genomes), which silently
    # replaces its real nearest neighbour with a distant one.
    for g in ready:
        added = {a[0] for a in g.get("added", [])}
        for m in g["members"]:
            if m not in added:
                group_of[m] = g["name"]
    for g in ready:
        for m in g["members"]:
            group_of.setdefault(m, g["name"])

    for g in ready:
        name = g["name"]
        stats = os.path.join(WORK, name, "gubbins",
                             name + ".per_branch_statistics.csv")
        if os.path.exists(stats):
            vals = []
            for rec in csv.DictReader(open(stats), delimiter="\t"):
                key = [k for k in rec if "Outside" in k]
                ins = [k for k in rec if "Inside" in k]
                if key and ins:
                    try:
                        out_n, in_n = float(rec[key[0]]), float(rec[ins[0]])
                        if out_n > 0:
                            vals.append(in_n / out_n)
                    except (TypeError, ValueError):
                        pass
            if vals:
                vals.sort()
                rm[name] = vals[len(vals) // 2]

    os.makedirs(TREEDIR, exist_ok=True)
    fields = ["patient", "isolate_A", "isolate_B", "group", "reference",
              "snp", "comparable_sites", "nearest_other_A", "nearest_other_A_snp",
              "nearest_other_B", "nearest_other_B_snp", "margin", "exclusive",
              "classification"]
    out = []

    for r in rows:
        a, b = r["isolate_A"], r["isolate_B"]
        gname = group_of.get(a)
        if gname is None or group_of.get(b) != gname:
            continue
        s = alns[gname]
        if a not in s or b not in s:
            continue
        d, comp = snp_dist(s[a], s[b])
        near = {}
        for iso in (a, b):
            best, bd = None, 10 ** 9
            for m in s:
                if m == iso or patient.get(m) == patient.get(iso):
                    continue
                dd = snp_dist(s[iso], s[m])[0]
                if dd < bd:
                    best, bd = m, dd
            near[iso] = (best, bd)
        margin = (min(near[a][1], near[b][1]) / d) if d else float("inf")
        call = "Relapse" if d <= 30 else "Reinfection"
        ref = next(g["reference"] for g in state["groups"]
                   if g["name"] == gname)
        out.append({
            "patient": r["patient"], "isolate_A": a, "isolate_B": b,
            "group": gname, "reference": ref,
            "snp": d, "comparable_sites": comp,
            "nearest_other_A": near[a][0], "nearest_other_A_snp": near[a][1],
            "nearest_other_B": near[b][0], "nearest_other_B_snp": near[b][1],
            "margin": ("inf" if margin == float("inf")
                       else "%.1f" % margin),
            "exclusive": (margin >= MARGIN_X) if call == "Relapse" else "n/a",
            "classification": call,
        })

    with open(OUT_TSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(out)

    # Annotated trees.
    pats = sorted({p for p in patient.values()}, key=int)
    colour = {p: PALETTE[i % len(PALETTE)] for i, p in enumerate(pats)}
    for g in state["groups"]:
        name = g["name"]
        tre = os.path.join(WORK, name, "gubbins", name + ".final.treefile")
        if not os.path.exists(tre):
            continue
        text = open(tre).read()
        for iso in sorted(patient, key=len, reverse=True):
            if iso in text:
                text = re.sub(r"\b%s\b" % re.escape(iso),
                              "P%s_ep%s_%s" % (patient[iso], episode[iso], iso),
                              text)
        open(os.path.join(TREEDIR, name + ".annotated.tre"), "w").write(text)

        members = [m for m in g["members"]]
        with open(os.path.join(TREEDIR, name + ".itol_colours.txt"), "w") as fh:
            fh.write("DATASET_COLORSTRIP\nSEPARATOR TAB\n"
                     "DATASET_LABEL\tpatient\nCOLOR\t#000000\n"
                     "LEGEND_TITLE\tRecurrence patient\n")
            fh.write("LEGEND_SHAPES\t" + "\t".join("1" for _ in pats) + "\n")
            fh.write("LEGEND_COLORS\t" + "\t".join(colour[p] for p in pats) + "\n")
            fh.write("LEGEND_LABELS\t" + "\t".join("patient " + p for p in pats) + "\n")
            fh.write("DATA\n")
            for m in members:
                fh.write("%s\t%s\t%s\n"
                         % (m, colour.get(patient.get(m), GREY),
                            ("patient " + patient[m]) if m in patient
                            else "context"))
        with open(os.path.join(TREEDIR, name + ".itol_labels.txt"), "w") as fh:
            fh.write("LABELS\nSEPARATOR TAB\nDATA\n")
            for m in members:
                if m in patient:
                    fh.write("%s\tP%s ep%s  %s\n"
                             % (m, patient[m], episode[m], m))

    print("wrote %s (%d pairs)" % (OUT_TSV, len(out)))
    print("wrote annotated trees and iTOL annotation to %s" % TREEDIR)
    if rm:
        print("median r/m per group: "
              + ", ".join("%s=%.2f" % (k, v) for k, v in sorted(rm.items())))
    print()
    print("%-4s %-11s %-11s %-7s %-6s %-9s %-8s %s"
          % ("pt", "A", "B", "group", "snp", "nearest", "margin", "exclusive"))
    for r in out:
        print("%-4s %-11s %-11s %-7s %-6s %-9s %-8s %s"
              % (r["patient"], r["isolate_A"], r["isolate_B"], r["group"],
                 r["snp"],
                 min(r["nearest_other_A_snp"], r["nearest_other_B_snp"]),
                 r["margin"], r["exclusive"]))


if __name__ == "__main__":
    main()
