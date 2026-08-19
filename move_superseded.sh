#!/usr/bin/env bash
# Move superseded Gubbins output to the external drive.
#
# COPY, VERIFY, THEN DELETE -- never a bare `mv`. Across filesystems `mv` is a
# copy followed by an unlink, and if it is interrupted partway (unplugged drive,
# full target, I/O error) it can leave the source already removed for files it
# believes it copied. These directories are the ONLY surviving copy of those
# results: the work dirs that produced them were purged. So the source is removed
# only after a checksum-level comparison reports zero differences.
#
# Verification is `rsync -nc --delete`, which re-reads both sides and compares
# CHECKSUMS rather than the size+mtime heuristic rsync uses by default. Slower,
# and the entire point.
set -uo pipefail
BASE=/home/phemarajata/Downloads/snp-mod-local-working
DEST=${DEST:-/media/phemarajata/TB1/snp_superseded}
LOG=$BASE/MOVE_SUPERSEDED.log

ITEMS=( "pp2802_out/Clusters" "all35_out/Clusters" )

say(){ printf '[%s] %s\n' "$(date '+%F %T')" "$*" | tee -a "$LOG"; }

[ -d "$DEST" ] || { say "ERROR: $DEST does not exist"; exit 1; }
touch "$DEST/.wt" 2>/dev/null || { say "ERROR: $DEST not writable"; exit 1; }
rm -f "$DEST/.wt"

for item in "${ITEMS[@]}"; do
    src="$BASE/$item"
    [ -d "$src" ] || { say "SKIP $item (not present)"; continue; }
    tgt="$DEST/$(dirname "$item")"
    mkdir -p "$tgt"

    sz=$(du -sh "$src" | cut -f1)
    n_src=$(find "$src" -type f | wc -l)
    say "copying $item ($sz, $n_src files) -> $tgt/"
    if ! rsync -a --no-compress "$src" "$tgt/" >>"$LOG" 2>&1; then
        say "ERROR: rsync failed for $item -- source left intact"; exit 1
    fi

    say "verifying $item by checksum (this re-reads both copies)"
    diff_out=$(rsync -nc -ii -a "$src/" "$tgt/$(basename "$item")/" 2>&1 | grep -vE '^\.|sending|total size|^$' || true)
    n_dst=$(find "$tgt/$(basename "$item")" -type f | wc -l)
    if [ -n "$diff_out" ]; then
        say "ERROR: checksum verify found differences -- source left intact:"
        printf '%s\n' "$diff_out" | head -20 | tee -a "$LOG"; exit 1
    fi
    if [ "$n_src" -ne "$n_dst" ]; then
        say "ERROR: file count $n_src != $n_dst -- source left intact"; exit 1
    fi

    say "verified $item: $n_dst files identical by checksum; removing source"
    rm -rf "$src"
    say "done $item"
done

say "free on / now: $(df -h "$BASE" | tail -1 | awk '{print $4}')"
say "free on drive : $(df -h "$DEST" | tail -1 | awk '{print $4}')"
