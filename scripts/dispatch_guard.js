// Copy into the persistent JavaScript executor; no Node APIs or global scheduler.
async function dispatchAfterReady({request, check, dispatch} = {}) {
  const nonempty = value => typeof value === 'string' && value.trim().length > 0;
  const fields = ['request_id', 'project_root', 'tool_entry', 'task_path', 'task_id',
    'owner', 'phase', 'candidate', 'context'];
  let bound;
  try {
    if (!request || typeof request !== 'object' || Array.isArray(request) ||
        typeof check !== 'function' || typeof dispatch !== 'function' ||
        !fields.every(key => nonempty(request[key]))) {
      return {dispatched: false, reason: 'invalid-request', check: null, delegation: null};
    }
    bound = Object.freeze(Object.fromEntries(fields.map(key => [key, request[key]])));
  } catch (error) {
    return {dispatched: false, reason: 'invalid-request', check: null, delegation: null};
  }
  let observation;
  try { observation = await check(bound); }
  catch (error) {
    return {dispatched: false, reason: 'check-error', check: {error: String(error)}, delegation: null};
  }
  let ready;
  try {
    const expected = [bound.tool_entry, '--dispatch-check', bound.task_path,
      '--context', bound.context, '--phase', bound.phase, '--owner', bound.owner];
    const argv = observation?.argv;
    const offset = Array.isArray(argv) && argv[1] === '-B' ? 2 : 1;
    if (!observation || typeof observation !== 'object' || Array.isArray(observation) ||
        observation.state !== 'completed' || !Number.isInteger(observation.exit_code) ||
        observation.exit_code !== 0 || observation.request_id !== bound.request_id ||
        observation.cwd !== bound.project_root || !Array.isArray(argv) ||
        !nonempty(argv[0]) || argv.length !== expected.length + offset ||
        !expected.every((value, index) => argv[index + offset] === value) ||
        !observation.terminal_evidence || typeof observation.terminal_evidence !== 'object' ||
        Array.isArray(observation.terminal_evidence) ||
        !nonempty(observation.terminal_evidence.source) || !nonempty(observation.terminal_evidence.id) ||
        typeof observation.stdout !== 'string' || typeof observation.stderr !== 'string') {
      return {dispatched: false, reason: 'invalid-check', check: observation, delegation: null};
    }
    ready = JSON.parse(observation.stdout);
    if (!ready || typeof ready !== 'object' || Array.isArray(ready) ||
        ready.readiness !== 'READY' || ready.task_path !== bound.task_path ||
        ready.task_id !== bound.task_id || ready.phase !== bound.phase ||
        ready.candidate !== bound.candidate) {
      return {dispatched: false, reason: 'not-ready', check: observation, delegation: null};
    }
  } catch (error) {
    return {dispatched: false, reason: 'invalid-check', check: observation, delegation: null};
  }
  try {
    const delegation = await dispatch(bound, ready);
    return {dispatched: true, reason: 'dispatched', check: observation, delegation};
  } catch (error) {
    return {dispatched: true, reason: 'dispatch-error', check: observation,
      delegation: {error: String(error)}};
  }
}
