"""Validation for the null resume patch (run_null skip logic).

Proves: replaying-and-discarding N genome draws from Random(1000) leaves the
stream at the exact next draw, so a resumed run generates byte-identical scenes
without re-simming. Compares rebuilt .vxa text against the live files the
original run produced. Read-only against /tmp/stage1.
"""
import json, random, sys
sys.path.insert(0, ".")
import genomes, vxa_scene

OUT = "/tmp/stage1/null"

def build_tag(mat, ph, tag):
    p = f"{OUT}/{tag}.vxa"
    return vxa_scene.build_vxa(mat, ph, lattice_dim=0.05, stop_time=11.0,
                               init_cm_time=1.0, temp_period=0.5, gravity=-0.1,
                               fitness_file=p + ".fitness")

def main():
    report = []
    # 1. durable partial integrity
    rows = json.load(open(f"{OUT}/null.json"))
    assert all(r["i"] == k for k, r in enumerate(rows)), "rows not contiguous"
    assert all(set(r) == {"i", "F", "F_A", "F_B", "failed"} for r in rows), "row schema drift"
    n = len(rows)
    report.append(f"durable rows: {n}, contiguous i=0..{n-1}, schema ok")

    checks = [n, n + 9]  # next design to sim, and one further out
    # 2. reference stream: fresh sequential draws 0..max(checks)
    rng_ref = random.Random(1000)
    ref = {}
    for i in range(max(checks) + 1):
        mat, ph = genomes.valid_random_genome(rng_ref)
        if i in checks:
            ref[i] = build_tag(mat, ph, f"n{i}_A")
    # 3. resume stream: skip n draws (discard), then continue
    rng_res = random.Random(1000)
    for _ in range(n):
        genomes.valid_random_genome(rng_res)
    ok = True
    for j, i in enumerate(range(n, max(checks) + 1)):
        mat, ph = genomes.valid_random_genome(rng_res)
        if i in checks:
            rebuilt = build_tag(mat, ph, f"n{i}_A")
            live = open(f"{OUT}/n{i}_A.vxa").read()
            same_ref = rebuilt == ref[i]
            same_live = rebuilt == live
            ok &= same_ref and same_live
            report.append(f"design n{i}: rebuilt==fresh-stream: {same_ref}, rebuilt==live-file: {same_live}")
    report.append("RESUME VALIDATION: " + ("PASS" if ok else "FAIL"))
    print("\n".join(report))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
