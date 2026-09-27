# 03 — Design System

## What we took from robertaspizza.com
These values were pulled from the reference site's live CSS in September 2026 and then adapted.

| Reference element | Roberta's value | Quadrozzi adaptation |
|---|---|---|
| Display headline | "Offset TM", uppercase, h1 7.5rem, line-height .875 | **Big Shoulders Display** 800, uppercase, `clamp(3.4rem, 11vw, 9rem)`, line-height .86 |
| Serif voice | "Borensa" | **Cormorant Garamond** italic for ledes and pull quotes |
| Palette | Smoke `#2b2f36`, greys `#111`–`#eee`, **one** accent `#ed2023` | Smoke `#1c1f23`, ivory `#f5f1ea`, **one** accent oxblood `#7a1f1f`, brass `#b08d57` for ornaments |
| Section dividers | top/bottom "divisor" bands | 1px brass rule plus a scrolling marquee band of venture names |
| Ornaments | Star icons and illustrated mascots beside titles | A small brass 4-point star (✦) beside eyebrows. **No mascots.** |
| Title reveal | Cascading line-by-line reveal | Kept. Lines slide up with an 80ms stagger. Turned off under `prefers-reduced-motion` |
| Buttons | 999rem pills in groups of 2–3 | The same pill shape: solid oxblood, or outline ivory/smoke |
| Split sections | Large image beside a smaller offset image | Heritage section: large photo plus a small overlapping photo |
| Preloader | Word-sequence preloader | **Dropped**, because it adds friction on a corporate site |

## Tokens
```css
--smoke:   #1c1f23;  /* primary dark surface, text on light */
--smoke-2: #2b2f36;  /* raised dark surface (from reference) */
--ivory:   #f5f1ea;  /* page background */
--paper:   #ffffff;  /* cards */
--oxblood: #7a1f1f;  /* single accent: CTAs, active states */
--brass:   #b08d57;  /* rules, ornaments, eyebrows on dark */
--stone:   #6b6660;  /* secondary text on light (AA on ivory) */
--line:    #d9d2c6;  /* hairlines on light */
```
Contrast: ivory on smoke is about 15:1, smoke on ivory about 15:1, ivory on oxblood about 9:1, and stone on ivory about 5.2:1. All pass AA.

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
