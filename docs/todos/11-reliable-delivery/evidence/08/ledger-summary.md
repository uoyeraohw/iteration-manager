# Task 08 decision and ledger material — 2026-11-15 UTC

Decision: retain the current product implementation. This is a measurement spike; no optimization or cross-call acceptance cache was implemented. The candidate observed was Git HEAD `6a54aceb2fc540d20480f9cdb5e5a683359c8e1a` plus the uncommitted source hashes recorded in `measurements.json` and `source-manifest.json`. No future implementation commit is asserted.

The synthetic workloads adapt `tests/test_completion_gates.py::make_reviewed_candidate` and `tests/test_filesystem_delivery_controller.py::fixture`: independent per-card scopes, real Git C/registration histories or filesystem manifests and byte snapshots, frozen cards/goals, check outputs and review reports. All receipts, reports, commands and approvals in those workloads are synthetic: they do not claim real execution, independent human review or business acceptance. Every audit had to return PASS and the untimed board accepted count had to equal size before any trial. The retained temporary workload roots are in measurements.

| Mode | Cards / accepted | Operation | Mean seconds | Range seconds | Git calls per trial | Path-read bytes per trial |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| git | 10 / 10 | board | 0.5579 | 0.5367–0.5797 | 221,221,221 | 36360,36360,36360 |
| git | 10 / 10 | all_envelopes | 0.6737 | 0.6118–0.7363 | 250,250,250 | 24830,24830,24830 |
| git | 10 / 10 | inventory | 0.6469 | 0.6090–0.6690 | 260,260,260 | 31070,31070,31070 |
| git | 10 / 10 | http_evidence | 0.5618 | 0.5546–0.5658 | 222,222,222 | 36427,36427,36427 |
| git | 100 / 100 | board | 6.0656 | 6.0288–6.1262 | 2201,2201,2201 | 363600,363600,363600 |
| git | 100 / 100 | all_envelopes | 6.7058 | 6.5659–6.8386 | 2500,2500,2500 | 248300,248300,248300 |
| git | 100 / 100 | inventory | 7.2009 | 6.9934–7.3303 | 2600,2600,2600 | 310700,310700,310700 |
| git | 100 / 100 | http_evidence | 5.9955 | 5.8173–6.1178 | 2202,2202,2202 | 363667,363667,363667 |
| filesystem | 10 / 10 | board | 0.0242 | 0.0238–0.0248 | 0,0,0 | 55610,55610,55610 |
| filesystem | 10 / 10 | all_envelopes | 0.0209 | 0.0203–0.0215 | 0,0,0 | 42750,42750,42750 |
| filesystem | 10 / 10 | inventory | 0.0235 | 0.0228–0.0241 | 0,0,0 | 49010,49010,49010 |
| filesystem | 10 / 10 | http_evidence | 0.0273 | 0.0236–0.0314 | 0,0,0 | 55727,55727,55727 |
| filesystem | 100 / 100 | board | 0.2529 | 0.2304–0.2689 | 0,0,0 | 555650,555650,555650 |
| filesystem | 100 / 100 | all_envelopes | 0.2084 | 0.2034–0.2122 | 0,0,0 | 427500,427500,427500 |
| filesystem | 100 / 100 | inventory | 0.2726 | 0.2566–0.2911 | 0,0,0 | 490100,490100,490100 |
| filesystem | 100 / 100 | http_evidence | 0.2387 | 0.2359–0.2434 | 0,0,0 | 555767,555767,555767 |

Each comma-separated count is an actual trial; in this sample each count and byte value was constant, so its mean and range equal that value. The inventory was BLOCKED for completed cards, while its acceptance verdicts were PASS: readiness and acceptance are separate. Fixture construction, the pretrial audit, board acceptance check, HTTP server startup/shutdown and source hashing were excluded. Time includes actual operation, assertions and, for HTTP, the stdlib client request and full body read; the handler first generates the complete board. Git counts are launched Git subprocesses, not simulated calls. Bytes count only bytes returned by `Path.read_bytes` and UTF-8 encoded text returned by `Path.read_text`; they include FS source/snapshot reads, but exclude Git subprocess reads, other Python I/O, kernel I/O and socket traffic. No browser or UI interaction was measured.

The Git 100-card board launched 2201 Git processes per trial, and HTTP launched 2202; the latter handler generates the board before reading evidence. `scripts/iter_contracts.py::validate_binding` resolves base/head/contract independently and reads both contract and head versions of card and goal; this workload deliberately uses the same commit for head and contract. Those are concrete within-call repetition candidates, but this experiment does not isolate their cost or prove a speedup. `iter_inventory.inventory` already reuses audits inside one inventory call. A future change could investigate invocation-local reuse keyed by resolved immutable commit and path, preserving separate error handling, working-tree drift, mutable inputs and all binding/compatibility tests; establish a controlled before/after on the same fixture before adopting it. No reuse across calls is proposed.

Limits: three samples characterize these runs only and do not establish robust tail latency, production load, human approval, other platforms, real external business completion, or a comparison to task 07. Git and FS workloads have different binding mechanisms and are not an equivalence or speedup experiment. The code uses synthetic Spike cards and simple small files, on the recorded Linux 4-vCPU AMD EPYC VM, Python 3.11.17 and Git 2.47.3; `measurements.json` has precise environment and all individual timings.

Interfaces for a future consumer: `tests/benchmarks/approval_chain.py:main(argv=None) -> int`, `--sizes <positive integers> --repeats <positive integer> --output PATH`, and JSON fields `environment`, `base`, `source_sha256`, `definitions`, `workloads[].approved_count`, and `workloads[].operations[].trials`. Count definitions and limitations must travel with results. Context is synthetic; no new FS recovery or platform support is implied.

Evidence: `fixture-test-01.json` and raw output preserve the initial two Git failures caused by a shared multi-card candidate; `fixture-test-03.json` and raw output record 4 passing tests after per-card commits, including real source drift rejection and neighbor preservation in both modes. `experiment-01.json` and raw output record the complete matrix, exit 0 and terminal tree. No fake TDD RED is claimed for this Spike. Independent candidate C, review of C and frozen specification, registration D, and frozen local strict remain with the controller; this document is material for the existing card ledger, not a new state ledger.
