#!/usr/bin/env python3
"""
write_if_changed_bp.py

Replace a file only when its CONTENT differs. Importable helper.

WHY THIS EXISTS, and it cost a cache. Nextflow's default cache mode hashes each
input file by path, size and **last-modified time**. `run_wf_curated_L1.sh`
regenerates the samplesheet, the cluster TSV and the normalized reference FASTAs
on every invocation. The bytes are identical each time, but the mtimes are new,
so a `-resume` that should have been a no-op instead invalidated the entire
run -- 2,070 INFILE_HANDLING tasks resubmitted, and 4,140 snippy tasks (~7 hours)
about to follow.

Rewriting only on real change makes the runner idempotent, so `-resume` after a
parameter tweak re-runs only the stages that parameter actually touches.

Do NOT reach for `cache = 'lenient'` to work around this. It changes how hashes
are computed and invalidates everything (measured: 0 tasks cached, restart from
task one).
"""

import os
import shutil
import tempfile


def write_if_changed(path, data, binary=False):
    """
    Write `data` to `path` only if it differs. Returns True if written.

    The write is atomic via a temp file in the same directory, so an interrupted
    run cannot leave a half-written samplesheet that looks valid.
    """
    mode_r, mode_w = ("rb", "wb") if binary else ("r", "w")
    if os.path.exists(path):
        try:
            with open(path, mode_r) as fh:
                if fh.read() == data:
                    return False
        except OSError:
            pass
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp_wic_")
    try:
        with os.fdopen(fd, mode_w) as fh:
            fh.write(data)
        shutil.move(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return True


def copy_if_changed(src, dst):
    """Same idea for whole files; preserves dst's mtime when content matches."""
    with open(src, "rb") as fh:
        data = fh.read()
    return write_if_changed(dst, data, binary=True)
