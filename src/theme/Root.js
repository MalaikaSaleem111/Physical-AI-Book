import React from 'react';
import { ChatWidget } from '../components/RagChatbot';

// Root component that wraps the entire app
function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}

export default Root;