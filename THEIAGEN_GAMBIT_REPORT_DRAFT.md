# Draft report to Theiagen, GAMBIT 3.0.0 database and *B. pseudomallei*

Paste-ready. Edit freely; the numbers are all verifiable from
`BATCH3_QC_REPORT_2026-08-21.md` and `BATCH3_QC_2026-08-21.tsv`.

---

**Title:** GAMBIT 3.0.0 database assigns *Burkholderia mallei* to *B. pseudomallei*
assemblies (40/40 in our batch); taxon call propagates into `ts_mlst` scheme
selection

Hi Theiagen team,

We run TheiaProk for a *Burkholderia pseudomallei* genomics project and hit a
species-call change after updating to TheiaProk 4.3.0. Wanted to flag it with
the data, in case it's useful.

**What we saw**

Forty *B. pseudomallei* isolates assembled with TheiaProk 4.3.0 all returned
`gambit_predicted_taxon = "Burkholderia mallei"` at species rank.
`kmerfinder_top_hit` agreed on all 40.

The same lab, the same organism, and the same pipeline family four days earlier
gave the opposite result:

| batch | date | n | called *B. pseudomallei* | called *B. mallei* |
|---|---|---|---|---|
| previous TheiaProk | 2026-08-17 | 195 | **189** | **0** |
| TheiaProk 4.3.0 | 2026-08-21 | 40 | **0** | **40** |

The older run also correctly identified one *B. thailandensis* and left four at
genus level, so it was discriminating within the complex rather than defaulting.

**Why we believe these are *B. pseudomallei***

- Mash distance to K96243 (*B. pseudomallei* reference, `-s 10000 -k 21`):
  **0.0041–0.0077** across all 40. For calibration, a genome we previously
  excluded from this project as wrong-species/divergent measured 0.0135.
- Core-genome coverage of K96243: **91.3–98.6%** (median 96.9%).
- BUSCO `burkholderiales_odb10`: Complete median **99.5%**, minimum 95.1%.
- The 40 span **22 distinct sequence types** (including ST92, ST70, ST297,
  ST369), 3 BioProjects and 4 countries, so this isn't one unusual clade.
- Most are from CDC-deposited melioidosis case investigations.

**Versions**

The GAMBIT tool version is unchanged at v1.0.0 (`staphb/gambit:1.0.0`) in both
runs. What changed is the database:

```
gambit-metadata-3.0.0-20260601.gdb
gambit-signatures-3.0.0-20260601.gs
```

Two small related things:

1. **The docs and `main` disagree.** The TheiaProk input documentation still
   lists `gs://gambit-databases-rp/2.2.0/gambit-metadata-2.2.0-20251111.gdb` as
   the default for `gambit_db_genomes`, while `tasks/taxon_id/task_gambit.wdl`
   on `main` has the 3.0.0 paths. That may be why the change wasn't obvious to
   users.
2. **The DB inputs aren't exposed at workflow level.** `wf_theiaprok_illumina_pe.wdl`
   passes only `assembly` and `samplename` to the `gambit` task, so overriding
   requires the fully-qualified `theiaprok_illumina_pe.gambit.gambit_db_genomes`.
   That works, but surfacing them as workflow inputs would make pinning easier.

**The part we think matters most: it propagates downstream**

TheiaProk passes the GAMBIT call into `ts_mlst` as
`taxonomy = select_first([expected_taxon, gambit.gambit_predicted_taxon])`.
In our batch, **2 of 40 were consequently typed against the `bcc`
(*B. cepacia* complex) MLST scheme instead of `bpseudomallei`, and both returned
"No ST predicted"**, `SRR31683025` and `SRR34776626`, both confirmed
*B. pseudomallei* by mash (0.0063 and 0.0055 to K96243). The other 38 still
resolved to `bpseudomallei`, so the effect is inconsistent, but it means the
taxon assignment isn't only a reported label, it silently changes which scheme
downstream typing uses.

**Why we're flagging it rather than just working around it**

We recognize this is a genuinely hard pair: *B. mallei* is a clonal derivative
of *B. pseudomallei*, and separating them from assembly data alone is a real
problem, not a careless one.

The reason we think it's worth a look anyway is the asymmetry of consequence in
a public health lab setting, which is TheiaProk's main audience. Both organisms
are HHS/USDA Tier 1 Select Agents, so this doesn't move anything into or out of
regulation. But melioidosis is an expected finding in the US, now recognized as
endemic on parts of the Gulf Coast, whereas glanders is essentially absent from
the Western Hemisphere. A *B. mallei* call from a US clinical or environmental
isolate is an extraordinary result that would trigger a much larger and
different response than melioidosis, and in the other direction, a lab that
trusted the call would report the wrong disease.

**Scope of what we actually tested**

We only tested *B. pseudomallei*, n=40. **We have not tested whether GAMBIT
3.0.0 still identifies true *B. mallei* correctly**, and we haven't looked at
any other taxa, so we can't say whether this is specific to this species pair or
broader.

**Happy to help**

We can share the 40 assemblies, the SRA run accessions, or the full Terra table
if that's useful for reproducing. We're also re-running the same 40 against the
2.2.0 database as a controlled comparison, same assemblies, same tool version,
only the database differs, and can send those results when they're done.

Thanks for TheiaProk; it's been a workhorse for us.

[name / affiliation]

---

## Notes for you, not for them

- **Consider running the 2.2.0 comparison before sending.** It converts "we
  think the database changed the answer" into "we changed only the database and
  the answer flipped back." That is a much harder report to set aside, and it
  costs one Terra rerun.
- **The `bcc` finding is the strongest single item.** A cosmetic label change is
  arguable; silently switching MLST schemes on 2 of 40 samples is not. Lead the
  GitHub issue title with it if you want attention.
- **Don't claim the select-agent angle harder than the above.** Both are Tier 1,
  so the regulatory status doesn't change, the argument is about response
  proportionality, and it is strong enough on its own. Overreaching there is the
  one thing that would make this easy to dismiss.
- Where to file: `github.com/theiagen/public_health_bioinformatics/issues`. GAMBIT
  itself is a separate project (`github.com/jlumpe/gambit`), but the 2.x/3.x
  databases are distributed by Theiagen/CDC, not upstream, so Theiagen is the
  right first stop.
