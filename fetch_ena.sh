#!/usr/bin/env bash
# Re-fetch every BioSample through ENA.
#
# NCBI's efetch db=biosample id=<acc> STRIPS the alpha prefix and resolves the
# numeric part as an NCBI UID, so SAMEA807037 silently returns SAMN00807037 --
# a human cell line. 1,094 of our 1,784 accessions are SAMEA/SAMD and every one
# of them came back as an unrelated sample. ENA serves all INSDC accessions and
# resolves them correctly.
set -uo pipefail
cd "$(dirname "$0")"

: > analysed_samples_ena.xml
cut -f1 bs_map.tsv > .acc_all.txt
echo "fetching $(wc -l < .acc_all.txt) samples from ENA in batches of 100"

split -l 100 -d -a 3 .acc_all.txt .enabatch_
n=0
for f in .enabatch_*; do
    n=$((n+1))
    ids=$(paste -sd, "$f")
    for attempt in 1 2 3; do
        if curl -sS --max-time 180 \
             "https://www.ebi.ac.uk/ena/browser/api/xml/${ids}" \
             >> analysed_samples_ena.xml; then
            break
        fi
        echo "  batch $n attempt $attempt failed, retrying" >&2
        sleep 5
    done
    [ $((n % 5)) -eq 0 ] && echo "  batch $n — $(grep -c '<PRIMARY_ID>' analysed_samples_ena.xml || true) ids so far"
    sleep 0.4
done
rm -f .enabatch_* .acc_all.txt
echo "ENA FETCH COMPLETE: $(grep -c '<SAMPLE ' analysed_samples_ena.xml) sample records"
