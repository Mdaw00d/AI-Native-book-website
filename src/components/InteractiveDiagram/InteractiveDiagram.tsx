import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';
import styles from './InteractiveDiagram.module.css';

interface InteractiveDiagramProps {
  /** Diagram format */
  type: 'mermaid' | 'svg';
  /** Diagram source code (for mermaid) or SVG path (for svg) */
  content: string;
  /** Optional caption */
  caption?: string;
}

// Initialize Mermaid with configuration
if (typeof window !== 'undefined') {
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'var(--ifm-font-family-base)',
  });
}

/**
 * InteractiveDiagram component for Mermaid diagrams and SVG images
 *
 * @example
 * <InteractiveDiagram type="mermaid" caption="System Architecture">
 *   graph LR
 *     A[Component A] --> B[Component B]
 * </InteractiveDiagram>
 */
export default function InteractiveDiagram({
  type,
  content,
  caption,
}: InteractiveDiagramProps): JSX.Element {
  const mermaidRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (type === 'mermaid' && mermaidRef.current) {
      // Clear previous content
      mermaidRef.current.innerHTML = content;

      // Render Mermaid diagram
      try {
        mermaid.contentLoaded();
      } catch (error) {
        console.error('Mermaid rendering error:', error);
        mermaidRef.current.innerHTML = `
          <div class="${styles.error}">
            <p><strong>Error rendering diagram</strong></p>
            <p>Please check the Mermaid syntax.</p>
          </div>
        `;
      }
    }
  }, [type, content]);

  return (
    <div className={styles.diagramContainer}>
      {type === 'mermaid' ? (
        <div
          ref={mermaidRef}
          className={`mermaid ${styles.mermaidDiagram}`}
        >
          {content}
        </div>
      ) : (
        <div className={styles.svgDiagram}>
          <img
            src={content}
            alt={caption || 'Diagram'}
            loading="lazy"
            className={styles.svgImage}
          />
        </div>
      )}

      {caption && (
        <p className={styles.caption}>{caption}</p>
      )}
    </div>
  );
}
