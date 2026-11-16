# Scripts by role

The repository root holds **104 Python scripts and 48 shell wrappers**. They are
at the top level by necessity, not sprawl: `.gitignore` re-admits code only at
the top level (subdirectories are denied), the `run_*.sh` wrappers call the
Python scripts by bare filename, and the scripts resolve their data files
against the current directory, which is the root. Moving them into folders would
break the wrappers and the literal-name references in the docs and CI.

This index groups the Python scripts by role so the list is navigable. One-line
descriptions are the scripts' own module docstrings. The headline entry points
are `freeze_basis_bp.py` then `generate_numbers.py` (regenerate every quotable
figure), `grouping_test_bp.py` and `resolution_curve_bp.py` (attribution), and
`context_snps_bp.py` with `context_report_bp.py` (the recurrence series).

The shell scripts are mostly thin wrappers. `run_*.sh` drive the Nextflow
workflow at the pinned profile and parameters (see `PRODUCTION_RUN_PIN_2026-08-24.md`),
and `run_full_workflow.sh` runs the whole panel.

### Panel construction and QC

| script | what it does |
|---|---|
| `build_v4c_panel.py` | Panel/bundle helper for the unattended v4c build. One mode per step so |
| `build_global_backbone_bp.py` | Build the global backbone tree over unit medoids. |
| `assembly_stats_bp.py` | Panel-wide assembly statistics for the accessory-attribution control. |
| `species_id_bp.py` | Positive species identification for Burkholderia pseudomallei. |
| `qc_batch3_2026-08-21.py` | QC the 2026-08-21 additions, using the gates calibrated in |
| `reqc_spades_batch.py` | Re-QC the SPAdes re-assembly batch, using the same gates as NEW200_QC_2026-08-17. |
| `classify_ena_origin_bp.py` | Classify ENA records by how much their ORIGIN metadata can be trusted. |
| `parse_ena.py` | Classify every analysed genome as clinical / environmental / animal / unknown |
| `finalise_sources.py` | Consolidate isolation source for all 2,070 analysed genomes. |
| `retire_exclusions_bp.py` | Retire the four unevidenced PANEL_EXCLUSIONS rows. idempotent and re-runnable. |
| `verify_exclusions_bp.py` | Re-measure the QC evidence behind four PANEL_EXCLUSIONS.tsv rows. |

### Partitioning into analysis units

| script | what it does |
|---|---|
| `build_L1_partition_bp.py` | Build the level-1 PopPUNK/fastbaps partition into analysis units. |
| `cluster_diversity_bp.py` | Per-cluster core-SNP diversity. |
| `cluster_diagnostics_bp.py` | Gap 2 companion: cluster-size diagnostics and the Gubbins contrast arithmetic |
| `compare_partitions_bp.py` | Compare two partitions unit by unit. |
| `repartition_sweep_bp.py` | Sweep partition settings to test stability. |
| `mash_threshold_sweep_bp.py` | Sweep the Mash clustering threshold to find a FOUND partition, not an imposed one. |
| `measure_diversity_bp.py` | Measure true within-cluster core-SNP diversity directly, replacing the Mash proxy. |
| `consolidate_L1_rm_bp.py` | Consolidate per-unit r/m across the level-1 partition. |

### Per-unit reference selection

| script | what it does |
|---|---|
| `pick_cluster_references_bp.py` | Pick the constrained medoid reference for each unit. |
| `rank_reference_alternates_bp.py` | Rank alternate references per unit. |
| `merge_L1_refs_bp.py` | Merge the chosen per-unit references into one table. |
| `reference_sensitivity_bp.py` | Reference-sensitivity protocol across arms. |
| `reduced_refsens_bp.py` | Reduced reference-sensitivity protocol: 4 arms instead of 12, for threshold-finding. |
| `verify_references_bp.py` | Re-verify the per-unit reference choices. |
| `exclude_reference_branches_bp.py` | Drop the reference branch from a per-unit alignment. |
| `normalize_reference_headers_bp.py` | Normalize FASTA headers on the per-unit references. |
| `cap_location_bp.py` | Locate the Gubbins diversity cap from the reference-sensitivity runs. |

### Operating-range calibration (the ruler)

| script | what it does |
|---|---|
| `calibrate_mash_snp_bp.py` | Calibrate the Mash-to-SNP proxy against measured mean pairwise distances. |
| `gate1_from_alignment_bp.py` | Gate 1 diversity from ALIGNMENT-derived distances instead of the Mash proxy. |
| `spikein_sensitivity_bp.py` | Detection sensitivity, measured by SPIKING KNOWN RECOMBINATION INTO REAL DATA. |
| `nu_slice_bp.py` | The SimBac nu-slice: at the nu we actually measured, would we detect |
| `nu_hypothesis_bp.py` | Test the nu hypothesis for the depressed-r/m residue. |

### Variant calling and caller diagnostics

| script | what it does |
|---|---|
| `caller_annotation_overlap_bp.py` | Do snippy's clustered SNPs sit in mobile elements or rRNA (paralogy)? |
| `caller_repeat_overlap_bp.py` | Are snippy's tightly-clustered SNPs real, or mismapping artefacts in repeats? |
| `caller_spacing_bp.py` | Snippy vs SKA: is SNP recovery coupled to local SNP spacing? |
| `callable_variance_bp.py` | Tier 1.4 -- does VARIANCE in per-genome callable fraction explain the r/m |
| `xmfa_to_core_bp.py` | Concatenate a Parsnp XMFA into a core alignment that Gubbins can consume. |
| `recomb_filtered_distances_bp.py` | Recombination-filtered pairwise SNP distances from Gubbins output. |

### Recombination rate and its decomposition

| script | what it does |
|---|---|
| `triage_analysable_bp.py` | N3: triage the 45 analysable-set production runs on union AND pooled r/m. |
| `clonalframe_nu_bp.py` | Tier 1.3 -- decompose the r/m residue with ClonalFrameML: is the unexplained |
| `mge_hotspot_audit_bp.py` | Tier 1.2 -- the MGE / hotspot audit: is shared recombinant positioning an |
| `constant_sites_sensitivity_bp.py` | Tier 1.1 -- is the declared constant-site limitation actually material? |
| `collapse_unsupported_bp.py` | Tier 0.1 -- collapse poorly-supported branches into polytomies. |
| `tier0_evidence_bp.py` | Tier 0 evidence base: recompute, from disk, every number the Tier 0 |
| `treebuilder_equivalence_bp.py` | Does the Gubbins tree builder change the recombination calls? |
| `rebuild_support_fconst_bp.py` | Rebuild the per-unit support trees with `-fconst` instead of `GTR+ASC`. |
| `validate_modality_bp.py` | Validate the modality statistic's SIZE DEPENDENCE by subsampling. |

### Attribution scoring

| script | what it does |
|---|---|
| `attribution_score_bp.py` | Score origin attribution against the genomes whose exposure country is known. |
| `grouping_test_bp.py` | Which grouping of isolates supports the most accurate prediction? |
| `resolution_curve_bp.py` | Attribution accuracy as a function of how many loci you type. |
| `score_cgmlst_lichtenegger.py` | Attribution scoring on the Lichtenegger cgMLST profiles, expanded panel. |
| `score_accessory_bp.py` | Accessory-genome attribution, scored under the same regime as the core genome. |
| `cgmlst_analysis_bp.py` | cgMLST layer: QC, concordance with the v4c units, and attribution scoring. |
| `concordance_frozen_bp.py` | cgMLST vs recombination-filtered SNP concordance, on the FROZEN BASIS. |
| `mlst_to_allele_table_bp.py` | Reshape MLST_v4c.tsv into the wide allele table score_cgmlst_lichtenegger.py eats. |
| `fetch_cgmlst_scheme_bp.py` | Fetch the PubMLST B. pseudomallei cgMLST scheme (scheme 2) as per-locus FASTA. |
| `abstention_rule_bp.py` | The abstention rule: when should the method answer "unattributable" instead of |
| `accessory_control_bp.py` | PRE-REGISTERED controls for the accessory-attribution experiment. |

### Significance, nulls and confounder controls

| script | what it does |
|---|---|
| `null_simulation_bp.py` | Tier 2 -- the zero-recombination null, and the p-values that replace our |
| `bioproject_within_country_bp.py` | Does BioProject structure the tree WITHIN a single country? |
| `downsample_control_bp.py` | Downsampling control: is region attribution an artifact of panel imbalance? |
| `pseudoreplication_bp.py` | Is the structure that breaks our partitions actually PSEUDO-REPLICATION? |
| `phylogeography_association_bp.py` | Association index between geography and tree structure. |
| `phylogeography_diagnostics_bp.py` | Gap 4 companion: sampling-frame and phylogeography diagnostics for |
| `test_phylogeography_bp.py` | Tests for the phylogeography diagnostics. |

### Recurrence series (Nakhon Phanom relapse and reinfection)

| script | what it does |
|---|---|
| `recurrence_mash_bp.py` | Relapse vs reinfection calls for the Nakhon Phanom recurrence series, on |
| `context_snps_bp.py` | Recombination-aware SNP distances and local context trees for the recurrence |
| `context_report_bp.py` | Turn the per-group Gubbins output into recurrence answers: recombination-filtered |

### Figures, tables, trees and interactive viewers

| script | what it does |
|---|---|
| `make_figure1_bp.py` | Figure 1, study flow,, generated from NUMBERS.tsv so it cannot go stale. |
| `make_figure2_bp.py` | Figure 2 -- the Gate 1 detection window, generated so it cannot go stale. |
| `make_figure3_bp.py` | Figure 3 -- the global maximum-likelihood tree over unit medoids. |
| `make_figure4_bp.py` | Figure 4 -- geography against its own confounder, per unit. |
| `make_figure5_bp.py` | Figure 5 -- detection is bounded from both sides. |
| `make_figure6_bp.py` | Figure 6 -- the global genome-level tree, with the PopPUNK strains as shaded |
| `make_figure_attribution_bp.py` | The attribution resolution ceiling -- publication figure. |
| `make_tables_bp.py` | make_tables_bp.py -- Tables 1 to 5, generated from the frozen basis. |
| `make_itol_bp.py` | make_itol_bp.py -- iTOL components for the global maximum-likelihood tree. |
| `make_itol_annotations.py` | Generate iTOL annotation files for the grafted all-sample tree. |
| `make_itol_grafted_bp.py` | make_itol_grafted_bp.py -- iTOL package for the GENOME-level global tree, |
| `make_auspice_microreact_bp.py` | Export the global tree and its metadata for Microreact and Auspice. |
| `make_tree_explorer_bp.py` | Assemble TREE_EXPLORER.html from the template and the generated data payload. |
| `make_tree_explorer_data_bp.py` | Build the data payload for the interactive global tree. |

### Virtual-manuscript video and narration

| script | what it does |
|---|---|
| `make_narrated_videos_bp.py` | Lay synthesized narration onto the silent Animo clips. Engine agnostic. |
| `make_narration_csv_bp.py` | Narration for the current clips, as a CSV a voice studio can work from. |
| `make_voice_lines_bp.py` | Bridge the narration SRTs to a voice engine, per cue. |
| `make_virtual_manuscript_video_bp.py` | Assemble the full virtual-manuscript video from the narrated clips. |
| `retime_narration_bp.py` | Re-time all five narration scripts against the animations' actual beats. |
| `retime_7.01_bp.py` | Re-time and rewrite the 7.01 narration against the animation's actual beats. |
| `make_captions_bp.py` | Build captions for the five Animo animations from the narration SRTs. |
| `make_animo_pack_bp.py` | Build ANIMO_PACK/, the transferable subset of VM_HANDOFF_PACK. |
| `stage_for_claude_design_bp.py` | Stage a transfer folder for redesigning the video edition with Claude Design. |

### Numbers, freeze, bibliography and review package

| script | what it does |
|---|---|
| `freeze_basis_bp.py` | Freeze the analysis basis: one panel, one partition, coordinated, checkable. |
| `generate_numbers.py` | Regenerate every quotable figure from primary data into one file: NUMBERS.tsv. |
| `manuscript_numbers_bp.py` | Collect the manuscript's quotable numbers. |
| `build_bibliography_bp.py` | Build the manuscript bibliography. |
| `compare_bibliographies_bp.py` | Compare the two bibliographies in a document that carries both. |
| `build_review_package_bp.py` | Build the independent-review package. |
| `country_share_bp.py` | Per-country share of the panel. |

### Pipeline checks, guards and small utilities

| script | what it does |
|---|---|
| `pipeline_checks_bp.py` | pipeline_checks_bp.py -- runnable checks for Gap 3 of the B. pseudomallei SNP |
| `audit_defaults_bp.py` | Fail if any script has an argparse INPUT default naming a specific run. |
| `fix_crlf_writers.py` | Add lineterminator="\n" to every csv writer that currently defaults to CRLF. |
| `write_if_changed_bp.py` | Write a file only when its content changed (idempotent output). |
| `ska_feasibility_bp.py` | Feasibility arithmetic for applying SKA2 to Burkholderia pseudomallei. |
---

Every script is standalone and run from the repository root. Most are one-off
analyses or figure and table builders invoked by hand. A handful are driven by
the `run_*.sh` wrappers, and a few are imported by other scripts. Sixteen are
not referenced from any wrapper, document or other script, which marks them as
one-off tools rather than dead code.
