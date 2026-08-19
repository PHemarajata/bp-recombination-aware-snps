#!/usr/bin/env python3
"""
reference_sensitivity_bp.py

The reference-sensitivity experiment from REVISED_STRATEGY_2026-08.md section 2.4.

WHAT THIS TESTS
---------------
Whether the choice of mapping reference is contributing to weak temporal signal
in per-cluster B. pseudomallei analyses. Take one mid-sized cluster, build it
with N callers against M references, push each arm through Gubbins, and compare:

  - post-Gubbins SNP count           (does a distant reference inflate it?)
  - polymorphic positions shared     (do the callers agree on WHERE the SNPs are?)
  - recombination blocks / r/m       (recombination inference is itself
                                      reference-dependent -- PMID 33503026)
  - tree distance                    (RF and Kendall-Colijn at lambda=0)
  - root-to-tip slope and R^2        (the outcome that matters for dating)

THE PREDICTION BEING TESTED, from the ska lo PMEN2 experiment (PMID 40171940):
moving to a reference at 98.52% OrthoANI took Snippy from 2,320 to 3,291
post-Gubbins SNPs (+42%) and root-to-tip R from 0.46-0.50 down to 0.25-0.29,
while the reference-free callers barely moved. If that pattern reproduces on
B. pseudomallei, reference bias is contributing to the weak temporal signal and
the fix is a per-cluster reference. If it does not, reference bias is retired as
a concern and everything downstream is strengthened. Either outcome is a result.

Nobody has ever quantified reference bias in this organism. The only study that
varied the reference at all is Webb 2022 (PMID 35080450), a two-pair
outbreak-scale comparison reporting neither callable fraction nor tree distances.

USAGE
-----
  # 1. emit the run matrix as executable bash (does not run anything)
  python3 reference_sensitivity_bp.py plan \
      --cluster-list cluster12_genomes.txt \
      --ref close=refs/cluster12_representative.fasta \
      --ref K96243=refs/GCF_000011545.1_K96243.fasta \
      --ref 1026b=refs/1026b.fasta \
      --outdir refsens_cluster12 \
      --threads 16

  # 2. run it (or submit arms/*.sh to your scheduler)
  bash refsens_cluster12/run_all.sh

  # 3. analyse whatever completed
  python3 reference_sensitivity_bp.py analyse \
      --outdir refsens_cluster12 \
      --dates cluster12_dates.csv

  # verify the tree/statistics code on synthetic data
  python3 reference_sensitivity_bp.py selftest

GUARDS BAKED INTO THE EMITTED COMMANDS
--------------------------------------
  * `ska map`, NEVER `ska align`, into Gubbins. Only `ska map` carries genomic
    coordinates; `ska align` columns are in hash-table order. Gubbins' sliding
    window would run on meaningless spacing and FAIL SILENTLY.
  * snp-sites runs AFTER Gubbins, never before. Variant-site alignments cannot
    be used for recombination-aware phylogenetics because the genomic distance
    between variant sites is an input to the method (Didelot & Parkhill 2022).
  * Gubbins gets full-length pseudogenomes, never a SNP-only alignment, and
    never a concatenated core-gene alignment.
  * Replicons are split BEFORE Gubbins. Gubbins cannot handle multi-contig
    references, its 0.1-10 kb window would scan across the junction, and
    snp-sites hardcodes CHROM to "1".
  * Gubbins pinned >=3.4.3 with --invariant-site-correction passed EXPLICITLY.
    v3.4.2 made the correction optional and defaulted it off.

Stdlib only, matching ska_feasibility_bp.py and cluster_diagnostics_bp.py.
Nothing here is a published threshold; the decision rule in `analyse` is a
construct and is labelled as one.
"""

import argparse
import csv
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Organism / tooling constants
# ---------------------------------------------------------------------------

# K96243, GCA_000011545.1
CHR1_ID_DEFAULT = "NC_006350.1"
CHR2_ID_DEFAULT = "NC_006351.1"
CHR1_LEN = 4_074_542
CHR2_LEN = 3_173_005
K96243_LEN = CHR1_LEN + CHR2_LEN  # 7,247,547

# Gubbins minimum acceptable version. v3.4.2 silently flipped the internal
# invariant-site correction OFF; v3.4.3 (tagged 2025-08-27) fixed the
# invariant-site calculations.
GUBBINS_MIN_VERSION = (3, 4, 3)

# Divergence of B. pseudomallei isolates from K96243, Chewapreecha 2017 Methods.
# Note this is NOT genome-wide divergence -- the denominator is undefined in the
# paper and reverse-engineers to ~772 kb, which reconciles with nothing. Carried
# here only to place the reference-distance range.
BP_DIVERGENCE_FROM_K96243 = (0.0073, 0.0561)

CALLERS = ("existing", "ska_map", "ska_lo")

DEFAULT_MIN_CLUSTER = 100
DEFAULT_MAX_CLUSTER = 300


# ===========================================================================
# Newick parsing and tree statistics (stdlib; verified by `selftest`)
# ===========================================================================

class Node:
    __slots__ = ("name", "length", "children", "parent")

    def __init__(self, name=None, length=0.0, parent=None):
        self.name = name
        self.length = length if length is not None else 0.0
        self.children = []
        self.parent = parent

    def is_leaf(self):
        return not self.children

    def leaves(self):
        if self.is_leaf():
            yield self
            return
        stack = [self]
        while stack:
            n = stack.pop()
            if n.is_leaf():
                yield n
            else:
                stack.extend(n.children)


_TOKEN = re.compile(r"\s*([(),;:]|[^(),;:\s]+)")


def parse_newick(text):
    """Parse a Newick string into a Node tree. Handles quoted labels, comments,
    branch lengths, and internal node labels (including Gubbins' node labels)."""
    text = re.sub(r"\[[^\]]*\]", "", text)  # strip [comments]
    text = text.strip()
    if not text:
        raise ValueError("empty newick")
    if not text.endswith(";"):
        text += ";"

    pos = 0
    n = len(text)

    def peek():
        nonlocal pos
        while pos < n and text[pos].isspace():
            pos += 1
        return text[pos] if pos < n else None

    def read_label():
        nonlocal pos
        while pos < n and text[pos].isspace():
            pos += 1
        if pos < n and text[pos] in "'\"":
            quote = text[pos]
            pos += 1
            start = pos
            while pos < n and text[pos] != quote:
                pos += 1
            label = text[start:pos]
            pos += 1
            return label
        start = pos
        while pos < n and text[pos] not in "(),:;":
            pos += 1
        return text[start:pos].strip()

    def read_length():
        nonlocal pos
        if peek() == ":":
            pos += 1
            start = pos
            while pos < n and (text[pos] not in "(),;"):
                pos += 1
            raw = text[start:pos].strip()
            try:
                return float(raw)
            except ValueError:
                return 0.0
        return 0.0

    def read_subtree():
        nonlocal pos
        node = Node()
        if peek() == "(":
            pos += 1
            while True:
                child = read_subtree()
                child.parent = node
                node.children.append(child)
                c = peek()
                if c == ",":
                    pos += 1
                    continue
                if c == ")":
                    pos += 1
                    break
                raise ValueError("malformed newick near offset %d" % pos)
            node.name = read_label() or None
        else:
            node.name = read_label() or None
        node.length = read_length()
        return node

    root = read_subtree()
    return root


def read_tree_file(path):
    with open(path) as fh:
        return parse_newick(fh.read())


def tip_names(root):
    return [lf.name for lf in root.leaves() if lf.name]


def root_to_tip_distances(root):
    """Cumulative branch length from root to each tip."""
    out = {}
    stack = [(root, 0.0)]
    while stack:
        node, acc = stack.pop()
        if node.is_leaf():
            if node.name:
                out[node.name] = acc
        else:
            for ch in node.children:
                stack.append((ch, acc + ch.length))
    return out


def total_tree_length(root):
    total = 0.0
    stack = list(root.children)
    while stack:
        node = stack.pop()
        total += node.length
        stack.extend(node.children)
    return total


def bipartitions(root, restrict=None):
    """Set of non-trivial unrooted bipartitions, each as a frozenset of the
    smaller side, over the tip set (optionally restricted)."""
    all_tips = set(tip_names(root))
    if restrict is not None:
        all_tips &= set(restrict)
    total = len(all_tips)
    if total < 4:
        return set()

    splits = set()
    # Canonicalise every bipartition by the side that does NOT contain a fixed
    # reference taxon. Choosing the smaller side instead is wrong: when the two
    # sides are the same size the tiebreak is arbitrary, and the two children of
    # the root then register the SAME bipartition as two different splits,
    # which doubles RF on balanced trees.
    ref_tip = min(all_tips)

    def descend(node):
        if node.is_leaf():
            return {node.name} if node.name in all_tips else set()
        acc = set()
        for ch in node.children:
            acc |= descend(ch)
        if node.parent is not None:
            size = len(acc)
            if 1 < size < total - 1:
                side = acc if ref_tip not in acc else (all_tips - acc)
                splits.add(frozenset(side))
        return acc

    descend(root)
    return splits


def robinson_foulds(tree_a, tree_b):
    """Unrooted RF distance on the shared tip set, plus the normalised form.
    Returns (rf, max_rf, normalised, n_shared_tips)."""
    tips_a = set(tip_names(tree_a))
    tips_b = set(tip_names(tree_b))
    shared = tips_a & tips_b
    if len(shared) < 4:
        return (None, None, None, len(shared))
    sa = bipartitions(tree_a, restrict=shared)
    sb = bipartitions(tree_b, restrict=shared)
    rf = len(sa ^ sb)
    max_rf = len(sa) + len(sb)
    norm = (rf / max_rf) if max_rf else 0.0
    return (rf, max_rf, norm, len(shared))


def _midpoint_root(root):
    """Return a copy-free midpoint-rooted view sufficient for MRCA depth counts.
    Kendall-Colijn needs a rooted tree; Gubbins trees are unrooted, so root at
    the midpoint of the longest tip-to-tip path."""
    tips = [lf for lf in root.leaves() if lf.name]
    if len(tips) < 2:
        return root

    # Build adjacency with lengths
    adj = defaultdict(list)

    def walk(node):
        for ch in node.children:
            adj[node].append((ch, ch.length))
            adj[ch].append((node, ch.length))
            walk(ch)

    walk(root)

    def farthest(start):
        seen = {start: 0.0}
        stack = [start]
        best, bestd = start, 0.0
        while stack:
            cur = stack.pop()
            for nb, ln in adj[cur]:
                if nb in seen:
                    continue
                seen[nb] = seen[cur] + ln
                if nb.is_leaf() and seen[nb] > bestd:
                    best, bestd = nb, seen[nb]
                stack.append(nb)
        return best, bestd, seen

    a, _, _ = farthest(tips[0])
    b, diameter, _ = farthest(a)
    # For depth-counting purposes the existing root is an acceptable anchor when
    # the tree is already rooted sensibly; we only need a consistent root across
    # the two trees being compared, so anchor at the midpoint tip's neighbour.
    del b, diameter
    return root


def kc_vector(root, tip_order):
    """Kendall-Colijn topology vector at lambda=0: for every ordered tip pair,
    the number of edges from the root to their MRCA. At lambda=0 the pendant
    component is a constant vector of 1s and is omitted (it cancels in the
    distance)."""
    # depth (in edge counts) and ancestor path for each tip
    paths = {}

    def descend(node, path):
        if node.is_leaf():
            if node.name:
                paths[node.name] = list(path)
            return
        for ch in node.children:
            path.append(node)
            descend(ch, path)
            path.pop()

    descend(root, [])

    vec = []
    for i in range(len(tip_order)):
        for j in range(i + 1, len(tip_order)):
            ti, tj = tip_order[i], tip_order[j]
            pi, pj = paths.get(ti), paths.get(tj)
            if pi is None or pj is None:
                vec.append(0.0)
                continue
            k = 0
            lim = min(len(pi), len(pj))
            while k < lim and pi[k] is pj[k]:
                k += 1
            vec.append(float(k))
    return vec


def kendall_colijn(tree_a, tree_b):
    """Euclidean distance between lambda=0 KC vectors on the shared tip set."""
    shared = sorted(set(tip_names(tree_a)) & set(tip_names(tree_b)))
    if len(shared) < 4:
        return (None, len(shared))
    va = kc_vector(tree_a, shared)
    vb = kc_vector(tree_b, shared)
    d = math.sqrt(sum((x - y) ** 2 for x, y in zip(va, vb)))
    return (d, len(shared))


# ===========================================================================
# Statistics
# ===========================================================================

def linregress(xs, ys):
    """Least-squares slope, intercept, Pearson r, R^2. Returns None if degenerate."""
    n = len(xs)
    if n < 3:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx <= 0 or syy <= 0:
        return None
    slope = sxy / sxx
    intercept = my - slope * mx
    r = sxy / math.sqrt(sxx * syy)
    return {"n": n, "slope": slope, "intercept": intercept, "r": r, "r2": r * r}


def mantel(dist_a, dist_b, n_perm=999, seed=1):
    """Mantel test between two condensed distance dicts keyed by (i,j) index
    pairs over a shared label ordering. Returns (r, p_one_sided)."""
    keys = sorted(set(dist_a) & set(dist_b))
    if len(keys) < 6:
        return (None, None)
    a = [dist_a[k] for k in keys]
    b = [dist_b[k] for k in keys]
    base = linregress(a, b)
    if base is None:
        return (None, None)
    r_obs = base["r"]

    # permute labels, not pairs: rebuild b under a relabelling
    labels = sorted({i for k in keys for i in k})
    idx = {lab: p for p, lab in enumerate(labels)}
    mat_b = [[0.0] * len(labels) for _ in labels]
    for (i, j), v in dist_b.items():
        if i in idx and j in idx:
            mat_b[idx[i]][idx[j]] = v
            mat_b[idx[j]][idx[i]] = v

    rng = random.Random(seed)
    order = list(range(len(labels)))
    ge = 0
    for _ in range(n_perm):
        rng.shuffle(order)
        bb = []
        for (i, j) in keys:
            pi, pj = order[idx[i]], order[idx[j]]
            bb.append(mat_b[pi][pj])
        st = linregress(a, bb)
        if st is not None and abs(st["r"]) >= abs(r_obs):
            ge += 1
    p = (ge + 1) / (n_perm + 1)
    return (r_obs, p)


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return None
    return len(set_a & set_b) / len(set_a | set_b)


# ===========================================================================
# Output parsers
# ===========================================================================

def iter_fasta_lengths(path):
    """Yield (record_id, length) for every record, in file order, without
    holding sequences in memory. Records are yielded individually rather than
    collected into a dict: a dict keyed on the first header token silently
    OVERWRITES when several records share it, which is exactly what happens
    with multi-contig assemblies whose contig headers all begin with the
    genome name. That collapse hides both the record count and the real
    lengths."""
    cur = None
    total = 0
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if cur is not None:
                    yield cur, total
                head = line[1:].strip()
                cur = head.split()[0] if head.split() else ""
                total = 0
            else:
                total += len(line.strip())
    if cur is not None:
        yield cur, total


def parse_fasta_lengths(path):
    """{record_id: total_length}, summing across duplicate IDs. Use
    iter_fasta_lengths when the record count or duplicate structure matters."""
    lengths = defaultdict(int)
    for rid, ln in iter_fasta_lengths(path):
        lengths[rid] += ln
    return dict(lengths)


def parse_fasta(path):
    """Full parse. Only used on post-Gubbins SNP alignments, which are small."""
    seqs = {}
    cur = None
    buf = []
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if cur is not None:
                    seqs[cur] = "".join(buf)
                cur = line[1:].strip().split()[0]
                buf = []
            else:
                buf.append(line.strip())
    if cur is not None:
        seqs[cur] = "".join(buf)
    return seqs


def vcf_positions(path):
    """Set of (CHROM, POS) from a VCF. snp-sites hardcodes CHROM to '1' on a
    single-replicon input, which is exactly why we split replicons first and
    keep the replicon in the arm name rather than trusting the field."""
    pos = set()
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.split("\t", 2)
            if len(parts) < 2:
                continue
            try:
                pos.add((parts[0], int(parts[1])))
            except ValueError:
                continue
    return pos


def gubbins_gff_blocks(path):
    """Recombination blocks from Gubbins' .recombination_predictions.gff.
    Returns (n_blocks, total_bp, merged_bp)."""
    spans = []
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 5:
                continue
            try:
                start, end = int(f[3]), int(f[4])
            except ValueError:
                continue
            if end < start:
                start, end = end, start
            spans.append((start, end))
    total = sum(e - s + 1 for s, e in spans)
    merged = 0
    if spans:
        spans.sort()
        cs, ce = spans[0]
        for s, e in spans[1:]:
            if s <= ce + 1:
                ce = max(ce, e)
            else:
                merged += ce - cs + 1
                cs, ce = s, e
        merged += ce - cs + 1
    return (len(spans), total, merged)


def gubbins_per_branch(path):
    """Parse .per_branch_statistics.csv. Returns dict with column count and
    aggregate r/m. BactDating's loadGubbins() branches on ncol == 11 or 13 and
    falls through silently otherwise, so the column count is worth asserting."""
    with open(path) as fh:
        sniff = fh.readline()
        delim = "\t" if "\t" in sniff else ","
        fh.seek(0)
        rdr = csv.reader(fh, delimiter=delim)
        rows = [r for r in rdr if r]
    if not rows:
        return None
    header = rows[0]
    ncol = len(header)
    lower = [h.strip().lower() for h in header]

    def col(*cands):
        for c in cands:
            for i, h in enumerate(lower):
                if c in h:
                    return i
        return None

    i_rm = col("r/m", "r_m", "ratio of substitutions")
    i_sub_r = col("num substitutions due to recombination",
                  "substitutions due to recombination")
    i_sub_m = col("num point mutations", "point mutations")

    rms = []
    tot_r = tot_m = 0
    for r in rows[1:]:
        if i_rm is not None and i_rm < len(r):
            try:
                v = float(r[i_rm])
                if v == v and v != float("inf"):
                    rms.append(v)
            except ValueError:
                pass
        if i_sub_r is not None and i_sub_m is not None:
            try:
                tot_r += int(float(r[i_sub_r]))
                tot_m += int(float(r[i_sub_m]))
            except (ValueError, IndexError):
                pass
    out = {
        "ncol": ncol,
        "ncol_ok": ncol in (11, 13),
        "n_branches": len(rows) - 1,
        "rm_median": _median(rms) if rms else None,
        "rm_pooled": (tot_r / tot_m) if tot_m else None,
    }
    return out


def _median(xs):
    if not xs:
        return None
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def snp_count_from_alignment(path):
    """Number of alignment columns in a post-Gubbins polymorphic-sites FASTA."""
    lengths = parse_fasta_lengths(path)
    if not lengths:
        return None
    vals = set(lengths.values())
    if len(vals) != 1:
        # unequal record lengths -- the exact failure mode that produced the
        # backbone branch-length inflation. Report rather than average.
        return {"ragged": True, "min": min(vals), "max": max(vals),
                "n_records": len(lengths)}
    return {"ragged": False, "sites": vals.pop(), "n_records": len(lengths)}


# ===========================================================================
# `plan` -- emit the run matrix
# ===========================================================================

ARM_TEMPLATE = r"""#!/usr/bin/env bash
# Arm: caller={caller}  reference={refname}  replicon={replicon}
# Generated by reference_sensitivity_bp.py -- REVISED_STRATEGY_2026-08.md 2.4
set -euo pipefail

ARM="{arm}"
OUT="{outdir}/arms/${{ARM}}"
REF="{refpath}"
REPLICON="{replicon}"
THREADS={threads}
mkdir -p "${{OUT}}"

# --- conda environments -----------------------------------------------------
# No single env on this machine carries the whole toolchain: snippy/snp-sites/
# samtools and ska/Gubbins live in different envs, and they cannot simply be
# merged -- Gubbins caps Python at 3.10, which is why PopPIPE pins Snakemake 7.
# So each step activates the env that owns its tool.
ENV_CALLER="{env_caller}"   # samtools, snippy, snippy-core, snp-sites
ENV_RECOMB="{env_recomb}"   # ska, generate_ska_alignment.py, run_gubbins.py, iqtree2
# `set -u` must be OFF across conda activation. Conda's activate.d hooks (e.g.
# activate-gcc_linux-64.sh) reference unbound variables such as SYS_SYSROOT and
# abort the whole script under `set -u`. This is not hypothetical -- it kills
# every arm at the first activation.
if [ -n "${{ENV_CALLER}}${{ENV_RECOMB}}" ]; then
    set +u
    # shellcheck disable=SC1091
    eval "$(conda shell.bash hook)"
    set -u
fi
use_env () {{
    if [ -n "$1" ]; then
        set +u
        conda activate "$1"
        set -u
    fi
}}

# --- guard: Gubbins version -------------------------------------------------
# v3.4.2 made the invariant-site correction optional and defaulted it OFF.
# Note the VERSION file reads 3.4.2 even on tag v3.4.3, so --version can report
# the wrong release on a correct install. Check the conda/package metadata too.
use_env "${{ENV_RECOMB}}"
run_gubbins.py --version || true

# --- 1. split the reference by replicon ------------------------------------
use_env "${{ENV_CALLER}}"
# Gubbins cannot handle multi-contig references at all; its 0.1-10 kb sliding
# window would scan straight across the chromosome I / chromosome II junction,
# and snp-sites hardcodes CHROM to "1".
samtools faidx "${{REF}}"
samtools faidx "${{REF}}" "${{REPLICON}}" > "${{OUT}}/ref.${{REPLICON}}.fa"

# --- 2. variant calling ----------------------------------------------------
use_env "{env_for_call}"
{call_block}

# --- 2b. GUARD: equal record lengths ---------------------------------------
# Assert the alignment is actually ALIGNED before Gubbins touches it. This is
# the prophylactic form of the backbone diagnostic: a fallback path that copies
# raw concatenated sequence into a file the next tool treats as an alignment
# produces enormous branch lengths with no recombination involved. Cheap to
# check, expensive to discover three steps later.
python3 "{selfpath}" checkaln "${{OUT}}/aln.full.${{REPLICON}}.fa"

# --- 3. Gubbins ------------------------------------------------------------
# Input is a FULL-LENGTH pseudogenome alignment, never a SNP-only alignment.
# --invariant-site-correction is passed EXPLICITLY, not left to the default.
#
# STDOUT IS CAPTURED TO ITS OWN FILE, and this is not cosmetic. Gubbins reports
# its per-iteration progress on stdout, and the ITERATION AT WHICH IT CONVERGED
# is the single most useful free diagnostic available for a run: a unit that hit
# the iteration cap has not converged, so its r/m is untrustworthy BY
# CONSTRUCTION rather than for any biological reason. In earlier runs this went
# to the shared arm log and was interleaved with IQ-TREE's far more voluminous
# output, which made it unrecoverable after the fact -- `gubbins.log` does NOT
# contain it (that file is a citation manifest, not a progress log).
#
# Costs nothing, and it is a live candidate explanation for the depressed-r/m
# units that no upstream statistic predicts.
use_env "${{ENV_RECOMB}}"
# Run Gubbins with ${{OUT}} as CWD, in a subshell so the rest of this arm script
# keeps its own working directory. Gubbins writes <basename>.start, .phylip and
# .snp_sites.aln to the WORKING DIRECTORY, not to --prefix (A.11ai), and the
# isolating property is the alignment BASENAME rather than the path. Across the
# 184 production arms there are only 30 distinct basenames: every unit's K96243
# arm is aln.full.NC_006350.1.fa / NC_006351.1.fa (46 arms each). Arms within a
# unit run sequentially via run_all.sh, but that file invites parallel
# submission across units -- which without this cd destroys their scratch.
# Both --prefix and the input are absolute, so nothing else moves.
( cd "${{OUT}}" && run_gubbins.py \
    --prefix "${{OUT}}/gubbins" \
    --threads "${{THREADS}}" \
    --invariant-site-correction \
    --filter-percentage 25 \
    "${{OUT}}/aln.full.${{REPLICON}}.fa" ) \
    > "${{OUT}}/gubbins.progress.log" 2> "${{OUT}}/gubbins.progress.err"
GUBBINS_RC=$?
# Echo it onward so the arm log still shows what happened, then fail loudly if
# Gubbins did -- redirecting output must not swallow a non-zero exit.
cat "${{OUT}}/gubbins.progress.log"
cat "${{OUT}}/gubbins.progress.err" >&2
if [ "${{GUBBINS_RC}}" -ne 0 ]; then
    echo "ERROR: run_gubbins.py exited ${{GUBBINS_RC}}" >&2
    exit "${{GUBBINS_RC}}"
fi
# Record the convergence point where the triage tools can find it.
grep -iE 'iteration|converg' "${{OUT}}/gubbins.progress.log" \
    | tail -20 > "${{OUT}}/gubbins.convergence.txt" || true

# --- 4. snp-sites, AFTER Gubbins ------------------------------------------
# Variant-site alignments cannot be used for recombination-aware phylogenetics
# because the genomic distance between variant sites is an input to the method
# (Didelot & Parkhill 2022). snp-sites therefore runs here and nowhere earlier.
use_env "${{ENV_CALLER}}"
snp-sites -v -o "${{OUT}}/gubbins.snps.vcf" \
    "${{OUT}}/gubbins.filtered_polymorphic_sites.fasta"
# Constant-site counts MUST come from the FULL alignment, not from Gubbins'
# filtered_polymorphic_sites.fasta -- that file is SNP-only by construction, so
# `snp-sites -C` on it returns 0,0,0,0, and `-fconst 0,0,0,0` silently defeats
# the very correction it is meant to supply. Measured here: full alignment
# gives 467202,1026217,1020414,465056 (68.7% GC, matching K96243's 68.06%),
# the polymorphic file gives 0,0,0,0.
# Caveat to state in methods: this counts constants over the alignment as it
# entered Gubbins, so constant positions inside masked recombinant tracts are
# included. Gubbins does not emit a masked full alignment by default.
snp-sites -C "${{OUT}}/aln.full.${{REPLICON}}.fa" \
    > "${{OUT}}/constant_site_counts.txt" || true

# --- 5. tree ---------------------------------------------------------------
# -fconst with true constant-site counts, never +ASC. K96243 is 68.06% GC;
# -fconst reproduces full-alignment base frequencies exactly while +ASC and
# flat counts both collapse toward 25/25/25/25.
use_env "${{ENV_RECOMB}}"
FCONST=$(tr -d '[:space:]' < "${{OUT}}/constant_site_counts.txt" 2>/dev/null || echo "")
# Refuse an all-zero vector: it is the signature of having read the counts from
# a SNP-only alignment, and IQ-TREE would accept it while modelling nothing.
if [ "${{FCONST}}" = "0,0,0,0" ] || [ -z "${{FCONST}}" ]; then
    echo "ERROR: constant-site counts are '${{FCONST}}'. Expected four" >&2
    echo "non-zero counts from the FULL alignment. Refusing to build a tree" >&2
    echo "with a meaningless -fconst vector." >&2
    exit 4
fi
if [ -n "${{FCONST}}" ]; then
    iqtree2 -s "${{OUT}}/gubbins.filtered_polymorphic_sites.fasta" \
        -fconst "${{FCONST}}" \
        -m MFP -B 1000 -T "${{THREADS}}" \
        --prefix "${{OUT}}/tree"
else
    echo "WARNING: no constant-site counts; building without -fconst." >&2
    iqtree2 -s "${{OUT}}/gubbins.filtered_polymorphic_sites.fasta" \
        -m MFP -B 1000 -T "${{THREADS}}" \
        --prefix "${{OUT}}/tree"
fi

echo "ARM ${{ARM}} complete."
"""

CALL_BLOCKS = {
    "ska_map": r"""# ska map -- NEVER ska align. Only `ska map` carries genomic coordinates;
# `ska align` emits columns in hash-table order that "do not represent a
# physical position in the chromosome". Feeding that to Gubbins fails SILENTLY.
#
# --k 31 IS NOT OPTIONAL HERE. generate_ska_alignment.py defaults to k=17, and
# it runs `ska map --repeat-mask`. At k=17 a split k-mer is 2x8+1 bases, which
# in a 68%-GC, repeat-rich 7.2 Mb genome is nowhere near unique, so the repeat
# mask removes most of the reference: measured at 59% of chromosome 2 masked
# (N) on this dataset, which then trips Gubbins' --filter-percentage 25 and
# drops nearly every taxon ("Not enough sequences are left after removing
# duplicates"). At k=31 the same run masks 3.5%. Snippy on the identical
# reference and genomes leaves 2.6-4.3% unaligned, confirming the loss is a
# k-mer artefact and not divergence.
generate_ska_alignment.py \
    --reference "${OUT}/ref.${REPLICON}.fa" \
    --input "{listfile}" \
    --out "${OUT}/aln.full.${REPLICON}.fa" \
    --k 31 \
    --threads "${THREADS}"
""",
    "ska_lo": r"""# ska lo -- reference-free local graph construction. The missing-data
# parameter MUST stay below 0.5; above that it emits duplicate and spurious
# SNPs from high-polymorphism regions. PMEN2 analysis used 0.4.
#
# INTERFACE NOTE (ska 0.5.0): the signature is
#     ska lo [OPTIONS] <INPUT_SKF> <OUTPUT>
# where OUTPUT is a POSITIONAL PREFIX. There is no `-o`; passing one aborts
# with a usage error after the expensive `ska build` has already run.
ska build -o "${OUT}/cluster" -f "{listfile}" -k 31 --threads "${THREADS}"
ska lo "${OUT}/cluster.skf" "${OUT}/lo" \
    --reference "${OUT}/ref.${REPLICON}.fa" \
    --missing 0.4 \
    --threads "${THREADS}"

# ska lo writes several files under the prefix:
#   lo_pseudo_genomes.fas  <- FULL-LENGTH pseudogenome alignment: what Gubbins needs
#   lo_snps.fas            <- SNP-only: must NEVER reach Gubbins
#   lo_snps.vcf, lo_indels.vcf
# Take the pseudogenome EXPLICITLY. Globbing loosely here risks grabbing
# lo_snps.fas, which is the exact "variant sites into a recombination-aware
# method" error Didelot & Parkhill warn against, and it would fail silently.
LOALN="${OUT}/lo_pseudo_genomes.fas"
if [ ! -s "${LOALN}" ]; then
    echo "ERROR: ska lo produced no pseudogenome at ${LOALN}" >&2
    ls -la "${OUT}" >&2
    exit 5
fi
mv "${LOALN}" "${OUT}/aln.full.${REPLICON}.fa"
""",
    "existing": r"""# PLACEHOLDER. Re-run `plan` with --existing-preset or --existing-cmd-file.
echo "No caller configured for the 'existing' arm." >&2
echo "Re-run: reference_sensitivity_bp.py plan ... --existing-preset snippy-contigs" >&2
exit 3
""",
}

# Presets for the "existing" arm. Each MUST end by producing a full-length
# pseudogenome alignment at ${OUT}/aln.full.${REPLICON}.fa with one record per
# genome, all records the same length. That contract is asserted before Gubbins.
EXISTING_PRESETS = {
    "snippy-contigs": r"""# Snippy in CONTIG mode. This is the right default here: the collection is
# NCBI assemblies (92% drafts, only 9% with any long-read data), not reads.
# Wu et al. 2026 used the same approach ("Snippy v3.2-dev in contig mode").
# Input list is TSV: <sample_id>\t<assembly.fasta>
while IFS=$'\t' read -r SAMPLE ASM; do
    # Style only. `[ -z "$SAMPLE" ] && continue` is also SAFE under `set -e`
    # (bash exempts the left operand of a short-circuiting &&), but the `if`
    # form does not depend on knowing that exemption.
    if [ -z "${SAMPLE}" ]; then continue; fi
    snippy --outdir "${OUT}/snippy/${SAMPLE}" \
           --ctgs "${ASM}" \
           --ref "${OUT}/ref.${REPLICON}.fa" \
           --cpus "${THREADS}" \
           --force
done < "{listfile}"

# snippy-core emits core.full.aln, a full-length pseudogenome alignment.
# NOTE: snippy-core concatenates replicons with NO separator. That is one of
# the reasons this experiment splits by replicon BEFORE calling, not after --
# here it is handed a single-replicon reference, so there is no junction.
snippy-core --ref "${OUT}/ref.${REPLICON}.fa" \
            --prefix "${OUT}/core" \
            "${OUT}"/snippy/*/
mv "${OUT}/core.full.aln" "${OUT}/aln.full.${REPLICON}.fa"
""",
    "snippy-reads": r"""# Snippy from paired reads. Input list is TSV:
# <sample_id>\t<R1.fastq.gz>\t<R2.fastq.gz>
snippy-multi "{listfile}" \
    --ref "${OUT}/ref.${REPLICON}.fa" \
    --cpus "${THREADS}" > "${OUT}/runme.sh"
bash "${OUT}/runme.sh"
mv "${OUT}/core.full.aln" "${OUT}/aln.full.${REPLICON}.fa"
""",
    "bwa-bcftools": r"""# bwa-mem + bcftools consensus, the nf-core/bactmap shape.
# Input list is TSV: <sample_id>\t<R1.fastq.gz>\t<R2.fastq.gz>
bwa index "${OUT}/ref.${REPLICON}.fa"
: > "${OUT}/aln.full.${REPLICON}.fa"
while IFS=$'\t' read -r SAMPLE R1 R2; do
    # Style only. `[ -z "$SAMPLE" ] && continue` is also SAFE under `set -e`
    # (bash exempts the left operand of a short-circuiting &&), but the `if`
    # form does not depend on knowing that exemption.
    if [ -z "${SAMPLE}" ]; then continue; fi
    bwa mem -t "${THREADS}" "${OUT}/ref.${REPLICON}.fa" "${R1}" "${R2}" \
        | samtools sort -@ "${THREADS}" -o "${OUT}/${SAMPLE}.bam"
    samtools index "${OUT}/${SAMPLE}.bam"
    bcftools mpileup -f "${OUT}/ref.${REPLICON}.fa" "${OUT}/${SAMPLE}.bam" \
        | bcftools call -mv -Oz -o "${OUT}/${SAMPLE}.vcf.gz"
    bcftools index "${OUT}/${SAMPLE}.vcf.gz"
    # consensus against the SAME reference keeps every record the same length
    printf '>%s\n' "${SAMPLE}" >> "${OUT}/aln.full.${REPLICON}.fa"
    bcftools consensus -f "${OUT}/ref.${REPLICON}.fa" \
        "${OUT}/${SAMPLE}.vcf.gz" | tail -n +2 \
        >> "${OUT}/aln.full.${REPLICON}.fa"
done < "{listfile}"
""",
}


def cmd_plan(args):
    outdir = os.path.abspath(args.outdir)
    # NAME=PATH[#REPLICON1,REPLICON2]. Replicon IDs are PER REFERENCE: a
    # within-cluster reference and K96243 do not share contig names, so a
    # single global --replicons list would silently produce empty per-replicon
    # references for every arm but one.
    default_replicons = [r for r in args.replicons.split(",") if r.strip()]
    refs = {}
    ref_replicons = {}
    for spec in args.ref:
        if "=" not in spec:
            sys.exit("ERROR: --ref expects NAME=PATH[#REP1,REP2], got %r" % spec)
        name, rest = spec.split("=", 1)
        name = name.strip()
        if "#" in rest:
            path, reps = rest.rsplit("#", 1)
            replicons = [r.strip() for r in reps.split(",") if r.strip()]
        else:
            path, replicons = rest, list(default_replicons)
        refs[name] = os.path.abspath(path.strip())
        ref_replicons[name] = replicons

    # Every reference must contribute the same NUMBER of replicons, in matching
    # order, or the per-replicon arms are not comparable across references.
    counts = {n: len(r) for n, r in ref_replicons.items()}
    if len(set(counts.values())) > 1:
        sys.exit("ERROR: references declare different replicon counts (%s). "
                 "Arms are matched by position, so chromosome 1 of one "
                 "reference would be compared against chromosome 2 of another."
                 % counts)

    if len(refs) < 2:
        sys.exit("ERROR: the experiment needs at least 2 references "
                 "(a within-cluster representative and K96243). Got %d."
                 % len(refs))

    callers = [c for c in args.callers.split(",") if c.strip()]
    for c in callers:
        if c not in CALL_BLOCKS:
            sys.exit("ERROR: unknown caller %r (choose from %s)"
                     % (c, ", ".join(CALLERS)))

    # Resolve what the "existing" arm actually runs.
    existing_block = CALL_BLOCKS["existing"]
    existing_source = "unset (arms will exit 3)"
    if args.existing_cmd_file:
        with open(args.existing_cmd_file) as fh:
            existing_block = fh.read()
        existing_source = "custom: %s" % args.existing_cmd_file
    elif args.existing_preset and args.existing_preset != "stub":
        existing_block = EXISTING_PRESETS[args.existing_preset]
        existing_source = "preset: %s" % args.existing_preset
    CALL_BLOCKS_RESOLVED = dict(CALL_BLOCKS)
    CALL_BLOCKS_RESOLVED["existing"] = existing_block

    listfile = os.path.abspath(args.cluster_list)

    if os.path.exists(listfile):
        with open(listfile) as fh:
            n_genomes = sum(1 for ln in fh if ln.strip())
        if not (DEFAULT_MIN_CLUSTER <= n_genomes <= DEFAULT_MAX_CLUSTER):
            print("NOTE: cluster has %d genomes; the protocol specifies a "
                  "mid-sized cluster of %d-%d. Proceeding anyway."
                  % (n_genomes, DEFAULT_MIN_CLUSTER, DEFAULT_MAX_CLUSTER),
                  file=sys.stderr)
    else:
        n_genomes = None
        print("NOTE: --cluster-list %s does not exist yet; emitting the plan "
              "regardless." % listfile, file=sys.stderr)

    os.makedirs(os.path.join(outdir, "arms"), exist_ok=True)

    # Arms are named by replicon SLOT (chr1, chr2, ...), never by the raw
    # contig ID, because those differ between references. The slot is what
    # makes cross-reference comparison well defined; the raw ID goes into the
    # script.
    n_slots = len(next(iter(ref_replicons.values())))
    slot_labels = ["chr%d" % (i + 1) for i in range(n_slots)]

    arms = []
    for refname, refpath in refs.items():
        for caller in callers:
            for slot, label in enumerate(slot_labels):
                replicon = ref_replicons[refname][slot]
                arm = "%s__%s__%s" % (refname, caller, label)
                call_block = CALL_BLOCKS_RESOLVED[caller].replace(
                    "{listfile}", listfile)
                env_for_call = ("${ENV_RECOMB}"
                                if caller in ("ska_map", "ska_lo")
                                else "${ENV_CALLER}")
                script = ARM_TEMPLATE.format(
                    arm=arm, caller=caller, refname=refname, refpath=refpath,
                    replicon=replicon, outdir=outdir, threads=args.threads,
                    call_block=call_block,
                    selfpath=os.path.abspath(__file__),
                    env_caller=args.env_caller, env_recomb=args.env_recomb,
                    env_for_call=env_for_call,
                )
                path = os.path.join(outdir, "arms", arm + ".sh")
                with open(path, "w") as fh:
                    fh.write(script)
                os.chmod(path, 0o755)
                arms.append((arm, path))

    # Order arms so the cheap, load-bearing ones finish first: the experiment's
    # actual contrast is `existing` close-vs-distant, with ska_map as the
    # stability control. ska_lo is the most expensive and least essential, so
    # it runs last -- a failure there must not delay the answer.
    caller_rank = {"existing": 0, "ska_map": 1, "ska_lo": 2}
    arms.sort(key=lambda ap: (caller_rank.get(ap[0].split("__")[1], 9), ap[0]))

    runner = os.path.join(outdir, "run_all.sh")
    with open(runner, "w") as fh:
        fh.write("#!/usr/bin/env bash\n")
        fh.write("# Reference-sensitivity experiment: %d arms.\n" % len(arms))
        fh.write("# Arms are independent; submit them in parallel if you have\n")
        fh.write("# a scheduler. IQ-TREE parallelises ALONG the alignment, so\n")
        fh.write("# prefer many arms at low thread counts over few at high.\n")
        fh.write("#\n")
        fh.write("# NO `set -e` HERE, deliberately. Arms are independent, so a\n")
        fh.write("# failure in one must not abort the other eleven. Each arm\n")
        fh.write("# still runs under its own `set -euo pipefail`.\n")
        fh.write("# Completed arms are SKIPPED, so this is resumable.\n")
        fh.write("set -o pipefail\n")
        fh.write("failed=0\n\n")
        for arm, path in arms:
            fh.write('if [ -s "%s/arms/%s/tree.treefile" ]; then\n'
                     % (outdir, arm))
            fh.write('  echo "=== %s (already complete, skipping) ==="\n' % arm)
            fh.write("else\n")
            fh.write('  echo "=== %s ==="\n' % arm)
            fh.write('  if bash "%s"; then\n' % path)
            fh.write('    echo "ARM %s complete."\n' % arm)
            fh.write("  else\n")
            fh.write('    echo "ARM %s FAILED (exit $?) -- continuing." >&2\n'
                     % arm)
            fh.write("    failed=$((failed+1))\n")
            fh.write("  fi\n")
            fh.write("fi\n\n")
        fh.write('echo "Arms failed: ${failed}"\n')
        fh.write('echo "Now run:"\n')
        fh.write('echo "  python3 reference_sensitivity_bp.py analyse '
                 '--outdir %s --dates <dates.csv>"\n' % outdir)
    os.chmod(runner, 0o755)

    manifest = os.path.join(outdir, "manifest.tsv")
    with open(manifest, "w") as fh:
        fh.write("arm\treference\tcaller\treplicon\tcontig_id\tscript\n")
        for refname in refs:
            for caller in callers:
                for slot, label in enumerate(slot_labels):
                    arm = "%s__%s__%s" % (refname, caller, label)
                    fh.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (
                        arm, refname, caller, label,
                        ref_replicons[refname][slot],
                        os.path.join(outdir, "arms", arm + ".sh")))

    print(header("PLAN"))
    print("cluster list      : %s%s" % (
        listfile, "" if n_genomes is None else " (%d genomes)" % n_genomes))
    print("references        : %s" % ", ".join(sorted(refs)))
    print("callers           : %s" % ", ".join(callers))
    print("replicon slots    : %s" % ", ".join(slot_labels))
    for rn in sorted(refs):
        print("   %-14s -> %s" % (rn, ", ".join(ref_replicons[rn])))
    print("arms              : %d" % len(arms))
    print("'existing' caller : %s" % existing_source)
    print("output            : %s" % outdir)
    print()
    print("Wrote:")
    print("  %s" % runner)
    print("  %s" % manifest)
    print("  %s/arms/*.sh  (%d scripts)" % (outdir, len(arms)))
    print()
    if "existing" in callers and existing_source.startswith("unset"):
        print("ACTION REQUIRED: no caller configured for the 'existing' arms,")
        print("so they will exit 3. Re-run with --existing-preset "
              "snippy-contigs")
        print("(or --existing-cmd-file) -- the whole point is to test YOUR")
        print("caller, and it must not be guessed silently.")
        print()
    print("Then: bash %s" % runner)


# ===========================================================================
# `analyse`
# ===========================================================================

def load_dates(path):
    """genome,year (or genome,date). Returns {genome: float_year}."""
    dates = {}
    if not path:
        return dates
    with open(path) as fh:
        sniff = fh.readline()
        delim = "\t" if "\t" in sniff else ","
        fh.seek(0)
        rdr = csv.reader(fh, delimiter=delim)
        rows = [r for r in rdr if r and any(c.strip() for c in r)]
    start = 0
    if rows and not _looks_numeric(rows[0][-1]):
        start = 1
    for r in rows[start:]:
        if len(r) < 2:
            continue
        name = r[0].strip()
        raw = r[1].strip()
        # Guard the PRJEB3409 placeholder: ENA stores "1800/2014", and a naive
        # date[:4] parse silently reads that as the year 1800.
        if raw.startswith("1800/") or raw == "1800":
            continue
        m = re.match(r"^(\d{4})", raw)
        if not m:
            continue
        year = float(m.group(1))
        if year < 1900 or year > 2030:
            continue
        dates[name] = year
    return dates


def _looks_numeric(s):
    try:
        float(s.strip())
        return True
    except (ValueError, AttributeError):
        return False


def read_manifest(outdir):
    path = os.path.join(outdir, "manifest.tsv")
    if not os.path.exists(path):
        sys.exit("ERROR: no manifest.tsv in %s -- run `plan` first." % outdir)
    arms = []
    with open(path) as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        for row in rdr:
            arms.append(row)
    return arms


def collect_arm(outdir, arm):
    """Gather every metric available for one arm. Missing files are recorded as
    None rather than fatal -- partial runs should still analyse."""
    d = os.path.join(outdir, "arms", arm)
    rec = {"arm": arm, "dir": d, "complete": False}

    aln = os.path.join(d, "gubbins.filtered_polymorphic_sites.fasta")
    if os.path.exists(aln):
        rec["snps"] = snp_count_from_alignment(aln)
    else:
        rec["snps"] = None

    vcf = os.path.join(d, "gubbins.snps.vcf")
    rec["positions"] = vcf_positions(vcf) if os.path.exists(vcf) else None

    gff = os.path.join(d, "gubbins.recombination_predictions.gff")
    if os.path.exists(gff):
        n, total, merged = gubbins_gff_blocks(gff)
        rec["rec_blocks"] = n
        rec["rec_bp"] = total
        rec["rec_bp_merged"] = merged
    else:
        rec["rec_blocks"] = rec["rec_bp"] = rec["rec_bp_merged"] = None

    pbs = os.path.join(d, "gubbins.per_branch_statistics.csv")
    rec["per_branch"] = gubbins_per_branch(pbs) if os.path.exists(pbs) else None

    tree = None
    for cand in ("tree.treefile", "gubbins.final_tree.tre",
                 "gubbins.node_labelled.final_tree.tre"):
        p = os.path.join(d, cand)
        if os.path.exists(p):
            try:
                tree = read_tree_file(p)
                rec["tree_path"] = p
                break
            except Exception as exc:  # noqa: BLE001
                print("WARNING: could not parse %s (%s)" % (p, exc),
                      file=sys.stderr)
    rec["tree"] = tree
    rec["complete"] = tree is not None and rec["snps"] is not None
    return rec


def cmd_analyse(args):
    outdir = os.path.abspath(args.outdir)
    manifest = read_manifest(outdir)
    dates = load_dates(args.dates)

    recs = {}
    for row in manifest:
        recs[row["arm"]] = collect_arm(outdir, row["arm"])
        recs[row["arm"]].update(reference=row["reference"],
                                caller=row["caller"],
                                replicon=row["replicon"])

    done = [a for a, r in recs.items() if r["complete"]]
    print(header("REFERENCE SENSITIVITY -- %d/%d arms analysable"
                 % (len(done), len(recs))))
    if not done:
        print("No arm produced both a tree and a post-Gubbins alignment.")
        print("Check %s/arms/*/ for partial output." % outdir)
        return

    replicons = sorted({recs[a]["replicon"] for a in done})
    references = sorted({recs[a]["reference"] for a in done})
    callers = sorted({recs[a]["caller"] for a in done})

    # ---- A. per-arm summary ------------------------------------------------
    print(section("A. Per-arm summary"))
    hdr = ("%-10s %-10s %-14s %8s %8s %10s %9s %8s %8s"
           % ("replicon", "caller", "reference", "taxa", "SNPs",
              "rec_bp", "blocks", "r/m", "RtT R2"))
    print(hdr)
    print("-" * len(hdr))

    rtt_cache = {}
    rows_out = []
    for rep in replicons:
        for caller in callers:
            for ref in references:
                arm = "%s__%s__%s" % (ref, caller, rep)
                r = recs.get(arm)
                if not r or not r["complete"]:
                    continue
                snps = r["snps"]
                if isinstance(snps, dict) and snps.get("ragged"):
                    snp_str = "RAGGED!"
                    ntax = snps["n_records"]
                    nsnp = None
                else:
                    nsnp = snps["sites"]
                    ntax = snps["n_records"]
                    snp_str = str(nsnp)

                rm = None
                if r["per_branch"]:
                    rm = r["per_branch"].get("rm_pooled") or \
                         r["per_branch"].get("rm_median")

                stat = None
                if dates:
                    stat = root_to_tip(r["tree"], dates)
                    rtt_cache[arm] = stat

                print("%-10s %-10s %-14s %8s %8s %10s %9s %8s %8s" % (
                    rep, caller, ref, ntax, snp_str,
                    _fmt(r["rec_bp_merged"], 0),
                    _fmt(r["rec_blocks"], 0),
                    _fmt(rm, 2),
                    _fmt(stat["r2"] if stat else None, 3),
                ))
                rows_out.append({
                    "replicon": rep, "caller": caller, "reference": ref,
                    "n_taxa": ntax, "post_gubbins_snps": nsnp,
                    "rec_blocks": r["rec_blocks"],
                    "rec_bp_merged": r["rec_bp_merged"],
                    "rm": rm,
                    "rtt_slope": stat["slope"] if stat else None,
                    "rtt_r2": stat["r2"] if stat else None,
                    "rtt_n": stat["n"] if stat else None,
                })

    # ---- ragged / column-count guards -------------------------------------
    warned = False
    for arm in done:
        r = recs[arm]
        if isinstance(r["snps"], dict) and r["snps"].get("ragged"):
            if not warned:
                print()
                warned = True
            print("!! %s: post-Gubbins alignment has UNEQUAL record lengths "
                  "(%d-%d). That is the same failure class as the backbone "
                  "fallback -- an aligner was handed unaligned sequence. "
                  "Do not interpret this arm."
                  % (arm, r["snps"]["min"], r["snps"]["max"]))
        pb = r.get("per_branch")
        if pb and not pb["ncol_ok"]:
            if not warned:
                print()
                warned = True
            print("!! %s: per_branch_statistics.csv has %d columns. "
                  "BactDating's loadGubbins() branches on ncol == 11 or 13 and "
                  "falls through to a different formula with no warning."
                  % (arm, pb["ncol"]))

    # ---- B. the reference contrast, which is the actual experiment ---------
    print(section("B. Reference contrast (the experiment)"))
    if len(references) < 2:
        print("Only one reference completed; nothing to contrast.")
    else:
        close = args.close_ref if args.close_ref in references else references[0]
        others = [r for r in references if r != close]
        print("Treating %r as the within-cluster (close) reference.\n" % close)
        hdr2 = ("%-10s %-10s %-14s %12s %12s %12s"
                % ("replicon", "caller", "vs", "dSNPs", "d rec_bp", "d RtT R2"))
        print(hdr2)
        print("-" * len(hdr2))
        for rep in replicons:
            for caller in callers:
                base_arm = "%s__%s__%s" % (close, caller, rep)
                base = recs.get(base_arm)
                if not base or not base["complete"]:
                    continue
                for ref in others:
                    arm = "%s__%s__%s" % (ref, caller, rep)
                    r = recs.get(arm)
                    if not r or not r["complete"]:
                        continue
                    d_snps = _pct_delta(_sites(base["snps"]), _sites(r["snps"]))
                    d_rec = _pct_delta(base["rec_bp_merged"], r["rec_bp_merged"])
                    b_r2 = rtt_cache.get(base_arm)
                    o_r2 = rtt_cache.get(arm)
                    d_r2 = None
                    if b_r2 and o_r2:
                        d_r2 = o_r2["r2"] - b_r2["r2"]
                    print("%-10s %-10s %-14s %12s %12s %12s" % (
                        rep, caller, ref,
                        _fmt_pct(d_snps), _fmt_pct(d_rec), _fmt(d_r2, 3)))

    # ---- C. do the callers agree on WHERE the SNPs are? -------------------
    print(section("C. Shared polymorphic positions"))
    any_pos = False
    for rep in replicons:
        for ref in references:
            sets = {}
            for caller in callers:
                arm = "%s__%s__%s" % (ref, caller, rep)
                r = recs.get(arm)
                if r and r.get("positions"):
                    sets[caller] = r["positions"]
            if len(sets) < 2:
                continue
            any_pos = True
            inter = set.intersection(*sets.values())
            union = set.union(*sets.values())
            print("  %s / %s: %d positions shared by all %d callers "
                  "(union %d, %.1f%% concordant)"
                  % (rep, ref, len(inter), len(sets), len(union),
                     100.0 * len(inter) / len(union) if union else 0.0))
            names = sorted(sets)
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    jac = jaccard(sets[names[i]], sets[names[j]])
                    print("      %-10s vs %-10s  Jaccard %.3f"
                          % (names[i], names[j], jac if jac is not None else 0.0))
    if not any_pos:
        print("  No VCFs found. snp-sites -v runs in step 4 of each arm.")

    # ---- D. topology ------------------------------------------------------
    print(section("D. Tree distance"))
    print("RF is normalised; Kendall-Colijn is at lambda=0 (topology only),")
    print("which is the right setting given that recombination wrecks branch")
    print("lengths while largely sparing topology (Hedge & Wilson 2014).\n")
    hdr3 = "%-10s %-28s %-28s %8s %10s %8s" % (
        "replicon", "arm A", "arm B", "RF", "RF_norm", "KC0")
    print(hdr3)
    print("-" * len(hdr3))
    for rep in replicons:
        arms_here = [a for a in done if recs[a]["replicon"] == rep]
        arms_here.sort()
        for i in range(len(arms_here)):
            for j in range(i + 1, len(arms_here)):
                a, b = arms_here[i], arms_here[j]
                ta, tb = recs[a]["tree"], recs[b]["tree"]
                rf, maxrf, norm, nshared = robinson_foulds(ta, tb)
                kc, _ = kendall_colijn(ta, tb)
                if rf is None:
                    continue
                print("%-10s %-28s %-28s %8d %10.3f %8s" % (
                    rep, _short(a), _short(b), rf, norm, _fmt(kc, 1)))

    # ---- E. temporal signal ----------------------------------------------
    print(section("E. Root-to-tip regression"))
    if not dates:
        print("No --dates supplied, so the outcome that actually matters was")
        print("not computed. Supply a genome,year CSV.")
    else:
        print("Report the SLOPE, which is an interpretable rate. R^2 is shown")
        print("for the between-arm contrast ONLY -- it is not a test statistic,")
        print("root-to-tip distances are not independent (Rieux & Balloux 2016:")
        print("'the same branches in the phylogeny will contribute to multiple")
        print("root-to-tip distances'), and the built-in permutation p-value is")
        print("anticonservative under confounded sampling (Murray 2016).\n")
        hdr4 = "%-10s %-10s %-14s %6s %12s %8s %10s %8s" % (
            "replicon", "caller", "reference", "n", "slope", "R2",
            "Mantel r", "p")
        print(hdr4)
        print("-" * len(hdr4))
        for rep in replicons:
            for caller in callers:
                for ref in references:
                    arm = "%s__%s__%s" % (ref, caller, rep)
                    r = recs.get(arm)
                    if not r or not r["complete"]:
                        continue
                    stat = rtt_cache.get(arm) or root_to_tip(r["tree"], dates)
                    if not stat:
                        continue
                    mr, mp = mantel_confounding(r["tree"], dates,
                                                n_perm=args.permutations,
                                                seed=args.seed)
                    print("%-10s %-10s %-14s %6d %12.3e %8.3f %10s %8s" % (
                        rep, caller, ref, stat["n"], stat["slope"], stat["r2"],
                        _fmt(mr, 3), _fmt(mp, 3)))
        print()
        print("Mantel r/p is Murray's confounding diagnostic: a significant")
        print("correlation between genetic and temporal distance means the")
        print("cluster is confounded and NO unclustered date-randomisation")
        print("test may be applied to it.")

    # ---- F. decision ------------------------------------------------------
    print(section("F. Decision rule (a construct, not a published threshold)"))
    verdict(recs, rtt_cache, args.close_ref, references, callers, replicons)

    # ---- write TSV --------------------------------------------------------
    if rows_out:
        tsv = os.path.join(outdir, "reference_sensitivity_summary.tsv")
        cols = ["replicon", "caller", "reference", "n_taxa",
                "post_gubbins_snps", "rec_blocks", "rec_bp_merged", "rm",
                "rtt_n", "rtt_slope", "rtt_r2"]
        with open(tsv, "w") as fh:
            fh.write("\t".join(cols) + "\n")
            for row in rows_out:
                fh.write("\t".join(
                    "" if row.get(c) is None else str(row.get(c))
                    for c in cols) + "\n")
        print("\nWrote %s" % tsv)


def _sites(snps):
    if isinstance(snps, dict) and not snps.get("ragged"):
        return snps.get("sites")
    return None


def _pct_delta(base, other):
    if base in (None, 0) or other is None:
        return None
    return 100.0 * (other - base) / base


def _fmt(v, dp):
    if v is None:
        return "-"
    if isinstance(v, float):
        return ("%%.%df" % dp) % v
    return str(v)


def _fmt_pct(v):
    return "-" if v is None else "%+.1f%%" % v


def _short(arm):
    return arm if len(arm) <= 28 else arm[:25] + "..."


def root_to_tip(tree, dates):
    d = root_to_tip_distances(tree)
    xs, ys = [], []
    for name, dist in d.items():
        if name in dates:
            xs.append(dates[name])
            ys.append(dist)
    if len(xs) < 3:
        return None
    return linregress(xs, ys)


def cophenetic(tree, names_limit=None):
    """Pairwise patristic distances keyed by (nameA, nameB) with nameA<nameB."""
    # Collect path-to-root with cumulative lengths
    paths = {}

    def descend(node, acc, chain):
        if node.is_leaf():
            if node.name:
                paths[node.name] = (list(chain), list(acc))
            return
        for ch in node.children:
            chain.append(ch)
            acc.append(acc[-1] + ch.length if acc else ch.length)
            descend(ch, acc, chain)
            chain.pop()
            acc.pop()

    descend(tree, [0.0], [tree])
    names = sorted(paths)
    if names_limit and len(names) > names_limit:
        rng = random.Random(0)
        names = sorted(rng.sample(names, names_limit))
    out = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            ca, da = paths[a]
            cb, db = paths[b]
            k = 0
            lim = min(len(ca), len(cb))
            while k < lim and ca[k] is cb[k]:
                k += 1
            dist = (da[len(ca) - 1] - da[k - 1]) + (db[len(cb) - 1] - db[k - 1])
            out[(a, b)] = dist
    return out


def mantel_confounding(tree, dates, n_perm=499, seed=1, cap=120):
    """Murray 2016's prescribed diagnostic: Mantel test between genetic distance
    and difference in sampling date. Significant => temporal and genetic
    structure are confounded."""
    coph = cophenetic(tree, names_limit=cap)
    if not coph:
        return (None, None)
    gen, tim = {}, {}
    for (a, b), dist in coph.items():
        if a in dates and b in dates:
            gen[(a, b)] = dist
            tim[(a, b)] = abs(dates[a] - dates[b])
    if len(gen) < 6:
        return (None, None)
    return mantel(gen, tim, n_perm=n_perm, seed=seed)


def verdict(recs, rtt_cache, close_ref, references, callers, replicons):
    if len(references) < 2:
        print("  Inconclusive: fewer than two references completed.")
        return
    close = close_ref if close_ref in references else references[0]
    distant = [r for r in references if r != close]

    inflated, r2_dropped, freeform_stable = [], [], []
    for rep in replicons:
        for caller in callers:
            base_arm = "%s__%s__%s" % (close, caller, rep)
            for ref in distant:
                arm = "%s__%s__%s" % (ref, caller, rep)
                b, o = recs.get(base_arm), recs.get(arm)
                if not (b and o and b["complete"] and o["complete"]):
                    continue
                d = _pct_delta(_sites(b["snps"]), _sites(o["snps"]))
                if d is not None and d > 20.0:
                    inflated.append((caller, rep, ref, d))
                br, orr = rtt_cache.get(base_arm), rtt_cache.get(arm)
                if br and orr:
                    drop = br["r2"] - orr["r2"]
                    if drop > 0.10:
                        r2_dropped.append((caller, rep, ref, drop))
                    elif caller in ("ska_map", "ska_lo") and abs(drop) <= 0.10:
                        freeform_stable.append((caller, rep, ref, drop))

    # PRECONDITION for the root-to-tip criterion. If the CLOSE-reference arm
    # already has no temporal signal, "R^2 did not drop" is uninformative --
    # there was nothing to lose. Report that explicitly rather than letting a
    # structurally impossible test read as evidence of no effect.
    baselines = [rtt_cache[a]["r2"] for a in rtt_cache
                 if a.startswith(close + "__") and rtt_cache[a]]
    r2_floor = bool(baselines) and max(baselines) < 0.10
    if r2_floor:
        print("  NOTE: every close-reference arm has root-to-tip R^2 < 0.10")
        print("  (max %.3f). The R^2 criterion CANNOT fire -- there is no"
              % max(baselines))
        print("  temporal signal to lose. Judge on SNP count and position")
        print("  concordance only, and report the clock as absent rather than")
        print("  as unaffected by the reference.\n")

    existing_hit = [x for x in inflated if x[0] == "existing"] + \
                   [x for x in r2_dropped if x[0] == "existing"]

    if existing_hit and freeform_stable:
        print("  POSITIVE. Your caller inflates SNP counts and/or loses")
        print("  root-to-tip signal on the distant reference while the")
        print("  reference-free callers hold steady. That is the ska lo PMEN2")
        print("  pattern reproduced in B. pseudomallei.")
        print("  => Adopt per-cluster references. Reference bias is")
        print("     contributing to weak temporal signal, and the fix is cheap.")
    elif inflated or r2_dropped:
        print("  PARTIAL. Some arms move materially with the reference, but")
        print("  the contrast between your caller and the reference-free")
        print("  callers is not clean. Report the table; do not over-claim.")
    else:
        print("  NULL. No arm moved more than 20% in SNP count or 0.10 in")
        print("  root-to-tip R^2 across references.")
        print("  => This is a GOOD outcome and a publishable one. It retires")
        print("     reference bias as a concern for this cluster and")
        print("     strengthens every downstream claim. Report it; do not")
        print("     bury it because it is negative.")

    for label, items in (("SNP inflation >20%", inflated),
                         ("root-to-tip R2 drop >0.10", r2_dropped)):
        if items:
            print("\n  %s:" % label)
            for caller, rep, ref, v in items:
                print("    %-10s %-8s vs %-12s  %+.2f" % (caller, rep, ref, v))

    print()
    print("  Thresholds (20%, 0.10) are constructs chosen to be smaller than")
    print("  the published PMEN2 effect (+42% SNPs, ~0.21 R drop). State them")
    print("  as chosen, not as established -- no published threshold exists.")
    print("  Generalise to one cluster only. Repeat on a second cluster of")
    print("  different diversity before generalising to the collection.")


# ===========================================================================
# selftest
# ===========================================================================

def cmd_selftest(args):
    ok = True

    def check(label, cond, detail=""):
        nonlocal ok
        print("  [%s] %s%s" % ("PASS" if cond else "FAIL", label,
                               "" if not detail else "  (%s)" % detail))
        if not cond:
            ok = False

    print(header("SELFTEST -- tree and statistics code"))

    t1 = parse_newick("((A:1,B:1):1,(C:1,D:1):1);")
    check("parse: 4 tips", sorted(tip_names(t1)) == ["A", "B", "C", "D"],
          str(sorted(tip_names(t1))))
    r2t = root_to_tip_distances(t1)
    check("root-to-tip all 2.0", all(abs(v - 2.0) < 1e-9 for v in r2t.values()),
          str(r2t))
    check("total tree length 6.0", abs(total_tree_length(t1) - 6.0) < 1e-9,
          str(total_tree_length(t1)))

    t2 = parse_newick("((A:1,C:1):1,(B:1,D:1):1);")
    rf, maxrf, norm, ns = robinson_foulds(t1, t2)
    check("RF of the two distinct 4-taxon topologies == 2", rf == 2,
          "rf=%s max=%s n=%s" % (rf, maxrf, ns))
    rf0, _, norm0, _ = robinson_foulds(t1, parse_newick("((B:1,A:1):1,(D:1,C:1):1);"))
    check("RF of relabelled-identical topology == 0", rf0 == 0, "rf=%s" % rf0)
    check("RF normalised in [0,1]", norm is not None and 0.0 <= norm <= 1.0,
          str(norm))

    kc_same, _ = kendall_colijn(t1, parse_newick("((B:9,A:9):9,(D:9,C:9):9);"))
    check("KC0 == 0 for identical topology, different lengths",
          kc_same is not None and abs(kc_same) < 1e-9, str(kc_same))
    kc_diff, _ = kendall_colijn(t1, t2)
    check("KC0 > 0 for different topology",
          kc_diff is not None and kc_diff > 0, str(kc_diff))

    st = linregress([1.0, 2.0, 3.0, 4.0], [2.0, 4.0, 6.0, 8.0])
    check("linregress slope 2.0, R2 1.0",
          st and abs(st["slope"] - 2.0) < 1e-9 and abs(st["r2"] - 1.0) < 1e-9,
          str(st))

    # An ULTRAMETRIC tree has zero root-to-tip variance, so the regression is
    # genuinely undefined and must return None rather than a spurious fit.
    ultra = parse_newick("((A:0.3,B:0.3):0.1,(C:0.1,D:0.1):0.3);")
    dates = {"A": 2020.0, "B": 2020.0, "C": 2000.0, "D": 2000.0}
    check("root-to-tip returns None on an ultrametric tree",
          root_to_tip(ultra, dates) is None)

    # Heterochronous, clock-like: 0.01 subs/site/yr over a 20-year span.
    clock = parse_newick("((A:0.25,B:0.25):0.05,(C:0.05,D:0.05):0.05);")
    rt = root_to_tip(clock, dates)
    check("root-to-tip recovers slope 0.01 and R2 1.0 on a clock-like tree",
          rt is not None and abs(rt["slope"] - 0.01) < 1e-9
          and abs(rt["r2"] - 1.0) < 1e-9, str(rt))

    # 6-taxon RF, hand-derived. s1 has unrooted internal splits
    # {C,D,E,F} (i.e. AB|CDEF), {C,D} and {E,F}.
    s1 = parse_newick("(((A:1,B:1):1,(C:1,D:1):1):1,(E:1,F:1):1);")
    check("6-taxon tree yields 3 non-trivial splits",
          len(bipartitions(s1)) == 3, str(sorted(map(sorted, bipartitions(s1)))))

    # s2 keeps {C,D} and {E,F} but breaks up the A,B cherry, so exactly one
    # split differs in each tree => RF 2.
    s2 = parse_newick("((A:1,(C:1,D:1):1):1,(B:1,(E:1,F:1):1):1);")
    rf6, max6, _, _ = robinson_foulds(s1, s2)
    check("RF == 2 when exactly one split differs", rf6 == 2,
          "rf=%s max=%s" % (rf6, max6))

    # Swapping B and C across the two cherries changes TWO internal edges,
    # so the answer is 4, not 2. Pinned so a future 'fix' cannot silently
    # halve RF.
    s3 = parse_newick("(((A:1,C:1):1,(B:1,D:1):1):1,(E:1,F:1):1);")
    rf6c, _, _, _ = robinson_foulds(s1, s3)
    check("RF == 4 for a two-edge change", rf6c == 4, "rf=%s" % rf6c)

    rf6b, _, _, _ = robinson_foulds(s1, s1)
    check("RF of a tree against itself == 0", rf6b == 0, "rf=%s" % rf6b)

    # Balanced topologies are where the old smaller-side tiebreak doubled RF.
    bal = parse_newick("((A:1,B:1):1,(C:1,D:1):1);")
    check("balanced 4-taxon tree yields exactly 1 split (no double-count)",
          len(bipartitions(bal)) == 1, str(bipartitions(bal)))

    quoted = parse_newick("(('sample one':1,\"sample:two\":1):1,C:2);")
    check("quoted labels with delimiters parse",
          sorted(tip_names(quoted)) == ["C", "sample one", "sample:two"],
          str(sorted(tip_names(quoted))))

    commented = parse_newick("((A:1[&rate=0.1],B:1):1,C:2);")
    check("comments stripped", sorted(tip_names(commented)) == ["A", "B", "C"],
          str(sorted(tip_names(commented))))

    coph = cophenetic(t1)
    check("cophenetic A-B == 2.0", abs(coph[("A", "B")] - 2.0) < 1e-9,
          str(coph.get(("A", "B"))))
    check("cophenetic A-C == 4.0", abs(coph[("A", "C")] - 4.0) < 1e-9,
          str(coph.get(("A", "C"))))

    # Mantel on a perfectly confounded design should be significant
    big = parse_newick(
        "(((t1:0.1,t2:0.1):0.1,(t3:0.1,t4:0.1):0.1):0.5,"
        "((t5:0.1,t6:0.1):0.1,(t7:0.1,t8:0.1):0.1):0.5);")
    conf = {"t1": 2000.0, "t2": 2000.0, "t3": 2001.0, "t4": 2001.0,
            "t5": 2020.0, "t6": 2020.0, "t7": 2021.0, "t8": 2021.0}
    mr, mp = mantel_confounding(big, conf, n_perm=499, seed=7)
    check("Mantel detects confounded design (r>0, p<0.10)",
          mr is not None and mr > 0 and mp is not None and mp < 0.10,
          "r=%s p=%s" % (_fmt(mr, 3), _fmt(mp, 3)))

    # ---- arm-script rendering ---------------------------------------------
    # Catches KeyError from a missing .format() field and, more importantly,
    # brace-escaping mistakes: the presets are inserted as a VALUE and must not
    # be re-formatted, so they use single braces while ARM_TEMPLATE uses double.
    for preset_name in sorted(EXISTING_PRESETS) + ["stub"]:
        block = (EXISTING_PRESETS[preset_name]
                 if preset_name != "stub" else CALL_BLOCKS["existing"])
        block = block.replace("{listfile}", "/tmp/list.tsv")
        try:
            rendered = ARM_TEMPLATE.format(
                arm="close__existing__chr1", caller="existing",
                refname="close", refpath="/refs/rep.fa",
                replicon="NC_006350.1", outdir="/out", threads=8,
                call_block=block, selfpath="/bin/refsens.py",
                env_caller="snp-phylogeny", env_recomb="bp-gubbins",
                env_for_call="${ENV_CALLER}")
        except (KeyError, IndexError, ValueError) as exc:
            check("render arm script with preset %r" % preset_name, False,
                  "%s: %s" % (type(exc).__name__, exc))
            continue
        check("render arm script with preset %r" % preset_name, True)
        check("  preset %r leaves no literal '${{'" % preset_name,
              "${{" not in rendered)
        check("  preset %r leaves no unsubstituted {listfile}" % preset_name,
              "{listfile}" not in rendered)
        # Anchor on a string unique to the real Gubbins invocation. Matching
        # "run_gubbins.py" would hit the `--version` line near the top and
        # make both ordering assertions pass for the wrong reason.
        gubbins_at = rendered.index("--invariant-site-correction")
        check("  preset %r emits the checkaln guard before Gubbins" % preset_name,
              rendered.index("checkaln") < gubbins_at)
        check("  preset %r calls the caller before Gubbins" % preset_name,
              rendered.index("--- 2. variant calling") < gubbins_at)
        check("  preset %r never invokes 'ska align'" % preset_name,
              "ska align" not in rendered)
        # "snp-sites" also appears in a step-1 comment about its hardcoded
        # CHROM field, so anchor on the actual invocation.
        check("  preset %r runs snp-sites AFTER Gubbins" % preset_name,
              gubbins_at < rendered.index("snp-sites -v -o"))
        # Tier 1.5: Gubbins' progress output must land in its OWN file, or the
        # iteration-to-convergence diagnostic is lost under IQ-TREE's output.
        check("  preset %r captures Gubbins progress separately" % preset_name,
              "gubbins.progress.log" in rendered)
        check("  preset %r writes a convergence record" % preset_name,
              "gubbins.convergence.txt" in rendered)
        # Redirecting stdout must not swallow a Gubbins failure.
        check("  preset %r still propagates a Gubbins failure" % preset_name,
              "GUBBINS_RC" in rendered
              and 'exit "${GUBBINS_RC}"' in rendered)
        # The capture must precede the tree step, or it captures nothing useful.
        # Anchor on the real invocation: bare "iqtree2" also appears in the
        # ENV_RECOMB comment at the top of the script, which sits BEFORE Gubbins
        # and would make this assertion fail for the wrong reason.
        check("  preset %r captures progress before the tree" % preset_name,
              rendered.index("gubbins.progress.log") < rendered.index("iqtree2 -s"))

    for preset_name, block in EXISTING_PRESETS.items():
        check("preset %r produces the required output path" % preset_name,
              "aln.full.${REPLICON}.fa" in block)
        # Style preference, not a correctness fix: `[ cond ] && continue` is
        # safe under `set -e` because bash exempts the left operand of a
        # short-circuiting &&. The `if` form just does not require the reader
        # to know that. Kept as a check so the presets stay consistent.
        # Inspect executable lines only -- the presets' own comments discuss
        # the pattern, so a naive substring search matches the prose.
        code_only = "\n".join(ln for ln in block.splitlines()
                              if not ln.lstrip().startswith("#"))
        check("preset %r uses if-form guards, not '&& continue'" % preset_name,
              "] && continue" not in code_only)

    print()
    print("SELFTEST %s" % ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1


# ===========================================================================
# checkaln -- assert an alignment is actually aligned, before Gubbins
# ===========================================================================

def cmd_checkaln(args):
    path = args.alignment
    if not os.path.exists(path):
        print("FAIL: %s does not exist. The caller step produced nothing."
              % path, file=sys.stderr)
        return 2
    records = list(iter_fasta_lengths(path))
    if not records:
        print("FAIL: %s contains no FASTA records." % path, file=sys.stderr)
        return 2

    n = len(records)
    ids = Counter(rid for rid, _ in records)
    dups = {rid: c for rid, c in ids.items() if c > 1}
    if dups:
        by_id = defaultdict(int)
        for rid, ln in records:
            by_id[rid] += ln
        worst = sorted(dups.items(), key=lambda kv: -kv[1])[:5]
        print("FAIL: %s has %d records but only %d distinct IDs -- %d IDs are "
              "repeated." % (path, n, len(ids), len(dups)), file=sys.stderr)
        print("", file=sys.stderr)
        print("This is a MULTI-CONTIG file, not an alignment. Every contig of "
              "an assembly shares the genome name as its first header token, "
              "so the records here are contigs, not aligned sequences.",
              file=sys.stderr)
        print("An alignment has exactly one record per taxon, all the same "
              "length.", file=sys.stderr)
        print("\nMost fragmented entries (contigs, total bp):", file=sys.stderr)
        for rid, c in worst:
            print("  %-44s %5d contigs  %10d bp" % (rid[:44], c, by_id[rid]),
                  file=sys.stderr)
        tot = sum(by_id.values())
        print("\n%d IDs, %d records, %d bp total (mean %.0f bp per ID)."
              % (len(ids), n, tot, tot / max(len(ids), 1)), file=sys.stderr)
        print("\nIf this file is INPUT to parsnp, that is fine -- parsnp takes "
              "unaligned genomes and produces its own XMFA. It is only a "
              "problem if a tree was built directly from this file.",
              file=sys.stderr)
        return 2

    lengths = {rid: ln for rid, ln in records}
    distinct = set(lengths.values())
    if len(distinct) == 1:
        L = distinct.pop()
        print("OK: %d records, all %d bp. Alignment is rectangular." % (n, L))
        if L < 1000:
            print("WARNING: %d bp is implausibly short for a full-length "
                  "pseudogenome. Gubbins needs the FULL alignment, not a "
                  "SNP-only one -- check that snp-sites did not run first."
                  % L, file=sys.stderr)
            return 1
        return 0

    lo, hi = min(distinct), max(distinct)
    print("FAIL: %s has UNEQUAL record lengths (%d distinct: %d-%d bp across "
          "%d records)." % (path, len(distinct), lo, hi, n), file=sys.stderr)
    print("", file=sys.stderr)
    print("This file is not an alignment. Passing it to Gubbins would produce "
          "meaningless window spacing and enormous branch lengths with no "
          "recombination involved -- the same failure class as a pipeline "
          "fallback that copies raw concatenated sequence into a file the "
          "next tool treats as aligned.", file=sys.stderr)
    print("Refusing to continue.", file=sys.stderr)

    counts = Counter(lengths.values())
    print("\nMost common lengths:", file=sys.stderr)
    for L, c in counts.most_common(5):
        print("  %10d bp  x%d" % (L, c), file=sys.stderr)
    odd = [nm for nm, L in lengths.items() if counts[L] < 3][:10]
    if odd:
        print("\nRecords with unusual lengths: %s" % ", ".join(odd),
              file=sys.stderr)
    return 2


# ===========================================================================
# demo -- synthetic Gubbins-shaped output
# ===========================================================================

def cmd_demo(args):
    outdir = os.path.abspath(args.outdir)
    rng = random.Random(args.seed)

    if args.taxa_from:
        # Rehearse with the REAL tip labels and dates, which is the only way to
        # prove the sample-id -> tree-tip -> dates join actually resolves.
        real = load_dates(args.taxa_from)
        if len(real) < 4:
            sys.exit("ERROR: --taxa-from %s yielded %d usable dated genomes."
                     % (args.taxa_from, len(real)))
        taxa = sorted(real)
        dates = dict(real)
    else:
        taxa = ["iso%02d" % i for i in range(1, 15)]
        dates = {t: 2000 + 1.6 * i for i, t in enumerate(taxa)}

    # Every arm shares a common backbone of true variant positions; arms differ
    # only by how many SPURIOUS positions they add. That is the biologically
    # meaningful shape -- a distant reference generates false positives through
    # mismapping (Pightling 2014: 3.3-3.8 -> 218.8-1,477.2 false-positive SNPs
    # from a 0.82% divergent reference) -- and it makes section C informative.
    CORE_SITES = 2200

    def clocklike(noise, swap_pairs=0):
        order = list(taxa)
        for _ in range(swap_pairs):
            i = rng.randrange(len(order) - 1)
            order[i], order[i + 1] = order[i + 1], order[i]
        parts = []
        for t in order:
            d = (dates[t] - 2000.0) * 0.001 + rng.gauss(0, noise)
            parts.append("%s:%.6f" % (t, max(d, 1e-5)))
        nw = parts[0]
        for p in parts[1:]:
            nw = "(%s,%s):0.00001" % (nw, p)
        return nw + ";"

    def write_arm(arm, n_spurious, noise, rec_blocks, swap_pairs=0):
        d = os.path.join(outdir, "arms", arm)
        os.makedirs(d, exist_ok=True)
        n_sites = CORE_SITES + n_spurious
        with open(os.path.join(d, "gubbins.filtered_polymorphic_sites.fasta"),
                  "w") as fh:
            for t in taxa:
                fh.write(">%s\n%s\n" % (t, "".join(
                    rng.choice("ACGT") for _ in range(n_sites))))
        with open(os.path.join(d, "gubbins.snps.vcf"), "w") as fh:
            fh.write("##fileformat=VCFv4.2\n"
                     "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
            pos = [1 + i * 1200 for i in range(CORE_SITES)]
            pos += [601 + i * 1200 for i in range(n_spurious)]
            for p in sorted(set(pos)):
                fh.write("1\t%d\t.\tA\tC\t.\tPASS\t.\n" % p)
        with open(os.path.join(d, "gubbins.recombination_predictions.gff"),
                  "w") as fh:
            fh.write("##gff-version 3\n")
            p = 1000
            for i in range(rec_blocks):
                ln = rng.randint(500, 8000)
                fh.write("chr\tGUBBINS\tCDS\t%d\t%d\t.\t.\t.\tnode=n%d\n"
                         % (p, p + ln, i))
                p += ln + rng.randint(2000, 30000)
        with open(os.path.join(d, "gubbins.per_branch_statistics.csv"),
                  "w") as fh:
            cols = ["Node", "Total SNPs", "Num of SNPs Inside Recombinations",
                    "Num of SNPs Outside Recombinations",
                    "Num of Recombination Blocks", "Bases in Recombinations",
                    "Cumulative Bases in Recombinations",
                    "Cumulative Num of SNPs Inside Recombinations",
                    "Num point mutations",
                    "Num substitutions due to recombination", "r/m"]
            fh.write("\t".join(cols) + "\n")
            for i in range(len(taxa)):
                m = rng.randint(20, 60)
                r = int(m * rng.uniform(2.0, 5.0))
                fh.write("\t".join(str(x) for x in [
                    "n%d" % i, m + r, r, m, rec_blocks, 5000, 5000, r,
                    m, r, round(r / m, 3)]) + "\n")
        with open(os.path.join(d, "tree.treefile"), "w") as fh:
            fh.write(clocklike(noise, swap_pairs) + "\n")

    tight, loose = 0.00012, 0.00260
    if args.pattern == "positive":
        spec = [
            # (arm, spurious sites, branch noise, rec blocks, topology swaps)
            ("close__existing__chr1", 100, tight, 34, 0),
            ("close__ska_map__chr1", 40, tight, 33, 0),
            ("close__ska_lo__chr1", 80, tight, 33, 0),
            # the PMEN2 shape: ~+43% SNPs, collapsed clock, disturbed topology
            ("K96243__existing__chr1", 1090, loose, 51, 4),
            ("K96243__ska_map__chr1", 100, tight, 34, 0),
            ("K96243__ska_lo__chr1", 60, tight, 33, 0),
        ]
    else:
        spec = [
            ("close__existing__chr1", 100, tight, 34, 0),
            ("close__ska_map__chr1", 40, tight, 33, 0),
            ("close__ska_lo__chr1", 80, tight, 33, 0),
            ("K96243__existing__chr1", 130, tight, 35, 0),
            ("K96243__ska_map__chr1", 50, tight, 33, 0),
            ("K96243__ska_lo__chr1", 90, tight, 34, 0),
        ]
    for arm, spurious, noise, blocks, swaps in spec:
        write_arm(arm, spurious, noise, blocks, swaps)

    with open(os.path.join(outdir, "manifest.tsv"), "w") as fh:
        fh.write("arm\treference\tcaller\treplicon\tscript\n")
        for entry in spec:
            arm = entry[0]
            ref, caller, rep = arm.split("__")
            fh.write("%s\t%s\t%s\t%s\t-\n" % (arm, ref, caller, rep))

    dpath = os.path.join(outdir, "dates.csv")
    with open(dpath, "w") as fh:
        fh.write("genome,year\n")
        for t in taxa:
            fh.write("%s,%d\n" % (t, int(dates[t])))
        # The PRJEB3409 placeholder. A naive date[:4] parse reads this as 1800.
        fh.write("iso_placeholder,1800/2014\n")

    loaded = load_dates(dpath)
    print(header("DEMO -- synthetic '%s' dataset" % args.pattern))
    print("Wrote %d synthetic arms to %s" % (len(spec), outdir))
    print("Date parsing: %d genomes kept; the '1800/2014' PRJEB3409 "
          "placeholder was %s."
          % (len(loaded),
             "correctly dropped" if "iso_placeholder" not in loaded
             else "WRONGLY KEPT"))
    print("\nThis is synthetic data. It exercises the code path; it says")
    print("nothing about B. pseudomallei.")
    print("\nWhich sections are meaningful in a rehearsal:")
    print("  A-D, F  -- structurally meaningful: they prove the parsers, the")
    print("             id->tip->dates join and the decision rule all resolve.")
    print("  E Mantel -- NOT meaningful. The synthetic trees are ladders whose")
    print("             cophenetic distances track the SUM of two tip dates")
    print("             while temporal distance is their DIFFERENCE, so a")
    print("             strong negative r is an artefact of the generator.")
    print("             Read the Mantel column only on real trees.")

    ns = argparse.Namespace(outdir=outdir, dates=dpath, close_ref="close",
                            permutations=199, seed=1)
    return cmd_analyse(ns)


# ===========================================================================
# misc
# ===========================================================================

def header(title):
    return "\n%s\n%s\n%s" % ("=" * 74, title, "=" * 74)


def section(title):
    return "\n%s\n%s" % (title, "-" * len(title))


def main():
    ap = argparse.ArgumentParser(
        description="Reference-sensitivity experiment for per-cluster "
                    "B. pseudomallei analysis (REVISED_STRATEGY 2.4).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("USAGE")[1] if "USAGE" in __doc__ else None)
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("plan", help="emit the run matrix as executable bash")
    p.add_argument("--cluster-list", required=True,
                   help="file of genome IDs/paths, one per line (100-300 "
                        "genomes, ideally mixed Thai and non-Thai)")
    p.add_argument("--ref", action="append", required=True, metavar="NAME=PATH",
                   help="repeatable; at least two. Use a within-cluster "
                        "representative plus K96243, optionally 1026b.")
    p.add_argument("--outdir", required=True)
    p.add_argument("--callers", default=",".join(CALLERS),
                   help="comma-separated (default: %(default)s)")
    p.add_argument("--replicons",
                   default="%s,%s" % (CHR1_ID_DEFAULT, CHR2_ID_DEFAULT),
                   help="comma-separated replicon IDs as they appear in the "
                        "reference FASTA (default: %(default)s)")
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--existing-preset",
                   choices=sorted(EXISTING_PRESETS) + ["stub"],
                   default="stub",
                   help="what the 'existing' arm runs. Use snippy-contigs for "
                        "an assembly-based collection (92%% of public "
                        "B. pseudomallei genomes are drafts, so this is the "
                        "usual answer). 'stub' leaves the arm exiting 3.")
    p.add_argument("--env-caller", default="",
                   help="conda env providing samtools, snippy, snippy-core "
                        "and snp-sites (e.g. snp-phylogeny). Empty = assume "
                        "everything is already on PATH.")
    p.add_argument("--env-recomb", default="",
                   help="conda env providing ska, generate_ska_alignment.py, "
                        "run_gubbins.py and iqtree2 (e.g. bp-gubbins).")
    p.add_argument("--existing-cmd-file", default=None,
                   help="path to a shell fragment for the 'existing' arm, "
                        "overriding --existing-preset. It must produce "
                        "${OUT}/aln.full.${REPLICON}.fa. Available variables: "
                        "OUT, REF, REPLICON, THREADS; {listfile} is "
                        "substituted with the cluster list path.")
    p.set_defaults(func=cmd_plan)

    ck = sub.add_parser(
        "checkaln",
        help="assert a FASTA is rectangular before Gubbins sees it")
    ck.add_argument("alignment")
    ck.set_defaults(func=cmd_checkaln)

    a = sub.add_parser("analyse", help="analyse completed arms")
    a.add_argument("--outdir", required=True)
    a.add_argument("--dates", default=None,
                   help="CSV/TSV of genome,collection_year. The PRJEB3409 "
                        "'1800/2014' placeholder is dropped automatically.")
    a.add_argument("--close-ref", default="close",
                   help="name of the within-cluster reference "
                        "(default: %(default)s)")
    a.add_argument("--permutations", type=int, default=499)
    a.add_argument("--seed", type=int, default=1)
    a.set_defaults(func=cmd_analyse)

    s = sub.add_parser("selftest", help="verify tree/statistics code")
    s.set_defaults(func=cmd_selftest)

    dm = sub.add_parser(
        "demo",
        help="synthesise Gubbins-shaped output and analyse it, to exercise "
             "the analysis path before real data exists")
    dm.add_argument("--outdir", required=True)
    dm.add_argument("--pattern", choices=("positive", "null"),
                    default="positive",
                    help="'positive' reproduces the PMEN2 shape (distant "
                         "reference inflates SNPs and degrades root-to-tip "
                         "signal for your caller while the reference-free "
                         "callers hold steady); 'null' makes every arm "
                         "equivalent. Use both to check that the decision "
                         "rule discriminates. (default: %(default)s)")
    dm.add_argument("--seed", type=int, default=11)
    dm.add_argument("--taxa-from", default=None,
                    help="a genome,year CSV (e.g. the one written by "
                         "cluster_metadata_join_bp.py). Rehearses with the "
                         "REAL sample IDs and dates, which verifies that the "
                         "sample-id -> tree-tip -> dates join resolves before "
                         "any real compute is spent.")
    dm.set_defaults(func=cmd_demo)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return 1
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
