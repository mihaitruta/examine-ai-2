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


  const processedMessages = conversation.map(msg => {
    let avatarSymbol, label;
    switch (msg.type) {
      case 'user':
        avatarSymbol = '👨‍💻';
        label = 'You';
        break;
      case 'bot':
        avatarSymbol = '🤖';
        label = 'AI';
        break;
      case 'eval':
        avatarSymbol = '🔍';
        label = 'Evaluation';
        break;
      default:
        avatarSymbol = '❓';
        label = 'Unknown';
    }

    return { ...msg, avatarSymbol, label };
  });


  return (
    <div className="chat-window">
  	  {/*
	  	<CodeBlock
	      codevalue = {codevalue}
	      language = {'python'}
	    />
	    */}
	    {processedMessages.map((msg, index) => (
	      <div key={index} className={`message ${msg.type}-message`}>
	        <div className="message-header">
	          <div className={`avatar ${msg.type}-avatar`}
	               onClick={() => copyToClipboard(msg.text)}>
	            <span className={`tooltip-text`}>Copy</span>
	            {msg.avatarSymbol} {/* Emoji based on message type */}
	          </div>
	          <div className="label">{msg.label}</div>
	        </div>
	        <div className="message-content" dangerouslySetInnerHTML={{ __html: msg.text }}></div>
	      </div>
	   ))}
	    {isVisible && <div className="toast">{message}</div>}
    </div>
  );
}

export default ChatWindow;