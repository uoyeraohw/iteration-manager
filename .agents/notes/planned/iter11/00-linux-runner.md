# Iteration 11 task00: Linux deadline runner

Status: planned; implementation requires independent review.

The 2026-11-15 explicit platform migration authorization supersedes the earlier Windows-only restriction for task00. The existing checkpoint-resume note records why a gated Windows Job is required and remains historical evidence; it does not establish Linux support. The common workflow source belongs to task12.

A dedicated supervisor becomes a Linux subreaper before the target can be launched, validates `/proc` and pidfd operations, and gates launch on the remaining deadline. It adopts orphans and repeatedly kills its own unreaped direct children by pidfd until `waitpid` proves no children remain; this also handles descendants that call setsid. The caller does not alter its own subreaper state. A lost supervisor or missing proof is unknown, never a successful tree terminal. Normal SIGTERM requests cleanup; hard kill remains unknown. This provides no claim about privileged container escape or unsupported systems.

A process group alone cannot contain setsid escapes and read-only cgroups cannot provide ownership here. Windows continues to use its original Job implementation. The version 1 receipt, direct argv, deadline reserve, exclusive evidence and distinct business/runner status remain shared. Linux results are supported only by actual task00 evidence; Windows historical evidence is not a current Windows rerun. Independent review and formal coordination still precede any frozen runner use by other tasks.

F1 continuation: the final launch gate orders caller EOF at its nonblocking pipe observation and cancellation signals at the blocked pending-signal observation. An observed cancellation or expired deadline refuses launch; once those observations pass, launch wins and a later signal or EOF requests cleanup of the launched tree. These separate observations do not claim an atomic snapshot of unrelated asynchronous events. The child restores the prior signal mask before exec. See fix1 raw RED and fixed-driver receipts for this candidate; independent review remains necessary.
