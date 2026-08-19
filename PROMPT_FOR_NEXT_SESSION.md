# Prompt for the next session

Copy everything below the line into a new chat, started in
`/home/phemarajata/Downloads/snp-mod-local-working`.

---

Read `HANDOFF_2026-08-17_SESSION7.md` first, then `THEIAPROK_SETTINGS.md`.
Together they carry the full state; the rest of this is orientation.

**Project.** Recombination-aware phylogenomics of ~2,800 *B. pseudomallei*
genomes. The applied goal is rapid origin-of-exposure attribution for
US/Americas cases with no travel history — the genome is the only evidence of
where the organism came from. Pipeline lives at `~/wf-assembly-snps-mod`
(`main` at `79ab645`, pushed), not in this workspace.

**Where things stand.** The v3 partition is validated and is the current result:
91 units, 2,282 genomes, 182/182 Tier1, exported to
`/media/phemarajata/TB1/snp_archive/snp_results_2026-08-16_v3/`. The older
82-unit export is marked `SUPERSEDED.txt`. Nothing is running.

**What I am waiting on.** 205 SRA accessions are being assembled externally
(`SRA_TO_ASSEMBLE.tsv`, annotated per-sample with coverage, platform, verdict
and rescue settings). 18 assemblies are already pulled and QC-passed in
`additions/fasta/`; 5 contaminated ones are quarantined; 3 are too shallow to
use. Terra input JSONs are in `terra_inputs/`.

**Open question right now.** The 5 PacBio CLR assemblies (Brazil, Ceará) came
out ~11 Mb against an expected 7.2 Mb. See `THEIAPROK_SETTINGS.md` §F for the
diagnostic decision tree and the one retry worth attempting. If they stay >8 Mb
the plan is to drop them — 32 Brazil Illumina runs cover the same clade.

**When the assemblies come back:** QC every one at **7.0–7.4 Mb** and a sane
contig count before it goes anywhere near the panel; merge on `origin_country`
(never ENA's `country`, which is isolation not origin); exclude the quarantined
5; then re-partition, re-run and re-export. The two units the additions are
meant to rescue are `strain_9_L1_2` (Mississippi, n=5) and `strain_9_L1_8`
(Mexico, n=6), both currently assign-only.

**How I want you to work.** Every significant defect in this project — seven so
far, listed in the handoff §0 — produced entirely plausible output from a silent
mismatch, and was caught only by comparing raw per-item values against what they
should have been, never by reading a summary. Requested accessions vs returned.
Per-country dropout vs the total. Per-unit diameters vs the median. Please check
things rather than infer them, tell me when a number I quote is wrong, and say
plainly when something is not worth doing.
