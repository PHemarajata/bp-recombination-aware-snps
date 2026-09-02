#!/usr/bin/env bash
# Archive a completed/superseded directory to TB1, verifying before deleting.
#
# Deliberately NOT `mv`: across filesystems that is a copy-then-delete with no
# atomicity, so an interruption can leave the source half-removed with no
# complete copy anywhere. This copies, verifies file list AND total byte count,
# and only then removes the source. Safe to re-run -- rsync resumes, and a
# directory already archived and deleted is simply skipped.
#
# Usage:  ./archive_to_tb1.sh <dest-subdir> <dir> [<dir> ...]
#   e.g.  ./archive_to_tb1.sh snp_superseded L1v3_out L1v4b_out
set -uo pipefail

TB1=/media/phemarajata/TB1
DEST_SUB="${1:?usage: archive_to_tb1.sh <dest-subdir> <dir>...}"; shift
DEST="$TB1/$DEST_SUB"

mountpoint -q "$TB1" || { echo "TB1 is not mounted at $TB1"; exit 1; }
mkdir -p "$DEST"

for d in "$@"; do
    d="${d%/}"
    if [ ! -d "$d" ]; then echo "== $d: not present, skipping"; continue; fi
    echo "== $d  ($(du -sh "$d" | cut -f1))"

    rsync -a --info=progress2 "$d/" "$DEST/$d/" || { echo "   rsync FAILED, source kept"; continue; }

    # verify: identical file lists and identical total bytes
    a_list=$(cd "$d" && find . -type f | sort | md5sum | cut -d' ' -f1)
    b_list=$(cd "$DEST/$d" && find . -type f | sort | md5sum | cut -d' ' -f1)
    a_size=$(find "$d" -type f -printf '%s\n' | paste -sd+ | bc)
    b_size=$(find "$DEST/$d" -type f -printf '%s\n' | paste -sd+ | bc)

    if [ "$a_list" = "$b_list" ] && [ "$a_size" = "$b_size" ]; then
        rm -rf "$d"
        echo "   verified ($a_size bytes) -> removed local copy"
    else
        echo "   VERIFY FAILED (list $a_list/$b_list, bytes $a_size/$b_size) -- source KEPT"
    fi
done

echo
echo "local free: $(df -h . | tail -1 | awk '{print $4}')   TB1 free: $(df -h "$TB1" | tail -1 | awk '{print $4}')"
