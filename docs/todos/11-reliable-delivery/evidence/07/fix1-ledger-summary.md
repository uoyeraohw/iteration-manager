# Task 07 F1/F2 handoff — 2026-11-15 UTC

F1: The payload run still checks the real whitelist and absence of maintenance history. It now requires outer process success, nested runner COMPLETED, terminal tree, raw exit 0, and nonempty output. Pytest exit 5 covers an empty collection; no fixed passing-test total is assumed. `fix1-regression.json` records the single targeted regression, and `fix1-payload-receipt.json` preserves the nested receipt with its actual temporary cwd. No original evidence is overwritten.

F2: Reuse the original three-run samples, not reconstructed or repeated. Values below are wall-clock seconds per run; relative change is `(after mean - before mean) / before mean * 100`.

| Metric | Before | After | Change |
| --- | ---: | ---: | ---: |
| Run 1 (s) | 2.015566 | 1.904979 | — |
| Run 2 (s) | 2.013032 | 1.670483 | — |
| Run 3 (s) | 1.637504 | 1.955465 | — |
| Mean (s) | 1.888701 | 1.843643 | -0.045058 s (-2.39%) |
| Historical-path consumers | 2 | 0 | -2 |

These three samples are descriptive and do not establish or promise a performance improvement. Both phases use the same Linux Python, measurement script, selected test and sample; unique phase/run temporary roots differ. Before at 2026-11-15T05:14:42.102796+00:00 on original BASE `3158e75869d5c4346c51256de878f14ea190f305`; After at 2026-11-15T05:15:29.737267+00:00 is bound to implementation candidate `d09888af23991785f96ea98d902821b002961534`. The before phase necessarily used the original historical harness and consumers; the after phase used the extracted support. F1 changes only the separate portability test, not the selected test, support, measurement script or shared scripts. The current files match the original candidate SHA256 bindings; see `fix1-delivery.json` for hashes and retained receipts. Compatibility and baseline evidence remain applicable to their stated inputs; none is relabeled as a new run. Initial benchmark script failure remains recorded.

Formal regression ran with explicit frozen runner and external basetemp. No full suite, real browser, Windows, deployment or installation is asserted. Controller must append this table to the card before new C, then seek independent review, register D and run frozen local strict; implementer has not changed card or approved it. Coordinator fdcc4cc known defects cannot self-approve.
