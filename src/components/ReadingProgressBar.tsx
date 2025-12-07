import React, { useEffect, useState, useCallback } from 'react';
import styles from './ReadingProgressBar.module.css';

const ReadingProgressBar = () => {
  const [progress, setProgress] = useState(0);

  const updateScrollProgress = useCallback(() => {
    const docContent = document.querySelector('.main-wrapper');
    if (!docContent) return;

    const scrollHeight = docContent.scrollHeight - docContent.clientHeight;
    if (scrollHeight === 0) {
      setProgress(0);
      return;
    }

    const scrolled = docContent.scrollTop;
    const newProgress = (scrolled / scrollHeight) * 100;
    setProgress(newProgress);
  }, []);

  useEffect(() => {
    const docContent = document.querySelector('.main-wrapper');
    if (!docContent) return;

    updateScrollProgress(); // Set initial progress

    docContent.addEventListener('scroll', updateScrollProgress);
    window.addEventListener('resize', updateScrollProgress);

    return () => {
      docContent.removeEventListener('scroll', updateScrollProgress);
      window.removeEventListener('resize', updateScrollProgress);
    };
  }, [updateScrollProgress]);

  return (
    <div className={styles.progressBarContainer}>
      <div
        className={styles.progressBar}
        style={{ width: `${progress}%` }}
      ></div>
    </div>
  );
};

export default ReadingProgressBar;
