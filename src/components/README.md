# Reusable Components for Module 2 - Digital Twin

This directory contains custom React components used throughout Module 2 documentation.

## Available Components

### 1. CodeBlock
Syntax-highlighted code with copy button and line highlighting.

**Import**:
```tsx
import CodeBlock from '@site/src/components/CodeBlock';
```

**Usage**:
```mdx
<CodeBlock language="xml" title="robot.urdf" highlightLines="5-7">
<robot name="example">
  <!-- code -->
</robot>
</CodeBlock>
```

### 2. Callout
Highlight important information with styled boxes.

**Import**:
```tsx
import Callout from '@site/src/components/Callout';
```

**Usage**:
```mdx
<Callout type="warning" title="Common Pitfall">
Avoid zero inertia values in URDF models.
</Callout>
```

**Types**: `info`, `warning`, `danger`, `success`

### 3. VideoEmbed
Responsive video player for YouTube embeds.

**Import**:
```tsx
import VideoEmbed from '@site/src/components/VideoEmbed';
```

**Usage**:
```mdx
<VideoEmbed
  src="https://www.youtube.com/embed/VIDEO_ID"
  title="Tutorial Title"
  aspectRatio="16:9"
/>
```

### 4. InteractiveDiagram
Mermaid diagrams and SVG images.

**Import**:
```tsx
import InteractiveDiagram from '@site/src/components/InteractiveDiagram';
```

**Usage**:
```mdx
<InteractiveDiagram type="mermaid" caption="System Architecture">
graph LR
  A[Component A] --> B[Component B]
</InteractiveDiagram>
```

## Development

### Adding a New Component

1. Create directory: `mkdir src/components/ComponentName`
2. Create TSX file: `ComponentName.tsx`
3. Create CSS module: `ComponentName.module.css`
4. Export in `index.ts`
5. Document in `contracts/component-apis.md`

### Testing Components

Run the development server to test components:
```bash
npm run start
```

### Accessibility

All components must support:
- Keyboard navigation
- Screen readers (ARIA labels)
- High contrast mode
- Color contrast ≥ 4.5:1

For complete API documentation, see: `specs/1-module-2-digital-twin/contracts/component-apis.md`
