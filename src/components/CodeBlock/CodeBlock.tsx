import React, { useState } from 'react';
import { Highlight, themes } from 'prism-react-renderer';
import styles from './CodeBlock.module.css';

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

/**
 * CodeBlock component for syntax-highlighted code with copy functionality
 *
 * @example
 * <CodeBlock language="xml" title="robot.urdf" highlightLines="5-8">
 *   <robot name="humanoid">
 *     <link name="base_link">
 *       <!-- content -->
 *     </link>
 *   </robot>
 * </CodeBlock>
 */
export default function CodeBlock({
  language,
  title,
  showLineNumbers = true,
  highlightLines,
  children,
}: CodeBlockProps): JSX.Element {
  const [copied, setCopied] = useState(false);

  // Parse highlight lines string into Set of line numbers
  const parseHighlightLines = (highlightStr: string | undefined): Set<number> => {
    if (!highlightStr) return new Set();

    const lines = new Set<number>();
    const parts = highlightStr.split(',');

    for (const part of parts) {
      if (part.includes('-')) {
        const [start, end] = part.split('-').map(Number);
        for (let i = start; i <= end; i++) {
          lines.add(i);
        }
      } else {
        lines.add(Number(part));
      }
    }

    return lines;
  };

  const highlightedLines = parseHighlightLines(highlightLines);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(children.trim());
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  return (
    <div className={styles.codeBlockContainer}>
      {title && (
        <div className={styles.codeBlockTitle}>
          <span>{title}</span>
        </div>
      )}

      <div className={styles.codeBlockWrapper}>
        <button
          className={styles.copyButton}
          onClick={handleCopy}
          aria-label="Copy code to clipboard"
          type="button"
        >
          {copied ? (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          ) : (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
          )}
          <span className={styles.copyButtonText}>
            {copied ? 'Copied!' : 'Copy'}
          </span>
        </button>

        <Highlight
          theme={themes.vsDark}
          code={children.trim()}
          language={language}
        >
          {({ className, style, tokens, getLineProps, getTokenProps }) => (
            <pre className={`${className} ${styles.pre}`} style={style}>
              <code className={styles.code}>
                {tokens.map((line, i) => {
                  const lineNumber = i + 1;
                  const isHighlighted = highlightedLines.has(lineNumber);
                  const lineProps = getLineProps({ line, key: i });

                  return (
                    <div
                      key={i}
                      {...lineProps}
                      className={`${lineProps.className} ${
                        isHighlighted ? styles.highlightedLine : ''
                      }`}
                    >
                      {showLineNumbers && (
                        <span className={styles.lineNumber}>{lineNumber}</span>
                      )}
                      <span className={styles.lineContent}>
                        {line.map((token, key) => (
                          <span key={key} {...getTokenProps({ token, key })} />
                        ))}
                      </span>
                    </div>
                  );
                })}
              </code>
            </pre>
          )}
        </Highlight>
      </div>
    </div>
  );
}
