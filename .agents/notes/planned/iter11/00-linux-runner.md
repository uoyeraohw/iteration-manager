# Iteration 11 task00: Linux deadline runner

Status: planned; implementation requires independent review.

The 2026-11-15 explicit platform migration authorization supersedes the earlier Windows-only restriction for task00. The existing checkpoint-resume note records why a gated Windows Job is required and remains historical evidence; it does not establish Linux support. The common workflow source belongs to task12.

A dedicated supervisor becomes a Linux subreaper before the target can be launched, validates `/proc` and pidfd operations, and gates launch on the remaining deadline. It adopts orphans and repeatedly kills its own unreaped direct children by pidfd until `waitpid` proves no children remain; this also handles descendants that call setsid. The caller does not alter its own subreaper state. A lost supervisor or missing proof is unknown, never a successful tree terminal. Normal SIGTERM requests cleanup; hard kill remains unknown. This provides no claim about privileged container escape or unsupported systems.

A process group alone cannot contain setsid escapes and read-only cgroups cannot provide ownership here. Windows continues to use its original Job implementation. The version 1 receipt, direct argv, deadline reserve, exclusive evidence and distinct business/runner status remain shared. Linux results are supported only by actual task00 evidence; Windows historical evidence is not a current Windows rerun. Independent review and formal coordination still precede any frozen runner use by other tasks.
