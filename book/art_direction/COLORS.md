# Color Palette Reference

## Primary Backgrounds

| Name | Hex | Preview |
|------|-----|---------|
| Deep Navy | `#0A0E1A` | ███ Deepest background, full-canvas |
| Graphite | `#141820` | ███ Secondary panels, cards |
| Charcoal | `#1E2230` | ███ Tertiary containers, inner panels |
| Pure Black | `#000000` | ███ Full-bleed hero sections |

## Accent Colors

| Name | Hex | Preview | Usage |
|------|-----|---------|-------|
| Electric Cyan | `#00D4FF` | ███ Primary accent, data flow, active state, brand signature |
| Azure Blue | `#0080FF` | ███ Secondary accent, connections, links |
| Purple | `#7C3AED` | ███ Tertiary accent, highlight elements |

## Semantic Colors

| Name | Hex | Preview | Usage |
|------|-----|---------|-------|
| Emerald | `#10B981` | ███ Success, validation passes, healthy |
| Amber | `#F59E0B` | ███ Warnings, degraded, attention needed |
| Red | `#EF4444` | ███ Failures, errors, crashes, blocked |

## Neutral / Structural

| Name | Hex | Preview | Usage |
|------|-----|---------|-------|
| Slate Gray | `#6B7280` | ███ Muted elements, grid lines, secondary text equivalents |
| White (glass) | `#FFFFFF` | At 5-10% opacity for glass surfaces |
| White (edge) | `#FFFFFF` | At 30% opacity for thin borders (0.5px) |

## Gradient Specifications

All gradients: 135° angle (top-left to bottom-right).

### Primary Glow
- Start: `#0A0E1A` (Deep Navy)
- End: `#00D4FF` (Electric Cyan) at 15% opacity
- Radius: Large (200-400px)
- Use: Behind main subject in hero images

### Panel Background
- Start: `#141820` (Graphite)
- End: `#1E2230` (Charcoal)
- Use: Card and panel backgrounds

### Error State
- Start: `#0A0E1A` (Deep Navy)
- End: `#EF4444` (Red) at 10% opacity
- Use: Failure visualizations, error states

### Success State
- Start: `#0A0E1A` (Deep Navy)
- End: `#10B981` (Emerald) at 10% opacity
- Use: Validation visualizations, healthy states

## Color Application Rules

1. Backgrounds are always dark (Deep Navy, Graphite, or Pure Black) — never light
2. Cyan is the primary accent — every image must contain at least one cyan element
3. Red and Emerald are used ONLY for semantic states (failure/success) — never as decorative colors
4. Purple is reserved for special/highlight elements — use sparingly (once per image max)
5. Glass white is never used at full opacity — always 5-10% with backdrop blur
6. Never use saturated rainbows or full-spectrum gradients
7. Never use bright colors on dark backgrounds without an opacity buffer (at least 10% opacity)
