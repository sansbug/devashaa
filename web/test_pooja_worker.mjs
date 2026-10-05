/**
 * Pūjā — the Worker end to end, against a LOCAL `wrangler dev` (simulated D1,
 * R2 and Durable Objects). It walks what a pandit and a family actually do:
 * apply, be vetted, record for the voice library, take a booking, open a room.
 *
 *   npx wrangler d1 execute devashaa-accounts --local --file schema.sql     (once)
 *   npx wrangler dev --port 8799 --var POOJA_ADMIN_CODE:local-test-admin-code
 *   node test_pooja_worker.mjs [http://localhost:8799]
 *
 * It makes throwaway accounts, so it refuses to run against anything but a
 * local host.
 */
const BASE = process.argv[2] || 'http://localhost:8799'
if (!/^http:\/\/(localhost|127\.0\.0\.1):\d+$/.test(BASE)) { console.error('local hosts only'); process.exit(2) }
const CODE = process.env.POOJA_TEST_ADMIN_CODE || 'local-test-admin-code'
const rnd = (n) => [...crypto.getRandomValues(new Uint8Array(n))].map((b) => b.toString(16).padStart(2, '0')).join('')

let failed = 0
const ok = (name, cond, detail = '') => { console.log(`  ${cond ? 'OK ' : 'XX '}${name} ${detail}`); if (!cond) failed += 1 }
async function call(path, { method = 'GET', body, raw, type, as } = {}) {
  const headers = {}
  if (as) { headers['X-User'] = as.userid; headers['X-Auth'] = as.authId }
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (raw) headers['Content-Type'] = type || 'audio/wav'
  const r = await fetch(BASE + path, { method, headers, body: raw || (body !== undefined ? JSON.stringify(body) : undefined) })
  const ct = r.headers.get('Content-Type') || ''
  return { status: r.status, type: ct, body: ct.includes('json') ? await r.json() : new Uint8Array(await r.arrayBuffer()) }
}
async function account(tag) {
  const a = { userid: `${tag}-${rnd(4)}@example.com`, authId: rnd(32) }
  const r = await call('/api/account', { method: 'POST', body: a })
  if (r.status !== 201) throw new Error(`could not make the test account (${r.status})`)
  return a
}
// A tiny valid WAV: 0.1 s of a tone.
function wav(seed = 1) {
  const sr = 8000, n = 800, buf = new ArrayBuffer(44 + n * 2), v = new DataView(buf)
  const s = (o, t) => [...t].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)))
  s(0, 'RIFF'); v.setUint32(4, 36 + n * 2, true); s(8, 'WAVE'); s(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true)
  v.setUint32(24, sr, true); v.setUint32(28, sr * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); s(36, 'data'); v.setUint32(40, n * 2, true)
  for (let i = 0; i < n; i++) v.setInt16(44 + i * 2, Math.round(9000 * Math.sin(i * 0.2 * seed)), true)
  return new Uint8Array(buf)
}

const A = await account('pandit-a'), B = await account('pandit-b'), ADMIN = await account('owner'), C = await account('stranger')
const M = 'm.ganesha.abc123', X = 'x.ganesha.en.short.abc123'

console.log('\nthe roster and vetting')
ok('applying needs a sign-in', (await call('/api/pooja/priests/apply', { method: 'POST', body: { name: 'X' } })).status === 401)
const ap = await call('/api/pooja/priests/apply', { method: 'POST', as: A, body: { name: 'Pandit A (test)', voice: 'm', city: 'Kanpur', languages: 'Hindi, Sanskrit', contact: 'test-contact-a' } })
ok('pandit A applies → pending', ap.status === 200 && ap.body.status === 'pending')
const meA = (await call('/api/pooja/me', { as: A })).body
ok('…and is given a public id that is not his sign-in', /^[0-9a-f]{16}$/.test(meA.priest.pid) && !meA.priest.pid.includes('@'), meA.priest.pid)
ok('a pending pandit is not on the public roster', !(await call('/api/pooja/priests')).body.priests.some((p) => p.id === meA.priest.pid))
ok('a pending pandit cannot record', (await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: A, raw: wav() })).status === 403)
ok('a wrong admin code is refused', (await call('/api/pooja/admin/claim', { method: 'POST', as: ADMIN, body: { code: 'not-the-code' } })).status === 403)
ok('the owner claims admin with the code', (await call('/api/pooja/admin/claim', { method: 'POST', as: ADMIN, body: { code: CODE } })).body.role === 'admin')
const desk = (await call('/api/pooja/desk', { as: ADMIN })).body
const appl = desk.applicants.find((p) => p.id === meA.priest.pid)
ok('the admin’s desk lists the applicant, voice included', !!appl && appl.voice === 'm')
ok('…without his sign-in id', appl && !('userid' in appl) && !JSON.stringify(desk.applicants).includes('@example.com'))
ok('a stranger cannot vet', (await call(`/api/pooja/priests/${meA.priest.pid}/vet`, { method: 'POST', as: C, body: { decision: 'approve' } })).status === 403)
ok('the admin approves A', (await call(`/api/pooja/priests/${meA.priest.pid}/vet`, { method: 'POST', as: ADMIN, body: { decision: 'approve' } })).body.changed === 1)
const roster = (await call('/api/pooja/priests')).body.priests
const rA = roster.find((p) => p.id === meA.priest.pid)
ok('A is on the public roster, with his voice', !!rA && rA.voice === 'm' && rA.name === 'Pandit A (test)')
ok('the public roster carries no sign-in id and no contact', !JSON.stringify(roster).includes('@example.com') && !JSON.stringify(roster).includes('test-contact-a') && !('userid' in rA))
await call('/api/pooja/priests/apply', { method: 'POST', as: B, body: { name: 'Pandita B (test)', voice: 'f' } })
const meB = (await call('/api/pooja/me', { as: B })).body
ok('B cannot vet herself', (await call(`/api/pooja/priests/${meB.priest.pid}/vet`, { method: 'POST', as: B, body: { decision: 'approve' } })).status === 403)
ok('A, now approved, vets B — the roster grows by its own pandits', (await call(`/api/pooja/priests/${meB.priest.pid}/vet`, { method: 'POST', as: A, body: { decision: 'approve' } })).body.changed === 1)
ok('editing a profile keeps approval and the public id', (await call('/api/pooja/priests/apply', { method: 'POST', as: A, body: { name: 'Pandit A (test)', voice: 'm', city: 'Kanpur' } })).body.status === 'approved'
  && (await call('/api/pooja/me', { as: A })).body.priest.pid === meA.priest.pid)

console.log('\nthe voice library')
ok('recording needs a sign-in', (await call(`/api/pooja/chant/${M}`, { method: 'PUT', raw: wav() })).status === 401)
ok('a stranger cannot record', (await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: C, raw: wav() })).status === 403)
ok('the admin, not being a pandit, does not record', (await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: ADMIN, raw: wav() })).status === 403)
const wa = wav(1), wb = wav(2)
const putA = await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: A, raw: wa })
ok('pandit A records the mantra', putA.status === 200 && putA.body.id === meA.priest.pid)
ok('pandita B records the same mantra', (await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: B, raw: wb })).status === 200)
ok('A records an explanation in English', (await call(`/api/pooja/chant/${X}`, { method: 'PUT', as: A, raw: wa })).status === 200)
let lib = (await call('/api/pooja/chants')).body.clips
ok('the library lists both voices for the mantra', (lib[M] || []).length === 2 && lib[M].some((c) => c.voice === 'm' && c.by === 'Pandit A (test)') && lib[M].some((c) => c.voice === 'f' && c.by === 'Pandita B (test)'))
ok('…and the explanation', (lib[X] || []).length === 1 && lib[X][0].id === meA.priest.pid)
ok('the library names no sign-in id', !JSON.stringify(lib).includes('@example.com'))
const got = await call(`/api/pooja/chant/${M}/${meA.priest.pid}`)
ok('A’s chant plays back byte for byte, as audio/wav', got.status === 200 && got.type.startsWith('audio/wav') && got.body.length === wa.length && got.body.every((x, i) => x === wa[i]))
const gotB = await call(`/api/pooja/chant/${M}/${meB.priest.pid}`)
ok('B’s is her own recording, not A’s', gotB.body.length === wb.length && gotB.body.some((x, i) => x !== wa[i]))
ok('recording again replaces one’s own, it does not add a second', (await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: A, raw: wb })).status === 200 && (await call('/api/pooja/chants')).body.clips[M].length === 2)
ok('an oversized upload is refused', (await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: A, raw: new Uint8Array(6 * 1024 * 1024 + 10) })).status === 413)
ok('a malformed clip name is not found', (await call('/api/pooja/chant/..%2F..%2Frec', { method: 'PUT', as: A, raw: wa })).status === 404 && (await call('/api/pooja/chant/m..x', { method: 'PUT', as: A, raw: wa })).status === 404)
ok('B cannot remove A’s recording', (await call(`/api/pooja/chant/${M}/${meA.priest.pid}`, { method: 'DELETE', as: B })).status === 403)
ok('a stranger cannot remove it', (await call(`/api/pooja/chant/${M}/${meA.priest.pid}`, { method: 'DELETE', as: C })).status === 403)
ok('A removes his own', (await call(`/api/pooja/chant/${M}/${meA.priest.pid}`, { method: 'DELETE', as: A })).status === 200)
ok('the admin can remove any', (await call(`/api/pooja/chant/${M}/${meB.priest.pid}`, { method: 'DELETE', as: ADMIN })).status === 200)
lib = (await call('/api/pooja/chants')).body.clips
ok('the mantra is unrecorded again; the explanation remains', !lib[M] && (lib[X] || []).length === 1)
ok('a removed chant is gone', (await call(`/api/pooja/chant/${M}/${meA.priest.pid}`)).status === 404)
await call(`/api/pooja/chant/${X}/${meA.priest.pid}`, { method: 'DELETE', as: A })

console.log('\na voice the admin records for (a known pandit with no account)')
ok('only the admin adds a voice', (await call('/api/pooja/voices', { method: 'POST', as: A, body: { name: 'X Y', voice: 'm' } })).status === 403
  && (await call('/api/pooja/voices', { method: 'POST', body: { name: 'X Y', voice: 'm' } })).status === 401)
ok('a voice needs a name and male / female', (await call('/api/pooja/voices', { method: 'POST', as: ADMIN, body: { name: 'Guru Voice (test)' } })).status === 400)
const nv = await call('/api/pooja/voices', { method: 'POST', as: ADMIN, body: { name: 'Guru Voice (test)', voice: 'm' } })
const VP = nv.body.id
ok('the admin adds one', nv.status === 201 && /^[0-9a-f]{16}$/.test(VP || ''))
ok('it is on the admin’s desk', (await call('/api/pooja/desk', { as: ADMIN })).body.voices.some((v) => v.id === VP && v.voice === 'm'))
ok('…not on a pandit’s desk, and not on the bookable roster', (await call('/api/pooja/desk', { as: A })).body.voices.length === 0 && !(await call('/api/pooja/priests')).body.priests.some((p) => p.id === VP))
ok('a pandit cannot record in someone else’s name', (await call(`/api/pooja/chant/${M}?for=${VP}`, { method: 'PUT', as: A, raw: wa })).status === 403)
ok('the admin cannot record for a voice that is not there', (await call(`/api/pooja/chant/${M}?for=0123456789abcdef`, { method: 'PUT', as: ADMIN, raw: wa })).status === 404)
const forV = await call(`/api/pooja/chant/${M}?for=${VP}`, { method: 'PUT', as: ADMIN, raw: wa })
ok('the admin records (or uploads) for him', forV.status === 200 && forV.body.id === VP)
ok('the library offers it under his name and voice', ((await call('/api/pooja/chants')).body.clips[M] || []).some((c) => c.id === VP && c.by === 'Guru Voice (test)' && c.voice === 'm'))
ok('it plays', (await call(`/api/pooja/chant/${M}/${VP}`)).body.length === wa.length)
ok('no family can book a voice', (await call(`/api/pooja/bookings/${(await call('/api/pooja/bookings', { method: 'POST', body: { ritual: 'ganesh', starts_at: '2026-12-05T09:30', priest: VP, name: 'Voice test', contact: 'contact-voice' } })).body.id}`)).body.priest === null)
ok('only the admin removes a voice', (await call(`/api/pooja/voices/${VP}`, { method: 'DELETE', as: A })).status === 403)
ok('the admin removes him', (await call(`/api/pooja/voices/${VP}`, { method: 'DELETE', as: ADMIN })).status === 200)
ok('…and his recordings go with him', !(await call('/api/pooja/chants')).body.clips[M] && (await call(`/api/pooja/chant/${M}/${VP}`)).status === 404
  && !(await call('/api/pooja/desk', { as: ADMIN })).body.voices.some((v) => v.id === VP))

console.log('\nbookings and the room')
const bk = await call('/api/pooja/bookings', { method: 'POST', body: { ritual: 'ganesh', starts_at: '2026-12-01T09:30', tz: 'Asia/Kolkata', priest: meA.priest.pid, name: 'Test family', contact: 'family-contact-xyz', notes: 'gotra: test' } })
ok('a family asks for pandit A by his public id', bk.status === 201)
const id = bk.body.id
const pub = (await call(`/api/pooja/bookings/${id}`)).body
ok('the booking names the pandit by public id only', pub.priest && pub.priest.id === meA.priest.pid && pub.priest.name === 'Pandit A (test)' && !JSON.stringify(pub).includes('@example.com'))
ok('the family’s contact is not shown to whoever holds the link', !('contact' in pub) && pub.mine === false)
const asA = (await call(`/api/pooja/bookings/${id}`, { as: A })).body
ok('the booking’s own pandit sees it is his, and the contact', asA.mine === true && asA.contact === 'family-contact-xyz')
ok('another pandit does not see the contact', !('contact' in (await call(`/api/pooja/bookings/${id}`, { as: B })).body))
const open = (await call('/api/pooja/bookings', { method: 'POST', body: { ritual: 'ganesh', starts_at: '2026-12-02T09:30', name: 'Open family', contact: 'open-contact-123' } })).body.id
const deskB = (await call('/api/pooja/desk', { as: B })).body
const row = deskB.bookings.find((b) => b.id === open)
ok('an unassigned request is on every pandit’s desk — without the contact', !!row && row.contact === null && !JSON.stringify(deskB).includes('open-contact-123'))
ok('…and A’s booking is not on B’s desk', !deskB.bookings.some((b) => b.id === id))
await call(`/api/pooja/bookings/${open}/accept`, { method: 'POST', as: B, body: {} })
ok('once B takes it, B sees the contact', (await call('/api/pooja/desk', { as: B })).body.bookings.find((b) => b.id === open).contact === 'open-contact-123')
const self = (await call('/api/pooja/bookings', { method: 'POST', body: { ritual: 'ganesh', starts_at: '2026-12-03T09:30', self: true } })).body.id
ok('a family gathering is on no pandit’s desk', !(await call('/api/pooja/desk', { as: A })).body.bookings.some((b) => b.id === self))

const ice = await call(`/api/pooja/room/${id}/ice`)
ok('the room hands out ICE servers', ice.status === 200 && Array.isArray(ice.body.iceServers) && ice.body.iceServers.length > 0)
ok('with no TURN key configured here it says so: STUN only', ice.body.turn === false && ice.body.iceServers.every((s) => s.urls.every((u) => u.startsWith('stun:'))))
ok('no room, no servers: an unknown id is 404', (await call(`/api/pooja/room/${rnd(16)}/ice`)).status === 404)
const ws = (rid, peer) => new Promise((res) => { const w = new WebSocket(`${BASE.replace('http', 'ws')}/api/pooja/room/${rid}/ws?peer=${peer}&name=T&role=family`); w.onopen = () => res(w); w.onerror = () => res(null) })
const sock = await ws(id, 'aaaaaaaaaa')
ok('the room’s socket opens for a real booking', !!sock)
sock && sock.close()
ok('…and not for an id that is no booking', (await ws(rnd(16), 'bbbbbbbbbb')) === null)
await call(`/api/pooja/bookings/${self}/cancel`, { method: 'POST', body: {} })
ok('a cancelled gathering has no room', (await call(`/api/pooja/room/${self}/ice`)).status === 404)

const w = await call('/api/pooja/where')
ok('/where answers (a city, or nothing — never an error)', w.status === 200 && typeof w.body === 'object', JSON.stringify(w.body).slice(0, 90))

console.log('\ndeleting an account takes the pandit out of the service')
await call(`/api/pooja/chant/${M}`, { method: 'PUT', as: B, raw: wb })
ok('before: B is on the roster, has a recording, and holds a confirmed booking', (await call('/api/pooja/priests')).body.priests.some((p) => p.id === meB.priest.pid)
  && ((await call('/api/pooja/chants')).body.clips[M] || []).some((c) => c.id === meB.priest.pid) && (await call(`/api/pooja/bookings/${open}`)).body.status === 'confirmed')
ok('B deletes her account', (await call(`/api/account/${B.userid}`, { method: 'DELETE', as: B })).status === 200)
ok('…she is off the roster', !(await call('/api/pooja/priests')).body.priests.some((p) => p.id === meB.priest.pid))
ok('…her recording is gone, from the list and from storage', !(await call('/api/pooja/chants')).body.clips[M] && (await call(`/api/pooja/chant/${M}/${meB.priest.pid}`)).status === 404)
const back = (await call(`/api/pooja/bookings/${open}`)).body
ok('…and the family she had accepted is back in the queue for another pandit', back.status === 'requested' && back.priest === null)
ok('A is untouched', (await call('/api/pooja/priests')).body.priests.some((p) => p.id === meA.priest.pid))

// leave the local store as it was found
// (the id goes in the path as the site's own client sends it: '@' is legal there, and the Worker does not decode)
let swept = 0
for (const who of [A, ADMIN, C]) swept += (await call(`/api/account/${who.userid}`, { method: 'DELETE', as: who })).status === 200 ? 1 : 0
ok('the remaining throwaway accounts are removed again', swept === 3, String(swept))
ok('…and with them every test pandit', !(await call('/api/pooja/priests')).body.priests.some((p) => / \(test\)$/.test(p.name)))
console.log(failed ? `\n${failed} FAILED ✗` : '\nALL PASS ✓')
process.exit(failed ? 1 : 0)
