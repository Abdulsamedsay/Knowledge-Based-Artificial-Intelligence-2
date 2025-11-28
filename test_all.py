#Abdulsamed Say (s1146476)
#Ismail Vatansever (s1152889)

from time import time
from pathlib import Path
from os import makedirs
from conflictsets import ConflictSetRetriever
from hittingsets import run_hitting_set_algorithm

BASE_DIR = Path(__file__).resolve().parent
CIRCUITS_DIR = BASE_DIR / "circuits"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_CSV = RESULTS_DIR / "diagnosis_results.csv"

HEURISTICS = ["smallest_conflict", "most_frequent"]

def safe_str_list(items):
    """Pretty stringify a list (e.g., list of lists) for console/CSV."""
    return str(items).replace("\n", "").strip()

def unpack_result(res):
    """
    Support both (minimal, minimal, nodes) and (minimal, minimal)
    or (all_hs, minimal_hs, nodes). Return (minimal_hs, nodes_or_None).
    """
    if isinstance(res, tuple):
        if len(res) == 3:
            # (all_hs, minimal_hs, nodes) or (minimal, minimal, nodes)
            return res[1], res[2]
        elif len(res) == 2:
            # (all_hs, minimal_hs) or (minimal, minimal)
            return res[1], None
    # Fallback (unexpected shape): treat as minimal only
    return res, None

def run_suite():
    makedirs(RESULTS_DIR, exist_ok=True)

    # CSV header
    with open(RESULTS_CSV, "w", encoding="utf-8") as f:
        f.write("circuit,heuristic,conflict_count,diagnoses_count,nodes_expanded,runtime_s,conflicts,diagnoses\n")

    print("=" * 72)
    print("HITTING SETS — Batch run (circuits 1–7)")
    print("=" * 72)

    for i in range(1, 8):
        doc_path = CIRCUITS_DIR / f"circuit{i}.txt"
        print(f"\n--- Circuit {i} ---")
        if not doc_path.exists():
            print(f"Missing file: {doc_path}")
            continue

        csr = ConflictSetRetriever(str(doc_path))
        conflicts = csr.retrieve_conflict_sets()
        print(f"Conflicts ({len(conflicts)}): {safe_str_list(conflicts)}")

        for h in HEURISTICS:
            t0 = time()
            result = run_hitting_set_algorithm(conflicts, heuristic=h)
            dt = time() - t0

            minimal_diagnoses, nodes = unpack_result(result)

            print(f" Heuristic: {h}")
            print(f"   Minimal diagnoses ({len(minimal_diagnoses)}): {safe_str_list(minimal_diagnoses)}")
            if nodes is not None:
                print(f"   Nodes expanded: {nodes} | Runtime: {dt:.6f} s")
            else:
                print(f"   Nodes expanded: (not reported) | Runtime: {dt:.6f} s")

            with open(RESULTS_CSV, "a", encoding="utf-8") as f:
                nodes_val = "" if nodes is None else nodes
                f.write(
                    f"{i},{h},{len(conflicts)},{len(minimal_diagnoses)},{nodes_val},{dt:.6f},"
                    f"\"{safe_str_list(conflicts)}\",\"{safe_str_list(minimal_diagnoses)}\"\n"
                )

    print("\nSaved CSV results to:", RESULTS_CSV)

if __name__ == "__main__":
    run_suite()
