# Data Model: Module 2 - The Digital Twin

**Feature**: Module 2 - The Digital Twin (Gazebo & Unity)
**Date**: 2025-12-06
**Status**: ✅ Complete

## Overview

This document defines the structure and organization of MDX content, component specifications, and asset management for Module 2 documentation. Since this is a content/documentation feature (not a data-driven application), the "data model" refers to content structure, frontmatter schemas, and component usage patterns.

---

## Content Hierarchy

```
Module 2 (module-2-digital-twin/)
├── Module Introduction (index.mdx)
│   ├── Overview
│   ├── Learning Objectives
│   ├── Prerequisites
│   └── Chapter Navigation
│
├── Chapter 1: Physics Simulation (chapter-1-physics-simulation.mdx)
│   ├── Section 1.1: Gazebo Architecture
│   ├── Section 1.2: URDF Robot Models
│   ├── Section 1.3: Contact and Friction
│   ├── Section 1.4: Debugging Techniques
│   └── Section 1.5: Performance Optimization
│
├── Chapter 2: Sensor Simulation (chapter-2-sensor-simulation.mdx)
│   ├── Section 2.1: LiDAR Configuration
│   ├── Section 2.2: Depth Camera Setup
│   ├── Section 2.3: IMU Simulation
│   ├── Section 2.4: Sensor Synchronization
│   └── Section 2.5: Validation with Ground Truth
│
├── Chapter 3: Unity Rendering (chapter-3-unity-rendering.mdx)
│   ├── Section 3.1: Unity Setup
│   ├── Section 3.2: ROS-TCP-Connector
│   ├── Section 3.3: URDF Import
│   ├── Section 3.4: Lighting and Materials
│   └── Section 3.5: Performance Optimization
│
└── Chapter 4: Integration (chapter-4-integration.mdx)
    ├── Section 4.1: Scenario Scripting
    ├── Section 4.2: Dataset Generation
    ├── Section 4.3: Perception Integration
    ├── Section 4.4: CI/CD Testing
    └── Section 4.5: Best Practices
```

---

## Frontmatter Schema

### Required Fields

All MDX files MUST include the following frontmatter:

```yaml
---
id: string                    # Unique identifier (pattern: chapter-N-slug)
title: string                 # Display title (10-80 characters)
sidebar_label: string         # Sidebar text (max 30 characters)
sidebar_position: integer     # Sort order (1-indexed)
description: string           # SEO description (50-160 characters)
tags: string[]                # Categorization tags (min 3)
---
```

### Optional Fields

```yaml
keywords: string[]            # SEO keywords (comma-separated)
image: string                 # Open Graph image path (relative to static/)
hide_title: boolean           # Hide h1 title (default: false)
hide_table_of_contents: boolean  # Hide right sidebar TOC (default: false)
```

### Example Frontmatter

```yaml
---
id: chapter-1-physics-simulation
title: Chapter 1 - Simulating Physics in Gazebo
sidebar_label: Physics Simulation
sidebar_position: 1
description: Learn how to simulate physics, gravity, and collisions in Gazebo for realistic humanoid robot testing and validation.
tags: [gazebo, physics, simulation, urdf, ode]
keywords: [gazebo physics, robot simulation, urdf modeling, contact parameters]
image: /img/modules/module-2/gazebo-physics-og.png
---
```

---

## Component Catalog

### 1. CodeBlock

**Purpose**: Display syntax-highlighted code with copy button

**Props**:
- `language` (required): `string` - Syntax highlighting (python, cpp, xml, bash, yaml, json, etc.)
- `title` (optional): `string` - Filename or description displayed above code
- `showLineNumbers` (optional): `boolean` - Display line numbers (default: true)
- `highlightLines` (optional): `string` - Lines to emphasize (e.g., "2-4,7")

**Usage**:
```mdx
<CodeBlock language="xml" title="robot.urdf" highlightLines="5-8">
<robot name="humanoid">
  <link name="base_link">
    <inertial>
      <mass value="50.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0"
               iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>
</robot>
</CodeBlock>
```

**When to Use**:
- Code examples (configuration files, scripts)
- Command-line commands
- Terminal output
- Log file excerpts

### 2. Callout

**Purpose**: Highlight important information, warnings, or tips

**Props**:
- `type` (required): `"info" | "warning" | "danger" | "success"` - Visual style and icon
- `title` (optional): `string` - Callout heading

**Usage**:
```mdx
<Callout type="warning" title="Common Pitfall">
Zero or negative inertia values will cause Gazebo to crash. Always compute inertias using `meshlab` or analytical formulas for primitive shapes.
</Callout>
```

**When to Use**:
- `info`: Learning objectives, key concepts, definitions
- `warning`: Common mistakes, performance considerations
- `danger`: Critical errors, data loss risks, security issues
- `success`: Summaries, achievements, next steps

### 3. Tabs

**Purpose**: Present alternative content (multi-language code, different approaches)

**Props**:
- `groupId` (optional): `string` - Sync tabs across page (same groupId = same active tab)
- `defaultValue` (optional): `string` - Initially selected tab

**Usage**:
```mdx
<Tabs groupId="physics-engine">
<TabItem value="ode" label="ODE (Recommended)" default>

ODE provides stable simulation for articulated robots:

<CodeBlock language="xml">
<physics type="ode">
  <gravity>0 0 -9.81</gravity>
  <ode>
    <solver>
      <type>quick</type>
      <iters>50</iters>
    </solver>
  </ode>
</physics>
</CodeBlock>

</TabItem>
<TabItem value="bullet" label="Bullet">

Bullet offers faster collision detection:

<CodeBlock language="xml">
<physics type="bullet">
  <gravity>0 0 -9.81</gravity>
  <bullet>
    <solver>
      <type>sequential_impulse</type>
      <iters>50</iters>
    </solver>
  </bullet>
</physics>
</CodeBlock>

</TabItem>
</Tabs>
```

**When to Use**:
- Multi-language code examples (Python vs C++)
- Alternative approaches (2D vs 3D LiDAR config)
- Platform-specific instructions (Linux vs Windows)

### 4. VideoEmbed

**Purpose**: Embed responsive video player (YouTube, Vimeo, or self-hosted)

**Props**:
- `src` (required): `string` - Video URL (YouTube embed format)
- `title` (required): `string` - Accessible title for screen readers
- `aspectRatio` (optional): `string` - Aspect ratio (default: "16:9")

**Usage**:
```mdx
<VideoEmbed
  src="https://www.youtube.com/embed/XYZ123"
  title="Gazebo Physics Tutorial"
  aspectRatio="16:9"
/>
```

**When to Use**:
- Step-by-step GUI tutorials
- Live demonstrations
- Conference talks or lectures
- Screen recordings of debugging workflows

### 5. InteractiveDiagram

**Purpose**: Display interactive SVG or Mermaid diagrams

**Props**:
- `type` (required): `"mermaid" | "svg"` - Diagram format
- `content` (required): `string` - Diagram source code or SVG path

**Usage (Mermaid)**:
```mdx
<InteractiveDiagram type="mermaid">
graph LR
A[Gazebo Physics] --> C[Sensor Simulation]
B[Unity Rendering] --> C
C --> D[Perception Stack]
D --> E[Control Algorithms]
</InteractiveDiagram>
```

**When to Use**:
- System architecture diagrams
- Data flow visualizations
- State machines
- Sequence diagrams

---

## Content Guidelines

### Section Length Targets

| Content Type | Lines (MDX) | Words (Prose) |
|--------------|-------------|---------------|
| Module Intro | 100-150 | 300-500 |
| Chapter | 400-600 | 1500-2500 |
| Section (h2) | 80-150 | 300-600 |
| Subsection (h3) | 30-60 | 100-250 |

### Content Ratios (by line count)

- **Prose (explanations)**: 40-50%
- **Code examples**: 25-35%
- **Diagrams/callouts**: 10-15%
- **Lists/tables**: 10-15%

### Required Elements Per Chapter

✅ Must include:
- [ ] 1 learning objectives callout (top of chapter)
- [ ] 3-5 code examples with explanations
- [ ] 2-3 diagrams (Mermaid or images)
- [ ] 1-2 warning callouts (common pitfalls)
- [ ] 1 summary callout (end of chapter)
- [ ] 3-5 external links (official docs, papers, tutorials)

### Code Example Standards

**Principles**:
1. **Minimal**: Show only relevant code, omit boilerplate
2. **Runnable**: Provide complete context when needed (imports, setup)
3. **Explained**: Annotate with comments, reference in prose
4. **Syntax-Highlighted**: Use CodeBlock component with language tag
5. **Tested**: All code examples must be validated before publication

**Code Comment Style**:
```python
# Good: Explains WHY
samples = 720  # 0.5 degree angular resolution for precise mapping

# Bad: Repeats WHAT (obvious from code)
samples = 720  # Set samples to 720
```

### Diagram Standards

**Mermaid Diagram Types**:
- **Flowchart** (`graph TD`): Process workflows, decision trees
- **Sequence** (`sequenceDiagram`): Message passing, interactions
- **Component** (`graph LR`): System architecture, data flow
- **State** (`stateDiagram-v2`): FSMs, robot controller states

**Mermaid Color Palette** (use sparingly):
```
- Primary: #2e8555 (Docusaurus green)
- Secondary: #007ACC (blue)
- Warning: #FFA500 (orange)
- Danger: #DC3545 (red)
- Success: #28A745 (green)
```

**Image Specifications**:
- **Format**: PNG for screenshots, SVG for icons/diagrams, WebP for photos
- **Resolution**: 1200px max width (scaled for retina), compressed
- **Alt Text**: Descriptive (not "image of..."), conveys information
- **File Naming**: `module-2-chapter-N-topic.ext` (e.g., `module-2-chapter-1-gazebo-gui.png`)

### Link Conventions

**Internal Links** (within docs):
```mdx
[Chapter 2 - Sensor Simulation](./chapter-2-sensor-simulation)
[Module 1 Introduction](../module-1-robotic-nervous-system/index)
```

**External Links**:
```mdx
[Gazebo Classic Documentation](http://classic.gazebosim.org/tutorials) (opens in new tab)
[ROS2 Humble Docs](https://docs.ros.org/en/humble/)
```

**Link Text Best Practices**:
- ✅ **Good**: "See the [Gazebo URDF tutorial](URL) for details"
- ❌ **Bad**: "Click [here](URL)" (not accessible, not descriptive)

---

## Asset Organization

### Directory Structure

```
static/img/modules/module-2/
├── og-image.png                # Open Graph default (1200x630px)
├── chapter-1-gazebo-gui.png    # Screenshot of Gazebo interface
├── chapter-1-urdf-diagram.svg  # URDF structure diagram
├── chapter-2-lidar-scan.png    # LiDAR point cloud visualization
├── chapter-2-sensor-frames.svg # Coordinate frame diagram
├── chapter-3-unity-setup.png   # Unity editor screenshot
├── chapter-3-lighting.png      # Rendering comparison
└── chapter-4-pipeline.svg      # CI/CD pipeline diagram
```

### Asset Metadata

**Image Metadata** (tracked in separate CSV or database):
- Filename, Title, Description, Source, License, Date Added, File Size

**Optimization Checklist**:
- [ ] Compressed (TinyPNG, ImageOptim)
- [ ] Responsive (srcset for different resolutions)
- [ ] Lazy-loaded (below the fold)
- [ ] Alt text provided
- [ ] License verified (CC0, MIT, or project-created)

---

## Quality Assurance

### Content Validation Checklist

Before publishing a chapter:

**Technical Accuracy**:
- [ ] All code examples tested and functional
- [ ] External links valid (no 404s)
- [ ] Version numbers correct (Gazebo, ROS2, Unity)
- [ ] Commands work on target platform (Linux, macOS, Windows)

**Accessibility**:
- [ ] Alt text for all images
- [ ] Heading hierarchy correct (no skipped levels)
- [ ] Color contrast ≥ 4.5:1 (WCAG AA)
- [ ] Keyboard navigation works for all interactive elements

**Performance**:
- [ ] Images optimized (< 500KB each)
- [ ] Videos use external hosting (YouTube) or compressed
- [ ] Lighthouse score > 90 for the chapter page
- [ ] MDX compiles in < 5 seconds

**SEO**:
- [ ] Frontmatter complete (title, description, tags)
- [ ] Description 50-160 characters
- [ ] Open Graph image provided (1200x630px)
- [ ] Internal links use relative paths

**Style**:
- [ ] Voice consistent (professional, encouraging)
- [ ] No jargon without explanation
- [ ] Active voice preferred
- [ ] Spell check and grammar review passed

---

**Data Model Status**: ✅ **COMPLETE**

Content structure, frontmatter schemas, component specifications, and quality guidelines defined. Ready for content authoring.
