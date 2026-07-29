/**
 * Planetary motion (gati) & combustion.
 *
 * Facts first: speed, direction (retrograde), near-stationary and the distance
 * to the Sun come straight from the ephemeris. The gati NAMES and the combustion
 * ORBS are the classical scheme, shown on a `traditional` footing — NOT BPHS
 * (whose combustion is a proportional rule, not a fixed orb). Cheṣṭā bala — the
 * numeric motion-strength — is refused: BPHS instructs the Seeghrocha but never
 * gives one. That refusal is stated, not hidden.
 */

// Direction is the sign of the speed; the near-stationary state (which can occur
// on either side of a station) is carried by the gati label (vikala) beside it.
const DIR_LABEL = (m) => (m.retrograde ? 'retrograde ℞' : 'direct')

export default function MotionPanel({ data, namer }) {
  if (!data || data.error) return null
  const cb = data.cheshta_bala

  return (
    <section className="table-panel motion-panel" aria-label="Planetary motion and combustion">
      <h3>Motion (gati) &amp; combustion</h3>
      <p className="rc-note">
        Speed, direction and the separation from the Sun are <strong>facts</strong>{' '}
        from the ephemeris. The gati names (vakra / manda / …) and the combustion
        orbs are <strong>traditional</strong> — <em>not</em> BPHS, whose combustion
        is a proportional rule across 0–180° from the Sun, not a fixed orb.
      </p>

      {cb && !cb.available && (
        <p className="mp-cheshta">
          <span className="src conf conf-absent" title={`${cb.reason}\n\n${cb.citation}`}>
            Cheṣṭā bala · unavailable
          </span>
          <span className="mp-cheshta-why">
            The numeric strength of a graha's motion needs its Seeghrocha, which
            BPHS never tabulates — so it is refused. What follows is the motion{' '}
            <em>state</em>, not that bala.
          </span>
        </p>
      )}

      <div className="mp-scroll">
        <table className="mp-table">
          <thead>
            <tr>
              <th>Graha</th>
              <th>Motion</th>
              <th className="num">°/day</th>
              <th>Combustion</th>
            </tr>
          </thead>
          <tbody>
            {data.grahas.map(({ key, motion: m, combustion: c }) => (
              <tr key={key}>
                <td className="mp-graha">{namer.grahaKey(key)}</td>
                <td>
                  <span className={`mp-dir mp-${m.retrograde ? 'retro' : 'direct'}`}>
                    {DIR_LABEL(m)}
                  </span>
                  <span className="mp-gati" title={`${m.gati.en} — gati (traditional)`}>
                    {m.gati.iast}{m.pace ? ` · ${m.pace}` : ''}
                  </span>
                </td>
                <td className="num mp-speed"
                    title={`mean ${m.mean}°/day · ${Math.round(m.ratio * 100)}% of mean`}>
                  {m.speed.toFixed(3)}
                </td>
                <td>
                  {!c.applies ? (
                    <span className="mp-na" title={c.reason}>—</span>
                  ) : (
                    <span className={`mp-comb${c.combust ? ' is-combust' : ''}`}
                          title={`${c.separation}° from the Sun · orb ${c.orb}°\n\n${c.note}`}>
                      {c.combust ? 'combust' : 'free'} · {c.separation}°
                      <span className={`src mp-tier mp-${c.confidence === 'uncertain' ? 'uncertain' : 'trad'}`}>
                        {c.confidence === 'uncertain' ? 'uncertain' : 'traditional'}
                      </span>
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
