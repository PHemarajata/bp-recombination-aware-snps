#!/usr/bin/env python3
"""Build the independent-review package.

The first package was assembled by hand and had drifted within a day: three
documents stale, one missing. This script exists so a refresh is a command
rather than a memory exercise.

Safety property, and the reason this is worth reading before running it:
repository content is taken from `git ls-files` and nothing else. Both
repositories run a deny-by-default .gitignore that re-admits only source and
documentation by extension, so anything git does not track cannot reach the
package. That is a stronger guarantee than an exclusion list, which only
catches what someone remembered to name. The named checks below are a second
layer, not the first.

B. pseudomallei is a US Tier 1 Select Agent and the study metadata joins
accession to isolation location, collection date and exposure label, which is
re-identifiable for rare cases. No isolate-level table ships here.

Usage:
    python3 build_review_package_bp.py [--outdir DIR] [--date YYYY-MM-DD]
"""

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ANALYSIS_REPO = Path.home() / "Downloads" / "snp-mod-local-working"
PIPELINE_REPO = Path.home() / "wf-assembly-snps-mod"

# Deliberately withheld: per-genome tables that join accession to location,
# date or exposure. All four are untracked, so the git-only rule already
# excludes them; naming them makes the omission auditable rather than lucky.
WITHHELD = [
    "L1v4c_MERGED_METADATA.tsv",
    "CGMLST_LICHT_ATTRIBUTION.tsv",
    "GROUPING_PREDICTIONS.tsv",
    "FINAL_PARTITION.tsv",
]

# Extensions that would carry isolate-level rows if one ever slipped past git.
DATA_EXT = {".tsv", ".csv", ".fasta", ".fa", ".aln", ".gff", ".tre", ".nwk", ".vcf"}

# The only data-shaped files either repository tracks, both verified harmless:
# a three-line samplesheet template whose paths are literally /path/to/files/,
# and a zero-byte test fixture. Allowlisted by exact path rather than by
# extension, so a real .csv appearing anywhere else still stops the build.
DATA_ALLOWED = {
    "pipeline/assets/samplesheet.csv",
    "pipeline/test_input/test.fasta",
}

# Column names that make a table per-genome rather than aggregate. This, not the
# file extension, is what actually distinguishes a publishable summary from a
# re-identifiable one.
ACCESSION_COLS = {
    "accession", "assembly_accession", "genome", "genome_id", "biosample",
    "sample", "sample_id", "sample_name", "run_accession", "srr", "isolate",
    "strain_id", "taxon", "tip", "tip_label", "seq_id", "sequence_id",
}


def sh(cmd, cwd, allow_fail=False):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        if allow_fail:
            return ""
        sys.exit(f"REFUSING: {' '.join(cmd)} failed in {cwd}\n{r.stderr}")
    return r.stdout


def repo_state(repo):
    """Describe a repository precisely enough to be checked later."""
    if not repo.is_dir():
        sys.exit(f"REFUSING: {repo} does not exist")
    dirty = sh(["git", "status", "--porcelain"], repo).strip()
    return {
        "path": repo,
        "head": sh(["git", "rev-parse", "--short", "HEAD"], repo).strip(),
        "branch": sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo).strip(),
        "date": sh(["git", "log", "-1", "--format=%cs"], repo).strip(),
        "tag": sh(["git", "describe", "--tags", "--abbrev=0"], repo,
                          allow_fail=True).strip() or "(untagged)",
        "files": [f for f in sh(["git", "ls-files"], repo).splitlines() if f],
        "dirty": dirty,
    }


def copy_tracked(state, dest):
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for rel in state["files"]:
        src = state["path"] / rel
        if not src.is_file():          # deleted but still staged
            continue
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
        n += 1
    return n


def audit(root):
    """Fail loudly rather than ship an isolate-level table.

    Two rules, because the risk is not the file extension. `evidence/` ships
    tables by design, and they are safe for a reason worth stating: every one is
    aggregate, keyed on unit or on a summary row, and none carries an accession
    column. What would be unsafe is a table with one row per genome, since the
    metadata joins accession to isolation location, collection date and exposure
    label. So the extension rule guards the git-copied trees, where a data file
    has no business appearing at all, and the column rule guards everything,
    including anything a future hand adds to evidence/.
    """
    problems = []
    git_trees = ("repository/", "pipeline/")
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if p.name in WITHHELD:
            problems.append(f"withheld table present: {rel}")
        in_git_tree = rel.startswith(git_trees)
        if p.suffix.lower() in DATA_EXT:
            if in_git_tree and rel not in DATA_ALLOWED:
                problems.append(f"data-shaped file in a git tree: {rel}")
            if p.suffix.lower() in {".tsv", ".csv"} and rel not in DATA_ALLOWED:
                sep = "\t" if p.suffix.lower() == ".tsv" else ","
                try:
                    header = p.read_text(errors="replace").split("\n", 1)[0]
                except OSError:
                    continue
                cols = {c.strip().strip('"').lower() for c in header.split(sep)}
                hit = cols & ACCESSION_COLS
                if hit:
                    problems.append(
                        f"per-genome key in {rel}: {sorted(hit)}. Aggregate it or "
                        f"withhold it; the metadata is re-identifiable.")
    # An allowlist entry that no longer matches anything is a stale exemption,
    # and a stale exemption is how a real file eventually slips through.
    for rel in sorted(DATA_ALLOWED):
        if not (root / rel).is_file():
            problems.append(f"allowlist entry matches nothing, remove it: {rel}")
    return problems


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, default=Path.home() / "Downloads")
    ap.add_argument("--date", default=None, help="package date stamp; defaults to today")
    args = ap.parse_args()

    import datetime
    stamp = args.date or datetime.date.today().isoformat()

    analysis = repo_state(ANALYSIS_REPO)
    pipeline = repo_state(PIPELINE_REPO)

    for st, name in ((analysis, "analysis"), (pipeline, "pipeline")):
        if st["dirty"]:
            print(f"  ! {name} repo has uncommitted changes; the package will not "
                  f"match {st['head']}:")
            for line in st["dirty"].splitlines()[:10]:
                print(f"      {line}")

    pkg = args.outdir / f"BP_REVIEW_PACKAGE_{stamp}"
    prior = pkg.is_dir()
    # evidence/ and figures/ are carried forward: they are generated artifacts
    # and derived tables, not repository content. REVIEW/ is not carried
    # forward -- it is the most reviewer-facing writing in the project and it
    # lived only in this directory, untracked, where deleting the package would
    # have destroyed it. It is now REVIEW_*.md at the top level of the analysis
    # repository, kept there rather than in a REVIEW/ subdirectory because the
    # .gitignore re-admits only top-level files by extension and that rule is
    # load-bearing.
    carried = {}
    for sub in ("evidence", "figures"):
        if prior and (pkg / sub).is_dir():
            carried[sub] = pkg / sub

    staging = args.outdir / f".{pkg.name}.new"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    for sub, src in carried.items():
        shutil.copytree(src, staging / sub)

    n_a = copy_tracked(analysis, staging / "repository")
    n_p = copy_tracked(pipeline, staging / "pipeline")

    problems = audit(staging)
    if problems:
        shutil.rmtree(staging)
        sys.exit("REFUSING to build; package would carry isolate-level data:\n  "
                 + "\n  ".join(problems[:20]))

    # The review layer comes from the repository, so a correction made to the
    # register is a commit rather than an edit to a directory in ~/Downloads.
    review = staging / "REVIEW"
    review.mkdir(parents=True, exist_ok=True)
    n_r = 0
    for src in sorted(ANALYSIS_REPO.glob("REVIEW_*.md")):
        if src.name == "REVIEW_README.md":
            continue
        shutil.copy2(src, review / src.name[len("REVIEW_"):])
        n_r += 1
    if n_r == 0:
        shutil.rmtree(staging)
        sys.exit("REFUSING: no REVIEW_*.md found in the analysis repository. The "
                 "review layer is the package's whole point; shipping without it "
                 "silently would be worse than not building.")

    # README counts are rewritten so they cannot go stale the way they did when
    # the package was assembled by hand.
    text = (ANALYSIS_REPO / "REVIEW_README.md").read_text()
    text = re.sub(r"the complete tracked repository, \d+ files",
                  f"the complete tracked repository, {n_a} files", text)
    text = re.sub(r"the Nextflow workflow that produced the results, at\n"
                  r"\s*v[\d.]+\S*, \d+ files",
                  f"the Nextflow workflow that produced the results, at\n"
                  f"                     {pipeline['tag']}, {n_p} files", text)
    (staging / "README.md").write_text(text)

    if prior:
        shutil.rmtree(pkg)
    staging.rename(pkg)

    tar = args.outdir / f"{pkg.name}.tar.gz"
    if tar.exists():
        tar.unlink()
    with tarfile.open(tar, "w:gz") as tf:
        tf.add(pkg, arcname=pkg.name)

    print(f"\n  package   {pkg}")
    print(f"  analysis  {analysis['branch']}@{analysis['head']} ({analysis['date']}), "
          f"{n_a} files")
    print(f"  pipeline  {pipeline['branch']}@{pipeline['head']} ({pipeline['date']}), "
          f"tag {pipeline['tag']}, {n_p} files")
    for sub in ("REVIEW", "evidence", "figures"):
        d = pkg / sub
        if d.is_dir():
            print(f"  {sub:9} {sum(1 for _ in d.rglob('*') if _.is_file())} files")
    print(f"  tarball   {tar.name}  {tar.stat().st_size / 1e6:.1f} MB")
    print(f"  sha256    {digest(tar)}")
    print("\n  audit: no withheld table, no data-shaped file. Content is "
          "git-tracked only.")


if __name__ == "__main__":
    main()
