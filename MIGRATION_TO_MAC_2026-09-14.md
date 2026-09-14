# Moving this project to the Mac

Written 2026-09-14, from a survey of this workstation. The project is at the
presentation and communication stage, so the analysis basis is frozen and
nothing that moves needs to be recomputed. That changes the migration from a
329 GB problem into a 223 MB one.

Read section 5 for the steps. Sections 1 to 4 are why they are what they are.

## 1. What is actually needed

The workspace is 329 GB. Almost none of it is the project.

| what | size | moves? |
|---|---|---|
| `REPRO_2026-08-24_work/` | 237 GB | no. Nextflow scratch. |
| `REPRO_2026-08-24_out/`, `L1v4c_out/` | 17 GB each | no, except two tree files named below. |
| everything else under 2 GB per directory | ~40 GB | no, except the curated list. |
| **the curated bundle** | **223 MB** | **yes. This is the project.** |

The curated bundle is 1,014 files: the 252 tracked files, the 82 root-level
data files the top-level scripts actually read, `FINAL_BASIS_2026-08-22/`,
both handoff packs, the clip and narration directories, the rendered media,
and the six figure SVGs. Adding `mash_matrix_2802.tsv` takes it to 305 MB, and
nothing in the presentation path reads that file.

## 2. Both code repositories are already pushed. Clone them, do not copy them.

| repo | on disk | tracked | state |
|---|---|---|---|
| this one | 329 GB | 252 files, 4.6 MB | `main` at `27da6cc`, working branch `claude/citation-audit-2026-09-03` at `bb76521`, both 0 ahead and 0 behind. |
| `~/wf-assembly-snps-mod` | 27 GB | 164 files, 24 KB | `main` clean, 0 ahead and 0 behind. The 27 GB is `results_snp_archive_aug_2026/`. |
| `~/PopPIPE-bp` | 11 GB | n/a | has a remote. |

Cloning gets all three in under a minute and leaves 367 GB of run output
behind, which is the correct outcome. The upstream repo holds the parameters
and command lines for every run, and it is 24 KB of tracked content.

## 3. Four things are not in git and would be lost silently

The `.gitignore` here denies everything by default and re-admits only source
code and documentation at the top level. A fresh clone therefore has no data,
no trees, no tables and no media. That is deliberate, and it means the clone
alone is not a working copy.

1. **The untracked data the scripts read.** 82 files at the repo root plus
   `FINAL_BASIS_2026-08-22/`. Without these, `make_tables_bp.py` and the figure
   scripts cannot run.
2. **Uncommitted work.** 5 modified tracked files and 14 untracked scripts,
   including the whole narration and video toolchain: `make_narrated_videos_bp.py`,
   `make_voice_lines_bp.py`, `make_captions_bp.py`, `make_tree_explorer_bp.py`,
   `make_animo_pack_bp.py`, both retime scripts. Commit these before anything
   else, or they exist in exactly one place.
3. **The Claude Code project memory.** 122 files, 560 KB, at
   `~/.claude/projects/-home-phemarajata-Downloads-snp-mod-local-working/memory/`.
   It holds the accumulated corrections: which figures are stale, which
   defaults are traps, which numbers belong to which partition. See section 5
   step 6, because the directory name has to change on macOS or the memory is
   invisible.
4. **Home-level dependencies the scripts resolve through `expanduser`.**

| path | size | referenced by |
|---|---|---|
| `~/Downloads/ANIMO_DELIVERABLES_2026-09-09` | 59 MB | 7 references. The rendered clips, stills and narration. |
| `~/CLIP_GENERATION_STANDARD.md` | 11 KB | 2 references. |
| `~/PopPIPE-bp` | 11 GB | 1 reference, and it has a remote. |
| `~/skills/narrated-clip-production/` | 7 MB | the clip production skill. |
| `~/Downloads/BP_REVIEW_PACKAGE_2026-09-04` | 15 MB | the built reviewer package. |
| `~/Downloads/module_intros/` | 30 MB | `.claude/launch.json` serves from here. |
| `~/Downloads/final_deduped_all_BP_with_locations/` | 19 GB, 2,804 files | the assembly set. Only needed to re-run analysis. |

## 4. The bundle carries restricted data. Move it directly.

*B. pseudomallei* is a US Tier 1 Select Agent, and the curated bundle includes
`FINAL_PANEL.tsv`, `L1v4c_MERGED_METADATA.tsv` and `PANEL_v4d_2026-08-21.tsv`.
Those carry the accession to isolation location to collection date to exposure
label join that is re-identifiable for rare cases. Three consequences:

- **Transfer machine to machine.** Ethernet, Thunderbolt or `rsync` over `ssh`.
  Not Google Drive, and not the `peerah-gdrive:` rclone remote, even though the
  cluster trees already live there.
- **Turn FileVault on before the data lands**, not after.
- **The GitHub remote is public.** `git add -f` bypasses the whole `.gitignore`
  allowlist. Do not use it.

`ANIMO_PACK/` is the subset that is cleared to leave the machine, and it is
audited on build against genome accessions and exposure columns.
`VM_HANDOFF_PACK/` is not cleared: it holds the six withheld tables, including
`FINAL_PANEL.tsv` and `CGMLST_LICHT_ATTRIBUTION.tsv`. Move it inside the
encrypted bundle, and do not forward it.

## 5. Steps

**The Mac's default shell is zsh, and it does not treat `#` as an inline
comment.** Every command block below is comment-free for that reason. If you
copy a command from anywhere else in this document that has a trailing
`# ...`, delete the comment before you paste it, or zsh will hand the comment
words to the command as arguments. This is not hypothetical: it is how the
first run of this runbook extracted nothing and put the memory in the wrong
place.

### Step 0, on this workstation: commit the loose work

**Done on 2026-09-14**, in three commits: the Table 5 and Gate 1 numeric
reconciliations, the twelve-script presentation toolchain, and this runbook.
All five CI checks passed and the tracked tree stayed at 4.9 MB across 267
files. Kept here because it is the step that would be skipped on a re-run.

    git add -A && git commit && git push

Nothing else in this plan protects the 14 untracked scripts. Check
`git ls-files | xargs -r du -ch | tail -1` afterward and confirm it is still
about 4.6 MB, which is the evidence that no data file slipped into the commit.

### Step 1: freeze and verify before copying

    python3 freeze_basis_bp.py
    cd ANIMO_PACK && sha256sum -c MANIFEST.sha256 && cd ..
    cd FINAL_BASIS_2026-08-22 && sha256sum -c MANIFEST.sha256 && cd ..
    cd ~/Downloads/ANIMO_DELIVERABLES_2026-09-09 && sha256sum -c MANIFEST.sha256

Verify here, where a failure is diagnosable, rather than on the Mac where it is
ambiguous between a bad copy and a bad source.

### Step 2: build the bundle

Write the file list, then copy against it. The list is reproducible, which
matters more than the one-liner being short.

    cd /home/phemarajata/Downloads/snp-mod-local-working
    { git ls-files;
      grep -ohE '[A-Za-z0-9_-]+\.(tsv|csv|nwk|treefile|json|txt)' *.py \
        | sort -u | while read f; do [ -f "$f" ] && echo "$f"; done;
      find FINAL_BASIS_2026-08-22 ANIMO_PACK VM_HANDOFF_PACK clip_partitioning \
           voice narration_v2 narration_csv video_captioned \
           CLAUDE_DESIGN_STAGING_2026-09-09 RETIRED_2026-08-22 collaborator -type f;
      ls *.svg *.html;
      echo L1v4c_out/global_ml_tree.treefile;
      echo L1v4c_out/global_grafted_chr1.treefile;
    } | sort -u | grep -v '^mash_matrix_2802.tsv$' > /tmp/bundle.txt
    wc -l /tmp/bundle.txt
    while read f; do [ -e "$f" ] || echo "MISSING $f"; done < /tmp/bundle.txt
    tar czf ~/bp_bundle.tgz -T /tmp/bundle.txt

The count was 1,030 files at 223 MB on 2026-09-14. Do not treat that as a
target: it rises whenever a file is tracked or a clip directory grows. The
check that matters is the second line, which must print nothing.

Then the home-level pieces, separately, because they land outside the repo:

    tar czf ~/bp_home.tgz \
      -C ~ Downloads/ANIMO_DELIVERABLES_2026-09-09 CLIP_GENERATION_STANDARD.md \
         skills/narrated-clip-production Downloads/BP_REVIEW_PACKAGE_2026-09-04 \
         Downloads/module_intros

    tar czf ~/bp_memory.tgz \
      -C ~/.claude/projects/-home-phemarajata-Downloads-snp-mod-local-working memory

### Step 3: transfer

171 MB across three archives, plus `bp_TRANSFER_SHA256.txt`. Whichever route
you take, verify before unpacking:

    shasum -a 256 -c bp_TRANSFER_SHA256.txt

That is the macOS spelling. On Linux the command is `sha256sum -c`.

**This workstation does not run an ssh server.** Checked on 2026-09-14: nothing
listens on port 22 and the service is inactive. So the Mac cannot pull from it,
and the obvious `rsync user@linux-host:...` command fails with a connection
refusal rather than anything informative. Four routes, best first.

**Through the NoMachine session, if you are already connected over it.** This
is the route actually used on 2026-09-14. Both mechanisms are enabled by
default on the NoMachine 9.8.3 server here, and neither size limit is active:
`EnableUploadSizeLimit` and `EnableDownloadSizeLimit` both default to 0, which
the config documents as allowing transfers regardless of the 100 MiB default
ceiling. So the 107 MB bundle is not capped, despite appearances.

Prefer connecting a Mac folder over sending files one at a time. In the session
menu, ctrl+alt+0 or peel the top right corner, open Devices and connect a
folder from the Mac. It mounts here under `~/Desktop`, the default
`DiskSharingPrivateBasePath`. Then:

    cp ~/bp_bundle.tgz ~/bp_home.tgz ~/bp_memory.tgz \
       ~/bp_TRANSFER_SHA256.txt ~/Desktop/<mounted-folder>/

Transfer runs over the session channel rather than a raw socket, so budget a
few minutes for 171 MB. The traffic is encrypted machine to machine with no
third-party service, which satisfies section 4 on its own. If Devices will not
mount, the same menu's file transfer sends server to client, one archive at a
time.

**Push from here to the Mac.** Enable Remote Login on the Mac under System
Settings, General, Sharing. Then, from this workstation:

    rsync -avP --partial ~/bp_bundle.tgz ~/bp_home.tgz ~/bp_memory.tgz \
      ~/bp_TRANSFER_SHA256.txt <mac-user>@<mac-hostname>.local:

This is the recommended route. It needs no daemon and no `sudo` on the Linux
side, and one toggle on the Mac. This workstation is `192.168.1.142` on the LAN.

**Or serve the ssh daemon here and pull.** `sudo systemctl enable --now ssh`,
then rsync from the Mac. It works, but it starts a network service on the
machine holding the restricted data, for a one-time copy. Prefer the first
route, and if you do take this one, stop the service afterward.

**Or use a USB disk**, formatted exFAT so both machines can write it. Delete
the copy from the disk once the Mac verifies the checksums. Use this if the two
machines are not on the same network.

Not Google Drive, and not the `peerah-gdrive:` rclone remote, for the reason in
section 4.

### Step 4: on the Mac, clone then unpack over the clone

    git clone https://github.com/PHemarajata/bp-recombination-aware-snps.git
    cd bp-recombination-aware-snps
    tar xzf ~/bp_bundle.tgz
    cd .. && git clone https://github.com/PHemarajata/wf-assembly-snps-mod.git
    git clone https://github.com/PHemarajata/PopPIPE-bp.git

No branch checkout is needed. `main` carries every commit of the presentation
work as of 2026-09-14, so the default clone is the right tree.

Unpacking over the clone is safe: the tracked files in the tarball came from
the same commit, so they overwrite themselves byte for byte. Confirm with
`git status`, which should report a clean tree.

### Step 5: restore the home-level dependencies

    cd ~ && tar xzf ~/bp_home.tgz

The scripts resolve `~/Downloads/ANIMO_DELIVERABLES_2026-09-09` and
`~/CLIP_GENERATION_STANDARD.md` through `expanduser`, so they work unchanged as
long as the paths keep their shape under the Mac home directory. There are no
hardcoded `/home/phemarajata` paths in any top-level script, which is why this
step is a copy and not a rewrite.

Two files do carry absolute paths and need editing by hand:
`.claude/launch.json` serves from `/home/phemarajata/Downloads/module_intros/...`,
and `.claude/settings.local.json` holds about nine `/home/phemarajata` paths in
its permission rules. Neither is tracked, so neither arrives from the clone.

### Step 6: restore the project memory under its new name

Claude Code derives the directory name from the project path by replacing each
slash with a dash. On the Mac the project sits under `/Users/<you>/`, so the
name changes and the old directory will not be found. Rename it on arrival:

    P="$HOME/bp-recombination-aware-snps"
    D="$HOME/.claude/projects/$(printf '%s' "$P" | sed 's|/|-|g')"
    echo "$D"
    mkdir -p "$D"
    tar xzf ~/bp_memory.tgz -C "$D"
    ls "$D/memory" | wc -l

The `echo` prints the target before the extraction, so you can see it is a
`-Users-...` path and not a bare `~/.claude/projects/`. The count is about
123 files, not an exact number to match. If `$P` is ever empty the target
collapses to `~/.claude/projects/` and the memory lands in a stray `memory/`
directory there; if that happens, `rm -rf ~/.claude/projects/memory` and
re-run the block.

Check `MEMORY.md` is at `$D/memory/MEMORY.md`. Without this step the next
session starts with no history, and the traps recorded in those files get
rediscovered the expensive way.

The session transcripts are a separate 311 MB in the same project directory.
They are not needed and hold full conversation history, so leave them.

### Step 7: install what the presentation scripts need

    brew install ffmpeg
    python3 -m pip install matplotlib biopython

That is the whole dependency list. Across the 20 top-level scripts the only
external binaries invoked are `ffmpeg` and `ffprobe`, and the only third-party
imports are `matplotlib` and `Bio`. No R, no bioinformatics toolchain, no
containers.

### Step 8: verify on the Mac

Three checks, none of which writes anything. Run them in this order.

First, completeness. Every data file the top-level scripts name should exist:

    for f in $(grep -ohE '[A-Za-z0-9_-]+\.(tsv|csv|nwk|treefile|json|txt)' *.py | sort -u); do
      [ -e "$f" ] || echo "MISSING $f"
    done

Silence is the pass. On this workstation that loop reports nothing, so anything
it names on the Mac is a gap in the transfer and not a pre-existing absence.

Second, integrity. All three manifests verified here on 2026-09-14 with zero
failures, at 44, 2 and 40 files respectively, so any mismatch is the copy:

    ( cd ANIMO_PACK && sha256sum -c MANIFEST.sha256 ) | grep -c ': OK$'
    ( cd FINAL_BASIS_2026-08-22 && sha256sum -c MANIFEST.sha256 ) | grep -c ': OK$'
    ( cd ~/Downloads/ANIMO_DELIVERABLES_2026-09-09 && sha256sum -c MANIFEST.sha256 ) | grep -c ': OK$'

Third, the toolchain. This reports how the narration fits each clip and writes
nothing:

    python3 make_narrated_videos_bp.py --check

The stronger test is regenerating the tables, because it proves the numbers
reproduce and not merely that the files arrived. It is held back to last
because **`make_tables_bp.py` overwrites `TABLES.md` in place**, and `TABLES.md`
currently carries uncommitted manual edits. Commit those first, or copy the
file aside:

    cp TABLES.md ~/TABLES.md.mine
    python3 make_tables_bp.py
    diff ~/TABLES.md.mine TABLES.md

Read that diff rather than expecting it to be empty. A difference can mean the
bundle is incomplete, or it can mean the manual edits are not reproducible from
the script, which is a question about the manuscript and not about the move.

## 6. The Mac is better for narration, and worse for one thing

**Better.** `make_voice_lines_bp.py` already writes `voice/say_macos.sh`, which
drives the built-in macOS `say` with no API key, no network and no cost. The
narration pack is timed at 132 words per minute and `say -r` takes words per
minute directly, so the engine and the timings agree exactly. On this Linux box
that path does not exist and the alternative is a paid ElevenLabs key.

One caution. Changing the voice changes the line durations, so the retime step
has to be re-run against the new audio, not assumed. Pick the voice once, then
time to it.

**Worse.** The Mac cannot reproduce the analysis, and should not try. The
byte-reproducibility of the workflow under `--deterministic true` was
demonstrated on this hardware, and cross-hardware differences are already a
known feature of this project: the A100 control run gives 88 units where this
workstation gives 85. Treat `FINAL_BASIS_2026-08-22` as frozen input on the Mac.
If a number has to be regenerated, regenerate it here.

This is also why the assembly set, the 19 GB of 2,804 assemblies, is not in the
bundle. It is an input to analysis, and analysis is finished.

## 7. TB1 will not mount on the Mac

The archive of record is an external 916 GB disk labeled TB1, ext4, normally at
`/media/phemarajata/TB1`. It is not attached right now. It holds the superseded
results moved out of the workspace, and for the 53 GB moved on 2026-08-24 those
are the only copies. `TB1_ARCHIVE_REGISTER.md` in this repo is the register.

macOS cannot read ext4 without help. Three options, in the order I would try
them:

1. Leave TB1 with this workstation and keep it as the archive. Nothing in the
   presentation stage reads from it.
2. Install macFUSE with ext4fuse for read-only access, which is enough to
   retrieve a file.
3. Copy TB1 to a fresh exFAT disk. Only worth it if the Linux box is going
   away, and it needs a third disk, since reformatting in place destroys the
   only copies.

Do not reformat TB1 to make it Mac-readable while it holds sole copies.

## 8. Do not decommission this workstation yet

After the Mac is verified, this machine still uniquely holds 367 GB of run
output, the 19 GB assembly set, and the only working path to TB1. Keep it until
the manuscript is submitted. The presentation work moves; the archive stays.
