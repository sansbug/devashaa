import { useEffect, useId, useLayoutEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'

/**
 * Provenance chip — P1 of the "show your work" roadmap.
 *
 * A `.src`-style chip whose source detail used to live in a hover-only `title`
 * (invisible on touch, so mobile users never saw the citation). With a `detail`
 * prop this renders an accessible, TAPPABLE popover instead — works by pointer,
 * touch and keyboard alike, closes on Escape / outside-tap / scroll. Without
 * `detail` it is a plain static chip (the visible text is the whole claim).
 *
 * Drop-in for `<span className="src …" title={detail}>label</span>`:
 *   <Cite className="src …" detail={detail}>label</Cite>
 */
export default function Cite({ children, detail, className = 'src' }) {
  if (!detail) return <span className={className}>{children}</span>
  return <CitePopover className={className} detail={detail}>{children}</CitePopover>
}

function CitePopover({ children, detail, className }) {
  const [open, setOpen] = useState(false)
  const [pos, setPos] = useState(null)
  const btnRef = useRef(null)
  const popRef = useRef(null)
  const id = useId()

  // Position under the chip (viewport-fixed so a scrollable table never clips
  // it), clamped to the viewport, flipping above the chip when near the bottom.
  useLayoutEffect(() => {
    if (!open) return
    const b = btnRef.current?.getBoundingClientRect()
    const ph = popRef.current?.offsetHeight || 0
    if (!b) return
    const W = Math.min(280, window.innerWidth - 16)
    const left = Math.max(8, Math.min(b.left, window.innerWidth - W - 8))
    const below = b.bottom + 6
    const flip = below + ph > window.innerHeight - 8 && b.top - ph - 6 > 8
    setPos({ left, top: flip ? b.top - ph - 6 : below, width: W })
  }, [open])

  useEffect(() => {
    if (!open) return
    const onKey = (e) => { if (e.key === 'Escape') { setOpen(false); btnRef.current?.focus() } }
    const onOutside = (e) => {
      if (!popRef.current?.contains(e.target) && !btnRef.current?.contains(e.target)) setOpen(false)
    }
    const onReflow = () => setOpen(false)   // don't try to keep a fixed popover glued while scrolling
    window.addEventListener('keydown', onKey)
    document.addEventListener('pointerdown', onOutside)
    window.addEventListener('scroll', onReflow, true)
    window.addEventListener('resize', onReflow)
    return () => {
      window.removeEventListener('keydown', onKey)
      document.removeEventListener('pointerdown', onOutside)
      window.removeEventListener('scroll', onReflow, true)
      window.removeEventListener('resize', onReflow)
    }
  }, [open])

  return (
    <>
      <button
        ref={btnRef}
        type="button"
        className={`${className} cite-btn${open ? ' open' : ''}`}
        aria-expanded={open}
        aria-controls={open ? id : undefined}
        aria-describedby={open ? id : undefined}
        onClick={() => setOpen((o) => !o)}
      >
        {children}
      </button>
      {open && createPortal(
        // A <span> (phrasing content) so it is valid even when a <p> is its
        // JSX-tree ancestor; CSS makes it a fixed-position block. Portaled to
        // body so a transformed/scrolling ancestor can't clip it.
        <span
          ref={popRef}
          id={id}
          role="note"
          className="cite-pop"
          style={pos ? { left: pos.left, top: pos.top, width: pos.width } : { visibility: 'hidden' }}
        >
          {detail}
        </span>,
        document.body,
      )}
    </>
  )
}
