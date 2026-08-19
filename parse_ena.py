#!/usr/bin/env python3
"""
Classify every analysed genome as clinical / environmental / animal / unknown
from its ENA sample attributes, and report the breakdown per unit.

Attributes are fetched from ENA, NOT NCBI efetch: `efetch db=biosample
id=SAMEA807037` strips the alpha prefix, resolves 807037 as an NCBI UID, and
returns SAMN00807037 -- a human cell line. 1,094 of these 1,784 accessions are
SAMEA/SAMD and every one came back wrong. Verified by comparing requested
against returned accessions; the overlap was 685 of 1,784.

Classification is conservative: anything without a confident match is left
`unknown` rather than guessed, because the point of the exercise is to know
which genomes we can and cannot say this about.
"""
import collections
import csv
import re
import xml.etree.ElementTree as ET

XML = "analysed_samples_ena.xml"
MAP = "bs_map.tsv"
OUT = "ISOLATION_SOURCE.tsv"

# ENA returns one <ROOT> per batch; wrap them so this parses as one document.
chunks = re.findall(r"<SAMPLE\b.*?</SAMPLE>", open(XML).read(), re.S)
print("sample records parsed: %d" % len(chunks))

records = {}
for c in chunks:
    try:
        el = ET.fromstring(c)
    except ET.ParseError:
        continue
    acc = el.findtext(".//IDENTIFIERS/PRIMARY_ID") or el.get("accession") or ""
    attrs = {}
    for a in el.findall(".//SAMPLE_ATTRIBUTE"):
        t = (a.findtext("TAG") or "").strip().lower()
        v = (a.findtext("VALUE") or "").strip()
        if t and v:
            attrs.setdefault(t, v)
    records[acc] = {
        "organism": el.findtext(".//SCIENTIFIC_NAME") or "",
        "title": el.findtext("TITLE") or "",
        "attrs": attrs,
    }

SRC_KEYS = ["isolation source", "isolation_source", "environmental_sample",
            "sample type", "source", "isolate source", "host tissue sampled",
            "tissue", "body site", "specimen", "sample_type"]
HOST_KEYS = ["host", "specific_host", "host scientific name",
             "host common name", "host_scientific_name"]
DIS_KEYS = ["host health state", "host disease", "host_disease",
            "disease", "health state"]


def first(attrs, keys):
    for k in keys:
        if attrs.get(k):
            return attrs[k]
    return ""


CLIN = re.compile(
    r"\b(clinical|blood|sputum|pus|abscess|wound|urine|csf|cerebrospinal|"
    r"swab|tissue|bronch|pleural|synovial|aspirate|lung|liver|spleen|skin|"
    r"bone|joint|throat|nasal|septic|patient|human|serum|melioidosis|"
    r"tracheal|peritoneal|ascit|catheter|prostat|lymph|toe|groin|thigh|"
    r"respiratory|alveolar|aneurysm|homo sapiens)", re.I)
ENV = re.compile(
    r"\b(soil|water|environment|paddy|rice.?field|mud|sediment|borehole|"
    r"river|pond|stream|rain|dust|plant|rhizosphere|agricultur|irrigation|"
    r"swamp|puddle|bore ?water|football field|grass|ground)", re.I)
ANIMAL = re.compile(
    r"\b(goat|sheep|pig|swine|cattle|cow|bovine|horse|equine|camel|alpaca|"
    r"llama|deer|kangaroo|wallaby|koala|dog|canine|feline|macaca|macaque|"
    r"monkey|primate|dolphin|bird|parrot|iguana|ferret|veterinary|zoo)", re.I)
HUMAN = re.compile(r"homo sapiens|^human$|\bhuman\b", re.I)
NULL = re.compile(r"^(missing|unknown|not applicable|n/?a|none|-|not "
                  r"collected|not provided|restricted access)$", re.I)


def classify(r):
    a = r["attrs"]
    src = first(a, SRC_KEYS)
    host = first(a, HOST_KEYS)
    dis = first(a, DIS_KEYS)
    src = "" if NULL.match(src or "") else src
    host = "" if NULL.match(host or "") else host

    if host and ANIMAL.search(host):
        return "animal", src, host, dis
    if src and ENV.search(src):
        return "environmental", src, host, dis
    if host and HUMAN.search(host):
        return "clinical", src, host, dis
    if src and CLIN.search(src):
        return "clinical", src, host, dis
    if dis and re.search(r"melioidosis", dis, re.I):
        return "clinical", src, host, dis
    blob = " ".join([src, host, dis, r["title"]])
    if ANIMAL.search(blob):
        return "animal", src, host, dis
    if ENV.search(blob):
        return "environmental", src, host, dis
    if CLIN.search(blob):
        return "clinical", src, host, dis
    return "unknown", src, host, dis


rows = []
for line in open(MAP):
    acc, sid, unit, country = line.rstrip("\n").split("\t")
    r = records.get(acc)
    if r is None:
        rows.append(dict(sample_id=sid, unit=unit, country=country,
                         biosample=acc, source_class="not retrieved",
                         isolation_source="", host="", host_disease="",
                         organism=""))
        continue
    cls, src, host, dis = classify(r)
    rows.append(dict(sample_id=sid, unit=unit, country=country, biosample=acc,
                     source_class=cls, isolation_source=src, host=host,
                     host_disease=dis, organism=r["organism"]))

cols = ["sample_id", "unit", "country", "biosample", "source_class",
        "isolation_source", "host", "host_disease", "organism"]
with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)

print("\n=== sanity: organism of the retrieved records ===")
for v, n in collections.Counter(r["organism"] for r in rows).most_common(6):
    print("  %5d  %s" % (n, v or "(none)"))

print("\n=== classification of the %d genomes with a BioSample accession ===" % len(rows))
tot = collections.Counter(r["source_class"] for r in rows)
for k, n in tot.most_common():
    print("  %-16s %5d  (%4.1f%%)" % (k, n, 100.0 * n / len(rows)))
print("  (%d further analysed genomes have no BioSample accession on file)"
      % (2070 - len(rows)))

print("\n=== most common isolation_source values ===")
for v, n in collections.Counter(r["isolation_source"] for r in rows).most_common(20):
    print("  %5d  %s" % (n, v or "(empty)"))
print("\n=== most common host values ===")
for v, n in collections.Counter(r["host"] for r in rows).most_common(10):
    print("  %5d  %s" % (n, v or "(empty)"))
print("\nwrote %s" % OUT)
