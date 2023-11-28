import React from 'react';
import './MessageInput.css';

function MessageInput({ message, setMessage, sendMessage }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent default to avoid newline on Enter
      sendMessage();
    }
  };

  return (
    <textarea
      id="main_input"
      className="textarea"
      value={message}
      onChange={e => setMessage(e.target.value)}
      onKeyDown={handleKeyDown}
      placeholder="Type your message here..."
    ></textarea>
  );
}

export default MessageInput;