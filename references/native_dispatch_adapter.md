# Native dispatch adapter

`dispatchAfterReady({request, check, dispatch})` in `scripts/dispatch_guard.js` is plain JavaScript: copy the exact source into a persistent host JavaScript executor and run the check and dispatch callbacks in that same call. It does not depend on Node, run a process, discover a host tool, or intercept dispatches that bypass this entry. The controller retains the card and writer, confirms authorization and deadlines, and preserves the original native observations. Task 12 owns integration into default instructions; task 04 covers navigation.

The request contains nonempty strings `request_id`, `project_root`, `tool_entry`, `task_path`, `task_id`, `owner`, `phase`, `candidate`, and `context`. Use a unique request ID and the exact paths actually passed to the command. The CLI reports an absolute `task_path`, so use that exact absolute path in both request and argv. Use the same spelling for cwd and project root; no path normalization is performed. The guard snapshots the fields before awaiting the check.

The trusted `check(request)` callback starts the actual frozen CLI in `request.project_root` and waits for its native command terminal result. Adapt the host's real tool schema, rather than inventing fields, to return:

```js
{
  state: 'completed', exit_code: 0,
  argv: [python, '-B', request.tool_entry, '--dispatch-check', request.task_path,
    '--context', request.context, '--phase', request.phase, '--owner', request.owner],
  cwd: request.project_root, request_id: request.request_id,
  terminal_evidence: {source: 'native-tool-and-operation', id: 'native-result-reference'},
  stdout: rawStdout, stderr: rawStderr
}
```

`python` is the actual executable on Linux or Windows; `-B` may be omitted. The reported argv and cwd must be from the actual invocation, not constructed later as a claim. The evidence source and ID are nonempty references to the host's original terminal observation, retained separately. Return actual state/exit/stdout/stderr even for failure or unknown; do not map running or missing terminal proof to completed. If the host provides a running handle, wait or query according to its real schema; a returned `running` observation is refused. A check exception is refused.

The guard requires integer zero exit, completed state, matching argv/cwd/request ID, a terminal reference, one JSON document, READY, and exact task path/ID, phase and candidate. It returns `{dispatched, reason, check, delegation}`. On a valid result it calls `dispatch(request, ready)` once and returns its raw native result, including unknown. `dispatched: true` means the callback was invoked, not that a native session succeeded. A thrown dispatch is returned as `dispatch-error` with its error; its outcome may be unknown. There is no automatic retry, polling, cross-call cache, or deduplication: the controller must resolve an unknown outcome before any later attempt.

The callbacks are the trust boundary. The guard validates their reported shape and binding, but cannot authenticate native provenance, prove the executable or cwd actually used, establish that the context's contents are fresh, or prevent another route from dispatching. The controller and independent reviewer must check native originals, actual argv/cwd, context contents and timing, claim ownership, and candidate immediately before use. Preserve the native session ID, check output, terminal source, call order, and native result separately. Node callback tests are synthetic and do not establish real Codeg consumption or a native terminal state.
