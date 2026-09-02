# When adding a control makes the answer worse

**2026-09-02.** Prompted by the author's objection: "adding a control is better
than none" is false if the control can be significantly disputed. That is
correct, and what is wrong with the BioProject control has a specific name.

## 1. BioProject is not a confounder here. It is a descendant of the exposure.

A confounder must be a **common cause** of both the exposure (phylogenetic
position) and the outcome (country label). BioProject is not.

- Does BioProject cause phylogenetic clustering? **Yes** -- related isolates get
  sequenced together.
- Does BioProject cause country? **No. Country causes BioProject.** A study is
  defined by where it sampled. `PRJEB25606` is "Northeast Thailand"; the
  geography came first and the accession was assigned afterwards.

Conditioning on a variable that is **caused by** the exposure is over-adjustment:
it blocks part of the very effect being estimated. This is not a conservative
choice with a wide error bar. It is a mis-specified choice with a **known
direction of error**, and the direction is toward finding no geography.

## 2. This is the actual situation, not a theoretical worry

Four independent pieces of evidence, all already in this repository:

1. **V = 0.857** between BioProject and country; **113 of 119 (95%)** BioProjects
   are entirely single-country. The control variable is close to a relabelling of
   the exposure.
2. **The control fires on the wrong projects.** Of 12 discarded units, four are
   driven by *diversity panels* and five by *geographic frames*. **Zero** are
   driven by an identifiable clonal batch.
3. **The two genuinely batch-like projects drive no discard at all.**
   `PRJNA429426` (single soil sample) is dominant in no unit; `PRJEB2119` (serial
   patient) is 86% of a unit the control cannot even speak about.
4. **12 of the 26 clustered units are discarded despite showing no within-country
   batch structure** when tested directly.

## 3. What the count actually depends on

| rule | units retained |
|---|---|
| no control at all | **26** |
| discount only if FDR-confirmed within-country batch | **24** |
| discount if any nominal within-country batch | **18** |
| **BioProject discriminant (what we currently report)** | **6** |
| + collection period | **2** |

**The discriminant is the outlier, not the consensus.** A correctly specified
control -- one that asks whether batch structure exists *independent of
geography* -- retains 18 to 24 units. The instrument we chose retains 6.

## 4. But that control is underpowered, and I will not over-correct

**64 of 94 unit-country rows (68%) are untestable** by the conditional test, for
want of tips or of distinct BioProjects within a country. Its higher count is
therefore inflated by **absence of evidence**, not by evidence of absence. 18-24
is not "the right answer" either.

I have spent this session repeatedly moving this number down, and the correct
specification moves it up. That deserves the same scepticism as the moves down
received, which is why this section exists.

## 5. Recommendation

1. **Demote the BioProject discriminant to a sensitivity analysis.** Do not
   present it as the primary control. State the over-adjustment argument and the
   evidence in section 2.
2. **Promote the conditional within-country test to the primary control**, and
   report its 68% untestable rate in the same breath. It is the only instrument
   here that asks the right question.
3. **Report the range with its mechanism, not a point estimate.** The defensible
   statement is that between 6 and 24 units show country structure depending on
   whether the control is specified as a discriminant on a
   geography-determined variable or as a test of batch structure independent of
   geography, and that neither instrument resolves it.
4. **Do not add further controls.** Each one is another filter, and the ones
   available are all entangled with geography to some degree. More controls will
   lower the count without improving the estimate.

## 6. The general lesson, which belongs in the Discussion

A control is only conservative if it is correctly specified. Where the candidate
control is largely determined by the exposure -- as submission accession is by
sampling location -- **conditioning on it does not widen the error bar, it
relocates the estimate**. In a field that routinely treats BioProject as a batch
proxy, that is worth saying out loud.
