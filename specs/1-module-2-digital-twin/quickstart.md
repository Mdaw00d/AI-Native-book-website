# Contributor Quickstart: Module 2 - The Digital Twin

**Purpose**: Enable contributors to quickly create new chapters or modules following project standards

**Created**: 2025-12-06
**Target Audience**: Content authors, technical writers, robotics engineers contributing documentation

---

## Prerequisites

Before contributing to Module 2 documentation, ensure you have:

- [x] **Node.js** ≥ 20.0 LTS installed ([download](https://nodejs.org/))
- [x] **Git** installed and configured
- [x] **Text Editor** with MDX support (VS Code recommended with [MDX extension](https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-mdx))
- [x] **Basic knowledge** of Markdown, React, and Docusaurus

**Optional but Recommended**:
- [x] **Prettier** extension for code formatting
- [x] **ESLint** extension for code quality
- [x] **GitLens** for Git integration in VS Code

---

## Local Setup (First Time)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon-1
```

### 2. Install Dependencies

```bash
cd my-website
npm install
# or
yarn install
```

Expected output: Dependencies installed successfully (~2-3 minutes)

### 3. Start Development Server

```bash
npm run start
# or
yarn start
```

Expected output:
```
[SUCCESS] Docusaurus website is running at http://localhost:3000
```

Open your browser to `http://localhost:3000` and navigate to Module 2.

---

## Creating a New Chapter

### Step 1: Checkout Feature Branch

```bash
git checkout -b feature/module-2-chapter-N
```

Replace `N` with the chapter number (e.g., `chapter-5`).

### Step 2: Create Chapter File

Create a new MDX file in the module directory:

```bash
cd my-website/docs/module-2-digital-twin
touch chapter-N-topic-name.mdx
```

**File Naming Convention**:
- Format: `chapter-N-topic-name.mdx`
- N = chapter number (sequential)
- topic-name = kebab-case description (e.g., `physics-simulation`, `sensor-fusion`)

### Step 3: Add Frontmatter

Copy this frontmatter template and customize:

```yaml
---
id: chapter-N-topic-name
title: Chapter N - Title of the Chapter
sidebar_label: Short Label
sidebar_position: N
description: SEO description explaining what this chapter covers (50-160 characters).
tags: [tag1, tag2, tag3, tag4, tag5]
keywords: [keyword1, keyword2, keyword3]
image: /img/modules/module-2/chapter-N-og-image.png
---
```

**Validation**:
- `id`: Must match filename pattern `chapter-N-topic-name`
- `title`: 10-80 characters
- `sidebar_label`: Max 30 characters
- `description`: 50-160 characters (SEO requirement)
- `tags`: Minimum 3 tags
- `image`: Optional, but recommended for social sharing

### Step 4: Import Required Components

Add component imports after frontmatter:

```mdx
import CodeBlock from '@site/src/components/CodeBlock';
import Callout from '@site/src/components/Callout';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import VideoEmbed from '@site/src/components/VideoEmbed';
import InteractiveDiagram from '@site/src/components/InteractiveDiagram';
```

### Step 5: Follow Chapter Template

Use the template from `contracts/content-structure.md`:

```mdx
# Chapter N - Title

<Callout type="info" title="Learning Objectives">
By the end of this chapter, you will be able to:
- [Specific, measurable goal]
- [Another goal]
- [Another goal]
</Callout>

## Introduction

[Why this topic matters, what problem it solves]

## [Main Sections...]

[Content following the template structure]

## Summary

<Callout type="success">
**Key Takeaways**:
- [Main point]
- [Important concept]
- [Practical skill]

**Next Steps**: Proceed to Chapter N+1 to learn [next topic].
</Callout>

## Further Reading

- [Resource](URL) - Description
```

---

## Component Usage Patterns

### CodeBlock

Use for all code examples:

```mdx
<CodeBlock language="xml" title="robot.urdf" highlightLines="5-7">
<robot name="example">
  <link name="base_link">
    <!-- content -->
  </link>
</robot>
</CodeBlock>
```

**Supported Languages**: xml, python, cpp, csharp, bash, yaml, json

### Callout

Use for important information:

```mdx
<Callout type="info" title="Key Concept">
This is an important concept explanation.
</Callout>

<Callout type="warning" title="Common Pitfall">
Avoid this common mistake.
</Callout>
```

**Types**: `info`, `warning`, `danger`, `success`

### Tabs

Use for alternatives (multi-language, different approaches):

```mdx
<Tabs groupId="approach">
<TabItem value="basic" label="Basic" default>
Basic approach explanation and code.
</TabItem>
<TabItem value="advanced" label="Advanced">
Advanced approach explanation and code.
</TabItem>
</Tabs>
```

### VideoEmbed

Use for visual demonstrations:

```mdx
<VideoEmbed
  src="https://www.youtube.com/embed/VIDEO_ID"
  title="Descriptive title for accessibility"
  aspectRatio="16:9"
/>
```

---

## Adding Images and Diagrams

### Image File Organization

Place images in the module asset directory:

```bash
cd my-website/static/img/modules/module-2
# Add your images here
```

**File Naming**:
- `chapter-N-description.png` (screenshots)
- `chapter-N-description.svg` (diagrams)
- `chapter-N-og-image.png` (Open Graph image, 1200x630px)

### Image Optimization

Before committing images:

1. **Compress**: Use [TinyPNG](https://tinypng.com/) or ImageOptim
2. **Format**: PNG for screenshots, SVG for diagrams, WebP for photos
3. **Size**: Max 500KB per image
4. **Resolution**: Max 1200px width (scales for retina)

### Using Images in MDX

```mdx
![Alt text describing the image](/img/modules/module-2/chapter-1-gazebo-gui.png)
```

**Alt Text Requirements**:
- Descriptive, not "image of..."
- Conveys information, not just decoration
- Example: "Gazebo GUI showing robot model with collision geometries highlighted"

### Creating Mermaid Diagrams

Use InteractiveDiagram component:

```mdx
<InteractiveDiagram type="mermaid" caption="System Architecture">
graph LR
  A[Component A] --> B[Component B]
  B --> C[Component C]
</InteractiveDiagram>
```

---

## Testing Your Changes

### 1. Local Preview

While dev server is running (`npm run start`), changes hot-reload automatically.

**Check**:
- Content displays correctly
- Code blocks syntax-highlighted
- Links work (internal and external)
- Images load properly
- No console errors

### 2. Build Test

Test production build:

```bash
npm run build
```

Expected output: `[SUCCESS] Generated static files in "build"`

**Common Build Errors**:
- Syntax errors in MDX → Check line numbers in error message
- Missing imports → Add component imports at top of file
- Broken links → Verify file paths are correct

### 3. Link Validation

Check for broken links:

```bash
npm run check-links
# or manually with markdown-link-check
npx markdown-link-check docs/module-2-digital-twin/*.mdx
```

### 4. Accessibility Audit

Run Lighthouse on your chapter page:

1. Build and serve: `npm run serve`
2. Open Chrome DevTools → Lighthouse tab
3. Run audit (Performance, Accessibility, Best Practices, SEO)
4. Target: All scores > 90

---

## Pre-Commit Checklist

Before committing your changes, verify:

**Technical Accuracy**:
- [ ] All code examples tested and functional
- [ ] External links valid (no 404s)
- [ ] Version numbers correct for tools mentioned
- [ ] Commands tested on at least one platform

**Content Quality**:
- [ ] Frontmatter complete and validated against schema
- [ ] Learning objectives clearly stated
- [ ] 3-5 code examples included
- [ ] 2-3 diagrams or images included
- [ ] 1-2 warning callouts for common pitfalls
- [ ] Summary callout at end
- [ ] 3-5 external links in Further Reading

**Accessibility**:
- [ ] All images have descriptive alt text
- [ ] Heading hierarchy correct (no skipped levels)
- [ ] Color contrast sufficient (if custom styling)
- [ ] Keyboard navigation works for all components

**Performance**:
- [ ] Images optimized and compressed
- [ ] Videos externally hosted or compressed
- [ ] Build completes without errors
- [ ] No console warnings in dev mode

**Style**:
- [ ] Spell check and grammar review passed
- [ ] Voice consistent (professional, encouraging)
- [ ] Code comments explain "why", not "what"
- [ ] Active voice preferred

---

## Committing and Pushing

### 1. Stage Your Changes

```bash
git add my-website/docs/module-2-digital-twin/chapter-N-*.mdx
git add my-website/static/img/modules/module-2/chapter-N-*
```

### 2. Commit with Semantic Message

```bash
git commit -m "docs(module-2): add chapter N on [topic]

- Added chapter N MDX file with learning objectives
- Included [X] code examples and [Y] diagrams
- Optimized images for performance
- Validated all external links

Closes #issue-number (if applicable)"
```

**Commit Message Format**:
- Type: `docs`, `fix`, `feat`, `style`, `refactor`
- Scope: `module-2`, `component`, `config`
- Subject: Brief description (< 50 chars)
- Body: Detailed changes (optional)

### 3. Push to Your Branch

```bash
git push origin feature/module-2-chapter-N
```

---

## Creating a Pull Request

### 1. Open PR on GitHub

1. Go to repository on GitHub
2. Click "Compare & pull request"
3. Fill out PR template:

```markdown
## Summary

Added Chapter N: [Topic Name] to Module 2 - The Digital Twin

## Changes

- Created `chapter-N-topic-name.mdx` with [X] sections
- Added [Y] code examples (URDF, Python, C#, etc.)
- Included [Z] diagrams (Mermaid architecture, screenshots)
- Optimized [N] images for web performance

## Checklist

- [x] All code examples tested and functional
- [x] Links validated (no 404s)
- [x] Images optimized (< 500KB each)
- [x] Accessibility audit passed (Lighthouse > 90)
- [x] Build succeeds without errors
- [x] Follows content structure guidelines

## Preview

[Link to deploy preview if available]
```

### 2. Request Review

Tag reviewers with relevant expertise:
- **Technical accuracy**: Robotics/ROS expert
- **Content quality**: Technical writer
- **Accessibility**: A11y specialist (if available)

### 3. Address Feedback

Respond to review comments:
- Make requested changes
- Push updates to same branch
- Re-request review when ready

---

## Style Guide Summary

### Voice and Tone

✅ **DO**:
- Use second person ("you will configure...")
- Active voice ("Configure the sensor" vs "The sensor should be configured")
- Explain "why" before "how"
- Define acronyms on first use

❌ **DON'T**:
- Use first person plural ("we will do...")
- Passive voice ("It was configured by...")
- Assume prior knowledge without explanation
- Use jargon without definition

### Code Style

✅ **DO**:
- Add comments explaining "why", not "what"
- Use descriptive variable names
- Keep examples minimal and focused
- Test all code before including

❌ **DON'T**:
- Include boilerplate without explanation
- Use single-letter variable names (except iterators)
- Show untested or broken code
- Add comments that repeat code

---

## Troubleshooting

### Common Issues

**Issue**: MDX syntax error on build
**Solution**: Check for unclosed tags, missing imports, or invalid JSX

**Issue**: Images not displaying
**Solution**: Verify path starts with `/img/modules/module-2/` and file exists in `static/`

**Issue**: Build is slow (> 10 seconds)
**Solution**: Optimize images, reduce Mermaid diagram complexity, or split large chapters

**Issue**: Links broken after renaming files
**Solution**: Search codebase for old filename, update all references

### Getting Help

- **Slack/Discord**: #module-2-docs channel
- **GitHub Issues**: Tag with `documentation` label
- **Email**: docs-team@example.com
- **Office Hours**: Fridays 2-4 PM (for synchronous help)

---

## Resources

### Official Documentation

- [Docusaurus Docs](https://docusaurus.io/docs)
- [MDX Documentation](https://mdxjs.com/)
- [Mermaid Diagram Syntax](https://mermaid.js.org/intro/)

### Internal Resources

- [Component API Documentation](./contracts/component-apis.md)
- [Content Structure Guidelines](./contracts/content-structure.md)
- [Frontmatter Schema](./contracts/frontmatter-schema.json)
- [Data Model](./data-model.md)

### Tools

- [TinyPNG](https://tinypng.com/) - Image compression
- [Hemingway App](https://hemingwayapp.com/) - Readability check
- [Grammarly](https://www.grammarly.com/) - Grammar and style
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Color contrast validation

---

**Quickstart Status**: ✅ **COMPLETE**

New contributors can now set up their environment, create chapters, and submit PRs following project standards. Estimated time to first contribution: < 30 minutes.
