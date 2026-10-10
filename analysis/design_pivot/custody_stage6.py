"""Stage-6 custody: archive all sim scenes + logs + result jsons into results/design_pivot/stage6/,
verify archive coverage against the full design index at archive time, write SHA256SUMS.txt."""
import glob, hashlib, json, os, shutil, tarfile

SRC = "/tmp/stage6"
DST = "/home/sandbox/mega27-19-xenobot-causal-networks/results/design_pivot/stage6"
RUNS = ["seed30", "seed31", "seed32", "null9000"]
os.makedirs(os.path.join(DST, "custody"), exist_ok=True)

# 1. copy logs and result jsons
copies = []
for r in RUNS:
    for f in glob.glob(f"{SRC}/{r}*.log") + glob.glob(f"{SRC}/{r}/*.json") + glob.glob(f"{SRC}/{r}/checkpoint.json"):
        base = os.path.basename(f)
        name = f"{r}-{base}" if not base.startswith(r) else base
        tgt = os.path.join(DST, name)
        shutil.copyfile(f, tgt); copies.append(tgt)
for f in glob.glob(f"{SRC}/audit/*.json") + glob.glob(f"{SRC}/audit/*.jsonl") + [f"{SRC}/audit.log", f"{SRC}/novelty_stage6.log", f"{SRC}/pooled_stage6.json", f"{SRC}/morphology_stage6.json"]:
    tgt = os.path.join(DST, os.path.basename(f))
    shutil.copyfile(f, tgt); copies.append(tgt)
print(f"copied {len(copies)} logs/jsons")

# 2. tarball of every scene file (vxa + fitness) across run dirs and audit re-runs
scene_files = []
for r in RUNS + ["audit"]:
    scene_files += sorted(glob.glob(f"{SRC}/{r}/*.vxa") + glob.glob(f"{SRC}/{r}/*.vxa.fitness"))
tar_path = os.path.join(DST, "custody", "stage6-scenes.tar.gz")
with tarfile.open(tar_path, "w:gz") as tar:
    for f in scene_files:
        run = os.path.basename(os.path.dirname(f))
        tar.add(f, arcname=f"{run}/{os.path.basename(f)}")
print(f"archived {len(scene_files)} scene files")

# 3. verification: tar/disk equality + every referenced scene in the design index
with tarfile.open(tar_path) as tar:
    members = set(tar.getnames())
disk = {f"{os.path.basename(os.path.dirname(f))}/{os.path.basename(f)}" for f in scene_files}
assert members == disk, f"tar/disk mismatch: {len(members)} vs {len(disk)}"
print(f"tar/disk equality: {len(disk)} files, 0 missing")

checked, missing = 0, []
def need(path):
    global checked
    checked += 1
    if path not in members:
        missing.append(path)
for r in ["null9000"]:
    d = json.load(open(f"{SRC}/{r}/null.json"))
    for row in d["rows"]:
        i = row["i"]
        need(f"{r}/n{i}_A.vxa")
        if row.get("F_B") is not None:
            need(f"{r}/n{i}_B.vxa")
audit = json.load(open(f"{SRC}/audit/audit_stage6.json"))["results"]
for row in audit:
    arm, tag = row["arm"], row["tag"]
    need(f"{arm}/{tag}_A.vxa")
    if row.get("F_B") is not None:
        need(f"{arm}/{tag}_B.vxa")
    for rr in ("r1", "r2"):
        for ab in ("A", "B"):
            p = f"audit/{arm}_{tag}_{ab}_{rr}.vxa"
            if p in disk:
                need(p)
print(f"design-index references checked: {checked}, missing: {len(missing)}")
assert not missing, missing[:10]

# 4. SHA256SUMS over everything in the stage4 dir
sums = []
for root, _, files in os.walk(DST):
    for fn in sorted(files):
        p = os.path.join(root, fn)
        if os.path.basename(p) == "SHA256SUMS.txt":
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        sums.append(f"{h}  {os.path.relpath(p, DST)}")
open(os.path.join(DST, "SHA256SUMS.txt"), "w").write("\n".join(sums) + "\n")
print(f"SHA256SUMS.txt: {len(sums)} entries")
print("CUSTODY DONE")
