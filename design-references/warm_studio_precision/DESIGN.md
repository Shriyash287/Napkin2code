---
name: Warm Studio Precision
colors:
  surface: '#faf9fb'
  surface-dim: '#dbd9dc'
  surface-bright: '#faf9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f5'
  surface-container: '#efedf0'
  surface-container-high: '#e9e8ea'
  surface-container-highest: '#e3e2e4'
  on-surface: '#1b1c1e'
  on-surface-variant: '#464555'
  inverse-surface: '#2f3032'
  inverse-on-surface: '#f2f0f3'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#4e45d5'
  on-secondary: '#ffffff'
  secondary-container: '#6860ef'
  on-secondary-container: '#fffbff'
  tertiary: '#434853'
  on-tertiary: '#ffffff'
  tertiary-container: '#5b606b'
  on-tertiary-container: '#d7dbe8'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#e3dfff'
  secondary-fixed-dim: '#c3c0ff'
  on-secondary-fixed: '#100069'
  on-secondary-fixed-variant: '#372abf'
  tertiary-fixed: '#dee2ef'
  tertiary-fixed-dim: '#c2c6d3'
  on-tertiary-fixed: '#171c25'
  on-tertiary-fixed-variant: '#424751'
  background: '#faf9fb'
  on-background: '#1b1c1e'
  surface-variant: '#e3e2e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.025em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 26px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 21px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0em
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-md: 1.5rem
  gutter-lg: 2rem
  margin: 1.25rem
  margin-md: 2rem
  margin-lg: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system embodies a calm, warm-minimalist aesthetic tailored for creative developers, system architects, and technical product designers. It fuses the quiet tactile warmth of drafting paper and sketchbooks with the exactness of a high-performance local AI code workbench. 

The emotional signature is focused, private, and effortless: zero telemetry anxiety, zero visual noise, and no aggressive futurism or tacky neon glows. Instead, visual weight is distributed through balanced proportion, soft architectural surfaces, diffused ambient light, and restrained glassmorphic layering. The interface stays transparent to the creative cycle—allowing physical ink sketches to organically translate into structured, production-ready code interfaces.

## Colors

The palette draws inspiration from Japanese paper stock, fine-tip pigment liners, and muted compile-state indicators.

- **Canvas & Backgrounds**: The base canvas is anchored in `#FBFBFA` with secondary workspace canvas at `#F7F7F5`.
- **Surfaces & Containers**: Elevated panels and canvas overlays leverage `#FFFFFF` at `80%` to `90%` opacity, layered alongside subtle container fills of `#F0F0EC`.
- **Borders & Dividers**: Precision hairline borders use `#E5E5DF` or `#E2E2DC` at `80%` opacity to define boundaries without harsh contrast.
- **Typography & Neutral Hierarchy**:
  - Primary text: Deep charcoal `#1C1D1F` for supreme optical contrast without the stark harshness of pure black.
  - Secondary text: Slate charcoal `#383A40` for structural metadata, secondary labels, and active subtext.
  - Muted text: Neutral pencil `#6C6F78` for placeholders, disabled values, and hotkey helpers.
- **Accent & Interaction**:
  - Primary Action / Focus: Restrained Indigo `#4F46E5` for affirmative generation states, focal callouts, and clean outline rings.
  - Interactive Hover / Pressed: Deep Indigo `#4338CA`.
  - Wash / Selection Tint: Frosted Indigo wash `#EEF2FF` for active selection bounds, code selection highlights, and subtle pill fills.
- **System Feedback**: Functional semantics respect the muted palette (Success: `#15803D` / Warning: `#B45309` / Error: `#B91C1C`), avoiding hyper-saturated alarm states.

## Typography

The type system creates a deliberate rhythm between clean neutral human-centric interfaces (`Inter`) and precise, technical tokenized execution (`JetBrains Mono`). 

- **Headlines & Interface Text**: Set in `Inter` with tight, optical kerning and measured line-heights. Titles use medium-to-semibold weights to maintain presence against open white space without shouting.
- **Code, Stream Tokens & Metadata**: Set in `JetBrains Mono`. Monospace is not reserved solely for full code editor blocks; it designates Ollama generation state, model parameters (e.g., `qwen2.5-coder:7b`, latency meters, token counters), JSON payloads, and tactile keyboard accelerator pills.
- Optical sizing rules maintain a minimum of 13px for interactive subtext and code snippets to preserve legibility under frosted glass backdrops.

## Layout & Spacing

The layout philosophy uses a flexible multi-pane drafting board balanced by a consistent 4px/8px structural increment.

- **Drafting Canvas Structure**:
  - **Desktop (>= 1280px)**: Three-panel split layout featuring a collapsible tool palette (260px fixed), a central infinite/pan sketch-to-preview canvas (fluid), and an inspect/code dock (380px fixed). Content uses `margin-lg` (48px) and `gutter-lg` (32px).
  - **Tablet (768px - 1279px)**: Split viewport balancing visual input and generated output via a side-by-side or stacked tab configuration. Margin scales to `margin-md` (32px) with `gutter-md` (24px).
  - **Mobile (< 768px)**: Single-column linear flow prioritizing the sketch intake (camera/upload) and mobile preview dock. Canvas margin adapts to `margin` (20px) with `gutter` (16px).
- **Internal Density**: Micro-controls and metadata pills rely on `space-xs` (4px) and `space-sm` (8px). Structural cards and generation panels standardize on `space-lg` (24px) padding to ensure sketches and live previews have sufficient breathing room.

## Elevation & Depth

Visual depth is achieved through translucent material surfaces, fine hairline boundary definitions, and hyper-diffused ambient drop shadows. Laser-sharp edge lines ground the frosted surfaces without relying on heavy borders or skeuomorphic bevels.

- **Level 0 (Base Board)**: Flat surface `#FBFBFA` with an optional subtle sub-pixel grid (`#1C1D1F` at 2% opacity, 24px grid spacing) for canvas drafting.
- **Level 1 (Card & Sub-Panel Layer)**: Opaque or 90% alpha surface (`#FFFFFF`), bounded by a 1px solid border (`#E5E5DF`), cast with shadow: `0 1px 3px rgba(28, 29, 31, 0.04), 0 4px 12px rgba(28, 29, 31, 0.02)`.
- **Level 2 (Frosted Floating Toolbars & Header Navigation)**: Translucent glass (`rgba(255, 255, 255, 0.80)`) with `backdrop-filter: blur(12px) saturate(160%)`, 1px boundary (`rgba(226, 226, 220, 0.85)`), cast with shadow: `0 4px 20px -2px rgba(28, 29, 31, 0.06), 0 2px 6px -1px rgba(28, 29, 31, 0.03)`.
- **Level 3 (Modal Sheets & Model Settings Docks)**: Translucent elevated glass (`rgba(255, 255, 255, 0.92)`), backdrop blur 16px, 1px border (`#E2E2DC`), cast with shadow: `0 12px 32px -4px rgba(28, 29, 31, 0.08), 0 4px 12px -2px rgba(28, 29, 31, 0.04)`.
- **Focus Elevation**: Interactive items never emit intense neon glows. Active focus produces a clean, sharp offset ring: `box-shadow: 0 0 0 2px #FBFBFA, 0 0 0 4px #4F46E5`.

## Shapes

The geometric architecture balances generous, organic containers with ergonomic, compact internal controls.

- **Primary Canvas & Structural Cards**: Scaled with `rounded-xl` (16px to 20px) to echo sketchbook pages and drafting tablets.
- **Interactive Controls (Buttons, Inputs, Selectors)**: Scaled with `rounded` (8px to 10px), offering clean tap targets and tactile structure.
- **Micro Tokens & Tags (Pills, Hotkeys, Model Status Badges)**: Fully rounded capsules (`9999px`) or compact `rounded-sm` (4px) to retain distinct semantic differentiation from functional inputs.

## Components

### Buttons
- **Primary**: Solid Indigo (`#4F46E5`), text `#FFFFFF`, rounded 8px. Hover shifts to `#4338CA`. Subtle inward bevel or hairline top ring `inset 0 1px 0 rgba(255, 255, 255, 0.2)`. 
- **Secondary (Frosted Neutral)**: Translucent `#FFFFFF` (80% alpha) with `backdrop-blur-md`, text `#1C1D1F`, 1px border `#E5E5DF`. Hover background `#F0F0EC`.
- **Ghost / Tool**: Transparent background, text `#383A40`, rounded 8px. Hover background `#F0F0EC` at 70% opacity.
- **Focus Style**: A 2px high-contrast ring in Indigo (`#4F46E5`) separated by a 2px off-white gap.

### Input Fields & Prompt Inputs
- **Base Style**: Background `#FFFFFF` with 80% opacity, 1px border `#E5E5DF`, rounded 8px, padding `0.625rem 0.875rem`. Text `#1C1D1F`, placeholder `#6C6F78`.
- **Active / Focused**: Border transitions cleanly to `#4F46E5` accompanied by an indigo halo (`box-shadow: 0 0 0 3px #EEF2FF`).
- **Monospace Code Inputs**: Typography sets to `JetBrains Mono` 13px with subtle line numbering gutter in `#6C6F78`.

### Cards & Panels
- **Sketch Ingestion Dropzone**: Minimum height 320px, rounded 16px, dual-state border: default 1px dashed `#E2E2DC`, drag-over solid 1.5px `#4F46E5` with `#EEF2FF` backdrop wash.
- **Code Preview Panel**: Translucent panel (`#FFFFFF/90`), 1px border `#E5E5DF`, rounded 16px. Top header bar integrates tab switchers (Preview, React, HTML/Tailwind) and streaming status badges.

### Badges, Status Chips & Model Indicators
- **Local Model Status**: Pill capsule (`rounded-full`), padding `2px 8px`. Typography `JetBrains Mono` 11px. 
  - Connected / Ready: Background `#F0FDF4`, border `#DCFCE7`, text `#15803D`, accompanied by a solid 6px indicator dot.
  - Generating / Ollama Streaming: Background `#EEF2FF`, border `#E0E7FF`, text `#4338CA`.
- **Keyboard Shortcuts (Kbd)**: Bordered micro-tiles with background `#F7F7F5`, border `#E5E5DF`, border-bottom 2px solid `#D4D4CE`, text `#383A40`, font size 10px, rounded 4px.

### Checkboxes, Radio & Toggle Switches
- **Checkbox / Radio**: 16px square/circle, 1px border `#D4D4CE`, background `#FFFFFF`. Selected state fills with `#4F46E5` displaying a crisp white 1.5px stroke checkmark.
- **Toggle Switch**: Track width 36px, height 20px, rounded 9999px. Background `#E5E5DF`, shifting to `#4F46E5` when active. Thumb is crisp white `#FFFFFF` with `0 1px 3px rgba(0,0,0,0.15)` elevation.

### Lists & Code Tree Navigators
- **Tree Items**: Height 32px, rounded 6px, horizontal padding `space-sm` (8px). Inactive items `#383A40`. Hover item `#F0F0EC`. Selected item `#EEF2FF` text `#4338CA` font weight 500.

### Additional Specialty Component: Sketch Inspection Loupe
- Floating viewport loupe over the uploaded napkin sketch: circular or rounded-lg floating glass panel with a 2x vector-vector raster preview, 1px border `#4F46E5`, and real-time bounding box coordinate tags rendered in `JetBrains Mono` 10px.