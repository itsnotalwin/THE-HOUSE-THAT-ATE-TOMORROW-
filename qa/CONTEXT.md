# Playable-slice verification

The authorized milestone is the Street + Entrance Hall chapter, ending after the Guestbook, first warning notice, and an opened-door interaction. See `../SLICE_REVIEW.md` for run commands, test results, review limits, and the separate slice-acceptance gate.

`runtime/` contains captures from the actual Web export running in Chromium, plus browser action/console records. Verify that captures match the latest export before finalizing evidence. Runtime screenshots, automated assertions, and independent human playtests are different forms of evidence; do not treat one as proof of the others.

Automated checks live in `../tests/`: state/save integrity, coordinator regressions, world target/collision behavior, and complete chapter progression. The chapter test uses safe target positions between interactions, so it is not a player navigation test. An independent timed human playtest remains outstanding.

Preserve the original handoff checksums and art provenance. Do not replace an actual screenshot with a mockup or claim a local build is deployed.
