// Check the search filters on the list pages: node tools/test_lists.js
const assert = require('assert');
const { matches, newestFirst } = require('../site/assets/js/lists.js');

const a = { date: '2026-03-01', name: 'Eagle', category: 'Equine', company: 'GBX™' };
const b = { date: '2026-10-16', name: 'Patch', category: 'Concrete', company: 'Quadro▪cem™' };

assert(matches(a, {}));
assert(matches(a, { from: '', to: '', name: '', category: '', company: '' }));
assert(matches(a, { from: '2026-03-01', to: '2026-03-01' }), 'date range includes both ends');
assert(!matches(a, { from: '2026-03-02' }));
assert(!matches(a, { to: '2026-02-28' }));
assert(!matches(a, { name: 'Patch' }));
assert(!matches(a, { category: 'Concrete' }));
assert(!matches(a, { company: 'Quadro▪cem™' }));
assert(matches(b, { from: '2026-01-01', name: 'Patch', category: 'Concrete', company: 'Quadro▪cem™' }));
assert.deepStrictEqual([a, b].sort(newestFirst), [b, a]);
console.log('ok');
