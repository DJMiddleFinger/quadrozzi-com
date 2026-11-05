// Home page intro: a white-on-grey wireframe mixer truck backs up until its Q mudflap is the page's Q.
// The truck is drawn with WebGL, so the graphics card does the work and hidden edges are truly hidden: the model's
// faces go into the depth buffer unseen, then only the lines in front of them are drawn. The flaps are the page's real
// <figure> (and a clone) under a CSS matrix3d, so the Q stays sharp and lands exactly where it sits normally.
// Check the math with: node tools/test_truck.js
//
// The model is built by tools/build_truck.py (site/assets/truck.bin).
// Metres: x to the camera's right, y up, z from the flaps toward the cab. World coordinates are the truck's own at the
// moment it has stopped and settled, so everything lands on the identity transform and the page's Q is untouched.
//
// The camera stands still and the truck really reverses to it. It follows the no-slip path of a truck steered by its
// front wheels with the tandem rolling straight behind, its wheels roll exactly the distance they cover, and its body rides
// on simulated springs, so braking squats the rear and the stop itself lets the body rock back.
// All lines are under the flaps. Nothing sits behind the flap we land on (test_truck.js checks this).
// It reverses across a concrete yard, a texture generated here so there's no image to load.
(function () {
  var FLAP_H = 0.84;              // the flap's width comes from the image's shape
  var FLAP_X = -0.97;             // the flap we land on, behind the driver's-side duals; its twin is at -FLAP_X
  var FLAP_TOP = 0.96;
  var FLAP_Y = FLAP_TOP - FLAP_H / 2;

  // Timeline, in seconds. The shot opens with the truck already rolling.
  var BRAKE = 3.4, STOP = 4.5, GLIDE_END = 4, SETTLE = 5.2, FILL_START = 5.05, FILL_END = 5.7;

  // Reversing: walking pace, firm braking at a constant pedal, on a path a mixer can steer
  var REVERSE_SPEED = 2.6;              // metres per second
  var WHEELBASE = 5.485;                // front axle to the middle of the tandem
  var REAR_Z = 1.4;                     // the middle of the tandem: the point that rolls straight back along its own heading
  var MAX_CURVE = Math.tan(30 * Math.PI / 180) / WHEELBASE;
  var STRAIGHT_LAST = 1.6, UNWIND = 2.4;    // metres: straight at the end, and over how far the steering winds off

  // Springs: a half-car model of a loaded mixer, 7t on the front axle and 18t on the tandem.
  var FRONT_KG = 7000, REAR_KG = 18000;
  var RIDE_HZ = 1.8, RIDE_DAMPING = 0.18;   // leaf springs bounce slowly and are lightly damped
  var COG_Y = 2, GYRATION = 2.2;            // loaded drums carry their weight high
  var COG_Z = REAR_Z + WHEELBASE * FRONT_KG / (FRONT_KG + REAR_KG);
  var AIR_SWING = 0.035;                    // radians the moving air holds the rubber back at reversing speed
  var FLAP_HZ = 1.4, FLAP_DAMPING = 0.25;   // stiff rubber on a bracket, not a free pendulum
  var BRAKE_BITE = 0.3;                     // seconds for air brakes to build up

  var DEPTH_NEAR = 0.2, DEPTH_FAR = 60;

  // The yard: concrete at y = 0, where the tires touch, dissolving into the page's grey with distance
  var GROUND_TILE = 4, GROUND_SIZE = 512;   // one slab in metres, and in pixels (a power of two, so it can repeat)
  var GROUND_FADE = [12, 40];               // metres from the camera: fully there, fully gone

  // Slower machines, in average milliseconds per frame: above SLOW_MS draw at a lower resolution, above GIVE_UP_MS end the shot
  var SLOW_MS = 30, GIVE_UP_MS = 90;

  function lerp(a, b, k) { return a + (b - a) * k; }
  function smooth(k) { k = Math.min(1, Math.max(0, k)); return k * k * (3 - 2 * k); }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function norm(a) { var l = Math.sqrt(dot(a, a)); return [a[0] / l, a[1] / l, a[2] / l]; }

  // ---------- Motion ----------

  function speed(t) {
    return t < BRAKE ? REVERSE_SPEED : t < STOP ? REVERSE_SPEED * (STOP - t) / (STOP - BRAKE) : 0;
  }

  // How far the truck has reversed by time t (the integral of speed)
  function traveled(t) {
    if (t < BRAKE) return REVERSE_SPEED * t;
    var left = Math.max(0, STOP - t);
    return REVERSE_SPEED * BRAKE + REVERSE_SPEED * (STOP - BRAKE) / 2 - REVERSE_SPEED * left * left / (2 * (STOP - BRAKE));
  }
  var PATH_LENGTH = traveled(STOP);

  // How tightly the truck is turning with u metres still to go. Negative: the cab swings toward -x, the driver's side.
  function curveAt(u) {
    return -MAX_CURVE * smooth((u - STRAIGHT_LAST) / UNWIND);
  }

  // The path, worked back from the stopping point in steps of PATH_STEP: where the tandem's middle is, which way the truck
  // faces, and how far the front wheels roll. The tandem only moves along its heading, so there's no sideways slip.
  var PATH_STEP = 0.02;
  var PATH = (function () {
    var n = Math.ceil(PATH_LENGTH / PATH_STEP) + 2, table = new Float64Array(n * 4), x = 0, z = REAR_Z, psi = 0, front = 0;
    for (var i = 0; i < n; i++) {
      table.set([x, z, psi, front], i * 4);
      var u = i * PATH_STEP, mid = psi + curveAt(u) * PATH_STEP / 2, k = curveAt(u + PATH_STEP / 2);
      x += Math.sin(mid) * PATH_STEP;
      z += Math.cos(mid) * PATH_STEP;
      psi += k * PATH_STEP;
      front += Math.sqrt(1 + WHEELBASE * WHEELBASE * k * k) * PATH_STEP;   // 1 / cos(steering angle)
    }
    return table;
  })();

  function lookup(table, columns, at) {
    var i = Math.min(Math.floor(at), table.length / columns - 2), k = Math.max(0, at - i), out = [];
    for (var c = 0; c < columns; c++) out.push(lerp(table[i * columns + c], table[(i + 1) * columns + c], k));
    return out;
  }

  // The truck's place at time t: [x, z, heading, front wheels' rolling distance], and the distance still to go
  function pathAt(t) {
    var u = Math.max(0, PATH_LENGTH - traveled(t));
    var at = lookup(PATH, 4, u / PATH_STEP);
    return { x: at[0], z: at[1], psi: at[2], front: at[3], u: u };
  }

  // A little unevenness in the yard, as the suspension feels it, in metres
  function road(s) {
    return 0.003 * Math.sin(2 * Math.PI * s / 2.7) + 0.002 * Math.sin(2 * Math.PI * s / 1.1 + 1);
  }

  // The body and flap in time, simulated once. Braking pushes the wheels' grip forward below the body's high center of
  // gravity, which squats the rear. Holding the pedal to a stop ends that push all at once, so the body swings back
  // through level and rocks to rest. The same braking throws the flap toward the camera.
  var RIDE_STEP = 1 / 250;
  var RIDE = (function () {
    var w = 2 * Math.PI * RIDE_HZ, kf = FRONT_KG * w * w, kr = REAR_KG * w * w, cf = 2 * RIDE_DAMPING * FRONT_KG * w, cr = 2 * RIDE_DAMPING * REAR_KG * w;
    var mass = FRONT_KG + REAR_KG, inertia = mass * GYRATION * GYRATION;
    var toFront = WHEELBASE * REAR_KG / mass, toRear = WHEELBASE * FRONT_KG / mass;
    var root = 2 * Math.PI * FLAP_HZ, flapW = root * root, flapPush = 3 / (2 * FLAP_H);
    var y = 0, vy = 0, pitch = 0, vPitch = 0, swing = AIR_SWING, vSwing = 0;
    var n = Math.ceil(FILL_END / RIDE_STEP) + 2, table = new Float32Array(n * 3);
    for (var i = -750; i < n; i++) {    // the first three seconds only let it settle into rolling
      var t = i * RIDE_STEP, s = traveled(t), brake = t >= BRAKE && t < STOP ? smooth((t - BRAKE) / BRAKE_BITE) * REVERSE_SPEED / (STOP - BRAKE) : 0;
      var front = -kf * (y - pitch * toFront - road(s - WHEELBASE)) - cf * (vy - vPitch * toFront);
      var rear = -kr * (y + pitch * toRear - road(s)) - cr * (vy + vPitch * toRear);
      vy += (front + rear) / mass * RIDE_STEP;
      vPitch += (-toFront * front + toRear * rear - mass * brake * COG_Y) / inertia * RIDE_STEP;
      y += vy * RIDE_STEP;
      pitch += vPitch * RIDE_STEP;
      var v = speed(t) / REVERSE_SPEED;
      vSwing += (flapW * (AIR_SWING * v * v - swing) - 2 * FLAP_DAMPING * root * vSwing - flapPush * brake) * RIDE_STEP;
      swing += vSwing * RIDE_STEP;
      if (i >= 0) table.set([pitch, y, swing], i * 3);
    }
    return table;
  })();

  // Body pitch (radians, positive cab down), body rise (metres) and flap swing (radians, positive toward the cab) at time t.
  // All three ease to exactly nothing by the end of the shot.
  function rideAt(t) {
    var at = lookup(RIDE, 3, Math.max(0, t) / RIDE_STEP), fade = 1 - smooth((t - SETTLE) / (FILL_END - SETTLE));
    return { pitch: at[0] * fade, rise: at[1] * fade, swing: at[2] * fade };
  }

  // ---------- Camera ----------

  // Focal length and standing distance for a screen and the rectangle the flap must land on
  function framing(screenW, screenH, rect) {
    var f = 1.2 * Math.min(screenW, screenH);
    return {
      f: f,
      ox: rect.left + rect.width / 2,
      oy: rect.top + rect.height / 2,
      flapW: FLAP_H * rect.width / rect.height,
      end: f * FLAP_H / rect.height   // at this distance the flap is exactly rect's size
    };
  }

  // Stands where the flap will end up in front of it. Follows the truck in as it comes, stooping to the flap's height.
  function cameraAt(t, frame) {
    var g = smooth(t / GLIDE_END), mid = transform(poseMatrix(t), [0, 1.6, 3.5]);
    var pos = [FLAP_X, lerp(1.25, FLAP_Y, g), -frame.end];
    var look = [lerp(mid[0], FLAP_X, g), lerp(mid[1], FLAP_Y, g), lerp(mid[2], 0, g)];
    var forward = norm([look[0] - pos[0], look[1] - pos[1], look[2] - pos[2]]);
    var right = norm(cross([0, 1, 0], forward));
    return { pos: pos, right: right, up: cross(forward, right), forward: forward, f: frame.f, ox: frame.ox, oy: frame.oy };
  }

  // A point in truck coordinates to camera coordinates; z is the distance in front of the camera
  function toView(cam, p) {
    var v = [p[0] - cam.pos[0], p[1] - cam.pos[1], p[2] - cam.pos[2]];
    return [dot(v, cam.right), dot(v, cam.up), dot(v, cam.forward)];
  }

  function toScreen(cam, v) {
    return [cam.ox + cam.f * v[0] / v[2], cam.oy - cam.f * v[1] / v[2]];
  }

  // ---------- The flaps ----------

  // The flap's corners on screen, clockwise from top left. It hangs from its top edge on the body and swings about it.
  function flapQuad(cam, frame, x, swing, body) {
    var half = frame.flapW / 2, low = FLAP_TOP - FLAP_H * Math.cos(swing), back = FLAP_H * Math.sin(swing);
    return [[x - half, FLAP_TOP, 0], [x + half, FLAP_TOP, 0], [x + half, low, back], [x - half, low, back]].map(function (p) {
      return toScreen(cam, toView(cam, transform(body, p)));
    });
  }

  // The CSS matrix3d values taking a w by h box with its corner at the origin onto quad (a square-to-quad homography)
  function quadMatrix(w, h, quad) {
    var x0 = quad[0][0], y0 = quad[0][1], x1 = quad[1][0], y1 = quad[1][1];
    var x2 = quad[2][0], y2 = quad[2][1], x3 = quad[3][0], y3 = quad[3][1];
    var dx1 = x1 - x2, dx2 = x3 - x2, sx = x0 - x1 + x2 - x3;
    var dy1 = y1 - y2, dy2 = y3 - y2, sy = y0 - y1 + y2 - y3;
    var den = dx1 * dy2 - dx2 * dy1;
    var g = (sx * dy2 - dx2 * sy) / den, k = (dx1 * sy - sx * dy1) / den;
    return [
      (x1 - x0 + g * x1) / w, (y1 - y0 + g * y1) / w, 0, g / w,
      (x3 - x0 + k * x3) / h, (y3 - y0 + k * y3) / h, 0, k / h,
      0, 0, 1, 0,
      x0, y0, 0, 1
    ];
  }

  // ---------- The truck ----------

  // The parts in truck.bin; the file's layout is described in tools/build_truck.py
  function readTruck(buffer) {
    var count = new Float32Array(buffer, 0, 1)[0], head = new Float32Array(buffer, 4, count * 11), offset = 4 + count * 44, parts = [];
    for (var n = 0; n < count; n++) {
      var h = head.subarray(n * 11, n * 11 + 11);
      var verts = new Int16Array(buffer, offset, h[0] * 3);
      offset += h[0] * 6;
      var quads = new Uint16Array(buffer, offset, h[1] * 4), tris = new Uint16Array(h[1] * 6);
      offset += h[1] * 8;
      for (var i = 0; i < h[1]; i++) {
        var a = quads[i * 4], b = quads[i * 4 + 1], c = quads[i * 4 + 2], d = quads[i * 4 + 3];
        tris.set([a, b, c, a, c, d], i * 6);
      }
      var lines = new Uint16Array(buffer, offset, h[2] * 2);
      offset += h[2] * 4;
      parts.push({ verts: verts, tris: tris, lines: lines, o: [h[3], h[4], h[5]], k: [h[6], h[7], h[8]], rate: h[9], kind: h[10] });
    }
    return parts;
  }

  // ---------- The ground ----------

  // One slab of concrete as premultiplied RGBA over the page's grey (white lightens it, black darkens it): soft blotches and
  // aggregate specks that wrap around the edges, and a saw-cut joint along two sides. Seeded, so it looks the same every visit.
  function groundTexture(size) {
    var seed = 12345, GRID = 32, blotches = [], data = new Uint8Array(size * size * 4);
    function rand() { seed = seed * 16807 % 2147483647; return seed / 2147483647; }
    for (var i = 0; i < GRID * GRID; i++) blotches.push(rand() - 0.5);
    function blotch(x, y, cells) {    // soft noise, cells wide per tile (a factor of GRID), wrapping around the edges
      var gx = x / size * cells, gy = y / size * cells, ix = Math.floor(gx), iy = Math.floor(gy), kx = smooth(gx - ix), ky = smooth(gy - iy);
      function cell(a, b) { return blotches[(b % cells) * GRID + a % cells]; }
      return lerp(lerp(cell(ix, iy), cell(ix + 1, iy), kx), lerp(cell(ix, iy + 1), cell(ix + 1, iy + 1), kx), ky);
    }
    for (var y = 0; y < size; y++) {
      for (var x = 0; x < size; x++) {
        var shade = blotch(x, y, 6) * 0.08 + blotch(x, y, GRID) * 0.1 + (rand() - 0.5) * 0.22;
        if (rand() < 0.03) shade += (rand() - 0.5) * 0.7;
        if (x < 2 || y < 2) shade = -0.32;
        var a = Math.min(1, Math.abs(shade)) * 255, v = shade > 0 ? a : 0, at = (y * size + x) * 4;
        data[at] = data[at + 1] = data[at + 2] = v;
        data[at + 3] = a;
      }
    }
    return data;
  }

  // ---------- Matrices (column by column, as WebGL wants them) ----------

  // Truck coordinates to clip space, matching toScreen exactly so the lines stay registered with the flaps
  function viewProjection(cam, W, H) {
    var a = 2 * cam.f / W, b = 2 * cam.ox / W - 1, c = 2 * cam.f / H, d = 1 - 2 * cam.oy / H;
    var A = (DEPTH_FAR + DEPTH_NEAR) / (DEPTH_FAR - DEPTH_NEAR), B = -2 * DEPTH_FAR * DEPTH_NEAR / (DEPTH_FAR - DEPTH_NEAR);
    var r = cam.right, u = cam.up, f = cam.forward, p = cam.pos, m = new Float32Array(16);
    for (var col = 0; col < 4; col++) {
      var rc = col < 3 ? r[col] : -dot(r, p), uc = col < 3 ? u[col] : -dot(u, p), fc = col < 3 ? f[col] : -dot(f, p);
      m[col * 4] = a * rc + b * fc;
      m[col * 4 + 1] = c * uc + d * fc;
      m[col * 4 + 2] = A * fc + (col === 3 ? B : 0);
      m[col * 4 + 3] = fc;
    }
    return m;
  }

  // Rodrigues' rotation by angle about the line through o along unit vector k
  function spinMatrix(o, k, angle) {
    var cs = Math.cos(angle), sn = Math.sin(angle), t = 1 - cs, x = k[0], y = k[1], z = k[2];
    var R = [
      cs + t * x * x, t * x * y + sn * z, t * x * z - sn * y,
      t * x * y - sn * z, cs + t * y * y, t * y * z + sn * x,
      t * x * z + sn * y, t * y * z - sn * x, cs + t * z * z
    ];
    return new Float32Array([
      R[0], R[1], R[2], 0,
      R[3], R[4], R[5], 0,
      R[6], R[7], R[8], 0,
      o[0] - R[0] * o[0] - R[3] * o[1] - R[6] * o[2], o[1] - R[1] * o[0] - R[4] * o[1] - R[7] * o[2], o[2] - R[2] * o[0] - R[5] * o[1] - R[8] * o[2], 1
    ]);
  }

  function multiply(a, b) {
    var m = new Float32Array(16);
    for (var c = 0; c < 4; c++) {
      for (var r = 0; r < 4; r++) m[c * 4 + r] = a[r] * b[c * 4] + a[r + 4] * b[c * 4 + 1] + a[r + 8] * b[c * 4 + 2] + a[r + 12] * b[c * 4 + 3];
    }
    return m;
  }

  function transform(m, p) {
    return [0, 1, 2].map(function (i) { return m[i] * p[0] + m[i + 4] * p[1] + m[i + 8] * p[2] + m[i + 12]; });
  }

  // Where the truck stands: turned to its heading about the tandem's middle, which is moved to its place on the path
  function poseMatrix(t) {
    var at = pathAt(t), m = spinMatrix([0, 0, REAR_Z], [0, 1, 0], at.psi);
    m[12] += at.x;
    m[14] += at.z - REAR_Z;
    return m;
  }

  // The body: on the truck's pose, leaning and rising on its springs
  function bodyMatrix(t) {
    var ride = rideAt(t), m = spinMatrix([0, COG_Y, COG_Z], [1, 0, 0], ride.pitch);
    m[13] += ride.rise;
    return multiply(poseMatrix(t), m);
  }

  // How far a wheel at sideways position x has rolled. Turning, the wheels on the inside of the curve cover less ground.
  function wheelAngle(part, t) {
    var at = pathAt(t);
    return ((part.kind === 3 ? at.front : at.u) - part.o[0] * at.psi) / -part.rate;
  }

  // A front wheel's steering angle at time t. Each aims along its own circle around the turning center (Ackermann).
  function steerAngle(x, t) {
    var k = curveAt(pathAt(t).u);
    return Math.atan(WHEELBASE * k / (1 - x * k));
  }

  function partMatrix(part, t) {
    if (part.kind === 0) return bodyMatrix(t);
    if (part.kind === 1) return multiply(bodyMatrix(t), spinMatrix(part.o, part.k, part.rate * t));
    if (part.kind === 4) return poseMatrix(t);
    var roll = spinMatrix(part.o, part.k, wheelAngle(part, t));
    if (part.kind === 2) return multiply(poseMatrix(t), roll);
    return multiply(poseMatrix(t), multiply(spinMatrix(part.o, [0, 1, 0], steerAngle(part.o[0], t)), roll));
  }

  // ---------- Drawing ----------

  function shader(gl, type, source) {
    var s = gl.createShader(type);
    gl.shaderSource(s, source);
    gl.compileShader(s);
    return s;
  }

  // Sends the model to the graphics card and returns the function that draws a frame. Throws without WebGL.
  function makeRenderer(canvas, parts, W, H) {
    var gl = canvas.getContext('webgl');
    if (!gl) throw new Error('no WebGL');
    var at = 0;
    function link(vertex, fragment) {
      var p = gl.createProgram();
      gl.attachShader(p, shader(gl, gl.VERTEX_SHADER, vertex));
      gl.attachShader(p, shader(gl, gl.FRAGMENT_SHADER, fragment));
      gl.bindAttribLocation(p, at, 'p');
      gl.linkProgram(p);
      return p;
    }
    var program = link('attribute vec3 p;uniform mat4 vp,model;void main(){gl_Position=vp*model*vec4(p*.001,1.);}', 'void main(){gl_FragColor=vec4(1.);}');
    var vp = gl.getUniformLocation(program, 'vp'), model = gl.getUniformLocation(program, 'model');
    var groundProgram = link('attribute vec3 p;uniform mat4 vp;varying vec3 w;void main(){w=p;gl_Position=vp*vec4(p,1.);}',
      'precision highp float;uniform sampler2D tile;uniform vec3 eye;varying vec3 w;void main(){' +
      'gl_FragColor=texture2D(tile,w.xz/' + GROUND_TILE.toFixed(1) + ')*(1.-smoothstep(' + GROUND_FADE[0].toFixed(1) + ',' + GROUND_FADE[1].toFixed(1) + ',distance(w,eye)));}');
    var groundVp = gl.getUniformLocation(groundProgram, 'vp'), groundEye = gl.getUniformLocation(groundProgram, 'eye');
    gl.enableVertexAttribArray(at);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.polygonOffset(1, 1);
    gl.clearColor(0, 0, 0, 0);    // the grey is the page's own background
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);   // the canvas and the ground's texture are both premultiplied

    gl.bindTexture(gl.TEXTURE_2D, gl.createTexture());
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, GROUND_SIZE, GROUND_SIZE, 0, gl.RGBA, gl.UNSIGNED_BYTE, groundTexture(GROUND_SIZE));
    gl.generateMipmap(gl.TEXTURE_2D);   // far away the specks average out instead of shimmering
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    var aniso = gl.getExtension('EXT_texture_filter_anisotropic');
    if (aniso) gl.texParameterf(gl.TEXTURE_2D, aniso.TEXTURE_MAX_ANISOTROPY_EXT, Math.min(8, gl.getParameter(aniso.MAX_TEXTURE_MAX_ANISOTROPY_EXT)));

    function upload(target, data) {
      var buffer = gl.createBuffer();
      gl.bindBuffer(target, buffer);
      gl.bufferData(target, data, gl.STATIC_DRAW);
      return buffer;
    }
    parts.forEach(function (part) {
      part.gl = { verts: upload(gl.ARRAY_BUFFER, part.verts), tris: upload(gl.ELEMENT_ARRAY_BUFFER, part.tris), lines: upload(gl.ELEMENT_ARRAY_BUFFER, part.lines) };
    });
    var groundQuad = upload(gl.ARRAY_BUFFER, new Float32Array([-DEPTH_FAR, 0, -2, DEPTH_FAR, 0, -2, DEPTH_FAR, 0, DEPTH_FAR, -DEPTH_FAR, 0, DEPTH_FAR]));

    function pass(kind, mode, count) {
      parts.forEach(function (part) {
        gl.bindBuffer(gl.ARRAY_BUFFER, part.gl.verts);
        gl.vertexAttribPointer(at, 3, gl.SHORT, false, 0, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, part.gl[kind]);
        gl.uniformMatrix4fv(model, false, part.model);
        gl.drawElements(mode, part[kind].length, gl.UNSIGNED_SHORT, 0);
      });
    }

    return function draw(cam, t) {
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      var matrix = viewProjection(cam, W, H);
      gl.useProgram(program);
      gl.uniformMatrix4fv(vp, false, matrix);
      parts.forEach(function (part) { part.model = partMatrix(part, t); });
      // Faces into the depth buffer only, pushed back a touch so the lines on them win
      gl.colorMask(false, false, false, false);
      gl.enable(gl.POLYGON_OFFSET_FILL);
      pass('tris', gl.TRIANGLES);
      gl.colorMask(true, true, true, true);
      gl.disable(gl.POLYGON_OFFSET_FILL);
      // The ground, wherever the truck's faces don't hide it; then the lines
      gl.useProgram(groundProgram);
      gl.uniformMatrix4fv(groundVp, false, matrix);
      gl.uniform3fv(groundEye, cam.pos);
      gl.bindBuffer(gl.ARRAY_BUFFER, groundQuad);
      gl.vertexAttribPointer(at, 3, gl.FLOAT, false, 0, 0);
      gl.depthMask(false);
      gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);
      gl.depthMask(true);
      gl.useProgram(program);
      pass('lines', gl.LINES);
    };
  }

  if (typeof module !== 'undefined') {
    module.exports = { framing: framing, cameraAt: cameraAt, flapQuad: flapQuad, quadMatrix: quadMatrix, viewProjection: viewProjection, spinMatrix: spinMatrix,
      speed: speed, traveled: traveled, pathAt: pathAt, curveAt: curveAt, rideAt: rideAt, poseMatrix: poseMatrix, bodyMatrix: bodyMatrix,
      partMatrix: partMatrix, wheelAngle: wheelAngle, steerAngle: steerAngle, transform: transform, readTruck: readTruck, groundTexture: groundTexture,
      FLAP_X: FLAP_X, FLAP_Y: FLAP_Y, FLAP_TOP: FLAP_TOP, FLAP_H: FLAP_H, BRAKE: BRAKE, STOP: STOP, FILL_END: FILL_END, REAR_Z: REAR_Z, WHEELBASE: WHEELBASE };
    return;
  }

  // ---------- The shot ----------

  var root = document.documentElement;
  if (!root.classList.contains('drop')) return;

  var face = document.getElementById('main');
  var fig = face.querySelector('figure');
  var canvas, fill, twin, raf;

  function finish() {
    cancelAnimationFrame(raf);
    [canvas, fill, twin].forEach(function (el) { if (el) el.remove(); });
    fig.removeAttribute('style');
    root.classList.remove('drop');
    ['pointerdown', 'keydown'].forEach(function (type) { removeEventListener(type, finish); });
    removeEventListener('resize', finish);
    document.removeEventListener('visibilitychange', finish);
  }

  function start(buffer) {
    if (!root.classList.contains('drop')) return;   // the fallback in the page's <head> already gave up
    window.qIntro = true;
    if (document.hidden) { finish(); return; }
    ['pointerdown', 'keydown'].forEach(function (type) { addEventListener(type, finish); });
    addEventListener('resize', finish);
    document.addEventListener('visibilitychange', finish);

    var W = face.clientWidth, H = face.clientHeight, scale = Math.min(window.devicePixelRatio || 1, 1.5);   // WebGL lines are one pixel wide: not too fine
    var rect = fig.getBoundingClientRect();
    var frame = framing(W, H, rect);

    canvas = document.createElement('canvas');
    canvas.className = 'fx';
    canvas.width = Math.round(W * scale);
    canvas.height = Math.round(H * scale);
    face.insertBefore(canvas, face.firstChild);
    var draw = makeRenderer(canvas, readTruck(buffer), W, H);

    // Yellow spreads from the flap's outline to the edges of the screen; it sits between the lines and the flaps
    fill = document.createElement('div');
    fill.className = 'fx intro-fill';
    fill.style.visibility = 'hidden';
    face.insertBefore(fill, canvas.nextSibling);

    twin = fig.cloneNode(true);
    twin.setAttribute('aria-hidden', 'true');
    twin.querySelector('img').alt = '';
    twin.style.cssText = 'position:absolute;left:' + rect.left + 'px;top:' + rect.top + 'px;width:' + rect.width + 'px;height:' + rect.height + 'px;';
    face.appendChild(twin);

    [fig, twin].forEach(function (el) { el.style.transformOrigin = '0 0'; el.style.visibility = 'visible'; });

    function place(el, cam, x, swing, body) {
      var quad = flapQuad(cam, frame, x, swing, body).map(function (p) { return [p[0] - rect.left, p[1] - rect.top]; });
      el.style.transform = 'matrix3d(' + quadMatrix(rect.width, rect.height, quad).join(',') + ')';
    }

    var began, frames = -2, mark;
    function tick(now) {
      if (began === undefined) began = now;
      var t = (now - began) / 1000;
      if (t >= FILL_END) { finish(); return; }

      // Every ten frames (the first draw doesn't count: the card is still settling), see if this machine is keeping up
      if (++frames === 0) mark = now;
      else if (frames === 10) {
        var ms = (now - mark) / 10;
        frames = 0;
        mark = now;
        if (ms > GIVE_UP_MS) { finish(); return; }
        if (ms > SLOW_MS && scale > 0.75) {
          scale = scale > 1 ? 1 : 0.75;
          canvas.width = Math.round(W * scale);
          canvas.height = Math.round(H * scale);
        }
      }

      var cam = cameraAt(t, frame);
      draw(cam, t);

      var swing = rideAt(t).swing, body = bodyMatrix(t);
      place(fig, cam, FLAP_X, swing, body);
      place(twin, cam, -FLAP_X, swing, body);

      if (t > FILL_START) {
        var k = smooth((t - FILL_START) / (FILL_END - FILL_START)), left = 1 - k;
        fill.style.visibility = 'visible';
        fill.style.clipPath = 'inset(' + rect.top * left + 'px ' + (W - rect.right) * left + 'px ' + (H - rect.bottom) * left + 'px ' + rect.left * left + 'px' +
          ' round 0 0 ' + rect.width * 0.175 * left + 'px ' + rect.width * 0.175 * left + 'px / 0 0 ' + rect.height * 0.12 * left + 'px ' + rect.height * 0.12 * left + 'px)';   // same corners as the figure's CSS
      }
      raf = requestAnimationFrame(tick);
    }
    raf = requestAnimationFrame(tick);
  }

  try {
    var img = fig.querySelector('img');
    Promise.all([
      fetch('assets/truck.bin').then(function (r) { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); }),
      img.decode ? img.decode() : null
    ]).then(function (done) { start(done[0]); }).catch(finish);
  } catch (e) {
    finish();
  }
})();
