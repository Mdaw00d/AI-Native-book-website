import React from 'react';
import BookChatWidget from '@site/src/components/BookChatWidget';

export default function Root({children}) {
  return (
    <>
      {children}
      <BookChatWidget />
    </>
  );
}
