import React from 'react';
import type {PropsWithChildren} from 'react';
import ReadingProgressBar from '@site/src/components/ReadingProgressBar';
import useReadingPosition from '@site/src/hooks/useReadingPosition';

export default function Root({children}: PropsWithChildren): JSX.Element {
  useReadingPosition();
  return (
    <>
      <ReadingProgressBar />
      {children}
    </>
  );
}
