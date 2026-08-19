#!/usr/bin/env bash
# Snippy re-measurement of analysed unit s1_L1_9 (n=90), close reference.
# Companion to run_snippy_s1_L1_19.sh. Same reference, replicons, Gubbins flags
# and tree builder as prod_s1_L1_9 -- ONLY the variant caller differs.
#
# WHY THIS UNIT: it sits on the UPPER edge of the empty r/m band (4.28; band is
# 2.30-4.28). s1_L1_19 tested the lower edge and moved further BELOW under
# snippy (2.30 -> 1.96). If that downward direction repeats here, s1_L1_9 moves
# DOWN INTO the band -- which would close it and undercut the 26/853 split. So
# this unit tests the band from the side where a downward shift is damaging.
set -o pipefail
cd /home/phemarajata/Downloads/snp-mod-local-working
for arm in close__existing__chr1 close__existing__chr2; do
  echo "=== ${arm} ==="
  bash "snippy_s1_L1_9/arms/${arm}.sh" && echo "ARM ${arm} OK" || echo "ARM ${arm} FAILED (exit $?)"
done
echo "ALL ARMS FINISHED"
