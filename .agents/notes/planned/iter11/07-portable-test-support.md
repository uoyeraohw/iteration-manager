# 07 · Portable browser test support

2026-11-15. The two handoff consumers previously loaded a historical evidence artifact. Keep that artifact unchanged and extract the same harness into the delivered `tests/support/` tree, changing only the root-parent index needed by its new location. This retains the nonisolated real inventory path and the synthetic isolated inventory rather than changing their meaning.

Use `iter_install._inventory` as the actual delivery whitelist to construct a temporary payload; run affected tests there with the explicitly selected runner and no maintenance history. This proves the tested Linux/Python payload only, not an installed release, native browser interaction, Windows, or an entire maintenance suite. Test defaults permit local use; formal validation explicitly selects the frozen runner and deadline. See task07 evidence for measurements and receipts.
