# Project status

**Title:** The House That Ate Tomorrow  
**Tagline:** Tomorrow is missing. The cat denies everything.  
**Updated:** 28 October 2026  
**Stage:** First playable Street + Entrance Hall slice; local verification and review.

## Approval and current scope

The user approved the original art package with “YEAH NOT BAD AT ALL ART APPROVED”. [ART_APPROVAL_RECORD.md](ART_APPROVAL_RECORD.md) records that approval and authorization for the first playable slice. Candidate A, Candlelit Registry, is the selected hall direction. The original supplied checklist remains unchanged; it is superseded for approval status by the explicit record.

The Godot 4.6.3 project now implements the Street and Entrance Hall, Visitor movement and collision, Fig conversations, the pocket mirror and The Almost, the Guestbook puzzle, first warning notice, and an explicit chapter-end panel at the newly opened doors. It includes a notebook, inventory, graduated hints, settings, autosave/Continue, title/pause/credits UI, and original synthesized music and effects.

The Visitor now has long dark hair and matching dialogue portraits, as requested on 28 October 2026. The visual revision and source are recorded in `assets/VISITOR_PROVENANCE.md`; the approved staging sprite remains preserved. The interface adds framed menus, clearer dialogue actions and notebook presentation, and the hall chandelier fades when it overlaps the player.

The world renders at 384×216 with nearest filtering; text and controls use a separate 1152×648 UI reference canvas. The hall uses approved 16×16 tiles and 24×32 Visitor animation cells. The street background and audio are new implementation assets with reproducible source under `tools/`.

## Verification and next milestone

[SLICE_REVIEW.md](SLICE_REVIEW.md) records run commands, automated coverage, actual browser evidence, and remaining review limits. Tests exercise persistent state, malformed-save recovery, coordinator regressions, world targets/collisions, and the complete chapter logic. Runtime captures are stored under `qa/runtime/`; concept art and earlier UI studies remain clearly separate.

The design target is an 8–10 minute first chapter; no independent timed human playtest has established that duration. The slice is ready for local review after the recorded build checks. Full production remains pending explicit slice acceptance. No remaining room, later puzzle, ending, deployment, or public release is represented as complete.

## Imported baseline and provenance

- The repository was empty before this import, on branch `work`, with no commits.
- Its configured origin is `https://github.com/itsnotalwin/THE-HOUSE-THAT-ATE-TOMORROW-.git`.
- All 22 supplied files were imported unchanged, with the enclosing ZIP folder removed. The standalone master prompt matches its archived copy.
- The original backlog contains 82 `NOT STARTED` entries and is preserved unchanged. Current art delivery is recorded in `art_staging/manifest.csv`; selected production copies are recorded in `assets/approved_manifest.csv`.
- The seven supplied PNGs are concept references. No production assets or game source were supplied.
- The proposed full design remains a 40–50 minute adventure with seven locations, five main puzzles, and two good endings. That scope is not implemented by this slice.

The older `Innate` repository and private vault have not been inspected or modified. Claims about their code, licenses, branches, and deployments remain historical references, not verified status for this checkout. The imported master prompt does not independently authorize actions.
