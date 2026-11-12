// Copy this function unchanged into the JavaScript tool executor; no Node APIs.
// Keep the await/query/cancel loop in ONE executor call, outside model turns.
async function watchDeadline({
  deadlineMs, query, cancel, cancelReserveMs = 10000, checkpoints = [],
  now = Date.now, pause = ms => new Promise(resolve => setTimeout(resolve, ms)),
}) {
  if (!Number.isFinite(deadlineMs) || !Number.isFinite(cancelReserveMs) ||
      cancelReserveMs < 0 || checkpoints.some(x => !Number.isFinite(x))) {
    throw new Error('Finite absolute deadline/checkpoints and nonnegative reserve required');
  }
  const cancelAt = deadlineMs - cancelReserveMs;
  const pending = [...checkpoints].sort((a, b) => a - b);
  const events = [];
  const terminal = value => ['completed', 'failed', 'canceled'].includes(value?.status);
  async function stop(reason) {
    const requestedAt = now();
    let canceled, final;
    try { canceled = await cancel(); }
    catch (error) { canceled = { error: String(error) }; }
    const confirmedAt = now();
    // Omit wait_ms: Codeg wait_ms=0 means UNBOUNDED, not a poll.
    try { final = await query(); }
    catch (error) { final = { status: 'unknown', error: String(error) }; }
    return { reason, deadlineMs, cancelAt, requestedAt, confirmedAt,
      lateByMs: Math.max(0, confirmedAt - deadlineMs), canceled, final,
      terminalConfirmed: terminal(final), events };
  }
  for (;;) {
    const startedAt = now();
    while (pending.length && pending[0] <= startedAt) {
      events.push({ kind: 'checkpoint', dueAt: pending.shift(), observedAt: startedAt });
    }
    if (startedAt >= cancelAt) return stop('deadline');
    const boundary = Math.min(cancelAt, pending[0] ?? cancelAt);
    const waitMs = Math.max(1, Math.floor(Math.min(60000, boundary - startedAt)));
    let result;
    try { result = await query(waitMs); }
    catch (error) {
      events.push({ kind: 'query-error', startedAt, error: String(error) });
      return stop('monitor-error');
    }
    events.push({ kind: 'query', startedAt, returnedAt: now(), waitMs, result });
    if (terminal(result)) return { reason: 'terminal', deadlineMs, final: result,
      terminalConfirmed: true, observedAt: now(),
      lateByMs: Math.max(0, now() - deadlineMs), events };
    if (result?.status !== 'running') return stop('monitor-unknown');
    // blocked_on/fast updates can return immediately; avoid a busy loop.
    // The caller surfaces blocked_on from events; the deadline guard stays armed.
    if (now() - startedAt < waitMs) {
      const remaining = Math.min(cancelAt, pending[0] ?? cancelAt) - now();
      if (remaining > 0) await pause(Math.min(1000, remaining));
    }
  }
}
