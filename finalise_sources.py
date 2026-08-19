#!/usr/bin/env python3
"""
Consolidate isolation source for all 2,070 analysed genomes.

Four sources of truth, in this precedence order:

  1. study      -- the IP-/IE- genomes are this study's own unpublished isolates
                   from Nakhon Phanom, Thailand. IP = patient, IE = environmental
                   (confirmed by the data owner, 2026-08-16). They are in no
                   public archive, so no database lookup could ever have found
                   them.
  2. ena        -- ENA sample XML for genomes with a BioSample accession on file.
  3. ena_run    -- for genomes identified only by a run accession (the id carries
                   an assembler suffix, e.g. SRR11097783_SPAdes, which must be
                   stripped), run -> sample via the ENA filereport endpoint, then
                   the sample XML.
  4. ncbi_retry -- seven 2025-release samples ENA had not mirrored. Safe to take
                   from NCBI because all seven are SAMN; the prefix-stripping bug
                   only affects SAMEA/SAMD accessions.

Never use NCBI efetch for a SAMEA/SAMD accession: it strips the alpha prefix,
resolves the digits as an internal UID and returns a different sample with
HTTP 200. Always diff requested against returned accessions.
"""
import collections
import csv
import re

A = {r["sample_id"]: r for r in csv.DictReader(
    open("/media/phemarajata/TB1/snp_results_2026-08-16/tables/L1_ASSIGNMENTS.tsv"),
    delimiter="\t")}
PREV = {r["sample_id"]: r for r in csv.DictReader(
    open("ISOLATION_SOURCE.tsv"), delimiter="\t")}

# ---------------------------------------------------------------- attributes
def tags_from_xml(path):
    out = {}
    txt = open(path).read()
    for c in re.findall(r"<SAMPLE\b.*?</SAMPLE>", txt, re.S):
        m = re.search(r"<PRIMARY_ID>(SAM\w+)", c)
        if not m:
            continue
        d = {k.strip().lower(): v.strip() for k, v in
             re.findall(r"<TAG>(.*?)</TAG>\s*<VALUE>(.*?)</VALUE>", c, re.S)}
        out[m.group(1)] = d
    return out


def tags_from_ncbi(path):
    out = {}
    for rec in re.split(r"\n(?=\d+: )", open(path).read()):
        m = re.search(r"BioSample: (SAM\w+)", rec)
        if not m:
            continue
        out[m.group(1)] = {k.strip().lower(): v.strip() for k, v in
                           re.findall(r'/([^=]+)="([^"]*)"', rec)}
    return out


ena = tags_from_xml("analysed_samples_ena.xml")
ena.update(tags_from_xml("runs_samples.xml"))
ncbi = tags_from_ncbi("retry7_ncbi.txt")

run2sample = {}
for line in open("runs_resolved.tsv"):
    f = line.rstrip("\n").split("\t")
    if len(f) == 3 and f[1].startswith("SAM"):
        run2sample[f[0]] = f[1]

# ------------------------------------------------------------ classification
SRC_KEYS = ["isolation source", "isolation_source", "sample type", "source",
            "isolate source", "host tissue sampled", "tissue", "body site",
            "specimen", "sample_type", "environmental_sample"]
HOST_KEYS = ["host", "specific_host", "host scientific name",
             "host common name", "host_scientific_name"]
DIS_KEYS = ["host health state", "host disease", "host_disease", "disease"]

CLIN = re.compile(
    r"\b(clinical|blood|sputum|pus|abscess|wound|urine|csf|cerebrospinal|swab|"
    r"tissue|bronch|pleural|synovial|aspirate|lung|liver|spleen|skin|bone|"
    r"joint|throat|nasal|septic|patient|human|serum|melioidosis|tracheal|"
    r"peritoneal|ascit|catheter|prostat|lymph|toe|groin|thigh|respiratory|"
    r"alveolar|lavage|aneurysm|homo sapiens)", re.I)
ENV = re.compile(
    r"\b(soil|water|environment|paddy|rice.?field|mud|sediment|borehole|river|"
    r"pond|stream|rain|dust|plant|rhizosphere|agricultur|irrigation|swamp|"
    r"puddle|bore ?water|football field|grass|ground)", re.I)
# Widened after the first pass left a Singapore veterinary/zoo collection
# unclassified: `specific_host` there reads Sus, Gorilla, Chimpanzee,
# "Canis lupus familiaris", even "German Shepherd".
ANIMAL = re.compile(
    r"\b(sus\b|swine|pig|boar|goat|capra|sheep|ovis|cattle|cow|bos\b|bovine|"
    r"horse|equus|equine|camel|alpaca|llama|deer|kangaroo|wallaby|koala|dog|"
    r"canis|canine|shepherd|cat\b|felis|feline|macaca|macaque|monkey|primate|"
    r"gorilla|chimpanzee|orangutan|pan troglodytes|dolphin|bird|parrot|avian|"
    r"iguana|reptile|ferret|rodent|mouse|rat\b|veterinary|zoo\b|animal|"
    r"sambar|langur|gibbon|lemur|tapir|antelope|wallaroo)", re.I)
HUMAN = re.compile(r"homo sapiens|\bhuman\b", re.I)
# Lab-passaged material has no natural isolation site at all: its recorded
# country is where the LABORATORY sits, not where the organism came from. Four
# of our five "United Kingdom" genomes are Salisbury/Exeter/London laboratory
# stocks, i.e. not UK acquisitions. Kept as its own class so phylogeography can
# exclude them rather than counting them as cases.
LAB = re.compile(r"laborator(y|ies)|lab stock|cell culture|bacterial culture|"
                 r"reference strain|type strain|passage", re.I)
NULL = re.compile(r"^(missing|unknown|not known|not applicable|n/?a|none|-|"
                  r"not collected|not provided|restricted access|)$", re.I)


def pick(d, keys):
    for k in keys:
        v = (d.get(k) or "").strip()
        if v and not NULL.match(v):
            return v
    return ""


def classify(d):
    src, host, dis = pick(d, SRC_KEYS), pick(d, HOST_KEYS), pick(d, DIS_KEYS)
    if src and LAB.search(src):
        return "laboratory", src, host, dis
    if host and ANIMAL.search(host):
        return "animal", src, host, dis
    if src and ENV.search(src):
        return "environmental", src, host, dis
    if host and HUMAN.search(host):
        return "clinical", src, host, dis
    if src and CLIN.search(src):
        return "clinical", src, host, dis
    blob = " ".join([src, host, dis])
    for rx, lab in ((ANIMAL, "animal"), (ENV, "environmental"), (CLIN, "clinical")):
        if rx.search(blob):
            return lab, src, host, dis
    return "unknown", src, host, dis


# ---------------------------------------------------------------------- build
rows = []
for sid, a in sorted(A.items()):
    unit, country = a["subcluster"], a["country"]

    # 1. this study's own isolates
    if re.match(r"^IP-", sid):
        rows.append(dict(sample_id=sid, unit=unit, country=country, biosample="",
                         source_class="clinical", evidence="study",
                         isolation_source="patient", host="Homo sapiens",
                         host_disease="", note="Nakhon Phanom, unpublished"))
        continue
    if re.match(r"^IE-", sid):
        rows.append(dict(sample_id=sid, unit=unit, country=country, biosample="",
                         source_class="environmental", evidence="study",
                         isolation_source="environmental", host="",
                         host_disease="", note="Nakhon Phanom, unpublished"))
        continue

    acc, ev = "", ""
    prev = PREV.get(sid)
    if prev and prev["biosample"].startswith("SAM"):
        acc, ev = prev["biosample"], "ena"
    else:
        run = re.sub(r"_(SPAdes|contigs)$", "", sid)
        if run in run2sample:
            acc, ev = run2sample[run], "ena_run"

    d = ena.get(acc)
    if d is None and acc in ncbi:
        d, ev = ncbi[acc], "ncbi_retry"
    if d is None:
        rows.append(dict(sample_id=sid, unit=unit, country=country, biosample=acc,
                         source_class="unknown", evidence="none",
                         isolation_source="", host="", host_disease="",
                         note="no record retrieved"))
        continue

    cls, src, host, dis = classify(d)
    rows.append(dict(sample_id=sid, unit=unit, country=country, biosample=acc,
                     source_class=cls, evidence=ev, isolation_source=src,
                     host=host, host_disease=dis, note=""))

cols = ["sample_id", "unit", "country", "biosample", "source_class", "evidence",
        "isolation_source", "host", "host_disease", "note"]
with open("ISOLATION_SOURCE_v2.tsv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)

print("total analysed genomes: %d" % len(rows))
print("\n=== classification ===")
c = collections.Counter(r["source_class"] for r in rows)
for k, n in c.most_common():
    print("  %-16s %5d  (%4.1f%%)" % (k, n, 100.0 * n / len(rows)))
known = len(rows) - c["unknown"]
print("  ---")
print("  SOURCE KNOWN     %5d  (%4.1f%%)" % (known, 100.0 * known / len(rows)))
print("\n=== evidence ===")
for k, n in collections.Counter(r["evidence"] for r in rows).most_common():
    print("  %-12s %5d" % (k, n))
print("\nwrote ISOLATION_SOURCE_v2.tsv")
