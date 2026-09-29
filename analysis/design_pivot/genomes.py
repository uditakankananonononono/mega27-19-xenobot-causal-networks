"""Genome generation and validity for the design pivot (prereg sec. 3)."""
import random

NX, NY, NZ = 8, 8, 7
MIN_FILL = 0.5

def random_genome(rng):
    mat = [[[rng.randint(0, 4) for _ in range(NX)] for _ in range(NY)] for _ in range(NZ)]
    ph = [[[rng.uniform(-1, 1) for _ in range(NX)] for _ in range(NY)] for _ in range(NZ)]
    return mat, ph

def is_valid(mat):
    filled = sum(1 for z in range(NZ) for y in range(NY) for x in range(NX) if mat[z][y][x])
    if filled < MIN_FILL * NX * NY * NZ:
        return False
    if not any(mat[z][y][x] in (3, 4) for z in range(NZ) for y in range(NY) for x in range(NX)):
        return False
    # 6-connected single component
    cells = {(x, y, z) for z in range(NZ) for y in range(NY) for x in range(NX) if mat[z][y][x]}
    seen = {next(iter(cells))}
    stack = list(seen)
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            n = (x+dx, y+dy, z+dz)
            if n in cells and n not in seen:
                seen.add(n); stack.append(n)
    return seen == cells

def valid_random_genome(rng, max_tries=200):
    for _ in range(max_tries):
        mat, ph = random_genome(rng)
        if is_valid(mat):
            return mat, ph
    raise RuntimeError("no valid genome in %d tries" % max_tries)
