# Iteration 11 task03: native dispatch guard

Existing execution-readiness decision requires a fresh per-dispatch check but leaves native dispatch to the controller. Use one injectable async guard in the host executor: bind the reported command, request and READY output, then invoke the native callback once. It preserves the existing event ledger and does not change the deadline guard or add a scheduler. A pending check cannot dispatch early; failed, unknown or inconsistent observations fail closed.

The callbacks and original host evidence remain trusted inputs. String identity and source references do not authenticate command execution or context freshness; controller and independent reviewer verify originals. A dispatch exception or unknown native response remains unresolved and is never automatically retried. Synthetic Node tests establish guard behavior only; real host consumption and independent review remain separate.
