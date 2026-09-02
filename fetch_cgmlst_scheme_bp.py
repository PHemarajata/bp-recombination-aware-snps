#!/usr/bin/env python3
"""
Fetch the PubMLST B. pseudomallei cgMLST scheme (scheme 2) as per-locus FASTA.

Why PubMLST and not cgMLST.org: the published 4,221-target scheme (Ashcroft et
al., JCM 2021) is distributed through Ridom's cgMLST.org, a commercial platform
whose allele definitions we cannot assume we may redistribute. The same scheme
is curated openly at PubMLST as scheme 2 -- 4,090 loci, 1,154 profiles as of
this run -- with a documented REST API. That removes the licensing question
entirely and makes the download reproducible.

Output is one FASTA per locus, which is exactly the layout
`chewBBACA.py PrepExternalSchema` expects.

Courtesy: PubMLST is a shared academic resource. Concurrency is deliberately low
and 429/503 are backed off rather than retried hard. Resumable -- a locus whose
file is already non-empty is skipped, so an interrupted run costs nothing.

Usage
-----
    fetch_cgmlst_scheme_bp.py [--out-dir DIR] [--workers N] [--scheme N]
"""
import argparse
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://rest.pubmlst.org/db/pubmlst_bpseudomallei_seqdef"
UA = "snp-mod-local-working/1.0 (research; contact peerah@gmail.com)"


def get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503, 504) and i < tries - 1:
                time.sleep(2 ** i * 3)       # back off, do not hammer
                continue
            if e.code == 404:
                return None
            raise
        except Exception:
            if i < tries - 1:
                time.sleep(2 ** i * 2)
                continue
            raise
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="cgmlst_scheme/alleles")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--scheme", type=int, default=2)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    meta = json.loads(get(f"{BASE}/schemes/{a.scheme}"))
    loci = meta["loci"]
    print(f"scheme {a.scheme} ({meta.get('description')}): {len(loci)} loci, "
          f"{meta.get('records')} profiles, updated {meta.get('last_updated')}",
          flush=True)
    with open(os.path.join(os.path.dirname(a.out_dir), "scheme_meta.json"), "w") as fh:
        json.dump({k: v for k, v in meta.items() if k != "loci"}, fh, indent=2)

    todo = []
    for u in loci:
        name = u.rstrip("/").split("/")[-1]
        p = os.path.join(a.out_dir, f"{name}.fasta")
        if not (os.path.isfile(p) and os.path.getsize(p) > 0):
            todo.append((name, u, p))
    print(f"already present: {len(loci) - len(todo)}   to fetch: {len(todo)}", flush=True)

    done = [0]
    failed = []

    def work(item):
        name, u, p = item
        try:
            b = get(f"{u}/alleles_fasta")
            if not b:
                failed.append(name)
                return
            tmp = p + ".part"
            with open(tmp, "wb") as fh:
                fh.write(b)
            os.replace(tmp, p)               # atomic, so resume never sees a partial
        except Exception as e:
            failed.append(f"{name}: {e}")
        finally:
            done[0] += 1
            if done[0] % 200 == 0:
                print(f"  {done[0]}/{len(todo)}", flush=True)

    if todo:
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            list(ex.map(work, todo))

    n = len([f for f in os.listdir(a.out_dir) if f.endswith(".fasta")])
    print(f"\nlocus FASTAs on disk: {n} of {len(loci)}")
    if failed:
        print(f"FAILED {len(failed)}: {failed[:10]}{' ...' if len(failed) > 10 else ''}")
        sys.exit(1)


if __name__ == "__main__":
    main()
