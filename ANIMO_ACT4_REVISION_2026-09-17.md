# Act 4 revision note: replace the act, do not patch it

For the APHL film, render `6067b766-632a-475f-b130-bffa59eeee14`. Written
2026-09-17.

**This is a rebuild, not a re-render.** `NOTES.md` section 3 was right that the two
picture defects it found are layout-only and move no beat. This note is a separate
matter: the act's central claim is wrong and has to be replaced, which moves beats
and changes the act's runtime. Budget accordingly.

The other three items in `NOTES.md` stand unchanged and are not affected by this
note: the Act 3 label collision still needs its layout fix, the word budgets still
need the refit, and the voice still has to be generated and measured before any
delivery re-render.

---

## 1. Why the act cannot ship as built

Two claims in `SPINE.md`, both repeated in its **Accuracy guards** section, are
contradicted by `NUMBERS.tsv` in that file's own notes.

**"Six units clear both. All six are Southeast Asian."**

| the film says | the record says |
|---|---|
| Six units pass the full control | `phylo.spec_ladder`: *"Neither endpoint defensible -- 6 is not the answer with the rest as sensitivity"* |
| All six are Southeast Asian | `phylo.national_passes`: *"They are NOT all Southeast Asian: strain_1_L1_11 is China 8, Thailand 8, Laos 3, Malaysia 2, Portugal 1, USA 1, Israel 1"* |

The manuscript is more explicit still. Results section 8 carries a subheading
reading *The count is a function of the specification*, gives the full ladder
(26 units with no control, 24, 18, 6, then 2), and concludes:

> **We do not report a count of geographically structured units, because we cannot
> defend one.**

So the act reports, as its finding, the number the paper refuses to report. And
`NOTES.md` section 3 found that the standing note **"Six units pass both controls"
sits on screen from 0.5 s to 44 s**, which is the whole act. The wrong number is
not a caption at the end; it is the act's premise, displayed throughout.

This was not a builder error. The brief told the builder to put it there.

---

## 2. What is actually solid in this territory

Three things, all canonical, none contested.

1. **The collection is not a sample of the world.** Thailand is **67%** of the
   analysed set, 1,561 of 2,340 genomes (`phylo.thailand_share_analysed`).
2. **Country and collection history cannot be separated in a collection assembled
   this way.** 113 of 119 BioProjects, **95%**, are entirely single-country, and
   the two variables associate at **Cramer's V 0.857**
   (`phylo.bioproject_nesting`). This *is* the manuscript's reported conclusion,
   as opposed to the count, which is not.
3. **For the Americas it is worse than weak, it is unmeasurable.** All **five**
   Americas-dominated units fall outside the detection window: two below the floor
   at 243 and 211 mean pairwise core SNPs, three above the ceiling
   (`americas.all_outside_window`, "5 of 5"). No Americas-dominated unit passes any
   specification (`phylo.national_passes`).

Point 2 is the strongest thing in this part of the paper and the old act skipped
past it to get to a number. It is also, structurally, a better setup for act 5.

---

## 3. The replacement act

**New title: "Why this collection cannot answer the country question."**

**The claim.** Before asking whether a genome can name a country, this collection
already cannot settle the question: it is concentrated in a few countries, its
studies and its countries are nearly the same variable, and for the Americas the
measurement cannot be made at all.

**The quantity that carries it.** The degree to which country and study are the
same variable, against the degree to which they would have to differ for the
question to be identifiable. One association, read against what it would need to
be. Not a count of units.

**Why motion.** The act is an elimination: three separate reasons stack up and each
one narrows what can still be asked. A still can show three facts side by side; the
viewer has to watch the space close.

### The three beats

**Beat 1, the map is not the world.** Two thirds of the analysed genomes are from
one country. Most public genomes come from a few heavily studied places. You cannot
find structure where nobody has looked.

**Beat 2, the confound, and this is the act's centre.** Ninety-five percent of
sequencing projects in this collection sampled a single country. So when a group of
genomes looks geographically structured, there is no way to tell whether that is
geography or the fact that one study sampled one place. Country and collection
history are not separable here. **State that as the finding.** Do not follow it
with a number of units that survive a control, in either direction.

**Beat 3, the Americas, where the applied question actually lives.** All five
Americas-dominated units fall outside the detection window entirely, two below the
floor and three above the ceiling. For the region the opening question cares about
most, recombination cannot even be measured, let alone geography inferred.

**The pivot, and the act must end here rather than on beat 3.** None of this says
the genome is uninformative. It says the country-level question is not the one this
collection can settle. So ask the question it can: act 5.

- **Inherits:** the window from act 3, used in beat 3 to say what falls outside it.
- **Owes:** act 5's question, now sharpened from "can a genome place a case" to
  "at what resolution can it."

---

## 4. Guards on the replacement

- **Do not state a count of geographically structured units.** Not 6, not 24, not
  a range presented as a result. The paper declines to report one and so does this
  act. If a number of units appears anywhere on screen in this act, the revision
  has failed.
- **Do not say the passing units are all Southeast Asian.** They are not, and with
  beat 2 as written no passing units are named at all.
- **Do not present the sampling bias as a flaw in the study.** It is a property of
  the public record that this collection inherited. The project added 312 genomes
  to it.
- **Do not imply any Americas unit carries a surviving geographic signal.**
- **Beat 3 uses the alignment-derived window, [700, 4700] mean pairwise core
  SNPs.** Never the retired ska 1,270 floor.
- **Reserve solid rendering for measured values.** Everything in this act is
  measured; if any element is a schematic map or a stylised group, mark it.
- **Writing style on screen:** no em dashes, no en dashes, no semicolons, no curly
  quotes, American spelling.

## 5. Runtime and budget

The act was 45.9 s with a refit budget of 75 words at 18% silence. Three beats plus
a pivot will not fit 75 words comfortably; **budget about 90 words and let the
runtime land near 52 to 55 s.** That moves the film from 235.0 s to roughly 241 to
244 s, which is still inside the 4 to 5 minute target in `SPINE.md`.

As everywhere else: the word budget binds, the runtime follows, and both are
provisional until the voice is generated and measured. Do not commission the
runtime against a nominal rate.

## 6. What this does to the rest of the film

- **Act 3 is unaffected** except for its own label-collision fix.
- **Act 5 gets stronger.** Act 4 now ends by narrowing the question rather than by
  answering a different one, so act 5's region result lands as the answer to a
  question the viewer is holding. Act 5's own content does not change.
- **Watch the tone.** Acts 3, 4 and 5 now run limit, limit, limit-then-answer. Act
  4's pivot is what stops the middle of the film reading as a list of things that
  did not work, so it is load-bearing and should not be trimmed for time.
- **One wording fix in act 5 while it is open.** The spine describes country
  attribution as "barely above chance". It is 22% against a 26% baseline, so it is
  at or below chance. "No better than chance" is accurate and is also the stronger
  line.

## 7. You may refuse this

If the material does not support the claim or the quantity, say so and propose what
it does support. The specific risk here is beat 2: an association between two
variables is an abstract thing to draw, and if it cannot be made concrete without
inventing a picture of units passing or failing a test, say so. Beats 1 and 3 carry
the act on their own if beat 2 has to become a single stated sentence over a held
frame.
