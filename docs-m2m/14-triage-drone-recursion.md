# Triage: Drone Recursion Bug Patch

> **Status:** Patched — safe traversal guard applied  
> **Severity:** High (process hang / stack overflow in production agents)  
> **Affects:** `labs/agent-network-scan.js`, `labs/agent-retrieval.js`, `labs/agent-mission-intel.js`

---

## Bug Summary

The NetworkBuster lab agents perform a depth-first graph traversal of discovered network nodes while building the connection topology. When the network contains **cycles** (e.g., Node A → Node B → Node C → Node A) or an unusually deep mesh, the unbounded recursive walk exhausts the JavaScript call stack.

**Symptom:** The agent process hangs and must be killed; the parent scheduler (registered via `register-tasks.ps1`) restarts it up to 3 times, each time hitting the same cycle — causing a restart storm.

---

## Reproduction Steps

Given a cyclic network topology the agent maps:

```
Node A  →  Node B
Node B  →  Node C
Node C  →  Node A   ← cycle
Node C  →  Node E
Node A  →  Node D
Node D  →  Node E
```

When `agent-network-scan.js` calls `scanNode('A')` without a visited-set guard, the call chain becomes:

```
scanNode('A') → scanNode('B') → scanNode('C') → scanNode('A') → scanNode('B') → ...
```

Node.js throws `RangeError: Maximum call stack size exceeded` after ~10,000 frames, or the
process hangs if the cycle is slower / IO-gated.

---

## Root Cause

```js
// BEFORE — no cycle guard (vulnerable)
async function scanNode(nodeId, graph) {
  const neighbors = await fetchNeighbors(nodeId);
  graph[nodeId] = neighbors;
  for (const n of neighbors) {
    await scanNode(n, graph);   // ← recurses without checking if n was already visited
  }
}
```

---

## The Patch — Three Safe Patterns

All three patterns are demonstrated and verified in [`tools/drone-recursion-guard.js`](/tools/drone-recursion-guard.js).

### Pattern 1 — Visited Set (minimal change to existing recursive code)

Add a `visited` `Set` parameter and check it before recursing:

```js
// AFTER — Pattern 1: visited-set guard
async function scanNode(nodeId, graph, visited = new Set(), maxDepth = 64, depth = 0) {
  if (visited.has(nodeId)) return;           // ← cycle guard
  if (depth > maxDepth) {                    // ← depth-limit guard
    console.warn(`[scanNode] max depth reached at "${nodeId}" — stopping branch`);
    return;
  }

  visited.add(nodeId);
  const neighbors = await fetchNeighbors(nodeId);
  graph[nodeId] = neighbors;

  for (const n of neighbors) {
    await scanNode(n, graph, visited, maxDepth, depth + 1);
  }
}
```

**When to use:** Lowest-friction fix; preserves the recursive structure if the rest of the code relies on call-stack order.

---

### Pattern 2 — Iterative BFS (no stack risk)

Replace recursion with an explicit queue; zero stack-overflow risk regardless of graph size:

```js
// AFTER — Pattern 2: iterative BFS
async function scanGraph(startId, maxDepth = 64) {
  const graph   = {};
  const visited = new Set();
  const queue   = [{ nodeId: startId, depth: 0 }];

  while (queue.length > 0) {
    const { nodeId, depth } = queue.shift();

    if (visited.has(nodeId) || depth > maxDepth) continue;

    visited.add(nodeId);
    const neighbors = await fetchNeighbors(nodeId);
    graph[nodeId] = neighbors;

    for (const n of neighbors) {
      if (!visited.has(n)) {
        queue.push({ nodeId: n, depth: depth + 1 });
      }
    }
  }

  return graph;
}
```

**When to use:** Preferred for large or unknown-depth networks; also enables easy parallelism (batch-fetch neighbors).

---

### Pattern 3 — Async DFS with Circuit-Breaker Timeout

Adds a wall-clock deadline so the scan always finishes in bounded time, even against unreachable nodes:

```js
// AFTER — Pattern 3: async iterative DFS + circuit breaker
async function scanGraphWithTimeout(startId, { maxDepth = 64, timeoutMs = 5000 } = {}) {
  const deadline = Date.now() + timeoutMs;
  const graph    = {};
  const visited  = new Set();
  const stack    = [{ nodeId: startId, depth: 0 }];
  let   timedOut = false;

  while (stack.length > 0) {
    if (Date.now() > deadline) { timedOut = true; break; }

    const { nodeId, depth } = stack.pop();
    if (visited.has(nodeId) || depth > maxDepth) continue;

    visited.add(nodeId);
    const neighbors = await fetchNeighbors(nodeId);
    graph[nodeId] = neighbors;

    for (const n of neighbors) {
      if (!visited.has(n)) stack.push({ nodeId: n, depth: depth + 1 });
    }

    // Yield to event loop every 100 nodes so the process stays responsive
    if (visited.size % 100 === 0) {
      await new Promise(resolve => setImmediate(resolve));
    }
  }

  return { graph, timedOut, nodesScanned: visited.size };
}
```

**When to use:** Production agents that must not block the event loop indefinitely; result includes `timedOut` flag so callers can surface a partial result rather than hanging.

---

## Applied Files

| File | Change |
|------|--------|
| `labs/agent-network-scan.js` | Replace unbounded `scanNode()` recursion with Pattern 2 (iterative BFS) |
| `labs/agent-retrieval.js` | Add visited-set guard (Pattern 1) to document-graph walk |
| `labs/agent-mission-intel.js` | Add visited-set guard (Pattern 1) to mission-node traversal |
| `tools/drone-recursion-guard.js` | **New** — runnable demo harness; verifies all three patterns |

---

## Safety Notes

- **No credentials changed.** This patch only adds traversal guards.
- **No security posture change.** Guards are purely algorithmic; no new ports, no new auth flows.
- **Backward-compatible.** The `visited` parameter defaults to `new Set()`, so existing call sites that pass only `(nodeId, graph)` continue to work.
- **`maxDepth` default is 64.** Adjust per agent if your network legitimately exceeds 64 hops.
- **`timeoutMs` default is 5,000 ms** for Pattern 3. Set lower for health-check endpoints; set higher for deep-scan jobs.

---

## Testing

Run the standalone demo (requires Node.js ≥ 18):

```bash
node tools/drone-recursion-guard.js
```

Expected output confirms:

1. The unsafe recursive walk triggers `Maximum call stack size exceeded` (shown as a caught error)
2. All three safe patterns complete and print the correct traversal order without hanging

---

## Related Pages

- [Hidden Tools & Scripts](/02-hidden-tools)
- [API Server](/08-api-server)
- [CI/CD Pipelines](/05-cicd-pipelines)
- [Security Audit](/11-security-audit)
