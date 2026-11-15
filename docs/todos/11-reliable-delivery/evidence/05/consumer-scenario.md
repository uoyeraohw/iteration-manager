# Fresh-session consumer scenario (pending)

Read `references/support_matrix.md` and its linked primary sources independently. Answer with source links and the stated candidate and date; do not infer execution from source or command success from session completion.

1. Is the current Linux runner approved and what exact snapshot and baseline does that cover? Expected: task00 C2 `3f949f807d3c2eb47b97a116bd6932da55778edd`, six-file frozen platform snapshot; Python 3.11 baseline 513 passed/2 Windows skips at `48e731ed266a35c06c9146aff9eaaf866c3a2e3f`, with reuse applicability reviewed for unchanged source, limited to that environment. [Task00](../../00-linux-runner-and-dev-guide.md).
2. Is the Codeg worker operational? Expected: native invocation succeeded after READY, worker shell could not start due to bwrap proc mount; BLOCKED, not a successful command. [Raw chain](../03/native-codeg-chain.json).
3. Does the latest Windows historical release prove the current candidate on Windows? Expected: 493 passed at 2026-11-14 release `26652bad2fcfb7c883d8e9a8bcad4aeb96160816`, not a current Windows run. [Release](../../../../releases/iteration10-20261114/README.md).
4. Can an FS task use Git's interruption grant? Does normal release prove that? Expected: no; FS grant explicitly unsupported even in a Git repository, normal release/claim is separate. [Contract](../../../../../references/checkpoint_execution.md).
5. Was a complete external FS business lifecycle validated? Expected: UNKNOWN; isolated or historical local samples do not prove it. [Release](../../../../releases/iteration10-20261114/README.md).
6. Does Antigravity's consumption prove Gemini CLI auto discovery or configuration injection? Expected: no, both UNKNOWN; Linux symlink topology differs from Windows independent copies. [Release](../../../../releases/iteration10-20261114/README.md), [matrix](../../../../../references/support_matrix.md).
7. Is this candidate installed and consumed in a new session? Expected: UNKNOWN; no deployment in this task; historical explicit-root consumption is distinct. Historical files may be absent from installed package. [Matrix](../../../../../references/support_matrix.md).

Controller to run actual independent fresh consumer before C, preserve its answers and compare to these expectations. This document is a scenario, not a result.
