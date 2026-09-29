"""CM-trajectory fitness extraction for design-pivot behaviors.

Parses the `voxelyze -p` console output (Time / CM lines) and computes the
preregistered fitness quantities. Bounded tooling: evaluates single designs,
never performs selection.
"""
import math
import re
import subprocess

_CM = re.compile(r"^Time:\s*([0-9.eE+-]+)\s*$\nCM:\s*([0-9.eE+-]+)(?:\s*,\s*([0-9.eE+-]+))?(?:\s*,\s*([0-9.eE+-]+))?",
                 re.M)

def run_eval(vxa_path, driver, fitness_out, timeout=600):
    """Run one headless eval, return (cm_traj, fitness_xml_text).
    cm_traj = [(t, cx, cy, cz), ...] from -p output; cm components may be None
    if the driver prints a scalar - we detect that and treat as x-only."""
    proc = subprocess.run([driver, "-f", vxa_path, "-of", fitness_out, "-p"],
                          capture_output=True, text=True, timeout=timeout)
    traj = []
    for m in _CM.finditer(proc.stdout):
        t = float(m.group(1))
        cx = float(m.group(2))
        cy = float(m.group(3)) if m.group(3) is not None else None
        cz = float(m.group(4)) if m.group(4) is not None else None
        traj.append((t, cx, cy, cz))
    fx = open(fitness_out).read() if fitness_out else ""
    return traj, fx

def _displacement_x(traj, init_cm_time=0.3):
    """Net x displacement from the first sample at/after init_cm_time to final."""
    if not traj:
        return None
    base = next((c for (t, *c) in traj if t >= init_cm_time), traj[0][1:])
    x0 = base[0]
    xf = traj[-1][1]
    return xf - x0

def fitness_locomotion(traj, lattice_dim=0.01, init_cm_time=0.3):
    """Net +x displacement in body-voxel units."""
    d = _displacement_x(traj, init_cm_time)
    return None if d is None else d / lattice_dim

def fitness_bidirectional(traj_fwd, traj_rev, lattice_dim=0.01, init_cm_time=0.3):
    """min(+x under phase set A, -x under phase set B) in voxel units; >0 means
    the SAME design locomotes both ways under the two actuation conditions."""
    f = fitness_locomotion(traj_fwd, lattice_dim, init_cm_time)
    r = fitness_locomotion(traj_rev, lattice_dim, init_cm_time)
    if f is None or r is None:
        return None
    return min(f, -r)

def fitness_incline(traj, slope_deg, lattice_dim=0.01, init_cm_time=0.3):
    """Displacement projected on the up-slope direction, voxel units.
    Voxelyze FloorSlope tilts the floor about y; up-slope is +x with z lift:
    up-hill unit vector = (cos s, 0, sin s)."""
    d = _displacement_x(traj, init_cm_time)  # x-only CM prints; z lift tracked via scalar fallback
    if d is None:
        return None
    return (d * math.cos(math.radians(slope_deg))) / lattice_dim

def fitness_aperture(traj, wall_plane_x, margin_m, init_cm_time=0.3):
    """Meters the CM travels past the aperture plane; traversal counted only if
    this exceeds margin_m (= max possible half-extent of the design grid, so a
    pass means the whole body is through). Conservative: CM only."""
    if not traj:
        return None
    return traj[-1][1] - wall_plane_x
