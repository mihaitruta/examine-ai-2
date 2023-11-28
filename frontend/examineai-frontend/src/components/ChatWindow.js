import './ChatWindow.css';

import React from 'react';
import useToast from '.././hooks/useToast';

import CodeBlock from './CodeBlock';


function ChatWindow({ conversation, codevalue }) {

	const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      showToast("Message copied to clipboard!");
    }).catch(err => {
      console.error('Could not copy text: ', err);
    });
  };

  const { isVisible, message, showToast } = useToast();

  return (
  	<div className="chat-window">
  	  {/*
	  	<CodeBlock
	      codevalue = {codevalue}
	      language = {'python'}
	    />
	    */}
	    {conversation.map((msg, index) => (
	      <div key={index} className={`message ${msg.type === 'user' ? 'user-message' : 'bot-message'}`}>
	        <div className="message-header">
	          <div className={`avatar ${msg.type === 'user' ? 'user-avatar' : 'ai-avatar'}`}
	               onClick={() => copyToClipboard(msg.text)}>
	            <span className={`tooltip-text`}>Copy</span>
	            {msg.type === 'user' ? '👨‍💻' : '🤖'} {/* User and AI emojis */}
	          </div>
	          <div className="label">{msg.type === 'user' ? 'You' : 'AI'}</div>
	        </div>
	        <div className="message-content" dangerouslySetInnerHTML={{ __html: msg.text }}></div>
	      </div>
	    ))}
	    {isVisible && <div className="toast">{message}</div>}
    </div>
  );
}

export default ChatWindow;