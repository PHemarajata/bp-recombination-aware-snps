#!/usr/bin/env bash
# Snippy re-measurement of analysed unit s1_L1_19 (n=34), close reference.
# Same reference, replicons, Gubbins flags and tree builder as the production
# ska_map arms in prod_s1_L1_19 -- ONLY the variant caller differs. This turns
# the 23-43% ska-vs-snippy r/m gap (measured on refsens_cluster37) into a
# measurement on a unit that is actually in the analysed set of 26.
#
# s1_L1_19 chosen because it sits EXACTLY on the lower edge of the empty r/m
# band (2.30; band is 2.30-4.28). If snippy raises it ~30%, it moves INTO the
# band and the band -- which now justifies the 26/853 split -- closes.
set -o pipefail
cd /home/phemarajata/Downloads/snp-mod-local-working
for arm in close__existing__chr1 close__existing__chr2; do
  echo "=== ${arm} ==="
  bash "snippy_s1_L1_19/arms/${arm}.sh" && echo "ARM ${arm} OK" || echo "ARM ${arm} FAILED (exit $?)"
done
echo "ALL ARMS FINISHED"
