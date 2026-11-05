// Check the home page truck intro's math: node tools/test_truck.js
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { framing, cameraAt, flapQuad, quadMatrix, viewProjection, spinMatrix, speed, traveled, pathAt, curveAt, rideAt, poseMatrix, bodyMatrix,
  partMatrix, wheelAngle, steerAngle, transform, readTruck, FLAP_X, FLAP_Y, FLAP_TOP, FLAP_H, BRAKE, STOP, FILL_END, REAR_Z, WHEELBASE } = require('../site/assets/js/truck-intro.js');

const close = (a, b, msg, within = 1e-6) => assert(Math.abs(a - b) < within, `${msg}: ${a} vs ${b}`);

// The flap lands exactly on the page's Q on any screen shape: the final transform does nothing
const IDENTITY = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
for (const [W, H] of [[375, 812], [768, 1024], [1280, 800], [2560, 1080]]) {
  const height = Math.min(H, W * 2000 / 1455), width = height * 1455 / 2000;
  const left = (W - width) / 2, top = (H - height) / 2;
  const rect = { left, top, width, height, right: left + width, bottom: top + height };
  const frame = framing(W, H, rect);
  const cam = cameraAt(STOP, frame);

  const quad = flapQuad(cam, frame, FLAP_X, rideAt(FILL_END).swing, bodyMatrix(FILL_END));
  close(quad[0][0], left, 'left'); close(quad[0][1], top, 'top');
  close(quad[2][0], left + width, 'right'); close(quad[2][1], top + height, 'bottom');

  const m = quadMatrix(width, height, quad.map(p => [p[0] - left, p[1] - top]));
  m.forEach((v, i) => close(v, IDENTITY[i], `matrix[${i}] at ${W}x${H}`));
}

// The matrix sends each corner of the box to its point on a skewed quad
const quad = [[10, 20], [130, 5], [160, 210], [-5, 170]];
const m = quadMatrix(100, 200, quad);
[[0, 0], [100, 0], [100, 200], [0, 200]].forEach(([x, y], i) => {
  const w = m[3] * x + m[7] * y + m[15];
  close((m[0] * x + m[4] * y + m[12]) / w, quad[i][0], `corner ${i} x`);
  close((m[1] * x + m[5] * y + m[13]) / w, quad[i][1], `corner ${i} y`);
});

// WebGL's projection puts the truck exactly where the flaps' math does, partway through the shot too
const apply = (m, p) => [0, 1, 2, 3].map(i => m[i] * p[0] + m[i + 4] * p[1] + m[i + 8] * p[2] + m[i + 12] * p[3]);
{
  const W = 1280, H = 800, rect = { left: 349, top: 0, width: 582, height: 800, right: 931, bottom: 800 };
  const frame = framing(W, H, rect);
  for (const t of [0, 1.7, 3, STOP]) {
    const cam = cameraAt(t, frame), [corner] = flapQuad(cam, frame, FLAP_X, 0, IDENTITY);
    const c = apply(viewProjection(cam, W, H), [FLAP_X - frame.flapW / 2, FLAP_TOP, 0, 1]);
    close((c[0] / c[3] + 1) / 2 * W, corner[0], 'projected x', 0.01);
    close((1 - c[1] / c[3]) / 2 * H, corner[1], 'projected y', 0.01);
    assert(Math.abs(c[2] / c[3]) < 1, 'between the depth planes');
  }
}

// Spinning keeps the axis in place and doesn't change sizes; a part with no axis doesn't move
{
  const o = [0, 2.5, 1.9], k = [0, 0.6, 0.8], m = spinMatrix(o, k, 1.1);
  apply(m, [o[0] + k[0], o[1] + k[1], o[2] + k[2], 1]).slice(0, 3).forEach((v, i) => close(v, o[i] + k[i], 'axis stays put', 1e-5));
  const moved = apply(m, [1, 2.5, 1.9, 1]);
  close(Math.hypot(moved[0] - o[0], moved[1] - o[1], moved[2] - o[2]), 1, 'radius kept', 1e-5);
  spinMatrix([0, 0, 0], [0, 0, 0], 0).forEach((v, i) => close(v, IDENTITY[i], 'fixed part'));
}

// The truck rolls steadily, brakes, and stays stopped
close(traveled(0), 0, 'start');
assert.strictEqual(speed(STOP), 0);
close(traveled(STOP + 5), traveled(STOP), 'stays stopped');
for (let t = 0.05; t <= STOP; t += 0.05) {
  assert(traveled(t) > traveled(t - 0.05), `moves at ${t}`);
  close((traveled(t) - traveled(t - 0.05)) / 0.05, (speed(t) + speed(t - 0.05)) / 2, `speed matches distance at ${t}`, 0.15);
}

// No sliding: the tandem only ever moves along the way the truck faces
for (let t = 0.1; t < STOP - 0.1; t += 0.1) {
  const a = pathAt(t), b = pathAt(t + 0.01), dx = b.x - a.x, dz = b.z - a.z, length = Math.hypot(dx, dz);
  close(Math.abs(dx * Math.cos(a.psi) - dz * Math.sin(a.psi)) / length, 0, `sideways slip at ${t}`, 0.01);
  assert(dx * Math.sin(a.psi) + dz * Math.cos(a.psi) < 0, 'moving backward');
}
// A mixer can really steer this path: under 35 degrees, and straight before it stops
assert(Math.abs(steerAngle(0, 0)) < 35 * Math.PI / 180, 'steering angle');
close(curveAt(pathAt(BRAKE + 0.5).u), 0, 'straight at the end');
close(pathAt(STOP).x, 0, 'ends on the camera line');
close(pathAt(STOP).z, REAR_Z, 'ends at its mark');

// The wheels roll exactly the ground they cover: follow each wheel's center through the world and compare
{
  const r = 0.54;
  for (const part of [{ kind: 2, rate: -r, o: [-1, 0.55, 1.4] }, { kind: 2, rate: -r, o: [1, 0.55, 1.4] }, { kind: 3, rate: -r, o: [-1, 0.55, 6.885] }, { kind: 3, rate: -r, o: [1, 0.55, 6.885] }]) {
    let ground = 0, last = transform(poseMatrix(0), part.o);
    for (let t = 0.01; t <= 3; t += 0.01) {
      const here = transform(poseMatrix(t), part.o);
      ground += Math.hypot(here[0] - last[0], here[2] - last[2]);
      last = here;
    }
    const rolled = (wheelAngle(part, 0) - wheelAngle(part, 3)) * r;
    close(rolled / ground, 1, `wheel at ${part.o}: rolled ${rolled} over ${ground}`, 0.015);   // a steered wheel's sum is a close approximation
    assert(rolled > 0, 'turning the reversing way');
  }
  // Each front wheel aims along the way it's actually moving, so nothing scrubs sideways
  for (const x of [-1, 1]) {
    for (let t = 0.1; t < 2.5; t += 0.2) {
      const a = transform(poseMatrix(t), [x, 0, 6.885]), b = transform(poseMatrix(t + 0.01), [x, 0, 6.885]);
      const dx = b[0] - a[0], dz = b[2] - a[2], aim = pathAt(t).psi + steerAngle(x, t);
      close(Math.abs(dx * Math.cos(aim) - dz * Math.sin(aim)) / Math.hypot(dx, dz), 0, `front wheel scrub at ${t}`, 0.01);
    }
  }
  // Each front wheel aims where it's going, the inner one more sharply
  assert(Math.abs(steerAngle(-1, 0)) > Math.abs(steerAngle(1, 0)), 'Ackermann');
}

// The lurch: braking squats the rear, the stop lets it swing back above level, then it settles to exactly nothing
{
  const flapY = t => transform(bodyMatrix(t), [FLAP_X, FLAP_TOP, 0])[1] - FLAP_TOP;
  const during = flapY(STOP - 0.05);
  let peak = -1, deepest = 0, sum = 0, count = 0;
  for (let t = STOP; t < STOP + 0.5; t += 0.01) peak = Math.max(peak, flapY(t));
  for (let t = BRAKE; t < STOP; t += 0.01) deepest = Math.min(deepest, flapY(t));
  for (let t = 0.5; t < BRAKE; t += 0.05) { sum += flapY(t); count++; }
  assert(during < -0.008 && during > -0.05, `rear squats by a realistic amount: ${during}`);
  assert(peak > 0.002 && peak < -deepest, `rebound ${peak} is smaller than the squat ${deepest}`);
  assert(Math.abs(sum / count) < 0.003, 'level while rolling');
  assert(rideAt(STOP - 0.05).swing < -0.02, 'the flap is thrown toward the camera under braking');
  poseMatrix(FILL_END).forEach((v, i) => close(v, IDENTITY[i], 'pose ends on identity'));
  bodyMatrix(FILL_END).forEach((v, i) => close(v, IDENTITY[i], 'body ends on identity', 1e-5));
  close(rideAt(FILL_END).swing, 0, 'flap at rest');
}

// The model file reads back whole: every face and line uses real vertices, and the drum and six wheels are there to spin
const file = fs.readFileSync(path.join(__dirname, '../site/assets/truck.bin'));
const parts = readTruck(file.buffer.slice(file.byteOffset, file.byteOffset + file.length));
assert.strictEqual(parts.filter(p => p.rate > 0).length, 1, 'one drum');
assert.strictEqual(parts.filter(p => p.rate < 0).length, 6, 'six wheels');
assert.strictEqual(parts.filter(p => p.kind === 3).length, 2, 'two steered wheels');
assert.strictEqual(parts.filter(p => p.kind === 4).length, 1, 'the axles');
partMatrix(parts[0], 1).forEach(v => assert(Number.isFinite(v)));
for (const part of parts) {
  for (const i of part.tris) assert(i * 3 < part.verts.length, 'face with a missing vertex');
  for (const i of part.lines) assert(i * 3 < part.verts.length, 'line to a missing vertex');
}

// Nothing is behind the flap we land on, so drawing all lines under it is the right depth order
const halfW = FLAP_H * 1455 / 2000 / 2;
for (const part of parts.filter(p => p.rate === 0)) {   // at rest, in final position
  for (let i = 0; i < part.lines.length; i += 2) {
    const a = part.lines[i] * 3, b = part.lines[i + 1] * 3;
    for (let k = 0; k <= 1; k += 0.05) {
      const at = n => (part.verts[a + n] + (part.verts[b + n] - part.verts[a + n]) * k) / 1000;
      assert(!(at(2) < 0 && Math.abs(at(0) - FLAP_X) < halfW && Math.abs(at(1) - FLAP_Y) < FLAP_H / 2), 'line behind the flap');
    }
  }
}
console.log('ok');
