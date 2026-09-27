# 03 — Design System

## What we took from robertaspizza.com
These values were pulled from the reference site's live CSS in September 2026 and then adapted.

| Reference element | Roberta's value | Quadrozzi adaptation |
|---|---|---|
| Display headline | "Offset TM", uppercase, h1 7.5rem, line-height .875 | **Big Shoulders Display** 800, uppercase, `clamp(3.4rem, 11vw, 9rem)`, line-height .86 |
| Serif voice | "Borensa" | **Cormorant Garamond** italic for ledes and pull quotes |
| Palette | Smoke `#2b2f36`, greys `#111`–`#eee`, **one** accent `#ed2023` | Asphalt `#161616`, concrete `#f3f1ec`, fleet orange `#e8741e` and drum yellow `#f6d31c` (see below) |
| Section dividers | top/bottom "divisor" bands | Hazard-stripe bands framing a scrolling marquee of venture names |
| Ornaments | Star icons and illustrated mascots beside titles | Hazard-stripe chips and bands taken from the truck bumpers. **No mascots.** |
| Title reveal | Cascading line-by-line reveal | Kept. Lines slide up with an 80ms stagger. Turned off under `prefers-reduced-motion` |
| Buttons | 999rem pills in groups of 2–3 | The same pill shape: solid orange with black text, or outline ivory |
| Split sections | Large image beside a smaller offset image | Heritage section: large photo plus a small overlapping photo |
| Preloader | Word-sequence preloader | **Dropped**, because it adds friction on a corporate site |

## Brand colors — the Quadrozzi fleet
The palette was re-based (Sep 2026) on the company's concrete-mixer trucks: **orange cabs**, **yellow drums**,
**black "Quadrozzi" lettering** and **yellow/black hazard-striped bumpers**. The robertaspizza.com *structure*
(huge condensed headlines, dividers, marquee, pills) stays; the fleet supplies the color.

```css
--smoke:      #161616;  /* asphalt black — dark sections, text on light */
--smoke-deep: #0c0c0c;  /* marquee + footer */
--ivory:      #f3f1ec;  /* poured-concrete white — page background */
--orange:     #e8741e;  /* truck cab orange — buttons (black text), rules, hovers */
--orange-ink: #a84b09;  /* orange for small text on light backgrounds */
--yellow:     #f6d31c;  /* mixer-drum yellow — accents on dark */
--hazard:     repeating-linear-gradient(-45deg, yellow 0 14px, black 14px 28px);
```
Contrast rules: orange buttons use **black** text (about 7:1); white on orange fails AA. Yellow is only used on
black. On ivory, small orange text uses `--orange-ink` (about 5:1).

**Brand motifs:**
- The **hazard stripe** replaces the ✦ ornament. It appears as a chip before eyebrows, as bands above and below the marquee, on the top edge of the footer, and in the logo mark.
- **Wordmark:** "Quadrozzi" in Archivo 800, mixed case, echoing the black lettering on the trucks, next to a rounded hazard-stripe tile with an orange keyline.

## Type scale
| Role | Font | Size | Notes |
|---|---|---|---|
| Hero h1 | Big Shoulders Display 800 | clamp(3.4rem, 11vw, 9rem) | uppercase, lh .86, tracking -0.01em |
| Section h2 | Big Shoulders Display 800 | clamp(2.6rem, 6.5vw, 5.5rem) | uppercase, lh .9 |
| Card h3 | Big Shoulders Display 700 | clamp(1.8rem, 3vw, 2.4rem) | uppercase |
| Eyebrow | Inter 600 | .75rem | uppercase, tracking .18em, brass/oxblood |
| Lede / quote | Cormorant Garamond 500 italic | clamp(1.35rem, 2.4vw, 1.85rem) | lh 1.3 |
| Body | Inter 400 | 1rem–1.0625rem | lh 1.65 |

## Layout
- Container: `min(1240px, 100% - 32px)`, which gives a 16px gutter on phones.
- Section padding: `clamp(4.5rem, 10vw, 8rem)` top and bottom.
- Grid: holdings cards use `repeat(auto-fit, minmax(280px, 1fr))`, and the first card spans 2 columns on wide screens.
- Radii: 0 on images and cards (sharp, architectural), 999px on buttons only.

## Components
- **Holding card**: image slot (4:3), eyebrow category, h3 title, one-line description, and a "Visit site ↗" link. On hover the image scales to 1.03 and the arrow nudges. The whole card is clickable.
- **Marquee band**: venture names separated by ✦ on a smoke background, looping at 40s per cycle and paused under reduced motion.
- **Stat tile**: big condensed number, brass hairline, small caption.
- **Pull quote**: Cormorant italic with a large brass opening quote mark.

## Imagery direction
Documentary black-and-white or muted color: harbor, grain silos, the terminal at dusk, horses in
Prospect Park, and hands-on community moments. Every image slot has a gradient placeholder until real photos arrive.
