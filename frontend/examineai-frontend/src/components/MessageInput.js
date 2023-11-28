import React from 'react';
import './MessageInput.css';

function MessageInput({ message, setMessage, sendMessage, get_evaluation}) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent default to avoid newline on Enter
      sendMessage();
    }
  };

  return (
    <div className="input_container">
      <button className="evaluate-button" onClick={get_evaluation}>
        Evaluate
      </button>
      <textarea
        id="main_input"
        className="textarea"
        value={message}
        onChange={e => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message here..."
      ></textarea>
    </div>
  );
}

export default MessageInput;