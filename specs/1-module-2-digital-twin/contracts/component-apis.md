# Component API Contracts

**Purpose**: Define TypeScript interfaces and usage patterns for reusable React components in Module 2 documentation

**Created**: 2025-12-06
**Module**: Module 2 - The Digital Twin

---

## CodeBlock

**Purpose**: Display syntax-highlighted code with copy button and optional line numbers

### Props Interface

```typescript
interface CodeBlockProps {
  /** Programming language for syntax highlighting */
  language: string;

  /** Optional title displayed above the code block */
  title?: string;

  /** Show line numbers (default: true) */
  showLineNumbers?: boolean;

  /** Lines to highlight (e.g., "2-4,7,10-12") */
  highlightLines?: string;

  /** Code content */
  children: string;
}
```

### Usage Example

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

### Supported Languages

- `xml` - URDF, SDF, launch files
- `python` - ROS2 scripts, scenario automation
- `cpp` - C++ Gazebo plugins
- `csharp` - Unity C# scripts
- `bash` - Shell commands
- `yaml` - Configuration files
- `json` - Data formats

---

## Callout

**Purpose**: Highlight important information, warnings, tips, or success messages

### Props Interface

```typescript
interface CalloutProps {
  /** Visual style and icon */
  type: 'info' | 'warning' | 'danger' | 'success';

  /** Optional heading for the callout */
  title?: string;

  /** Callout content */
  children: React.ReactNode;
}
```

### Usage Examples

**Info Callout** (Learning objectives, key concepts):
```mdx
<Callout type="info" title="Learning Objectives">
By the end of this chapter, you will be able to:
- Configure Gazebo physics parameters for stable simulation
- Debug common simulation instabilities using GUI tools
- Optimize performance for real-time execution
</Callout>
```

**Warning Callout** (Common mistakes, performance considerations):
```mdx
<Callout type="warning" title="Common Pitfall">
Zero or negative inertia values will cause Gazebo to crash. Always compute inertias using `meshlab` or analytical formulas for primitive shapes.
</Callout>
```

**Danger Callout** (Critical errors, data loss risks):
```mdx
<Callout type="danger" title="Critical">
Never run `killall gzserver` while recording important simulation data. Use `Ctrl+C` to gracefully shutdown Gazebo instead.
</Callout>
```

**Success Callout** (Summaries, achievements):
```mdx
<Callout type="success">
**Checkpoint**: You've successfully configured a stable Gazebo physics simulation! Next, we'll add sensor simulation in Chapter 2.
</Callout>
```

---

## Tabs

**Purpose**: Present alternative content (multi-language code, different approaches, platform-specific instructions)

### Props Interface

```typescript
interface TabsProps {
  /** Sync tabs across the page (same groupId = same active tab) */
  groupId?: string;

  /** Initially selected tab value */
  defaultValue?: string;

  /** Tab items */
  children: TabItem[];
}

interface TabItemProps {
  /** Unique identifier for this tab */
  value: string;

  /** Label displayed on the tab */
  label: string;

  /** Make this tab the default selection */
  default?: boolean;

  /** Tab content */
  children: React.ReactNode;
}
```

### Usage Example

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

---

## VideoEmbed

**Purpose**: Embed responsive video player (YouTube, Vimeo, or self-hosted)

### Props Interface

```typescript
interface VideoEmbedProps {
  /** Video URL (YouTube embed format preferred) */
  src: string;

  /** Accessible title for screen readers */
  title: string;

  /** Aspect ratio (default: "16:9") */
  aspectRatio?: '16:9' | '4:3' | '21:9';
}
```

### Usage Example

```mdx
<VideoEmbed
  src="https://www.youtube.com/embed/XYZ123"
  title="Gazebo Physics Tutorial - Setting Up Your First Simulation"
  aspectRatio="16:9"
/>
```

### YouTube Embed URL Format

Convert standard YouTube URL to embed format:
- Standard: `https://www.youtube.com/watch?v=XYZ123`
- Embed: `https://www.youtube.com/embed/XYZ123`

---

## InteractiveDiagram

**Purpose**: Display interactive SVG or Mermaid diagrams

### Props Interface

```typescript
interface InteractiveDiagramProps {
  /** Diagram format */
  type: 'mermaid' | 'svg';

  /** Diagram source code (for mermaid) or SVG path (for svg) */
  content: string;

  /** Optional caption */
  caption?: string;
}
```

### Usage Example (Mermaid)

```mdx
<InteractiveDiagram type="mermaid" caption="Gazebo Architecture Overview">
graph LR
  A[Gazebo Client GUI] --> C[Gazebo Server gzserver]
  C --> D[ODE Physics Engine]
  C --> E[Sensor Plugins]
  E --> F[ROS2 Topics]
  F --> G[Perception Stack]
</InteractiveDiagram>
```

### Usage Example (SVG)

```mdx
<InteractiveDiagram
  type="svg"
  content="/img/modules/module-2/urdf-structure.svg"
  caption="URDF Robot Model Structure"
/>
```

### Supported Mermaid Diagram Types

- `graph LR` / `graph TD` - Flowcharts (left-to-right, top-to-down)
- `sequenceDiagram` - Interaction sequences
- `stateDiagram-v2` - Finite state machines
- `flowchart` - Process flows with decision nodes

---

## Component Import Patterns

### Importing Components

All components should be imported at the top of MDX files:

```mdx
---
id: chapter-1-physics-simulation
title: Chapter 1 - Simulating Physics in Gazebo
---

import CodeBlock from '@site/src/components/CodeBlock';
import Callout from '@site/src/components/Callout';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import VideoEmbed from '@site/src/components/VideoEmbed';
import InteractiveDiagram from '@site/src/components/InteractiveDiagram';

# Chapter 1 - Simulating Physics in Gazebo

<Callout type="info" title="Learning Objectives">
...
</Callout>
```

### Component Composition Rules

1. **CodeBlock**: Use for all code snippets, terminal commands, and configuration files
2. **Callout**: Use sparingly (2-4 per chapter), reserve for truly important information
3. **Tabs**: Use for alternatives (language variants, platform differences), not for sequential content
4. **VideoEmbed**: Use for visual tutorials, max 1-2 per chapter to avoid performance issues
5. **InteractiveDiagram**: Use for system architecture and data flow, prefer Mermaid over static images

---

## Accessibility Requirements

All components MUST support:

1. **Keyboard Navigation**: Tab, Enter, Space, Arrow keys
2. **Screen Readers**: ARIA labels, semantic HTML
3. **Color Contrast**: 4.5:1 minimum for text, 3:1 for UI elements
4. **Focus Indicators**: Visible focus state for all interactive elements
5. **Alternative Text**: All visual content must have text alternatives

---

## Performance Guidelines

1. **Lazy Loading**: Components below the fold should lazy-load
2. **Code Splitting**: Use React.lazy() for heavy components
3. **Memoization**: Prevent unnecessary re-renders with React.memo
4. **Asset Optimization**: Compress images, use WebP format
5. **Bundle Size**: Keep individual components < 50KB gzipped

---

**Component API Status**: ✅ **COMPLETE**

All component interfaces defined. Ready for implementation in Phase 2 (Foundational).
