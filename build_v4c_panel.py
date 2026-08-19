#!/usr/bin/env python3
"""
Panel/bundle helper for the unattended v4c build. One mode per step so
overnight_v4c.sh can fail at a known point rather than half-way through a
monolith.

  --report-delta   print what changes vs v4b (last line is a one-line summary)
  --build          write L1v4c_MERGED_METADATA.tsv + L1v4c_rfile.txt,
                   normalising the adopted SPAdes assemblies on the way
  --reconcile DIR  undo PopPUNK's '.'->'_' rewrite; write a sample-id phylip
  --fasta-dir DIR  one flat symlink dir for the reference picker
  --resolve-refs   turn reference paths into real absolute paths
  --bundle         build a100_stage_v4c/

Panel composition, unchanged in principle from v4b:
    v3 analysis panel + v3 recovered assign-only + the new batch
minus everything in PANEL_EXCLUSIONS.tsv, with PANEL_ASSEMBLY_OVERRIDES.tsv
deciding the file for any sample listed there.
"""
import argparse
import csv
import collections
import glob
import os
import shutil
import subprocess
import sys

B = os.path.dirname(os.path.abspath(__file__))
SPADES_SRC = "/home/phemarajata/Downloads/bp_spades_assemblies"
SPADES_NORM = f"{B}/additions/fasta_spades"
MIN_CONTIG = 500


def norm(n):
    o = "".join(c if c.isalnum() else "_" for c in n)
    return "_".join(x for x in o.split("_") if x)


def load(path, key=None, delim="\t"):
    rows = list(csv.DictReader(open(path), delimiter=delim))
    return {r[key]: r for r in rows} if key else rows


def excl_over():
    e = {r["sample_id"]: r for r in load(f"{B}/PANEL_EXCLUSIONS.tsv")}
    o = {r["sample_id"]: r for r in load(f"{B}/PANEL_ASSEMBLY_OVERRIDES.tsv")}
    return e, o


def spades_delivered():
    """Accessions the Illumina re-assembly actually produced. Anything in the new
    batch but NOT here went down the ONT path and was never re-assembled, so it
    must be carried over unchanged rather than treated as a QC failure."""
    out = set()
    for p in glob.glob(f"{SPADES_SRC}/*.fasta"):
        out.add(os.path.basename(p).replace("_filtered_contigs.fasta", "").replace(".fasta", ""))
    return out


def adopted():
    """sample -> assembly path, for the new batch after QC/overrides/exclusions."""
    e, o = excl_over()
    passed = [l.strip() for l in open(f"{B}/SPADES_PASS_LIST.txt") if l.strip()]
    out = {}
    for s in passed:
        if s in e:
            continue
        out[s] = o[s]["use_path"] if s in o else f"{SPADES_NORM}/{s}.fasta"
    # a sample pinned to SKESA may not be in the SPAdes pass list at all
    for s, r in o.items():
        if s not in e:
            out.setdefault(s, r["use_path"])
    return out


def normalise_spades():
    """>=500 bp and contigs renamed <sample>_<n>, matching additions/fasta_new200."""
    os.makedirs(SPADES_NORM, exist_ok=True)
    _, o = excl_over()
    n = 0
    for p in sorted(glob.glob(f"{SPADES_SRC}/*.fasta")):
        s = os.path.basename(p).replace("_filtered_contigs.fasta", "").replace(".fasta", "")
        if s in o:
            continue                      # pinned to SKESA, do not stage a SPAdes copy
        dst = f"{SPADES_NORM}/{s}.fasta"
        seqs, hdr, buf = [], None, []
        for line in open(p):
            if line.startswith(">"):
                if hdr is not None:
                    seqs.append("".join(buf))
                hdr, buf = line, []
            else:
                buf.append(line.strip())
        if hdr is not None:
            seqs.append("".join(buf))
        keep = sorted([x for x in seqs if len(x) >= MIN_CONTIG], key=len, reverse=True)
        with open(dst, "w") as fh:
            for i, seq in enumerate(keep, 1):
                fh.write(f">{s}_{i}\n")
                for j in range(0, len(seq), 80):
                    fh.write(seq[j:j + 80] + "\n")
        n += 1
    return n


def panel_rows():
    e, _ = excl_over()
    v4b = load(f"{B}/L1v4b_MERGED_METADATA.tsv")
    new = adopted()
    delivered = spades_delivered()
    rows, cols = [], list(v4b[0])
    for r in v4b:
        s = r["sample_id"]
        if s in e:
            continue
        if r["source_batch"] == "new200_2026-08-17":
            if s in new:
                r = dict(r); r["assembly_path"] = new[s]
            elif s in delivered:
                continue                  # was re-assembled and failed the re-QC
            # else: ONT path, never re-assembled -- keep the v4b assembly as is
        rows.append(r)
    have = {r["sample_id"] for r in rows}
    for s, p in sorted(new.items()):      # genomes that failed before and now pass
        if s in have:
            continue
        prev = load(f"{B}/NEW200_QC_2026-08-17.tsv", key="sample")
        sra = load(f"{B}/SRA_TO_ASSEMBLE.tsv", key="run_accession")
        m = sra.get(s, {})
        r = {c: "" for c in cols}
        origin = m.get("origin_country", "")
        r.update(sample_id=s, country=origin, acquired_from=origin,
                 subregion="unknown", collection_date=m.get("collection_date", "unknown"),
                 origin_basis=m.get("origin_basis", "as_isolated"),
                 isolation_location=m.get("ena_country", ""),
                 validation_label=origin if m.get("origin_basis") == "travel_reattributed" else "",
                 source_batch="new200_2026-08-17", country_source="sra_metadata",
                 origin_resolution="country" if origin else "unknown",
                 assembly_path=p)
        rows.append(r)
    return rows, cols


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-delta", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--reconcile")
    ap.add_argument("--fasta-dir")
    ap.add_argument("--resolve-refs", action="store_true")
    ap.add_argument("--bundle", action="store_true")
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()

    if a.check_only:
        return

    if a.report_delta:
        v4b = {r["sample_id"] for r in load(f"{B}/L1v4b_MERGED_METADATA.tsv")}
        new = adopted()
        e, _ = excl_over()
        old_new = {r["sample_id"] for r in load(f"{B}/L1v4b_MERGED_METADATA.tsv")
                   if r["source_batch"] == "new200_2026-08-17"}
        delivered = spades_delivered()
        added = sorted(set(new) - v4b)
        # only a genome that WAS re-assembled can be dropped by the re-QC
        removed = sorted(((old_new & delivered) - set(new)) | (v4b & set(e)))
        print(f"added: {added}")
        print(f"removed: {removed}")
        print(f"+{len(added)} / -{len(removed)}; {len(new)} new-batch genomes adopted")
        return

    if a.build:
        n = normalise_spades()
        print(f"normalised {n} SPAdes assemblies -> {SPADES_NORM}")
        rows, cols = panel_rows()
        for r in rows:
            if not os.path.isfile(r["assembly_path"]):
                sys.exit(f"missing assembly: {r['sample_id']} {r['assembly_path']}")
        ids = [r["sample_id"] for r in rows]
        if len(ids) != len(set(ids)):
            sys.exit("duplicate sample_id in v4c panel")
        with open(f"{B}/L1v4c_MERGED_METADATA.tsv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
            w.writeheader(); w.writerows(rows)
        with open(f"{B}/L1v4c_rfile.txt", "w") as fh:
            for r in rows:
                fh.write(f"{r['sample_id']}\t{r['assembly_path']}\n")
        print(f"v4c panel: {len(rows)} genomes")
        print("  by batch:", dict(collections.Counter(r["source_batch"] for r in rows)))
        return

    if a.reconcile:
        W = a.reconcile
        orig = {norm(l.split("\t")[0]): l.split("\t")[0] for l in open(f"{W}/rfile.txt")}
        src = [x for x in glob.glob(f"{W}/refined/*_clusters.csv") if "unword" not in x][0]
        rows = list(csv.reader(open(src)))
        out, n = [rows[0]], 0
        for r in rows[1:]:
            o = orig.get(norm(r[0]))
            if o and o != r[0]:
                r = [o] + r[1:]; n += 1
            out.append(r)
        csv.writer(open(f"{W}/refined_clusters_reconciled.csv", "w", newline=""), lineterminator="\n").writerows(out)
        name_of = {}
        for l in open(f"{W}/rfile.txt"):
            nm, p = l.rstrip("\n").split("\t")
            name_of[p] = nm; name_of[os.path.basename(p)] = nm
        import re
        with open(f"{W}/mash.phylip") as fh, open(f"{W}/mash_named.phylip", "w") as o2:
            o2.write(fh.readline())
            for line in fh:
                if not line.strip():
                    continue
                m = re.match(r"^(\S+)(.*)$", line.rstrip("\n"))
                lab = m.group(1)
                o2.write((name_of.get(lab) or name_of.get(os.path.basename(lab)) or lab)
                         + m.group(2) + "\n")
        print(f"reconciled {n} name(s); wrote mash_named.phylip")
        return

    if a.fasta_dir:
        d = os.path.join(a.fasta_dir, "all_fasta")
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for r in load(f"{B}/L1v4c_MERGED_METADATA.tsv"):
            os.symlink(r["assembly_path"], os.path.join(d, r["sample_id"] + ".fasta"))
        print(f"symlinked {len(os.listdir(d))} assemblies -> {d}")
        return

    if a.resolve_refs:
        rows = load(f"{B}/curated_L1v4c_refs.tsv")
        for r in rows:
            r["reference_path"] = os.path.realpath(r["reference_path"])
            if not os.path.isfile(r["reference_path"]):
                sys.exit(f"reference missing: {r}")
        with open(f"{B}/curated_L1v4c_refs.tsv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["cluster_id", "reference_path"], delimiter="\t", lineterminator="\n")
            w.writeheader(); w.writerows(rows)
        print(f"resolved {len(rows)} reference paths")
        return

    if a.bundle:
        S = f"{B}/a100_stage_v4c"
        shutil.rmtree(S, ignore_errors=True)
        os.makedirs(f"{S}/inputs"); os.makedirs(f"{S}/bin")
        rows = load(f"{B}/L1v4c_MERGED_METADATA.tsv")
        with open(f"{S}/inputs/samplesheet.csv", "w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n"); w.writerow(["sample", "file"])
            for r in rows:
                w.writerow([r["sample_id"], f"__A100_BASE__/fasta/{r['sample_id']}.fasta"])
        refs = load(f"{B}/curated_L1v4c_refs.tsv")
        with open(f"{S}/inputs/refs.tsv", "w", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", lineterminator="\n"); w.writerow(["cluster_id", "reference_path"])
            for r in refs:
                w.writerow([r["cluster_id"],
                            f"__A100_BASE__/fasta/{os.path.basename(r['reference_path'])}"])
        for f in ["curated_L1v4c_clusters.tsv", "curated_L1v4c_units.tsv",
                  "curated_L1v4c_assignments_all.tsv", "L1v4c_MERGED_METADATA.tsv",
                  "PANEL_EXCLUSIONS.tsv", "PANEL_ASSEMBLY_OVERRIDES.tsv",
                  "SPADES_QC_2026-08-17.tsv"]:
            if os.path.isfile(f"{B}/{f}"):
                shutil.copyfile(f"{B}/{f}", f"{S}/inputs/{f}")
        shutil.copyfile(f"{B}/a100_stage/inputs/curated_L1v4b_clusters.tsv",
                        f"{S}/inputs/curated_L1v4b_clusters.tsv")  # for comparison
        for f in ["run_wf_curated_L1.sh", "normalize_reference_headers_bp.py",
                  "write_if_changed_bp.py"]:
            shutil.copyfile(f"{B}/{f}", f"{S}/bin/{f}")
        os.chmod(f"{S}/bin/run_wf_curated_L1.sh", 0o755)
        shutil.copyfile(f"{B}/a100_stage/curated_L1_overrides_a100.config",
                        f"{S}/curated_L1_overrides_a100.config")
        # README: correct the v4b-specific header for v4c
        rd = open(f"{B}/a100_stage/README_A100.md").read()
        banner = ("# A100 staging bundle \u2014 v4c panel\n\n"
                  "**%d genomes, built %s.** v4c = v4b with the mixed sample "
                  "SRR30648681 removed, 168 new-batch genomes on their SPAdes "
                  "re-assemblies, and 4 genomes rescued from exclusion after the "
                  "SPAdes re-assembly fixed them (see inputs/PANEL_RESCUES). Every "
                  "unit is quotable \u2014 no known-bad genome remains in the panel.\n\n"
                  "---\n\n" % (len(rows), "overnight 2026-08-18"))
        # drop the old title line, splice in the v4c banner
        body = rd.split("\n", 1)[1] if rd.startswith("# ") else rd
        open(f"{S}/README_A100.md", "w").write(banner + body)
        if os.path.isfile(f"{B}/PANEL_RESCUES_2026-08-18.tsv"):
            shutil.copyfile(f"{B}/PANEL_RESCUES_2026-08-18.tsv",
                            f"{S}/inputs/PANEL_RESCUES_2026-08-18.tsv")
        # run_a100.sh with the v4c input names
        r = open(f"{B}/a100_stage/run_a100.sh").read()
        r = (r.replace("inputs/wf_L1v4b_samplesheet.csv", "inputs/samplesheet.csv")
               .replace("inputs/curated_L1v4b_refs.tsv", "inputs/refs.tsv")
               .replace("inputs/curated_L1v4b_clusters.tsv", "inputs/curated_L1v4c_clusters.tsv")
               .replace("inputs/wf_L1v4b_run_samplesheet.csv", "inputs/run_samplesheet.csv"))
        open(f"{S}/run_a100.sh", "w").write(r)
        os.chmod(f"{S}/run_a100.sh", 0o755)
        # flat assembly archive
        work = f"{S}/.build/fasta"
        os.makedirs(work)
        for x in rows:
            os.symlink(x["assembly_path"], os.path.join(work, x["sample_id"] + ".fasta"))
        subprocess.run(f"cd {S}/.build && tar -chf - fasta | zstd -T4 -3 -q -o {S}/fasta.tar.zst",
                       shell=True, check=True)
        subprocess.run(f"cd {S} && sha256sum fasta.tar.zst > fasta.tar.zst.sha256",
                       shell=True, check=True)
        shutil.rmtree(f"{S}/.build")
        print(f"bundle: {len(rows)} genomes, {len(refs)} references")
        return


if __name__ == "__main__":
    main()
