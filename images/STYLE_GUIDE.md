# Visual Style Guide — Python Browser Automation Cookbook

> One visual system. 11 assets. One premium brand.

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#050B1A` | Base dark canvas |
| Surface | `#0B1630` | Card/panel backgrounds |
| Surface light | `#111827` | Secondary surfaces |
| Cyan primary | `#22D3EE` | Primary highlights, interactive elements |
| Cyan mild | `#0891B2` | Secondary cyan |
| Amber accent | `#FBBF24` | Warnings, special states |
| Amber dim | `#D97706` | Secondary amber |
| Green success | `#34D399` | Success/completion paths |
| Red stop | `#EF4444` | Error/stop/termination |
| Slate text | `#94A3B8` | Secondary text/accents |
| Indigo gradient | `#050B1A` → `#1E0A3C` | Hero backgrounds |

## Lighting Rules

- **Volumetric:** Soft glow behind primary elements (cyan or amber)
- **Edge lighting:** Thin luminous strokes on glass surfaces (1-2px, cyan)
- **Directional:** Light source from top-left, subtle shadow bottom-right
- **No harsh:** Avoid flat fills, avoid hard drop shadows

## Geometry Rules

- **Prefer:** Circles, rounded rects (rx=8), thin lines
- **Avoid:** Sharp corners, irregular polygons, organic blobs
- **Grid System:** 40px base spacing unit
- **Connections:** 90° and 45° angles only for paths/arrows

## Composition Rules

- **Negative space:** Minimum 20% empty canvas per image
- **Focal point:** Single primary visual element per image
- **Hierarchy:** Size = importance. Largest element is most important
- **Balance:** Symmetrical for stable concepts, asymmetrical for dynamic ones

## Typography (Not in Images)

- **Font:** JetBrains Mono for captions and UI
- **Headings:** Inter or SF Pro for chapter titles
- **Size:** 12-24px for doc text, 24-48px for display

## Never Use

- ❌ People or hands
- ❌ Robots or humanoid figures
- ❌ Sci-fi tropes (flying cars, lasers, neon grids)
- ❌ Generic AI art style (oversharp, plastic, noise artifacts)
- ❌ Photographs or photo-real textures
- ❌ More than 3 colors in any single image
- ❌ Text characters in images
- ❌ Logos or brand marks
- ❌ Gears, circuits, hexagons (overused)
- ❌ Gradients spanning more than 2 color stops

## Material Quality

In order of preference:

1. Glassmorphism — translucent with backdrop blur and thin glow edges
2. Polished metal — subtle linear gradients with sharp reflections
3. Crystal — hard faceted geometry with internal light refraction
4. Solid — flat minimal shapes with only edge lighting (last resort)

## PNG Export Settings

- **Resolution:** 2048x1152 (16:9)
- **Format:** PNG (lossless)
- **Style Preset:** digital-art (Stability AI)
- **CFG Scale:** 7 (balance of adherence and creativity)

## Assets Inventory

| # | File | Type | Recipe | ChatGPT Prompt Version |
|---|------|------|--------|-----------------------|
| 1 | hero.png | SD3 | Cover | v2 |
| 2 | selector_hierarchy.png | SD3 | 13 | v2 |
| 3 | stop_vs_retry_flow.png | SD3 | 29 | v2 |
| 4 | pagination_safety.png | SD3 | 24 | v2 |
| 5 | download_lifecycle.png | SD3 | 26 | v2 |
| 6 | cookbook_mermaid.html | Mermaid | All | v2 |
| 7 | architecture.html | SVG | README | v2 |

## Prompt Template

```
[Global Style Prefix from PROMPTS.md]

[Image-specific description]

No text, no labels, no letters, no numbers, no robots.
16:9.
```
