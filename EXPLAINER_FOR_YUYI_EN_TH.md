# How the B. pseudomallei SNP phylogeny project works
# โปรเจกต์ SNP phylogeny ของเชื้อ B. pseudomallei ทำงานอย่างไร

For Yuyi — from the beginning, through to the finished results of 19 August 2026.
Technical terms are kept in English throughout.

สำหรับยูยี่ — อธิบายตั้งแต่ต้น จนถึงผลลัพธ์ที่เสร็จสมบูรณ์ (19 สิงหาคม 2026)
คำศัพท์ technical จะคงไว้เป็นภาษาอังกฤษทั้งหมด

---

## 1. What question are we trying to answer?

People get melioidosis from *Burkholderia pseudomallei*, a bacterium that lives
in soil and water. When a patient turns up in the United States or elsewhere in
the Americas with melioidosis and **no travel history**, the obvious question is:
where did this come from? Imported soil? A contaminated product? A local
environmental source that nobody knew about?

If we have the patient's isolate sequenced, we can try to answer that by asking
which known genomes it is most closely related to, and where those came from.
That is the applied goal of this project: **rapid origin-of-exposure attribution
for cases without travel history.**

### 1. เราพยายามตอบคำถามอะไร

โรค melioidosis เกิดจากเชื้อ *Burkholderia pseudomallei* ซึ่งอยู่ในดินและน้ำ
เมื่อมีผู้ป่วยในสหรัฐฯ หรือในทวีปอเมริกาที่เป็น melioidosis โดย**ไม่มีประวัติการเดินทาง**
คำถามที่ตามมาคือ เชื้อนี้มาจากไหน? ดินที่นำเข้ามา? ผลิตภัณฑ์ที่ปนเปื้อน?
หรือมีแหล่งเชื้อในสิ่งแวดล้อมท้องถิ่นที่เรายังไม่รู้?

ถ้าเรามี genome ของเชื้อจากผู้ป่วย เราสามารถตอบได้โดยดูว่า genome นั้นใกล้ชิดกับ
genome ไหนที่เรารู้ที่มาแล้วบ้าง เป้าหมายเชิงประยุกต์ของโครงการนี้คือ
**การระบุแหล่งที่มาของการรับเชื้อ (origin attribution) อย่างรวดเร็ว สำหรับผู้ป่วยที่ไม่มีประวัติการเดินทาง**

---

## 2. Why this is harder than it sounds: recombination

Normally you build a phylogenetic tree by finding the SNPs (single-nucleotide
differences) between genomes and assuming that genomes sharing more SNPs are
more closely related by descent.

*B. pseudomallei* breaks that assumption. It is **highly recombinogenic** — it
swaps chunks of DNA with other members of its own species. Its genome is ~7.2 Mbp
across **two chromosomes** (we call them replicons). When a genome imports a
recombinant block from a distant relative, that block carries a large number of
SNPs all at once. A naive tree reads those SNPs as evidence of shared ancestry
and pulls two unrelated genomes together.

So before we can trust a tree, we must **identify and remove the recombinant
regions**. The tool for that is **Gubbins**.

But Gubbins has an important limitation, and it drives the entire design of this
project: Gubbins works by finding regions with an unusually high density of SNPs
relative to the rest of the alignment. If you give it an alignment containing
several distinct sub-populations lumped together, the *genuine* between-population
differences look like high-density SNP regions, and Gubbins calls them
recombination. The result is an inflated **r/m** (the ratio of SNPs introduced by
recombination to those introduced by mutation) that is precise but wrong.

We have measured this in this very project: one early run analysed 35 large
PopPUNK strains whole and returned r/m = 10.31 for one of them, against a maximum
of 6.28 from careful manual analysis — with both replicons agreeing to four
significant figures. Agreement between replicons shows the estimate is *precise*.
It does not show it is *valid*.

### 2. ทำไมถึงยากกว่าที่คิด: recombination

ปกติเราสร้าง phylogenetic tree โดยหา SNPs (ความแตกต่างระดับ nucleotide เดี่ยว)
ระหว่าง genome แล้วสมมติว่า genome ที่มี SNPs เหมือนกันมากกว่า ก็มีบรรพบุรุษร่วมกันใกล้กว่า

แต่ *B. pseudomallei* ทำให้สมมติฐานนี้ใช้ไม่ได้ เพราะมี **recombination สูงมาก**
คือแลกเปลี่ยนชิ้นส่วน DNA กับเชื้อตัวอื่นในสปีชีส์เดียวกัน genome มีขนาดราว 7.2 Mbp
อยู่บน **chromosome สองแท่ง** (เราเรียกว่า replicons) เมื่อ genome หนึ่งรับ recombinant block
จากญาติห่าง ๆ เข้ามา block นั้นจะพา SNPs จำนวนมากเข้ามาพร้อมกัน
tree ที่สร้างแบบตรงไปตรงมาจะตีความว่านั่นคือหลักฐานของบรรพบุรุษร่วม
แล้วดึง genome สองตัวที่ไม่เกี่ยวกันให้มาอยู่ใกล้กัน

ดังนั้นก่อนจะเชื่อ tree ได้ เราต้อง **หาและตัด recombinant regions ออกก่อน**
เครื่องมือที่ใช้คือ **Gubbins**

แต่ Gubbins มีข้อจำกัดสำคัญ ซึ่งเป็นตัวกำหนดการออกแบบทั้งหมดของโครงการนี้:
Gubbins ทำงานโดยหาบริเวณที่มีความหนาแน่นของ SNPs สูงผิดปกติเมื่อเทียบกับส่วนที่เหลือของ alignment
ถ้าเราป้อน alignment ที่มี sub-population หลายกลุ่มปนกันเข้าไป ความแตกต่าง*จริง*ระหว่างกลุ่ม
จะดูเหมือนบริเวณ SNP หนาแน่น แล้ว Gubbins จะเรียกมันว่า recombination
ผลคือค่า **r/m** (อัตราส่วนของ SNPs ที่มาจาก recombination ต่อที่มาจาก mutation) จะสูงเกินจริง —
แม่นยำ (precise) แต่ผิด

เราเคยวัดเรื่องนี้ในโครงการนี้เอง: การรันครั้งแรกวิเคราะห์ PopPUNK strain ขนาดใหญ่ 35 กลุ่มทั้งก้อน
ได้ r/m = 10.31 ในกลุ่มหนึ่ง เทียบกับค่าสูงสุด 6.28 จากการวิเคราะห์ด้วยมืออย่างระมัดระวัง
และ replicon ทั้งสองให้ค่าตรงกันถึงทศนิยม 4 ตำแหน่ง
การที่ replicon สองแท่งให้ค่าตรงกันแสดงว่าค่านั้น *precise* — แต่ไม่ได้แสดงว่า *valid*

---

## 3. The core design: partition first, then Gubbins

The whole pipeline follows from that. **We never hand Gubbins a mixed
population.** Instead we first cut the collection into groups that are genuinely
closely related — we call these **analysis units** — and run Gubbins separately
inside each one.

The rule is applied uniformly, which matters for defensibility:

- **PopPUNK** defines *strains* from whole-genome distances.
- **fastbaps** (run through **PopPIPE**) subdivides *within* each strain.
- An **analysis unit** is a fastbaps level-1 subcluster kept at **n ≥ 7**.

A strain that fastbaps does not split becomes one unit. No strain is subdivided
just because it is big, and none is left whole just because it is small. That
uniformity is deliberate: subdividing only the inconvenient strains would be a
post-hoc, size-based cut that a reviewer would rightly reject.

The n ≥ 7 floor exists because Gubbins needs other taxa to detect recombination
*against*. A cluster of one or two genomes cannot produce a meaningful result.

### 3. หลักการออกแบบ: แบ่งกลุ่มก่อน แล้วค่อย Gubbins

ทั้ง pipeline ออกแบบตามหลักนี้ **เราไม่เคยป้อน population ที่ปนกันให้ Gubbins**
แต่จะแบ่งชุดข้อมูลออกเป็นกลุ่มที่ใกล้ชิดกันจริง ๆ ก่อน เรียกว่า **analysis units**
แล้วรัน Gubbins แยกกันในแต่ละกลุ่ม

กฎนี้ใช้อย่างสม่ำเสมอกับทุกกลุ่ม ซึ่งสำคัญมากต่อความน่าเชื่อถือ:

- **PopPUNK** กำหนด *strains* จากระยะห่างระดับ whole-genome
- **fastbaps** (รันผ่าน **PopPIPE**) แบ่งย่อย *ภายใน* แต่ละ strain
- **analysis unit** คือ fastbaps level-1 subcluster ที่มีสมาชิก **n ≥ 7**

strain ที่ fastbaps ไม่แบ่ง ก็จะกลายเป็น unit เดียว
ไม่มี strain ไหนถูกแบ่งเพียงเพราะใหญ่ และไม่มี strain ไหนถูกปล่อยทั้งก้อนเพียงเพราะเล็ก
ความสม่ำเสมอนี้ตั้งใจ เพราะถ้าเลือกแบ่งเฉพาะ strain ที่ไม่สะดวก
จะกลายเป็นการตัดตามขนาดแบบ post-hoc ซึ่ง reviewer ปฏิเสธได้อย่างถูกต้อง

เหตุที่ตั้งเกณฑ์ n ≥ 7 เพราะ Gubbins ต้องมี taxa อื่นไว้*เปรียบเทียบ*เพื่อตรวจจับ recombination
กลุ่มที่มี genome เดียวหรือสองตัวให้ผลที่มีความหมายไม่ได้

---

## 4. The data — how the panel was built

The panel is **2,976 assemblies**:

| source | n |
|---|---|
| established curated collection | 2,802 |
| new additions assembled with SPAdes | 169 |
| new additions from other assemblers | 5 |

The 5 are interesting and worth understanding, because they illustrate how
assembly choices are made per isolate rather than by blanket rule:

- **3 SKESA assemblies.** SPAdes failed on these. For two of them the library
  insert size (145 bp) was *shorter than the read length* (151 bp), so read pairs
  overlapped completely and read through into adapter; the pipeline also runs
  SPAdes with `--only-assembler`, which skips BayesHammer error correction.
  SPAdes collapsed to 4.3 Mb where SKESA produced 6.96 Mb. For the third, SPAdes
  assembled 11.88 Mb — revealing contamination that SKESA had quietly suppressed.
- **2 Oxford Nanopore assemblies.** These had no short-read counterpart at all,
  so there was nothing to swap.

Assemblies are gated on **core-genome coverage** and **gene-count ratio**, not on
length or contiguity. That choice was deliberate: a fragmented assembly is not
necessarily a bad one, and a contiguous assembly is not necessarily a good one.

### 4. ข้อมูลที่ใช้ — panel ถูกสร้างขึ้นมาอย่างไร

panel ประกอบด้วย **2,976 assemblies**:

| แหล่งที่มา | จำนวน |
|---|---|
| collection เดิมที่ curate ไว้แล้ว | 2,802 |
| ตัวอย่างใหม่ที่ assemble ด้วย SPAdes | 169 |
| ตัวอย่างใหม่จาก assembler อื่น | 5 |

ห้าตัวอย่างนี้น่าสนใจและควรเข้าใจ เพราะแสดงให้เห็นว่าการเลือก assembler
ทำเป็นราย isolate ตามหลักฐาน ไม่ใช่ใช้กฎเดียวกันหมด:

- **3 ตัวอย่างใช้ SKESA** เพราะ SPAdes ล้มเหลว สองตัวมี library insert (145 bp)
  *สั้นกว่า* read length (151 bp) ทำให้ read pair ซ้อนทับกันทั้งหมดและอ่านทะลุเข้าไปใน adapter
  ประกอบกับ pipeline รัน SPAdes ด้วย `--only-assembler` ซึ่งข้าม BayesHammer error correction
  SPAdes จึงยุบเหลือ 4.3 Mb ขณะที่ SKESA ได้ 6.96 Mb
  ส่วนตัวที่สาม SPAdes assemble ได้ 11.88 Mb ซึ่งเผยให้เห็น contamination ที่ SKESA กลบไว้
- **2 ตัวอย่างเป็น Oxford Nanopore** ซึ่งไม่มี short-read คู่กันเลย จึงไม่มีอะไรให้สลับ

เกณฑ์ QC ของ assembly ใช้ **core-genome coverage** และ **gene-count ratio**
ไม่ใช้ความยาวหรือ contiguity ซึ่งเป็นการเลือกโดยตั้งใจ
เพราะ assembly ที่แตกเป็นชิ้นไม่ได้แปลว่าแย่เสมอไป และ assembly ที่ต่อเนื่องก็ไม่ได้แปลว่าดีเสมอไป

---

## 5. The pipeline, end to end

```
2,976 assemblies
      |
      v
  Mash sketches  ->  distance matrix
      |
      v
  PopPUNK  (sketch db, bgmm K=5 + refine)   ->  310 strains, largest 901 genomes
      |
      v
  PopPIPE per strain:  SKA alignment -> NJ guide tree -> fastbaps (levels=3)
      |
      v
  Analysis units = fastbaps L1 subclusters at n >= 7   ->  86 units
      |
      v
  Reference selection per unit  (<= 2 contigs, most central, blocklist applied)
      |
      v
  Snippy: map every member to its unit reference  ->  core alignment per replicon
      |
      v
  Gubbins: remove recombinant blocks  (5 iterations, min 3 SNPs)
      |
      v
  IQ-TREE: ML tree per unit, ascertainment-bias corrected, with branch support
```

Two details that are easy to miss but matter a great deal:

**Replicons are split before Gubbins.** The two chromosomes are separate
molecules with different histories. Concatenating them and letting Gubbins scan
across the junction would create an artefact at the boundary. We also drop
replicons below 100 kb, which removes small plasmid-like contigs that would
otherwise be treated as chromosomes.

**Reference deflines are normalised.** Gubbins passes a run id of the form
`<unit>__<replicon>.core.full.iteration_N_reconstruction` to RAxML. RAxML v8
**segfaults** at a run id of 128 characters or more — and crashes before printing
its own error, so Gubbins reports only "Unable to fit model to data", which looks
exactly like a bad reference genome. On the current partition, **42 of 172
replicon-units (24%) would have exceeded that limit.** After normalisation the
longest run id is 70 characters.

### 5. ภาพรวม pipeline ตั้งแต่ต้นจนจบ

(ดูแผนภาพด้านบน — ขั้นตอนเดียวกัน)

รายละเอียดสองข้อที่มองข้ามง่ายแต่สำคัญมาก:

**แยก replicon ก่อนเข้า Gubbins** chromosome สองแท่งเป็นโมเลกุลคนละอันและมีประวัติต่างกัน
ถ้าต่อกันแล้วปล่อยให้ Gubbins สแกนข้ามรอยต่อ จะเกิด artefact ตรงรอยต่อนั้น
เราตัด replicon ที่เล็กกว่า 100 kb ออกด้วย เพื่อไม่ให้ contig เล็ก ๆ คล้าย plasmid
ถูกนับเป็น chromosome

**ต้อง normalise reference deflines** Gubbins ส่ง run id รูปแบบ
`<unit>__<replicon>.core.full.iteration_N_reconstruction` ให้ RAxML
และ RAxML v8 จะ **segfault** เมื่อ run id ยาวตั้งแต่ 128 ตัวอักษรขึ้นไป
โดย crash ก่อนจะพิมพ์ error ของตัวเอง ทำให้ Gubbins รายงานแค่ "Unable to fit model to data"
ซึ่งดูเหมือน reference genome เสีย ทั้งที่ไม่ใช่
ใน partition ปัจจุบัน **42 จาก 172 replicon-units (24%) จะเกินเกณฑ์นี้**
หลัง normalise แล้ว run id ที่ยาวที่สุดเหลือ 70 ตัวอักษร

---

## 6. Why there are so many versions (v3, v4, v4b, v4c)

Each version is a re-partition, not a re-analysis of the same partition. The
panel grew and the partition method was corrected:

- **v3** — 91 units. Valid, but the panel was smaller.
- **v4** — the panel was merged with the validation set, but was accidentally
  partitioned on the *analysis subset* (2,466) instead of the full collection,
  dropping 521 genomes including 4 of 5 Mississippi isolates.
- **v4b** — 2,973 genomes, 95 units. Full fastbaps re-run on every strain, so no
  archived labels were carried over anywhere.
- **v4c** — 2,976 genomes (7 rescued isolates added), 86 units. Coverage rose
  from 77.7% to 79.0%.

An important subtlety, and one that caused confusion this week: **strain labels
are not comparable between versions.** PopPUNK assigns numbers per fit. v4b's
`strain_4` and v4c's `strain_4` share zero members — all 261 genomes from v4b's
`strain_4` sit inside v4c's `strain_1`. If you want to compare two versions, you
must compare **unit membership**, never labels. Done that way, 66 of v4b's 95
units are exactly identical in v4c.

### 6. ทำไมถึงมีหลาย version (v3, v4, v4b, v4c)

แต่ละ version คือการ re-partition ใหม่ ไม่ใช่การวิเคราะห์ partition เดิมซ้ำ
panel ใหญ่ขึ้นเรื่อย ๆ และวิธี partition ก็ถูกแก้ให้ถูกต้องขึ้น:

- **v3** — 91 units ใช้ได้ แต่ panel เล็กกว่า
- **v4** — รวม validation set เข้ามา แต่เผลอ partition บน *analysis subset* (2,466)
  แทนที่จะเป็น collection เต็ม ทำให้หายไป 521 genome รวมถึง Mississippi 4 จาก 5 ตัว
- **v4b** — 2,973 genomes, 95 units รัน fastbaps ใหม่ทุก strain จึงไม่มี label เก่าหลงเหลือ
- **v4c** — 2,976 genomes (เพิ่มตัวอย่างที่กู้กลับมา 7 ตัว), 86 units
  coverage เพิ่มจาก 77.7% เป็น 79.0%

ข้อควรระวังที่สำคัญและเพิ่งทำให้สับสนเมื่อสัปดาห์นี้:
**label ของ strain เทียบข้าม version ไม่ได้** PopPUNK ให้หมายเลขใหม่ทุกครั้งที่ fit
`strain_4` ของ v4b กับ `strain_4` ของ v4c ไม่มีสมาชิกร่วมกันเลยแม้แต่ตัวเดียว —
genome ทั้ง 261 ตัวจาก `strain_4` ของ v4b ไปอยู่ใน `strain_1` ของ v4c ทั้งหมด
ถ้าจะเทียบสอง version ต้องเทียบที่ **สมาชิกของ unit** ไม่ใช่ที่ label
เมื่อเทียบแบบนั้นแล้ว 66 จาก 95 units ของ v4b เหมือนกันทุกประการใน v4c

---

## 7. How do we know a unit is the right size?

This is the part that took the longest to work out, and it is the key to reading
any r/m number correctly.

Gubbins works by spotting regions where SNPs are unusually **dense** compared
with the rest of the genome. That only works if the unit sits in a particular
range of diversity:

- **Too tight** (the genomes are nearly identical) — there are almost no SNPs
  anywhere, so there is no dense-versus-sparse contrast to find. Gubbins detects
  essentially no recombination.
- **Too diverse** (the genomes are only distantly related) — SNPs are dense
  *everywhere*, so nothing stands out as unusual. The estimate collapses.
- **In the middle** — recombinant blocks stand out against a clonal background,
  and the estimate is meaningful.

The field's stated rule is to subdivide "until diversity falls within the limit
of recombination detection", but **Gubbins publishes no such limit** — we checked
the paper, the manual, the docs and the manpage. So we measured it ourselves on
this dataset. The usable window is roughly **1,270–4,671 mean pairwise core
SNPs**. Both edges are brackets, not constants, and we report them as such.

**The consequence is the single most important thing to understand about our
results: a LOW r/m is not good news. It usually means the measurement failed.**

Because the failure is symmetric — collapse at both ends — a low number looks the
same whether the unit is too tight or too diverse. You cannot tell from the r/m
alone; you have to check where the unit sits in the window.

When we classified all 88 units in the final run:

| where the unit sits | units | median r/m |
|---|---|---|
| **inside the window** | **47** | **7.38** |
| below the floor (too tight) | 9 | 1.67 |
| above the ceiling (too diverse) | 32 | 2.48 |

That is exactly the U-shape predicted: high in the middle, collapsed at both
ends. So **the recombination result we report is r/m ≈ 7.38, from the 47 units
where it is actually measurable** — not the median of all 88 (5.70), which mixes
real measurements with failed ones.

The other 41 units are still used for the trees and for the geography analysis,
where being outside the Gubbins window does not matter. **We just do not quote
their r/m.**

There is a second gate, applied **after** this one: **modality** — is the unit one
population, or two clumps stuck together? The order matters. On a very tight
unit, a single divergent genome makes the modality statistic enormous, so
checking modality first gives misleading answers. And below **n = 25** modality
cannot be decided at all with this data.

### 7. เรารู้ได้อย่างไรว่า unit มีขนาดเหมาะสม

ส่วนนี้ใช้เวลานานที่สุดกว่าจะหาคำตอบได้ และเป็นกุญแจสำคัญในการอ่านค่า r/m ให้ถูกต้อง

Gubbins ทำงานโดยมองหาบริเวณที่ SNP **หนาแน่น**ผิดปกติเมื่อเทียบกับส่วนอื่นของ genome
วิธีนี้จะได้ผลก็ต่อเมื่อ unit นั้นมีความหลากหลาย (diversity) อยู่ในช่วงที่เหมาะสม:

- **แน่นเกินไป** (genome เกือบเหมือนกันหมด) — แทบไม่มี SNP เลย จึงไม่มีความต่าง
  ระหว่างบริเวณหนาแน่นกับเบาบางให้จับได้ Gubbins แทบตรวจไม่พบ recombination
- **หลากหลายเกินไป** (genome ห่างกันมาก) — SNP หนาแน่น*ไปหมดทุกที่* จึงไม่มีอะไรโดดออกมา
  ค่าที่ประมาณได้จะพังลง
- **อยู่ตรงกลาง** — recombinant block จะโดดเด่นออกมาจากพื้นหลังที่เป็น clonal
  ค่าที่ได้จึงมีความหมาย

ในวงการมีการบอกให้แบ่งกลุ่มย่อย "จนกว่า diversity จะอยู่ในขีดจำกัดที่ตรวจ recombination ได้"
แต่ **Gubbins ไม่ได้ประกาศขีดจำกัดนั้นไว้เลย** — เราตรวจทั้ง paper, manual, เอกสาร และ manpage แล้ว
เราจึงวัดเองจากชุดข้อมูลนี้ ช่วงที่ใช้งานได้อยู่ที่ประมาณ
**1,270–4,671 mean pairwise core SNPs** ขอบทั้งสองด้านเป็นช่วงคร่าว ๆ ไม่ใช่ค่าคงที่
และเรารายงานตามนั้น

**ผลที่ตามมาคือสิ่งสำคัญที่สุดที่ต้องเข้าใจเกี่ยวกับผลลัพธ์ของเรา:
ค่า r/m ที่ต่ำ ไม่ใช่ข่าวดี โดยทั่วไปมันแปลว่าการวัดล้มเหลว**

เนื่องจากความล้มเหลวเกิดได้ทั้งสองด้าน ค่าต่ำจึงหน้าตาเหมือนกันไม่ว่า unit จะแน่นเกินไป
หรือหลากหลายเกินไป ดูจากค่า r/m อย่างเดียวแยกไม่ออก ต้องดูว่า unit อยู่ตรงไหนของช่วงด้วย

เมื่อเราจำแนก unit ทั้ง 88 อันในการรันครั้งสุดท้าย:

| unit อยู่ตรงไหน | จำนวน | median r/m |
|---|---|---|
| **อยู่ในช่วง** | **47** | **7.38** |
| ต่ำกว่าพื้น (แน่นเกินไป) | 9 | 1.67 |
| สูงกว่าเพดาน (หลากหลายเกินไป) | 32 | 2.48 |

นี่คือรูปตัว U ตามที่ทำนายไว้พอดี — สูงตรงกลาง และพังลงทั้งสองปลาย
ดังนั้น **ผลเรื่อง recombination ที่เรารายงานคือ r/m ≈ 7.38 จาก 47 units
ที่วัดได้จริง** ไม่ใช่ median ของทั้ง 88 units (5.70) ซึ่งเอาค่าที่วัดได้จริง
ปนกับค่าที่วัดล้มเหลว

อีก 41 units ยังใช้สร้าง tree และใช้ในการวิเคราะห์เชิงภูมิศาสตร์ได้ตามปกติ
เพราะการอยู่นอกช่วงของ Gubbins ไม่มีผลกับงานส่วนนั้น **เราแค่ไม่อ้างอิงค่า r/m ของมัน**

ยังมี gate ที่สอง ซึ่งใช้**หลังจาก** gate แรกนี้ คือ **modality** — unit นี้เป็นประชากรเดียว
หรือเป็นสองก้อนที่ติดกันอยู่? ลำดับสำคัญมาก เพราะใน unit ที่แน่นมาก
genome ที่แตกต่างเพียงตัวเดียวจะทำให้ค่าสถิติ modality สูงผิดปกติ
ถ้าตรวจ modality ก่อนจะได้คำตอบที่ทำให้เข้าใจผิด และถ้า **n ต่ำกว่า 25**
ข้อมูลชุดนี้ตัดสิน modality ไม่ได้เลย

---
## 8. What happened on 19 August 2026

The workstation at home has only 62 GB of RAM, and `ska build` on a 901-genome
strain needs 500–600 GB. So the partitioning work moved to the **DGX Station
A100** (128 cores, 503 GB RAM). Today's session on the A100 did four things:

**Fixed a bug that had silently killed the previous run.** The references file
was written with Windows line endings (`\r\n`) because Python's `csv` writer
defaults to that. A shell loop then read each path with the `\r` still attached,
so every file looked missing; the error-reporting code piped its output to
`head -3`, which closed the pipe after three lines, and the fourth write raised
**SIGPIPE**. Under `set -o pipefail` that killed the script one line before it
would have printed the explanation. **The check written to report the problem is
what silenced it.** Signature to remember: exit code 141 with a zero-byte log
means SIGPIPE in the shell, not a failed tool.

**Checked the two ONT assemblies.** Both had a gene-count ratio just above 1
(1.08 and 1.06), which is the residual-indel signature — but they passed the
≤1.20 gate. We ran **BUSCO** against contiguity-matched controls, and that is
what made the answer unambiguous: three *complete* two-contig genomes scored 688
complete, 0 fragmented, 0 missing. The two ONT assemblies also have two contigs —
yet scored 654/22/12 and 623/44/21. Since contiguity cannot explain a fragmented
BUSCO in a two-contig assembly, the deficit must be base-level error: frameshifts
from residual indels truncating genes. `SRR28096039` was excluded.

The lesson generalises: **the ≤1.20 gene-count-ratio gate has no power on a
near-complete assembly**, because it was calibrated on fragmented PacBio CLR
failures at ≥1.35, where contiguity was doing part of the work.

**Checked whether the v4c partition was actually worse.** The plan was to re-fit
PopPUNK from scratch. On inspection, that would have changed nothing — PopPUNK's
`bgmm` fit is deterministic for a given input and exposes no random seed, so
re-running it reproduces the same answer. Instead we used the pairwise distances
already sitting in the PopPUNK database (all 4,426,800 of them) to ask a sharper
question: *which units actually contain separated sub-populations?*

The answer was counter-intuitive. Overall diversity told us nothing. What
mattered was **modality** — whether a unit's internal distance distribution has
two peaks. `strain_1_L1_26` is one of the *tightest* units in the whole panel
(median distance 0.00060) and yet contains three distinct clonal groups. Whereas
`strain_1_L1_35`, the most diverse of the suspect units, turned out to be a
single uniformly diverse population that was fine to leave alone.

**Launched the definitive run.** We split `strain_1_L1_26` into three, removed a
handful of divergent members from two other units, dropped `SRR28096039`, and
started the SNP pipeline on **88 units / 2,342 genomes**.

### 8. เกิดอะไรขึ้นในวันที่ 19 สิงหาคม 2026

workstation ที่บ้านมี RAM เพียง 62 GB แต่ `ska build` บน strain ที่มี 901 genome
ต้องใช้ 500–600 GB งาน partition จึงย้ายมาที่ **DGX Station A100** (128 cores, RAM 503 GB)
วันนี้เราทำสี่เรื่อง:

**แก้ bug ที่ฆ่าการรันครั้งก่อนแบบเงียบ ๆ** ไฟล์ references ถูกเขียนด้วย line ending
แบบ Windows (`\r\n`) เพราะ `csv` writer ของ Python ตั้งค่าเริ่มต้นเป็นแบบนั้น
แล้ว shell loop อ่าน path โดยยังมี `\r` ติดมาด้วย ทำให้ทุกไฟล์ดูเหมือนหายไป
โค้ดที่ทำหน้าที่รายงาน error ส่ง output ผ่าน `head -3` ซึ่งปิด pipe หลังจากสามบรรทัด
การเขียนบรรทัดที่สี่จึงเกิด **SIGPIPE** และภายใต้ `set -o pipefail` script ก็ตาย
ก่อนถึงบรรทัดที่จะพิมพ์คำอธิบายพอดี — **โค้ดที่เขียนไว้เพื่อรายงานปัญหา กลายเป็นตัวที่ปิดปากปัญหาเสียเอง**
ลายเซ็นที่ต้องจำ: exit code 141 พร้อม log ขนาด 0 byte = SIGPIPE ใน shell ไม่ใช่เครื่องมือทำงานล้มเหลว

**ตรวจสอบ ONT assemblies สองตัว** ทั้งคู่มี gene-count ratio สูงกว่า 1 เล็กน้อย (1.08 และ 1.06)
ซึ่งเป็นลายเซ็นของ residual indel แต่ผ่านเกณฑ์ ≤1.20
เราจึงรัน **BUSCO** เทียบกับ control ที่มี contiguity เท่ากัน ซึ่งทำให้คำตอบชัดเจน:
genome ที่ *สมบูรณ์* และมี 2 contigs สามตัว ได้ 688 complete, 0 fragmented, 0 missing
ส่วน ONT assemblies ก็มี 2 contigs เหมือนกัน แต่ได้ 654/22/12 และ 623/44/21
เมื่อ contiguity อธิบาย fragmented BUSCO ใน assembly ที่มีแค่ 2 contigs ไม่ได้
ส่วนที่ขาดไปจึงต้องมาจาก base-level error คือ frameshift จาก residual indel ที่ตัดยีนขาด
เราจึงตัด `SRR28096039` ออก

บทเรียนที่ใช้ได้ทั่วไป: **เกณฑ์ gene-count ratio ≤1.20 ไม่มีพลังจำแนกกับ assembly ที่เกือบสมบูรณ์**
เพราะถูก calibrate จาก PacBio CLR ที่ล้มเหลวและแตกเป็นชิ้นที่ค่า ≥1.35
ซึ่งตอนนั้น contiguity ช่วยทำงานอยู่ส่วนหนึ่ง

**ตรวจสอบว่า partition ของ v4c แย่ลงจริงหรือไม่** แผนเดิมคือ re-fit PopPUNK ใหม่ทั้งหมด
แต่เมื่อตรวจดูแล้วพบว่าทำไปก็ไม่เปลี่ยนอะไร เพราะ `bgmm` fit ของ PopPUNK
ให้ผลเหมือนเดิมทุกครั้งสำหรับ input เดียวกัน และไม่มี random seed ให้ตั้ง
เราจึงใช้ pairwise distances ที่มีอยู่แล้วใน PopPUNK database (ทั้งหมด 4,426,800 คู่)
เพื่อถามคำถามที่คมกว่า: *unit ไหนบ้างที่มี sub-population แยกกันจริง ๆ อยู่ข้างใน?*

คำตอบขัดกับสัญชาตญาณ ความหลากหลายโดยรวมไม่ได้บอกอะไรเลย
สิ่งที่สำคัญคือ **modality** — การกระจายของระยะห่างภายใน unit มีสองยอดหรือไม่
`strain_1_L1_26` เป็นหนึ่งใน unit ที่ *แน่นที่สุด* ใน panel (median 0.00060)
แต่กลับมี clonal group แยกกันชัดเจนถึงสามกลุ่มอยู่ข้างใน
ขณะที่ `strain_1_L1_35` ซึ่งหลากหลายที่สุดในกลุ่มที่น่าสงสัย กลับเป็น population เดียว
ที่หลากหลายอย่างสม่ำเสมอ และปล่อยไว้ได้เลย

**เริ่มการรันชุดสมบูรณ์** เราแบ่ง `strain_1_L1_26` เป็นสามส่วน
ตัดสมาชิกที่ห่างออกไปจากอีกสอง unit ตัด `SRR28096039` ออก
แล้วเริ่มรัน SNP pipeline บน **88 units / 2,342 genomes**

---

## 9. What we actually found — and the prediction that failed

Both runs finished cleanly: the A100's 88-unit run (176/176 replicon-units) and
the workstation's 86-unit control (172/172), each with **zero task failures** and
every unit at the highest confidence tier. Nothing had to be re-run.

**The two runs agree, and that is what makes everything else measurable.** 82
units have identical membership in both. Across those, r/m agrees to a median
difference of **0.38%**. Two different machines, two different resource
configurations, same answer — so where the two runs *do* differ, the difference
is real and not noise.

**The prediction in section 8 was falsifiable, and it did not hold.** The
reasoning was: the big lumped unit `strain_1_L1_26` should show an inflated r/m
before it was split, and lower values after. What we measured:

| | n | ~diversity | r/m | inside the window? |
|---|---|---|---|---|
| **before the split** | 154 | 3,421 | 3.10 | **yes — a valid measurement** |
| after — `strain_1_L1_26` | 98 | 955 | 1.07 | no, too tight |
| after — `strain_1_L1_36` | 47 | 3,374 | **6.68** | **yes** |
| after — `strain_1_L1_37` | 8 | 229 | 2.63 | no, too tight (and n < 25) |

The unit before splitting was **not inflated at all** — 3.10 sits below the
average, and it was comfortably inside the window. Meanwhile one of the pieces
came out *higher* than the original. The split took one measurable unit and
produced one measurable unit plus two clonal expansions that are too tight to
measure.

**This does not mean the split was wrong.** The population structure it found was
real: three tight clonal groups inside one unit. But it means we describe it
differently. `strain_1_L1_36` gives us a recombination result; the other two
pieces are reported as **identified clonal expansions — interesting
epidemiologically, probably an outbreak or a heavily-sampled sublineage, but with
no r/m attached.** The project's own earlier notes describe exactly this pattern,
so there is precedent for reporting it that way.

Two related corrections, both from the same cause:

- `strain_1_L1_35` (r/m 1.31) and `strain_4_L1_3` (r/m 0.75) were read as
  evidence that leaving them alone was right, because their r/m was low. In fact
  they sit **1.9× and 2.8× above the ceiling** — their low values are collapse,
  not cleanliness. Leaving them intact was still the right call, just not for
  that reason.
- Both ONT genomes are now excluded. `SRR28096043` was kept and flagged; its
  branch in the tree turned out to be **38–59× longer than the longest Illumina
  branch in the same unit** — same soil, same batch, same reference, only the
  sequencing platform differs. BUSCO agreed independently (654 complete / 22
  fragmented / 12 missing, against 688 / 0 / 0 for complete genomes). Two
  different kinds of evidence, one conclusion.

**Why this happened is worth knowing:** the A100 session did excellent work but
**did not have the methods document** — it lives on the workstation and was in no
bundle. That document is where the diversity window in section 7 is written down.
Without it, the refinement was designed on modality evidence alone. Not a mistake
in reasoning; a missing input.

### 9. เราพบอะไรจริง ๆ — และคำทำนายที่ไม่เป็นจริง

การรันทั้งสองครั้งจบเรียบร้อย: A100 รัน 88 units (176/176 replicon-units)
และ workstation รัน 86 units เป็นตัวควบคุม (172/172) โดย**ไม่มี task ไหนล้มเหลวเลย**
และทุก unit อยู่ใน confidence tier สูงสุด ไม่ต้องรันซ้ำเลยแม้แต่อันเดียว

**การรันสองครั้งให้ผลตรงกัน และนั่นคือสิ่งที่ทำให้วัดอย่างอื่นได้** มี 82 units
ที่มีสมาชิกเหมือนกันทั้งสองครั้ง ค่า r/m ของกลุ่มนี้ต่างกันเพียง median **0.38%**
คนละเครื่อง คนละ resource config แต่ได้คำตอบเดียวกัน — ดังนั้นตรงไหนที่ผลต่างกัน
ความต่างนั้นเป็นของจริง ไม่ใช่ noise

**คำทำนายในหัวข้อ 8 พิสูจน์ได้ว่าผิด และมันผิดจริง** เหตุผลเดิมคือ unit ใหญ่ที่ปนกัน
(`strain_1_L1_26`) ควรมี r/m สูงผิดปกติก่อนแบ่ง และควรต่ำลงหลังแบ่ง สิ่งที่วัดได้จริง:

| | n | ~diversity | r/m | อยู่ในช่วงไหม |
|---|---|---|---|---|
| **ก่อนแบ่ง** | 154 | 3,421 | 3.10 | **อยู่ — วัดได้จริง** |
| หลังแบ่ง — `strain_1_L1_26` | 98 | 955 | 1.07 | ไม่ แน่นเกินไป |
| หลังแบ่ง — `strain_1_L1_36` | 47 | 3,374 | **6.68** | **อยู่** |
| หลังแบ่ง — `strain_1_L1_37` | 8 | 229 | 2.63 | ไม่ แน่นเกินไป (และ n < 25) |

unit ก่อนแบ่ง**ไม่ได้สูงผิดปกติเลย** — ค่า 3.10 ต่ำกว่าค่าเฉลี่ยด้วยซ้ำ
และอยู่ในช่วงที่ใช้งานได้อย่างสบาย ๆ ขณะที่ชิ้นหนึ่งหลังแบ่งกลับมีค่า*สูงกว่า*ของเดิม
การแบ่งครั้งนี้เปลี่ยน unit ที่วัดได้ 1 อัน เป็น unit ที่วัดได้ 1 อัน
บวกกับ clonal expansion อีก 2 อันที่แน่นเกินกว่าจะวัดได้

**นี่ไม่ได้แปลว่าการแบ่งผิด** โครงสร้างประชากรที่พบเป็นของจริง — มี clonal group แน่น ๆ
สามกลุ่มอยู่ใน unit เดียว แต่มันแปลว่าเราต้องอธิบายผลต่างออกไป
`strain_1_L1_36` ให้ผลเรื่อง recombination ส่วนอีกสองชิ้นรายงานเป็น
**clonal expansion ที่ตรวจพบ — น่าสนใจในเชิงระบาดวิทยา อาจเป็น outbreak
หรือ sublineage ที่ถูกเก็บตัวอย่างมาก แต่ไม่มีค่า r/m กำกับ**
บันทึกเดิมของโครงการเองก็เคยอธิบายรูปแบบนี้ไว้แล้ว จึงมีแบบอย่างให้รายงานแบบนี้ได้

มีอีกสองเรื่องที่ต้องแก้ ซึ่งมาจากสาเหตุเดียวกัน:

- `strain_1_L1_35` (r/m 1.31) และ `strain_4_L1_3` (r/m 0.75) เคยถูกอ่านว่าเป็นหลักฐาน
  ว่าการไม่แบ่งมันถูกต้องแล้ว เพราะ r/m ต่ำ แต่จริง ๆ มันอยู่**สูงกว่าเพดาน 1.9 และ 2.8 เท่า**
  ค่าต่ำของมันคือการพังของการวัด ไม่ใช่ความสะอาด การไม่แบ่งยังถูกต้องอยู่ แต่ไม่ใช่ด้วยเหตุผลนั้น
- ตอนนี้ตัด genome ONT ออกทั้งสองตัวแล้ว `SRR28096043` เคยเก็บไว้และติดธงไว้
  ปรากฏว่า branch ของมันใน tree **ยาวกว่า branch ของ Illumina ที่ยาวที่สุดใน unit เดียวกัน 38–59 เท่า**
  ดินเดียวกัน batch เดียวกัน reference เดียวกัน ต่างกันแค่ platform ที่ใช้ sequence
  ผล BUSCO ก็สอดคล้องกันโดยอิสระ (654 complete / 22 fragmented / 12 missing
  เทียบกับ 688 / 0 / 0 ของ genome ที่สมบูรณ์) หลักฐานคนละชนิด แต่ได้ข้อสรุปเดียวกัน

**เหตุผลที่เกิดเรื่องนี้ก็ควรรู้ไว้:** งานที่ทำบน A100 นั้นดีมาก แต่**ไม่มีเอกสาร methods อยู่ด้วย**
เพราะเอกสารนั้นอยู่บน workstation และไม่ได้ถูกใส่ไปใน bundle ไหนเลย
เอกสารนั้นคือที่ที่บันทึกเรื่องช่วง diversity ในหัวข้อ 7 ไว้
เมื่อไม่มีมัน การปรับ partition จึงออกแบบจากหลักฐาน modality อย่างเดียว
ไม่ใช่ความผิดพลาดของการให้เหตุผล แต่เป็นข้อมูลที่ขาดไป

---
## 10. The habit behind all of this

One rule explains most of the decisions above: **check per-item values; never
infer from a summary line.**

Every serious defect in this project produced perfectly plausible output. The
CRLF bug produced a clean-looking "run finished". The RAxML crash produced
"Unable to fit model to data", which reads as a biology problem. The ONT
assemblies passed every automated gate. The lumped unit had one of the tightest
median distances in the panel. None of these was caught by looking at a summary;
all were caught by comparing raw values against what they should have been.

The newest example is the one in section 9: a low r/m reads as a good result, and
it is usually a failed measurement. The only way to tell is to check where the
unit sits against a window we had to measure ourselves, because the tool does not
publish one.

### 10. นิสัยการทำงานที่อยู่เบื้องหลังทั้งหมดนี้

กฎข้อเดียวอธิบายการตัดสินใจส่วนใหญ่ข้างต้นได้:
**ตรวจค่าทีละรายการเสมอ อย่าอนุมานจากบรรทัดสรุป**

ข้อบกพร่องร้ายแรงทุกอย่างในโครงการนี้ให้ output ที่ดูสมเหตุสมผลทั้งสิ้น
bug เรื่อง CRLF ให้ผลที่ดูเหมือน "รันเสร็จเรียบร้อย"
RAxML ที่ crash รายงานว่า "Unable to fit model to data" ซึ่งอ่านแล้วเหมือนปัญหาทางชีววิทยา
ONT assemblies ผ่านเกณฑ์อัตโนมัติทุกข้อ
unit ที่ปนกันกลับมี median distance แน่นที่สุดกลุ่มหนึ่งใน panel
ไม่มีอันไหนเลยที่จับได้จากการดูบรรทัดสรุป — ทั้งหมดจับได้จากการเทียบค่าดิบ
กับค่าที่ควรจะเป็น

ตัวอย่างล่าสุดคือเรื่องในหัวข้อ 9: ค่า r/m ที่ต่ำอ่านแล้วเหมือนผลดี
แต่ส่วนใหญ่มันคือการวัดที่ล้มเหลว วิธีเดียวที่จะแยกออกคือดูว่า unit อยู่ตรงไหน
เทียบกับช่วงที่เราต้องวัดขึ้นมาเอง เพราะตัวเครื่องมือไม่ได้ประกาศช่วงนั้นไว้
