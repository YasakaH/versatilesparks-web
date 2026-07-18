# Visual Design System v1.0 — Python Browser Automation Cookbook

This document is the constitution for every image in the book. Every generated image, diagram, and visualization must conform to the rules defined here. If a conflict arises between this document and any other image reference, this document wins.

## Philosophy

These are **engineering visualizations**, not illustrations.

Every image should make the reader think: "I understand this architecture in 10 seconds."

Not: "Nice picture."

## Design Inspirations (Frozen)

| Source | Borrow |
|--------|--------|
| Apple WWDC engineering visuals | Exploded views, process transparency, product photography lighting |
| Stripe engineering blog | Technical precision, diagrammatic clarity, restrained color |
| Linear documentation | Minimalist depth, dark-mode-first, subtle glow accents |
| Palantir Foundry UI | Data pipeline visualization, layered architecture, enterprise dashboard aesthetic |
| Vercel architecture pages | Isometric system diagrams, connected component views |
| Cloudflare Radar | Network flow visualization, pentestrike patterns, heat maps |
| NVIDIA technical presentations | GPU architecture cutaways, layered chip-die aesthetics |
| IBM Systems diagrams | Engineering blueprint precision, structural callouts |
| Raycast visual language | Glassmorphism, soft blur, matte surfaces, thin borders |

**Prohibited:** Stock illustrations, flat icons, cartoon browsers, clipart, generic isometric offices, programmer-at-laptop images, any image that looks like a stock photo.

## Canvas Specifications

| Property | Value |
|----------|-------|
| Resolution | 7680 × 4320 (8K) |
| Aspect ratio | 16:9 landscape |
| Format | PNG (lossless) or WebP (for web) |
| Orientation | Landscape only — never portrait or square |

Master resolution is always 8K. Scale down for export formats. Never upscale.

## Color Palette

### Backgrounds

| Name | Hex | Usage |
|------|-----|-------|
| Deep Navy | `#0A0E1A` | Primary background |
| Graphite | `#141820` | Secondary background, panels |
| Charcoal | `#1E2230` | Tertiary background, containers |
| Pure Black | `#000000` | Full-bleed backgrounds, hero sections |

### Content and Structure

| Name | Hex | Usage |
|------|-----|-------|
| Electric Cyan | `#00D4FF` | Primary accent, data flow, active state |
| Azure Blue | `#0080FF` | Secondary accent, connections, links |
| Purple | `#7C3AED` | Tertiary accent, highlight, special elements |
| Slate Gray | `#6B7280` | Secondary text, muted elements, grid lines |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| Emerald | `#10B981` | Success, validation passed, healthy |
| Amber | `#F59E0B` | Warnings, degraded state, attention needed |
| Red | `#EF4444` | Failures, errors, crashes, blocked |
| Electric Cyan | `#00D4FF` | Info, active processes, data flow |

### Material Surfaces

| Surface | Hex | Opacity | Effect |
|---------|-----|---------|--------|
| Glass | `#FFFFFF` | 5-10% | Backdrop blur 20px |
| Aluminum | `#2A2F3E` | 100% | Brushed vertical grain |
| Carbon fiber | `#1A1D2A` | 100% | Diagonal weave 45° |
| Matte acrylic | `#1E2230` | 100% | Soft shadow, 2px rounded corners |

### Gradient Specifications

All gradients use the same direction: 135° (top-left to bottom-right).

- **Primary glow:** Deep Navy → Electric Cyan (low opacity, large radius)
- **Panel background:** Graphite → Charcoal (subtle)
- **Error state:** Deep Navy → Red (low opacity, for failure visualizations)
- **Success state:** Deep Navy → Emerald (low opacity, for validation visualizations)

## Lighting

- **Type:** Professional studio softbox lighting
- **Quality:** Soft volumetric glow, not harsh directional light
- **Bloom:** Subtle, only on accent elements (cyan edges, active nodes)
- **Ambient:** Dark-mode-first environment with ambient reflections on surfaces
- **Shadows:** Soft, diffuse, never harsh. Shadow opacity: 30-40%.
- **Key light:** 45° above, slightly camera-right
- **Fill light:** 30% intensity, camera-left, to reduce contrast ratio
- **Edge light:** Thin rim light on foreground objects (cyan tint, 2px width)

**Prohibited:** Harsh shadows, multi-directional lighting, strong backlight that obscures details, lens flare effects.

## Materials

Every object in every image uses one of these materials:

| Material | Properties | Used For |
|----------|------------|----------|
| Glass | 5-10% opacity, backdrop blur, thin white border (0.5px, 30% opacity) | Containers, panels, overlays |
| Brushed aluminum | Vertical grain, 20% reflectivity, `#2A2F3E` base | Hardware nodes, server representations, physical objects |
| Carbon fiber | Diagonal weave pattern, `#1A1D2A` base | High-performance components, browser internals |
| Matte polymer | Soft shadow, 2px rounded corners, `#1E2230` base | UI elements, cards, buttons |
| Soft acrylic | Frosted finish, 10% opacity overlay with blur | Background panels, section dividers |
| Neon edge | 1-2px thin line, Electric Cyan or Azure Blue, subtle glow | Connections, data flow lines, active paths |

Never use: plastic sheen, glossy reflections, cartoon-like materials, or untextured flat colors.

## Typography

**No text in any image.**

All labels are handled by the book layout. Images contain only symbols, icons, and visual elements. The one exception is extremely short labels (3-5 characters) that serve as structural anchors, and even those should be avoided when possible.

## Perspective

Images use one of three perspectives:

| Perspective | Usage |
|-------------|-------|
| Isometric (30°) | System architecture, layered diagrams, infrastructure views |
| Straight-on (0°) | Process flows, timelines, comparison views, data pipelines |
| Exploded view | Component anatomy, internal structure, hardware cutaways |

Never use random or mixed perspectives within the same image.

## Composition Rules

1. **Rule of thirds** for hero images. The main subject should occupy the intersection of the upper-left or lower-right third.
2. **Negative space** — at least 20% of every image should be empty/dark to maintain visual breathing room.
3. **Depth layers** — every image should have at least 3 depth layers: foreground (main subject), midground (supporting elements), background (environment/atmosphere).
4. **Flow direction** — data and processes should flow left-to-right or top-to-bottom, following reading direction.
5. **Symmetry** — architectural diagrams should be symmetric when possible. Asymmetric only when showing imbalance or failure states.

## Complexity Level

High. Every image should have:
- Multiple transparent layers
- Visible depth through overlapping elements
- Micro-details on closer inspection
- Consistent parallax-like separation between layers

An image should reward zooming in. But the core message must be readable at thumbnail size.

## Visual Language Consistency Rules

Every image across the entire book must share:

- Same lighting setup (softbox, 45° key light)
- Same material library (glass, aluminum, carbon, matte)
- Same color palette (navy base, cyan accent)
- Same camera (equivalent of 50mm at f/2.8 for hero shots, wider for architecture)
- Same depth treatment (3+ layers, foreground/midground/background)
- Same rendering engine feel (CGI photorealism, not illustration)

A reader should instantly recognize any image as belonging to this book.

## Image Type Categories

| Type | Purpose | Count per chapter | Example |
|------|---------|-------------------|---------|
| A — Hero Concept | Single defining visual for the chapter | 1 | Browser lifecycle exploded view |
| B — Architecture | Layered system diagram | 1-2 | CDP event flow, deployment ladder |
| C — Process Flow | Sequential or pipeline visualization | 1-2 | Data extraction pipeline, auth flow |
| D — Failure Visualization | Error states, recovery, diagnostics | 1 | Browser crash, circuit breaker open |
| E — Comparison | Split-view good vs bad | 0-1 | Reliable vs fragile, valid vs invalid |
| F — Internal Anatomy | Cutaway or exploded view | 0-1 | Chrome process anatomy, DOM layers |

Minimum: 3 images per chapter (A + B + C). Maximum: 6 per chapter.

## Chapter-by-Chapter Image Plan

| Chapter | Hero (A) | Architecture (B) | Process (C) | Failure (D) | Comparison (E) | Anatomy (F) |
|---------|----------|------------------|-------------|-------------|----------------|-------------|
| Mindset | Automation ecosystem | — | — | — | Script vs System | — |
| Ch 1 | Browser lifecycle | Chrome process tree | Launch timeline | Orphaned Chrome | — | Chrome anatomy |
| Ch 2 | Page readiness phases | — | Navigation state machine | Empty report | — | — |
| Ch 3 | Reliability layers | Recovery architecture | Retry flow | 18 Chrome processes | Before/after logging | — |
| Ch 4 | DOM evolution | Selector hierarchy | Click validation | Structural selector break | — | Shadow DOM cutaway |
| Ch 5 | Identity graph | Auth stack | MFA checkpoint flow | 400-account cascade | — | — |
| Ch 6 | Data pipeline | — | Extraction → Validation → Store | ₹0 price failure | — | — |
| Ch 7 | Detection layers | — | Challenge response flow | CAPTCHA encounter | — | — |
| Ch 8 | Starter Kit exploded | Common/ dependency graph | New project setup flow | — | — | — |
| Ch 9 | CDP event streaming | CDP layer diagram | Event → Queue → Worker | Event queue overflow | — | — |
| Ch 10 | Environment divergence | — | Drift timeline | Four diverging workstations | Same script, different env | — |
| Ch 11 | DOM layers (3D) | Interaction pyramid | Canvas → Shadow → iframe flow | Invisible button | — | Virtual DOM cutaway |
| Ch 12 | Deployment ladder | Production system architecture | Full automation lifecycle | Exit code 0 with empty data | — | — |
| Ch 13 | Trust pyramid | Data lineage flow | Validation pipeline | ₹0 cascading through systems | Valid vs quarantined | — |
| Ch 14 | Full platform architecture | All five capstone architectures | — | — | — | — |
| Ops Guide | NOC dashboard | — | Incident response timeline | Alert cascade | — | — |

## Brand Signature

Every image carries a subtle visual signature:
- Thin cyan border (0.5px) on the bottom edge of the canvas
- Very subtle dark vignette (5% opacity falloff at corners)
- Consistent 2px corner radius on all rectangular elements

This is the equivalent of a brand mark. Readers will not notice it consciously, but they will recognize images that lack it as "not from this book."

## Quality Gate

Before any image is accepted into the book:

- [ ] Resolution is exactly 7680×4320
- [ ] Background is Deep Navy, Graphite, or Pure Black
- [ ] Lighting is soft volumetric (not harsh)
- [ ] At least 3 depth layers present
- [ ] No text (0 characters embedded in image)
- [ ] Color palette is restricted to the palette above
- [ ] Materials are from the approved library
- [ ] Perspective is consistent within the image
- [ ] Cyan accent is present somewhere (brand signature)
- [ ] Image communicates its concept in under 10 seconds at thumbnail size
- [ ] Image rewards zooming in with micro-details
- [ ] Bottom edge has the 0.5px cyan signature line
