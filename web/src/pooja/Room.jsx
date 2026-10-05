/**
 * The live room — the pandit and every family location on one screen.
 *
 * A WebRTC mesh: each browser holds a peer connection to every other, and the
 * media goes directly between them. The Worker's room object only relays the
 * handshake (who is here, offers, answers, ICE). A mesh is right for a pūjā —
 * a pandit and a handful of households — and it means no media server sits in
 * the middle of a family's ceremony.
 *
 * RECORDING is made here, in the pandit's browser: every tile is drawn onto
 * one canvas, every voice is mixed into one track, and the result is uploaded
 * in fifteen-second chunks as it is made — so a dropped connection loses
 * seconds, not the ceremony. The family watches it later from their booking
 * page. Everyone in the room sees that it is being recorded.
 *
 * THE STEPS sit beside the video. Whoever leads — the pandit, or in a family
 * gathering anyone — moves the step, and every screen follows; each person
 * reads what the step is and why in the language and depth they choose.
 *
 * Networks: the room asks the service for its ICE servers before it calls
 * anyone — STUN, and a TURN relay (a short-lived credential minted for this
 * room) so that two homes behind strict NATs or a firewall still connect. If
 * the service has no relay the room is STUN-only, and says so when a
 * connection fails rather than showing a silent black tile. A connection that
 * fails is tried once more with a fresh ICE gathering.
 */
import { useCallback, useEffect, useRef, useState } from 'react'
import { api } from './papi.js'
import Guide from './Guide.jsx'

const STUN = [{ urls: ['stun:stun.l.google.com:19302', 'stun:stun.cloudflare.com:3478'] }]
const newPeerId = () => [...crypto.getRandomValues(new Uint8Array(10))].map((b) => (b % 36).toString(36)).join('')

function Tile({ stream, name, role, me, state, relay, L }) {
  const ref = useRef(null)
  useEffect(() => { if (ref.current && ref.current.srcObject !== stream) ref.current.srcObject = stream || null }, [stream])
  return (
    <div className={`pu-tile${role === 'priest' ? ' priest' : ''}`}>
      <video ref={ref} autoPlay playsInline muted={me} data-name={name} />
      {!stream && <div className="pu-tile-wait">{state === 'failed'
        ? (relay ? L('Could not connect — check the connection, then leave and join again', 'जुड़ नहीं सका — कनेक्शन जाँचें, फिर कक्ष छोड़कर दोबारा जुड़ें') : L('Could not connect — this network needs the relay, which is not switched on yet', 'जुड़ नहीं सका — इस नेटवर्क को रिले चाहिए, जो अभी चालू नहीं है'))
        : L('connecting…', 'जुड़ रहा है…')}</div>}
      <div className="pu-tile-name">{role === 'priest' && <b>{L('Pandit', 'पंडित जी')} · </b>}{name}{me ? ` (${L('you', 'आप')})` : ''}</div>
    </div>
  )
}

export default function Room({ bookingId, name, role, canRecord, ritual, selfLed = false, lang = 'en', L, onLeave }) {
  const canLead = role === 'priest' || selfLed
  const [step, setStep] = useState(null)         // the step the leader is on, for everyone
  const stepRef = useRef(null)
  const recWire = useRef(null)                   // while recording: wires a late joiner's voice into the mix
  const ice = useRef(STUN)                        // replaced by the room's own servers (with the relay) before any call
  const [relay, setRelay] = useState(false)
  const called = useRef(new Set())               // peers this side made the offer to
  const retried = useRef(new Set())
  const [local, setLocal] = useState(null)
  const [peers, setPeers] = useState({})          // id -> { name, role, stream, state }
  const [micOn, setMicOn] = useState(true)
  const [camOn, setCamOn] = useState(true)
  const [status, setStatus] = useState('starting')
  const [err, setErr] = useState('')
  const [rec, setRec] = useState({ on: false, chunks: 0, failed: 0 })
  const [recSeen, setRecSeen] = useState(false)  // someone in the room is recording
  const me = useRef(newPeerId())
  const ws = useRef(null)
  const pcs = useRef({})
  const localRef = useRef(null)
  const recorder = useRef(null)
  const recLoop = useRef(null)
  const audioCtx = useRef(null)

  const send = (m) => { try { ws.current && ws.current.readyState === 1 && ws.current.send(JSON.stringify(m)) } catch { /* closing */ } }
  const patchPeer = (id, patch) => setPeers((p) => ({ ...p, [id]: { ...(p[id] || {}), ...patch } }))
  const dropPeer = useCallback((id) => {
    try { pcs.current[id] && pcs.current[id].close() } catch { /* closed */ }
    delete pcs.current[id]
    setPeers((p) => { const q = { ...p }; delete q[id]; return q })
  }, [])

  const makePc = useCallback((id, info) => {
    if (pcs.current[id]) return pcs.current[id]
    const pc = new RTCPeerConnection({ iceServers: ice.current })
    pcs.current[id] = pc
    patchPeer(id, { name: info?.name || 'Guest', role: info?.role || 'family', state: 'new' })
    if (localRef.current) localRef.current.getTracks().forEach((tr) => pc.addTrack(tr, localRef.current))
    else { pc.addTransceiver('video', { direction: 'recvonly' }); pc.addTransceiver('audio', { direction: 'recvonly' }) }
    pc.onicecandidate = (e) => { if (e.candidate) send({ t: 'ice', to: id, candidate: e.candidate }) }
    pc.ontrack = (e) => { patchPeer(id, { stream: e.streams[0] }); recWire.current && recWire.current(e.streams[0]) }
    pc.onconnectionstatechange = () => {
      patchPeer(id, { state: pc.connectionState })
      if (pc.connectionState === 'closed') dropPeer(id)
      // One fresh attempt, from the side that made the call, before the tile says it failed for good.
      if (pc.connectionState === 'failed' && called.current.has(id) && !retried.current.has(id)) {
        retried.current.add(id)
        ;(async () => {
          try {
            const offer = await pc.createOffer({ iceRestart: true })
            await pc.setLocalDescription(offer)
            send({ t: 'offer', to: id, sdp: pc.localDescription, name, role })
          } catch { /* it stays failed, and the tile says so */ }
        })()
      }
    }
    return pc
  }, [dropPeer])

  useEffect(() => {
    let dead = false
    ;(async () => {
      let stream = null
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 960 }, height: { ideal: 540 } }, audio: { echoCancellation: true, noiseSuppression: true } })
      } catch {
        try { stream = await navigator.mediaDevices.getUserMedia({ audio: true }); setCamOn(false) } catch { setErr(L('No camera or microphone — you are watching only.', 'कैमरा या माइक नहीं मिला — आप केवल देख रहे हैं।')) }
      }
      if (dead) { stream && stream.getTracks().forEach((tr) => tr.stop()); return }
      localRef.current = stream
      setLocal(stream)
      try {
        const j = await api.ice(bookingId)
        if (j && Array.isArray(j.iceServers) && j.iceServers.length) { ice.current = j.iceServers; setRelay(!!j.turn) }
      } catch { /* STUN only */ }
      if (dead) return
      const sock = new WebSocket(api.wsUrl(bookingId, me.current, name, role))
      ws.current = sock
      sock.onopen = () => setStatus('joined')
      sock.onclose = () => { if (!dead) setStatus('closed') }
      sock.onerror = () => { if (!dead) setErr(L('The room could not be reached.', 'कक्ष तक पहुँच नहीं हो सकी।')) }
      sock.onmessage = async (ev) => {
        let m
        try { m = JSON.parse(ev.data) } catch { return }
        try {
          if (m.t === 'hello') {
            // The newcomer calls everyone already here.
            for (const p of m.peers || []) {
              const pc = makePc(p.peer, p)
              called.current.add(p.peer)
              const offer = await pc.createOffer()
              await pc.setLocalDescription(offer)
              send({ t: 'offer', to: p.peer, sdp: pc.localDescription, name, role })
            }
          } else if (m.t === 'join') {
            patchPeer(m.peer.peer, { name: m.peer.name, role: m.peer.role, state: 'new' })
            if (recorder.current) send({ t: 'rec', on: true })
            // tell the newcomer which step the ceremony is on
            if (canLead && stepRef.current != null) send({ t: 'step', i: stepRef.current, to: m.peer.peer })
          } else if (m.t === 'offer') {
            const pc = makePc(m.from, { name: m.name, role: m.role })
            await pc.setRemoteDescription(m.sdp)
            const ans = await pc.createAnswer()
            await pc.setLocalDescription(ans)
            send({ t: 'answer', to: m.from, sdp: pc.localDescription })
          } else if (m.t === 'answer') {
            pcs.current[m.from] && await pcs.current[m.from].setRemoteDescription(m.sdp)
          } else if (m.t === 'ice') {
            pcs.current[m.from] && await pcs.current[m.from].addIceCandidate(m.candidate).catch(() => {})
          } else if (m.t === 'leave') {
            dropPeer(m.peer)
          } else if (m.t === 'rec') {
            setRecSeen(!!m.on)
          } else if (m.t === 'step') {
            // only the pandit moves the step — or, in a family gathering, anyone
            const lead = selfLed || (peersRef.current[m.from] && peersRef.current[m.from].role === 'priest')
            if (lead && Number.isInteger(m.i) && m.i >= 0 && m.i < 60) { stepRef.current = m.i; setStep(m.i) }
          }
        } catch (e) { setErr(String(e.message || e)) }
      }
    })()
    const beat = setInterval(() => send({ t: 'ping', to: me.current }), 25000)
    return () => {
      dead = true
      clearInterval(beat)
      stopRecording()
      try { ws.current && ws.current.close() } catch { /* closed */ }
      Object.keys(pcs.current).forEach((id) => { try { pcs.current[id].close() } catch { /* closed */ } })
      pcs.current = {}
      localRef.current && localRef.current.getTracks().forEach((tr) => tr.stop())
    }
  }, [bookingId])  // eslint-disable-line react-hooks/exhaustive-deps

  const toggle = (kind, on, set) => {
    const s = localRef.current
    if (s) (kind === 'audio' ? s.getAudioTracks() : s.getVideoTracks()).forEach((tr) => { tr.enabled = !on })
    set(!on)
  }

  // ── recording: one canvas, one mixed audio track, chunks uploaded as made ──
  function startRecording() {
    if (recorder.current) return
    const canvas = document.createElement('canvas')
    canvas.width = 1280; canvas.height = 720
    const g = canvas.getContext('2d')
    const draw = () => {
      const vids = [...document.querySelectorAll('.pu-tile video')].filter((v) => v.srcObject && v.videoWidth)
      g.fillStyle = '#10201a'; g.fillRect(0, 0, 1280, 720)
      const n = Math.max(1, vids.length), cols = n <= 1 ? 1 : n <= 4 ? 2 : 3, rows = Math.ceil(n / cols)
      const w = 1280 / cols, h = 720 / rows
      vids.forEach((v, i) => {
        const x = (i % cols) * w, y = Math.floor(i / cols) * h
        const s = Math.min(w / v.videoWidth, h / v.videoHeight)
        const dw = v.videoWidth * s, dh = v.videoHeight * s
        g.drawImage(v, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)
        g.fillStyle = 'rgba(0,0,0,.55)'; g.fillRect(x + 8, y + h - 34, Math.min(w - 16, 14 + (v.dataset.name || '').length * 9), 26)
        g.fillStyle = '#fff'; g.font = '16px sans-serif'; g.fillText(v.dataset.name || '', x + 15, y + h - 16)
      })
    }
    recLoop.current = setInterval(draw, 1000 / 15)
    const ctx = new (window.AudioContext || window.webkitAudioContext)()
    audioCtx.current = ctx
    const dest = ctx.createMediaStreamDestination()
    const wired = new Set()
    const wire = (s) => {
      if (!s || wired.has(s.id) || !s.getAudioTracks().length) return
      wired.add(s.id)
      try { ctx.createMediaStreamSource(s).connect(dest) } catch { /* no audio in it yet */ wired.delete(s.id) }
    }
    wire(localRef.current)
    Object.values(peersRef.current).forEach((p) => wire(p.stream))
    recWire.current = wire                       // anyone who joins after this is mixed in as they arrive
    const out = new MediaStream([...canvas.captureStream(15).getVideoTracks(), ...dest.stream.getAudioTracks()])
    const mime = ['video/webm;codecs=vp8,opus', 'video/webm'].find((m) => window.MediaRecorder && MediaRecorder.isTypeSupported(m))
    if (!mime) { setErr(L('This browser cannot record.', 'यह ब्राउज़र रिकॉर्ड नहीं कर सकता।')); clearInterval(recLoop.current); recWire.current = null; return }
    const r = new MediaRecorder(out, { mimeType: mime, videoBitsPerSecond: 900000, audioBitsPerSecond: 64000 })
    let seq = 0
    let chain = Promise.resolve()
    r.ondataavailable = (e) => {
      if (!e.data || !e.data.size) return
      const n = seq++
      chain = chain.then(() => api.putChunk(bookingId, n, e.data))
        .then(() => setRec((x) => ({ ...x, chunks: x.chunks + 1 })))
        .catch(() => setRec((x) => ({ ...x, failed: x.failed + 1 })))
    }
    r.start(15000)
    recorder.current = r
    setRec({ on: true, chunks: 0, failed: 0 })
    send({ t: 'rec', on: true })
    setRecSeen(true)
  }
  function stopRecording() {
    if (!recorder.current) return
    try { recorder.current.stop() } catch { /* stopped */ }
    recorder.current = null
    recWire.current = null
    clearInterval(recLoop.current)
    try { audioCtx.current && audioCtx.current.close() } catch { /* closed */ }
    setRec((x) => ({ ...x, on: false }))
    send({ t: 'rec', on: false })
    setRecSeen(false)
  }
  const peersRef = useRef({})
  useEffect(() => { peersRef.current = peers }, [peers])

  const invite = `${typeof location !== 'undefined' ? location.origin : 'https://devashaa.com'}/pooja/room/${bookingId}`
  const ids = Object.keys(peers)

  return (
    <div className="pu-room">
      <div className="pu-room-bar">
        <span className={`pu-live ${status}`}>{status === 'joined' ? L('In the room', 'कक्ष में') : status === 'closed' ? L('Disconnected', 'संपर्क टूटा') : L('Joining…', 'जुड़ रहे हैं…')}</span>
        <span className="pu-room-count">{ids.length + 1} {L('here', 'उपस्थित')}</span>
        {relay && <span className="pu-room-count" title={L('Homes that cannot reach each other directly are connected through a relay.', 'जो घर सीधे नहीं जुड़ पाते, वे रिले से जुड़ते हैं।')}>· {L('relay ready', 'रिले तैयार')}</span>}
        {recSeen && <span className="pu-rec"><i /> {L('Recording', 'रिकॉर्डिंग चालू')}{rec.on ? ` · ${rec.chunks} ${L('saved', 'सुरक्षित')}${rec.failed ? ` · ${rec.failed} ${L('failed', 'विफल')}` : ''}` : ''}</span>}
      </div>
      {err && <p className="pu-err">{err}</p>}
      <div className={`pu-room-body${ritual ? ' with-guide' : ''}`}>
        <div className={`pu-grid n${Math.min(6, ids.length + 1)}`}>
          <Tile stream={local} name={name} role={role} me L={L} />
          {ids.map((id) => <Tile key={id} stream={peers[id].stream} name={peers[id].name} role={peers[id].role} state={peers[id].state} relay={relay} L={L} />)}
        </div>
        {ritual && (
          <aside className="pu-room-guide" aria-label={L('The steps of the ceremony', 'अनुष्ठान के चरण')}>
            <p className="pu-room-guide-head">
              <b>{ritual.name[lang] || ritual.name.en}</b>
              <span>{canLead
                ? (selfLed ? L('Anyone here moves the step for all', 'यहाँ कोई भी सबके लिए चरण बढ़ा सकता है') : L('You lead — every screen follows your step', 'आप संचालक हैं — हर स्क्रीन आपके चरण पर चलती है'))
                : L('Follows the pandit’s step', 'पंडित जी के चरण के साथ')}</span>
            </p>
            <Guide ritual={ritual} lang={lang} L={L} live canLead={canLead} remote={step}
                   onStep={(i) => { stepRef.current = i; setStep(i); send({ t: 'step', i }) }} />
          </aside>
        )}
      </div>
      <div className="pu-controls">
        <button type="button" className={micOn ? '' : 'off'} onClick={() => toggle('audio', micOn, setMicOn)}>{micOn ? L('Mute', 'माइक बंद') : L('Unmute', 'माइक चालू')}</button>
        <button type="button" className={camOn ? '' : 'off'} onClick={() => toggle('video', camOn, setCamOn)}>{camOn ? L('Camera off', 'कैमरा बंद') : L('Camera on', 'कैमरा चालू')}</button>
        {canRecord && (rec.on
          ? <button type="button" className="rec on" onClick={stopRecording}>{L('Stop recording', 'रिकॉर्डिंग रोकें')}</button>
          : <button type="button" className="rec" onClick={startRecording}>{L('Record the ceremony', 'पूजा रिकॉर्ड करें')}</button>)}
        <button type="button" onClick={() => { try { navigator.clipboard.writeText(invite) } catch { /* no clipboard */ } }} title={invite}>{L('Copy the family link', 'परिवार का लिंक कॉपी करें')}</button>
        <button type="button" className="leave" onClick={onLeave}>{L('Leave', 'कक्ष छोड़ें')}</button>
      </div>
      <p className="pu-note">{L('Video and sound travel directly between the people in the room. Share the family link with relatives in other homes — each joins from their own screen.', 'वीडियो और ध्वनि कक्ष के लोगों के बीच सीधे जाती है। दूसरे घरों के स्वजनों को परिवार का लिंक भेजें — हर कोई अपनी स्क्रीन से जुड़ता है।')}</p>
    </div>
  )
}
