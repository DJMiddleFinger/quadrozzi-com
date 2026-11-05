"""Turn a mixer truck FBX into the model the home page intro draws: site/assets/truck.bin

    python tools/build_truck.py path/to/Cement+truck.fbx

Keeps the faces (they hide what's behind them) and the edges that show the truck's shape. Drops bolts, the cab's
interior, whatever is inside the drum, and lines across smooth surfaces. Needs numpy. Reads binary FBX as data only;
the source model isn't kept in the repo.

Output, little-endian. In truck coordinates, x is to the right seen from behind, y up, z from the flaps toward the cab:
    Float32 part count, then for each part: verts, faces, lines, spin origin xyz, spin axis xyz, rate, kind
        rate: 0 fixed, above 0 turns at that many radians per second, below 0 a wheel of radius -rate
        kind: 0 body on the springs, 1 drum, 2 rear wheel, 3 front (steered) wheel, 4 axles (not on the springs)
    then for each part: Int16 xyz of each vertex in millimetres, Uint16 quads (a triangle repeats its last vertex),
    Uint16 pairs of vertex numbers for the lines
"""
import struct
import sys
import zlib
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / 'site' / 'assets' / 'truck.bin'

FLAP_Z = -3.90          # in the model's coordinates: just behind its tail lights and its own flaps
FLAP_INNER = 0.665      # inner edge of the Q flaps, from the truck's center line
MIN_SHELL = 0.15        # shells smaller across than this (metres) are bolts and the like
MIN_EDGE = 0.008
LONG_EDGE = 0.5
SMOOTH_DEG = {'body': 20, 'drum': 0, 'wheel': 7}    # an edge between faces bending less than this isn't drawn
STRAIGHT_DEG = 10       # consecutive edges bending less than this become one line
CAB_INSIDE = ((-0.95, 0.95), (1.2, 2.5), (1.3, 2.9))    # seats, dash and steering wheel
AXLES = [(-3.115, 0.61), (-1.885, 0.61), (2.985, 0.93)] # z of each axle and where its wheels start, out from the center
AXLE_Y, WHEEL_R = 0.55, 0.54
DRUM_RATE = 1.3
AXLE_REACH = 0.4         # shells this close to an axle's line move with the axle, not the body
AXLE_PART = 8


# ---------- Binary FBX ----------

def read_prop(b, o):
    t = chr(b[o]); o += 1
    if t in 'YCILFD':
        fmt = {'Y': '<h', 'C': '<B', 'I': '<i', 'L': '<q', 'F': '<f', 'D': '<d'}[t]
        return struct.unpack_from(fmt, b, o)[0], o + struct.calcsize(fmt)
    if t in 'SR':
        n = struct.unpack_from('<I', b, o)[0]
        return b[o + 4:o + 4 + n], o + 4 + n
    n, enc, size = struct.unpack_from('<III', b, o); o += 12
    raw = b[o:o + size]
    if enc == 1:
        raw = zlib.decompress(raw)
    return list(struct.unpack('<%d%s' % (n, {'f': 'f', 'd': 'd', 'l': 'q', 'i': 'i', 'b': 'B'}[t]), raw)), o + size


def read_node(b, o, wide):
    fmt, skip = ('<QQQ', 24) if wide else ('<III', 12)
    end, count, _ = struct.unpack_from(fmt, b, o); o += skip
    name_len = b[o]; o += 1
    if end == 0:
        return None, o
    node = {'name': b[o:o + name_len].decode('latin1'), 'props': [], 'kids': []}; o += name_len
    for _ in range(count):
        value, o = read_prop(b, o)
        node['props'].append(value)
    while o < end:
        child, o = read_node(b, o, wide)
        if child is None:
            break
        node['kids'].append(child)
    return node, end


def read_mesh(path):
    """The file's one mesh: vertices and polygons. Old FBX stores arrays as one property per number."""
    b = Path(path).read_bytes()
    assert b[:18] == b'Kaydara FBX Binary', 'not a binary FBX'
    wide = struct.unpack_from('<I', b, 23)[0] >= 7500
    o = 27
    while True:
        node, o = read_node(b, o, wide)
        if node['name'] == 'Objects':
            break
    meshes = [m for m in node['kids'] if any(k['name'] == 'Vertices' for k in m['kids'])]
    assert len(meshes) == 1, 'expected one mesh'

    def values(name):
        props = next(k for k in meshes[0]['kids'] if k['name'] == name)['props']
        return props[0] if isinstance(props[0], list) else props

    faces, face = [], []
    for i in values('PolygonVertexIndex'):
        face.append(~i if i < 0 else i)
        if i < 0:
            faces.append(face)
            face = []
    return np.array(values('Vertices'), dtype=float).reshape(-1, 3), faces


# ---------- Which part each shell belongs to ----------

def shells(n, faces):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for f in faces:
        for a in f[1:]:
            parent[find(a)] = find(f[0])
    return np.array([find(i) for i in range(n)])


def drum_axis(P):
    """The drum is a surface of revolution on the truck's center line: search for the line through it that makes
    the radius most constant at each station along it."""
    def spread(y0, slope):
        o = np.array([0, y0, -2.0])
        k = np.array([0, slope, 1.0])
        k /= np.linalg.norm(k)
        along = (P - o) @ k
        r = np.linalg.norm(P - o - np.outer(along, k), axis=1)
        bins = np.floor((along - along.min()) / 0.2).astype(int)
        mean = np.bincount(bins, r) / np.maximum(np.bincount(bins), 1)
        return ((r - mean[bins]) ** 2).sum()

    y0, slope, step = 2.5, -0.25, 0.05
    while step > 0.0005:
        y0, slope = min(((y0 + a * step, slope + b * step) for a in range(-5, 6) for b in range(-5, 6)), key=lambda c: spread(*c))
        step /= 3
    k = np.array([0, slope, 1.0])
    return np.array([0, y0, -2.0]), k / np.linalg.norm(k)


def classify(V, comp):
    """Part number for each kept shell: 0 body, 1 drum, 2 on wheels. Shells left out are dropped."""
    ids = np.unique(comp)
    skins = [i for i in ids if V[comp == i][:, 1].min() > 1.1 and V[comp == i][:, 2].max() < 0.15
             and np.ptp(V[comp == i][:, 2]) > 3 and np.ptp(V[comp == i][:, 0]) > 2]
    o, k = drum_axis(V[np.isin(comp, skins)])

    def station(P):
        along = (P - o) @ k
        return np.floor((along + 5) / 0.1).astype(int), np.linalg.norm(P - o - np.outer(along, k), axis=1)

    wheel_part, part = {}, {}
    for i in ids:
        P = V[comp == i]
        lo, hi = P.min(0), P.max(0)
        wheel = None
        for a, (z, inner) in enumerate(AXLES):
            if np.hypot(P[:, 1] - AXLE_Y, P[:, 2] - z).max() <= WHEEL_R + 0.02:
                for side in (-1, 1):
                    if (side * P[:, 0]).min() >= inner - 0.09:
                        wheel = wheel_part.setdefault((a, side), 2 + len(wheel_part))
        if wheel is not None:   # small parts stay here: lug nuts are what show a wheel turning
            part[i] = wheel
            continue
        if np.linalg.norm(hi - lo) < MIN_SHELL:
            continue
        if all(CAB_INSIDE[a][0] <= lo[a] and hi[a] <= CAB_INSIDE[a][1] for a in range(3)):
            continue
        if hi[1] - lo[1] < 0.62 and lo[1] > 0.1 and lo[2] > -3.9 and hi[2] < -3.8 and hi[1] < 0.75:
            continue    # the model's own mud flaps: the Q goes here
        part[i] = 0
        if any(np.hypot(P[:, 1] - AXLE_Y, P[:, 2] - z).max() <= AXLE_REACH for z, _ in AXLES):
            part[i] = AXLE_PART
        radial = station(P)[1]
        if part[i] == 0 and -3.85 <= lo[2] and hi[2] <= 0.15 and 0.8 < radial.max() <= 1.25 and lo[1] > 1.05:
            part[i] = 1

    # Anything strictly inside the drum's outer skin can never be seen
    outer = np.zeros(200)
    drum = [i for i in part if part[i] == 1]
    for i in drum:
        bins, r = station(V[comp == i])
        np.maximum.at(outer, bins, r)
    for i in drum:
        bins, r = station(V[comp == i])
        if (r < outer[bins] - 0.02).all():
            del part[i]
    return part, wheel_part, o, k


def wheel_details(T, used, center):
    """The model's wheels are perfectly round all the way around, so spinning shows nothing. Add what a real steel truck
    wheel has on its outer face: 10 lug nuts, 5 hand holes, and two blocks of tyre lettering. Returns extra points and lines."""
    P = T[used]
    side = np.sign(center[0])
    rho = np.hypot(P[:, 1] - center[1], P[:, 2] - center[2])
    points, lines = [], []

    def face_x(r):
        ring = np.abs(rho - rho[np.argmin(np.abs(rho - r))]) < 0.01    # the model's nearest ring of points
        return side * (side * P[ring, 0]).max() + side * 0.006

    def loop(outline, closed=True):
        """outline: (radius from the axle, angle round it) pairs"""
        start = len(points)
        for r, a in outline:
            points.append((face_x(r), center[1] + r * np.cos(a), center[2] + r * np.sin(a)))
        for i in range(len(outline) - (0 if closed else 1)):
            lines.append((start + i, start + (i + 1) % len(outline)))

    for n in range(10):     # lug nuts: hexagons on the usual 285mm bolt circle
        a0 = n * 2 * np.pi / 10
        loop([(0.1425 + 0.024 * np.cos(b), a0 + 0.024 * np.sin(b) / 0.1425) for b in np.arange(6) * np.pi / 3])
    for n in range(5):      # hand holes: ovals in the dish
        a0 = n * 2 * np.pi / 5
        loop([(0.235 + 0.03 * np.cos(b), a0 + 0.26 * np.sin(b)) for b in np.arange(10) * np.pi / 5])
    for a0 in (0.4, 0.4 + np.pi):   # tyre lettering: arcs of raised blocks on the sidewall
        arc = np.linspace(a0, a0 + 0.75, 7)
        loop([(0.46, a) for a in arc] + [(0.41, a) for a in arc[::-1]])
    return np.array(points), lines


# ---------- Which edges to keep ----------

def feature_edges(V, faces, smooth_deg):
    """Vertex-number pairs for edges at boundaries and creases."""
    normals = {}
    for f in faces:
        P = V[f]
        n = np.cross(P - P.mean(0), np.roll(P, -1, axis=0) - P.mean(0)).sum(0)
        length = np.linalg.norm(n)
        if length == 0:
            continue
        n = n / length
        for a, b in zip(f, f[1:] + f[:1]):
            if a != b:
                normals.setdefault((min(a, b), max(a, b)), []).append(n)
    limit = np.cos(np.radians(smooth_deg))
    # Long edges stay even on smooth surfaces, or handrails and ladder sides would vanish between their bends
    return [e for e, ns in normals.items()
            if len(ns) != 2 or abs(ns[0] @ ns[1]) <= limit or np.linalg.norm(V[e[0]] - V[e[1]]) > LONG_EDGE]


def simplify(V, edges):
    """Merge runs of nearly straight edges into one line and drop tiny ones."""
    links = {}
    for a, b in edges:
        links.setdefault(a, set()).add(b)
        links.setdefault(b, set()).add(a)
    limit = np.cos(np.radians(STRAIGHT_DEG))
    for m in list(links):
        if len(links[m]) != 2:
            continue
        a, b = links[m]
        u, w = V[m] - V[a], V[b] - V[m]
        if u @ w > limit * np.linalg.norm(u) * np.linalg.norm(w) and b not in links[a]:
            links[a].discard(m); links[b].discard(m)
            links[a].add(b); links[b].add(a)
            del links[m]
    return [(a, b) for a in links for b in links[a] if a < b and np.linalg.norm(V[a] - V[b]) >= MIN_EDGE]


def main(path):
    V, faces = read_mesh(path)
    comp = shells(len(V), faces)
    part, wheel_part, drum_o, drum_k = classify(V, comp)

    # The bumper bar reaches in front of the flaps: stop it short of them
    for i in np.unique(comp):
        P = V[comp == i]
        if len(P) == 8 and P[:, 2].min() < -4.2 and P[:, 1].max() < 0.75:
            V[comp == i, 0] = np.clip(P[:, 0], -FLAP_INNER + 0.02, FLAP_INNER - 0.02)

    # To truck coordinates. Seen from behind, the model's +x is on the right-hand side of a right-handed frame: the
    # intro's camera treats +x as right, so negate x. (Not a mirror image: the camera's frame is left-handed.)
    def to_truck(p):
        return np.array([-p[0], p[1], p[2] - FLAP_Z])

    T = np.column_stack([-V[:, 0], V[:, 1], V[:, 2] - FLAP_Z])

    # Weld coincident vertices (2mm)
    weld = {}
    canon = np.empty(len(T), dtype=int)
    for i, key in enumerate(map(tuple, np.round(T * 500).astype(int))):
        canon[i] = weld.setdefault(key, i)

    groups = {}
    for f in faces:
        q = part.get(comp[f[0]])
        if q is not None:
            groups.setdefault(q, []).append([int(canon[i]) for i in f])

    specs = {0: (np.zeros(3), np.zeros(3), 0.0, 0), 1: (to_truck(drum_o), np.array([-drum_k[0], drum_k[1], drum_k[2]]), DRUM_RATE, 1),
             AXLE_PART: (np.zeros(3), np.zeros(3), 0.0, 4)}
    for (axle, side), q in wheel_part.items():
        x = np.mean([T[i, 0] for f in groups[q] for i in f])    # the wheel's own center, for its steering and rolling
        specs[q] = (np.array([x, AXLE_Y, AXLES[axle][0] - FLAP_Z]), np.array([1.0, 0, 0]), -WHEEL_R, 3 if axle == 2 else 2)

    head, body, total = [], b'', 0
    for q in sorted(groups):
        edges = simplify(T, feature_edges(T, groups[q], SMOOTH_DEG['drum' if q == 1 else 'wheel' if 2 <= q < AXLE_PART else 'body']))
        used = sorted({i for f in groups[q] for i in f})
        number = {v: n for n, v in enumerate(used)}
        extra_points, extra_lines = wheel_details(T, used, specs[q][0]) if 2 <= q < AXLE_PART else (np.empty((0, 3)), [])
        verts = np.round(np.vstack([T[used], extra_points]) * 1000).astype('<i2')
        quads = np.array([[number[i] for i in (f if len(f) == 4 else f + f[-1:])] for f in groups[q]], dtype='<u2')
        pairs = np.array([(number[a], number[b]) for a, b in edges] + [(a + len(used), b + len(used)) for a, b in extra_lines], dtype='<u2')
        o, k, rate, kind = specs[q]
        head += [len(verts), len(quads), len(pairs), *o, *k, rate, kind]
        body += verts.tobytes() + quads.tobytes() + pairs.tobytes()
        total += len(pairs)
        print('part', q, 'verts', len(verts), 'faces', len(quads), 'lines', len(pairs), 'kind', kind)
    OUT.write_bytes(np.array([len(groups), *head], dtype='<f4').tobytes() + body)
    print('wrote', OUT.name, OUT.stat().st_size, 'bytes,', total, 'lines; drum axis', drum_o.round(3), drum_k.round(3))


if __name__ == '__main__':
    main(sys.argv[1])
