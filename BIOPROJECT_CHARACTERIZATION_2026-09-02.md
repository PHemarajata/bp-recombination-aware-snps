# What the BioProjects in this collection actually are

**2026-09-02.** Written because the confounder control uses BioProject as a proxy
for "batch", and nobody had checked what a BioProject means here. Titles fetched
from the ENA study API; composition computed from the frozen basis.

**The short answer: they are not the same kind of object, and the control treats
them as though they were.** One is 26 genomes from a single soil sample. Another
is a deliberately diverse 10-country panel spanning 55 years. Using one variable
to control for both is not a conservative choice; it is an undefined one.

---

## 1. The largest projects, characterised

| BioProject | n | countries | years | units | ENA title | what it actually is |
|---|---|---|---|---|---|---|
| `PRJEB25606` | 543 | 1 (Thailand) | 2015-2018 | 65 | Burkholderia_Northeast_Thailand | **regional survey** |
| `PRJEB35787` | 468 | 1 (Thailand) | 2015-2018 | 63 | Dissecting the genetic basis of melioidosis infection | **host-genetics study**, clinical series |
| `PRJNA285704` | 165 | 4 | **1965-2011** | 35 | Genome sequencing and assembly | **archive**, 46-year accumulation |
| `PRJNA669904` | 107 | 1 (China) | 2002-2018 | 18 | Genetic diversity and transmission, Hainan island | **geographic**, one island |
| `PRJEB2119` | 97 | 3 | 1997-2006 | 6 | Burkholderia pseudomallei **serial patient** | **clonal batch**, within-patient series |
| `PRJNA1172374` | 97 | 1 (China) | 2012-2023 | 14 | 105 genomes of B. pseudomallei | uncharacterised |
| `PRJEB2196` | 59 | 3 | 1996-2002 | 9 | Burkholderia pseudomallei **diversity** | **diversity panel** |
| `PRJNA1011490` | 49 | 1 (Thailand) | 2011-2018 | 6 | WGS from the environment and animals | **source-defined**, non-human |
| `PRJNA429426` | 26 | 1 (Thailand) | 2007 only | 4 | **intensive sequencing from a single soil sample** | **maximal clonal batch** |
| `PRJNA352974` | 22 | **10** | **1960-2015** | 4 | isolates associated with the **Western Hemisphere** | **diversity panel**, 55 years |

Note how many are titled only "Genome sequencing and assembly" (`PRJNA285704`,
`PRJNA904945`, `PRJNA528470`, `PRJNA1078842`). Those are submission containers
with no stated design at all.

## 2. A taxonomy, and which kinds are valid confounders

| design | examples | is BioProject a valid batch proxy? |
|---|---|---|
| **clonal batch** | `PRJNA429426` (one soil sample), `PRJEB2119` (serial patient) | **Yes.** This is the artifact the control exists to catch |
| **geographic frame** | `PRJEB25606` (NE Thailand), `PRJNA669904` (Hainan), `PRJNA892040` (Vietnam) | **No.** Geographic by construction, so controlling for it removes geography by definition |
| **diversity panel** | `PRJEB2196`, `PRJNA352974` | **No, and backwards.** Members are chosen to be *unlike* each other; this is the opposite of a batch |
| **clinical series** | `PRJEB35787` | **Partly.** A consecutive series is a population sample, not a clonal group |
| **archive** | `PRJNA285704`, and the untitled containers | **Unknown.** No stated design to reason about |

## 3. The control fires on the wrong projects

For each of the 12 units discarded as "confounded", the BioProject that dominates
its labelled tips:

| dominant project | units | design |
|---|---|---|
| `PRJEB2196` | 3 | **diversity panel** |
| `PRJNA1172374` | 2 | uncharacterised |
| `PRJEB25606` | 2 | **geographic frame** |
| `PRJNA669904` | 1 | **geographic frame** |
| `PRJNA892040` | 1 | **geographic frame** |
| `PRJEB35787` | 1 | clinical series |
| `PRJNA904945` | 1 | archive |
| `PRJNA352974` | 1 | **diversity panel** |

**Zero of the 12 are driven by a project we can identify as a genuine clonal
batch.** Four are driven by diversity panels, whose members were deliberately
selected to differ; five by geographic frames, where "controlling for BioProject"
and "controlling for geography" are the same operation.

Meanwhile the two genuinely batch-like projects drive no discard at all:

- `PRJNA429426` (single soil sample) spreads across 4 units, dominant in none;
  its largest share is 30% in a unit already called `null`.
- `PRJEB2119` (serial patient) is **86% of `strain_1_L1_3`** -- and that unit is
  classified `untestable: single-valued`, so the control never gets to speak.

This is the over-control in [[bioproject-is-nested-inside-country]] given a
mechanism: the control is not failing at random, it is systematically firing on
sampling frames rather than on batches.

## 4. The untestable stratum is also submitter-dominated

Of the 37 single-country units, **32 have one BioProject at >= 50%** of their
labelled tips and 8 at >= 80%; three are 100% one project.

This corrects a figure I reported earlier. I wrote "only 3 of 37 are also
single-BioProject", which used the strictest possible definition (exactly one
project) and understated the concentration. On a dominance threshold, **the
single-country stratum is overwhelmingly single-study as well**. Those units are
simultaneously one country and largely one submission, and nothing in the data
separates "this lineage is geographically restricted" from "one laboratory
sequenced one cluster". `strain_1_L1_3` is the clearest case: 86% serial-patient
isolates, and single-valued for country.

## 5. What this means for the Methods

1. **State the construct-validity limitation.** BioProject is an administrative
   submission unit, not a designed batch variable. In this collection it ranges
   from one soil sample to a 10-country 55-year panel.
2. **The control is a discriminant, not an adjustment**, and it over-controls
   where the sampling frame is geographic. That is now demonstrated with a
   mechanism, not just asserted.
3. **Do not report the confounded discards as null geographic results.** Report
   them with the conditional within-country test, which already softens 14 of 22
   testable discards.
4. **Do not present the 37 single-country units as geographic evidence.** They
   are untestable for country and 32 of 37 are also submitter-dominated.
5. **A better control exists in principle**: restrict the confounder to projects
   whose design is plausibly a batch, or use collection period and laboratory
   where recorded, rather than the submission accession. Not attempted here.

## 6. What would settle this properly

Characterising the top ten covers 1,591 of 1,914 genomes with a BioProject
(83%), so the picture above is representative rather than a sample of
convenience. What it cannot do is recover design for the untitled containers,
which is where a real limitation remains.

Two things would improve it, neither expensive:

- **Read the primary publications** for the top five projects and record the
  sampling frame in a register, rather than inferring from a title string.
- **Record laboratory and collection period per genome** where the archive has
  them. Both are better batch proxies than the submission accession, and both
  are already partly present in the panel.
