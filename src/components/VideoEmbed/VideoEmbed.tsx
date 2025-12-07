import React from 'react';
import styles from './VideoEmbed.module.css';

interface VideoEmbedProps {
  /** Video URL (YouTube embed format preferred) */
  src: string;
  /** Accessible title for screen readers */
  title: string;
  /** Aspect ratio (default: "16:9") */
  aspectRatio?: '16:9' | '4:3' | '21:9';
}

/**
 * VideoEmbed component for responsive video player
 *
 * @example
 * <VideoEmbed
 *   src="https://www.youtube.com/embed/XYZ123"
 *   title="Gazebo Physics Tutorial"
 *   aspectRatio="16:9"
 * />
 */
export default function VideoEmbed({
  src,
  title,
  aspectRatio = '16:9',
}: VideoEmbedProps): JSX.Element {
  const getAspectRatioClass = () => {
    switch (aspectRatio) {
      case '16:9':
        return styles.ratio16x9;
      case '4:3':
        return styles.ratio4x3;
      case '21:9':
        return styles.ratio21x9;
      default:
        return styles.ratio16x9;
    }
  };

  return (
    <div className={styles.videoEmbedContainer}>
      <div className={`${styles.videoWrapper} ${getAspectRatioClass()}`}>
        <iframe
          src={src}
          title={title}
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          className={styles.iframe}
          loading="lazy"
        />
      </div>
      {title && (
        <p className={styles.caption}>
          {title}
        </p>
      )}
    </div>
  );
}
