"""Build .vxa simulation scenes for the design pivot (headless Voxelyze).

Bounded tooling only - no evolution, no selection-used compute in this module.
Schema learned from reconfigurable_organisms/_voxcad/voxelyzeMain/Example_withPhaseOffset.vxa
(Kriegman 2020 PNAS pipeline, CC0) and VoxCad/SampleSimulation.vxa (Fixed_Regions).
"""
import math
import xml.sax.saxutils as sx

# Material palette copied from Kriegman 2020 example design (units: SI, voxels 1 cm).
PALETTE = {
    1: ("Passive_Soft", 5e6, 0.0),
    2: ("Passive_Hard", 5e8, 0.0),
    3: ("Active_+", 5e6, 0.01),
    4: ("Active_-", 5e6, -0.01),
}

def _material_block(mid, name, emod, cte):
    return f"""<Material ID="{mid}">
<MatType>0</MatType><Name>{name}</Name>
<Display><Red>0</Red><Green>1</Green><Blue>1</Blue><Alpha>1</Alpha></Display>
<Mechanical>
<MatModel>0</MatModel>
<Elastic_Mod>{emod:g}</Elastic_Mod>
<Plastic_Mod>0</Plastic_Mod><Yield_Stress>0</Yield_Stress>
<FailModel>0</FailModel><Fail_Stress>0</Fail_Stress><Fail_Strain>0</Fail_Strain>
<Density>1e+006</Density><Poissons_Ratio>0.35</Poissons_Ratio>
<CTE>{cte:g}</CTE><uStatic>1</uStatic><uDynamic>0.5</uDynamic>
</Mechanical>
</Material>"""

def _fixed_box(x, y, z, dx, dy, dz):
    """Immobile box region (world units, meters). Used for aperture walls."""
    return f"""<FRegion>
<PrimType>0</PrimType>
<X>{x:g}</X><Y>{y:g}</Y><Z>{z:g}</Z>
<dX>{dx:g}</dX><dY>{dy:g}</dY><dZ>{dz:g}</dZ>
<Radius>0</Radius><R>0</R><G>1</G><B>0</B><alpha>1</alpha><Fixed>1</Fixed>
</FRegion>"""

def build_vxa(grid, phase, lattice_dim=0.01, stop_time=5.0, init_cm_time=0.3,
              temp_amp=39.0, temp_base=25.0, temp_period=0.147,
              floor_slope=0.0, gravity=-9.81, fixed_boxes=None,
              fitness_file="fitness.xml"):
    """grid[z][y][x] of material IDs (0=empty); phase[z][y][x] float phase offsets.
    fixed_boxes: list of (x,y,z,dx,dy,dz) world-unit boxes (aperture walls).
    floor_slope: degrees (native Voxelyze FloorSlope; incline-climbing scene)."""
    nz, ny, nx = len(grid), len(grid[0]), len(grid[0][0])
    layers, phlayers = [], []
    for z in range(nz):
        rows = ["".join(str(grid[z][y][x]) for x in range(nx)) for y in range(ny)]
        layers.append("<Layer><![CDATA[%s]]></Layer>" % "".join(rows))
        prows = [", ".join(f"{phase[z][y][x]:.9g}" for x in range(nx)) + ", " for y in range(ny)]
        phlayers.append("<Layer><![CDATA[%s]]></Layer>" % "".join(prows))
    fixed = fixed_boxes or []
    # FRegion coords are NORMALIZED WORKSPACE FRACTIONS (IsTouching divides the
    # voxel world position by GetWorkSpace()); convert meter args to fractions.
    wsx, wsy, wsz = nx * lattice_dim, ny * lattice_dim, nz * lattice_dim
    norm = [(x / wsx, y / wsy, z / wsz, dx / wsx, dy / wsy, dz / wsz) for (x, y, z, dx, dy, dz) in fixed]
    fixed_xml = f"<NumFixed>{len(norm)}</NumFixed>" + "".join(_fixed_box(*b) for b in norm)
    mats = "".join(_material_block(m, *PALETTE[m]) for m in sorted(PALETTE))
    return f"""<?xml version="1.0" encoding="ISO-8859-1"?>
<VXA Version="1.0">
<Simulator>
<Integration><Integrator>0</Integrator><DtFrac>0.9</DtFrac></Integration>
<Damping><BondDampingZ>1</BondDampingZ><ColDampingZ>0.8</ColDampingZ><SlowDampingZ>0.01</SlowDampingZ></Damping>
<Collisions><SelfColEnabled>1</SelfColEnabled><ColSystem>3</ColSystem><CollisionHorizon>2</CollisionHorizon></Collisions>
<Features><FluidDampEnabled>0</FluidDampEnabled><PoissonKickBackEnabled>0</PoissonKickBackEnabled><EnforceLatticeEnabled>0</EnforceLatticeEnabled></Features>
<SurfMesh><CMesh><DrawSmooth>1</DrawSmooth><Vertices/><Facets/><Lines/></CMesh></SurfMesh>
<StopCondition><StopConditionType>2</StopConditionType><StopConditionValue>{stop_time:g}</StopConditionValue><InitCmTime>{init_cm_time:g}</InitCmTime></StopCondition>
<GA><WriteFitnessFile>1</WriteFitnessFile><FitnessFileName>{sx.escape(fitness_file)}</FitnessFileName></GA>
</Simulator>
<Environment>
<Fixed_Regions>{fixed_xml}</Fixed_Regions>
<Forced_Regions><NumForced>0</NumForced></Forced_Regions>
<Gravity><GravEnabled>1</GravEnabled><GravAcc>{gravity:g}</GravAcc><FloorEnabled>1</FloorEnabled><FloorSlope>{floor_slope:g}</FloorSlope></Gravity>
<Thermal><TempEnabled>1</TempEnabled><TempAmp>{temp_amp:g}</TempAmp><TempBase>{temp_base:g}</TempBase><VaryTempEnabled>1</VaryTempEnabled><TempPeriod>{temp_period:g}</TempPeriod></Thermal>
</Environment>
<VXC Version="0.93">
<Lattice><Lattice_Dim>{lattice_dim:g}</Lattice_Dim><X_Dim_Adj>1</X_Dim_Adj><Y_Dim_Adj>1</Y_Dim_Adj><Z_Dim_Adj>1</Z_Dim_Adj><X_Line_Offset>0</X_Line_Offset><Y_Line_Offset>0</Y_Line_Offset><X_Layer_Offset>0</X_Layer_Offset><Y_Layer_Offset>0</Y_Layer_Offset></Lattice>
<Voxel><Vox_Name>BOX</Vox_Name><X_Squeeze>1</X_Squeeze><Y_Squeeze>1</Y_Squeeze><Z_Squeeze>1</Z_Squeeze></Voxel>
<Palette>{mats}</Palette>
<Structure Compression="ASCII_READABLE">
<X_Voxels>{nx}</X_Voxels><Y_Voxels>{ny}</Y_Voxels><Z_Voxels>{nz}</Z_Voxels>
<Data>{''.join(layers)}</Data>
<PhaseOffset>{''.join(phlayers)}</PhaseOffset>
</Structure>
</VXC>
</VXA>"""

def parse_vxa_structure(path):
    """Return (grid, phase) from an existing .vxa (e.g. published design)."""
    import re
    txt = open(path).read()
    nx = int(re.search(r"<X_Voxels>(\d+)</X_Voxels>", txt).group(1))
    ny = int(re.search(r"<Y_Voxels>(\d+)</Y_Voxels>", txt).group(1))
    nz = int(re.search(r"<Z_Voxels>(\d+)</Z_Voxels>", txt).group(1))
    data = re.search(r"<Data>(.*?)</Data>", txt, re.S).group(1)
    dlayers = re.findall(r"<!\[CDATA\[([0-9]+)\]\]>", data)
    grid = []
    for z in range(nz):
        flat = dlayers[z].strip()
        assert len(flat) == nx * ny, f"layer {z}: {len(flat)} != {nx*ny}"
        grid.append([[int(flat[y * nx + x]) for x in range(nx)] for y in range(ny)])
    ph = re.search(r"<PhaseOffset>(.*?)</PhaseOffset>", txt, re.S)
    phase = [[[0.0] * nx for _ in range(ny)] for _ in range(nz)]
    if ph:
        players = re.findall(r"<!\[CDATA\[(.*?)\]\]>", ph.group(1), re.S)
        for z in range(min(nz, len(players))):
            vals = [float(v) for v in players[z].replace("\n", " ").split(",") if v.strip()]
            for i, v in enumerate(vals[: nx * ny]):
                phase[z][i // nx][i % nx] = v
    return grid, phase

def aperture_wall(gap_center_y, gap_halfwidth, wall_x, wall_thickness,
                  span_y, span_z, lattice_dim=0.01):
    """Two fixed boxes forming a wall in the y-z plane at x=wall_x with a gap.
    All args in meters (world units)."""
    y0, y1 = 0.0, span_y
    g0, g1 = gap_center_y - gap_halfwidth, gap_center_y + gap_halfwidth
    boxes = []
    if g0 > y0:
        boxes.append((wall_x, y0, 0.0, wall_thickness, g0 - y0, span_z))
    if y1 > g1:
        boxes.append((wall_x, g1, 0.0, wall_thickness, y1 - g1, span_z))
    return boxes

def build_aperture_scene(design_grid, design_phase, wall_x_idx, gap_y, gap_hw_y, gap_z, gap_hw_z,
                         wall_material=2, **kw):
    """Embed design at x=0 of a wider grid; place a 1-voxel-thick wall at x=wall_x_idx
    (all y,z except the gap), fixed via a Fixed_Region. Gap coords are voxel indices
    (center, halfwidth in voxels). Returns (vxa_text, wall_plane_m)."""
    nz, ny, ndx = len(design_grid), len(design_grid[0]), len(design_grid[0][0])
    assert wall_x_idx > ndx, "wall must be beyond the design"
    grid = [[[0] * (wall_x_idx + 1) for _ in range(ny)] for _ in range(nz)]
    phase = [[[0.0] * (wall_x_idx + 1) for _ in range(ny)] for _ in range(nz)]
    for z in range(nz):
        for y in range(ny):
            for x in range(ndx):
                grid[z][y][x] = design_grid[z][y][x]
                phase[z][y][x] = design_phase[z][y][x]
    for z in range(nz):
        for y in range(ny):
            in_gap = (abs(y - gap_y) < gap_hw_y) and (abs(z - gap_z) < gap_hw_z)
            if not in_gap:
                grid[z][y][wall_x_idx] = wall_material
    ld = kw.get("lattice_dim", 0.01)
    wall_plane_m = wall_x_idx * ld
    boxes = [(wall_plane_m, 0.0, 0.0, ld, ny * ld, nz * ld)]
    kw["fixed_boxes"] = boxes
    return build_vxa(grid, phase, **kw), wall_plane_m
