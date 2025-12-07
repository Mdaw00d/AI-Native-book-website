import React from 'react';
import styles from './Callout.module.css';

interface CalloutProps {
  /** Visual style and icon */
  type: 'info' | 'warning' | 'danger' | 'success';
  /** Optional heading for the callout */
  title?: string;
  /** Callout content */
  children: React.ReactNode;
}

/**
 * Callout component for highlighting important information
 *
 * @example
 * <Callout type="warning" title="Common Pitfall">
 *   Zero or negative inertia values will cause Gazebo to crash.
 * </Callout>
 */
export default function Callout({
  type,
  title,
  children,
}: CalloutProps): JSX.Element {
  const getIcon = () => {
    switch (type) {
      case 'info':
        return (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        );
      case 'warning':
        return (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
            <line x1="12" y1="9" x2="12" y2="13"></line>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
        );
      case 'danger':
        return (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        );
      case 'success':
        return (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        );
    }
  };

  const getAriaLabel = () => {
    switch (type) {
      case 'info':
        return 'Information';
      case 'warning':
        return 'Warning';
      case 'danger':
        return 'Danger';
      case 'success':
        return 'Success';
    }
  };

  return (
    <div
      className={`${styles.callout} ${styles[type]}`}
      role="note"
      aria-label={getAriaLabel()}
    >
      <div className={styles.calloutHeader}>
        <div className={styles.icon} aria-hidden="true">
          {getIcon()}
        </div>
        {title && <div className={styles.title}>{title}</div>}
      </div>
      <div className={styles.content}>{children}</div>
    </div>
  );
}
