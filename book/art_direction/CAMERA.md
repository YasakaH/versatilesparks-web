# Camera and Perspective Guide

## Camera Setup

| Setting | Value |
|---------|-------|
| Focal length | 50mm equivalent (hero), 35mm (architecture) |
| Aperture | f/2.8 (hero — shallow depth of field), f/8 (architecture — everything in focus) |
| Aspect ratio | 16:9 |
| Resolution | 7680 × 4320 |

## Perspective Options

### Isometric (30°)

```text
    ______
   /      /|
  /      / |
 /______/  |
 |      |  /
 |      | /
 |______|/
```

**Used for:** System architecture, infrastructure diagrams, layered deployments, the Deployment Ladder, Starter Kit exploded view, CDP layer diagram.

**Camera angle:** 30° elevation, 45° rotation.

**Characteristics:** All three axes visible, equal scaling on each axis, no perspective distortion.

---

### Straight-On (0°)

```
┌─────────────────────┐
│                     │
│    Main Subject     │
│                     │
└─────────────────────┘
```

**Used for:** Process flows, timelines, comparison views, data pipelines, state machines, the Navigation State Machine, Trust Pyramid, data flow diagrams.

**Camera angle:** Directly facing the subject, 0° elevation.

**Characteristics:** No perspective distortion, clear left-to-right or top-to-bottom reading order, good for sequential information.

---

### Exploded View

```
      ╱ ╲
     ╱   ╲    ← separated components
    ╱  .  ╲
   ╱     . ╲
  ╱        .╲
 ╱__________.╲
```

**Used for:** Component anatomy, Chrome process cutaway, DOM layer visualization, internal structure reveals.

**Camera angle:** 15-20° elevation, with components separated along their natural axis.

**Characteristics:** Components float apart along a single axis (usually vertical), with dashed or glowing connection lines showing how they assemble.

---

## Per-Image Camera Rules

1. Every image uses exactly one perspective — never mix
2. Hero images (Type A) use 50mm at f/2.8 for subject isolation
3. Architecture images (Type B) use 35mm at f/8 for maximum depth of field
4. Exploded views use consistent separation distance between layers
5. Process flows (Type C) are always straight-on for readability
