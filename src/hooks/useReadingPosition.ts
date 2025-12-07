import { useEffect } from 'react';
import { useLocation } from '@docusaurus/router';

const STORAGE_KEY_PREFIX = 'docusaurus-reading-position-';

const useReadingPosition = () => {
  const location = useLocation();

  useEffect(() => {
    const restoreScrollPosition = () => {
      const savedPosition = localStorage.getItem(STORAGE_KEY_PREFIX + location.pathname);
      if (savedPosition) {
        window.scrollTo(0, parseInt(savedPosition, 10));
      }
    };

    const saveScrollPosition = () => {
      localStorage.setItem(STORAGE_KEY_PREFIX + location.pathname, String(window.scrollY));
    };

    // Restore scroll position on page load/navigation
    // We use a timeout to ensure Docusaurus has rendered the content
    const timeoutId = setTimeout(restoreScrollPosition, 100);

    // Save scroll position before navigating away or closing
    window.addEventListener('beforeunload', saveScrollPosition);
    window.addEventListener('pagehide', saveScrollPosition);

    // Clean up event listeners
    return () => {
      clearTimeout(timeoutId);
      window.removeEventListener('beforeunload', saveScrollPosition);
      window.removeEventListener('pagehide', saveScrollPosition);
    };
  }, [location.pathname]);
};

export default useReadingPosition;
