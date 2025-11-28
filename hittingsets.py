#Abdulsamed Say (s1146476)
#Ismail Vatansever (s1152889)

from collections import Counter, deque

# --- helpers ---
def _hits_all_conflicts(H, conflicts):
    #Check if the set H intersects (hits) every conflict set
    return all(set(H) & set(C) for C in conflicts)

def _is_minimal(candidate, minimal_sets):
    # A candidate is minimal if it does not fully contain a previously found hitting set
    # (except if they are exactly the same)
    cset = set(candidate)
    return all(not set(ms).issubset(cset) or set(ms) == cset for ms in minimal_sets)

def _reduce_conflicts(conflicts, H):
    # Remove all conflicts that are already hit by the current partial hitting set H
    # This reduces the search space in the hitting set tree
    H = set(H)
    return [C for C in conflicts if not (H & set(C))]

def _choose_conflict(conflicts, mode="smallest_conflict"):
    # Decide which conflict to branch on
    # The "smallest_conflict" heuristic usually gives fewer branches
    if not conflicts:
        return None
    if mode == "smallest_conflict":
        return min(conflicts, key=len)
    # Alternative heuristic: use the conflict with the most frequent elements
    cnt = Counter(x for C in conflicts for x in C)
    return max(conflicts, key=lambda C: sum(cnt[x] for x in C))

def _order_elements(conflict, conflicts, element_order="freq_desc"):
    if element_order == "as_is":
        return list(conflict)
    cnt = Counter(x for C in conflicts for x in C)
    return sorted(conflict, key=lambda x: (-cnt[x], x))

def _hs_tree(conflicts, heuristic):
    # Main hitting set tree algorithm
    # Uses BFS (queue) to explore partial hitting sets
    minimal = [] # list of minimal hitting sets
    seen = set() # avoid duplicates
    nodes_expanded = 0
    q = deque()
    q.append((frozenset(), conflicts)) # start with empty set
    while q:
        H, rem = q.popleft()
        nodes_expanded += 1
         # If H already contains a smaller hitting set, skip it
        if not _is_minimal(H, minimal):
            continue
         # Remove conflicts that H already hits
        rem = _reduce_conflicts(rem, H)
        # If no conflicts left, then H is a complete hitting set
        if not rem:
            key = tuple(sorted(H))
            if key not in seen and _is_minimal(H, minimal):
                seen.add(key)
                minimal.append(list(key))
            continue
        C = _choose_conflict(rem, mode=heuristic if heuristic in ("smallest_conflict",) else "smallest_conflict")
        if C is None:
            continue
        for e in _order_elements(C, rem, element_order="freq_desc" if heuristic == "most_frequent" else "as_is"):
            q.append((frozenset(set(H) | {e}), rem))
    minimal.sort(key=lambda x: (len(x), x))
    return minimal, nodes_expanded

def run_hitting_set_algorithm(conflict_sets, heuristic="smallest_conflict"):
    # Wrapper used by main.py
    # Converts conflict sets to strings and runs the hitting set tree
    conflicts = [list(map(str, C)) for C in conflict_sets if C]
    if not conflicts:
        return [], [], 0
    minimal, nodes = _hs_tree(conflicts, heuristic=heuristic)
    return minimal, minimal, nodes

def assert_minimality(conflicts, diagnoses):
    # every diagnosis hits all conflicts
    for d in diagnoses:
        assert all(set(d) & set(C) for C in conflicts), f"Not a hitting set: {d}"
    # minimal: no diagnosis is a superset of another
    for i, d in enumerate(diagnoses):
        for j, e in enumerate(diagnoses):
            if i != j:
                assert not set(e).issubset(set(d)) or set(e) == set(d), f"Non-minimal: {d} ⊇ {e}"

