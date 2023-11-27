import React, { useState, useEffect } from 'react';
import './App.css';
import DarkButtonIcon from './resources/dark-mode-button.svg';
import LightButtonIcon from './resources/light-mode-button.svg';
import MenuButtonIconDark from './resources/menu-button-dark.svg';
import MenuButtonIconLight from './resources/menu-button-light.svg';
import CodeMirror from '@uiw/react-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { python } from '@codemirror/lang-python';
import { andromeda } from '@uiw/codemirror-theme-andromeda';
import { monokai } from '@uiw/codemirror-theme-monokai';

import exampleCode from './resources/codeContent';



function App() {

  const [isDropdownVisible, setIsDropdownVisible] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownVisible(!isDropdownVisible);
  };

  function DropdownMenu({ isVisible }) {
    return (
      <div className="menu-container" style={{ display: isVisible ? 'block' : 'none' }}>
        <div className="dropdown-menu">
          <div className="dropdown-item" onClick={() => handleMenuItemClick('Reset Chat')}>Reset Chat</div>
          <div className="dropdown-item" onClick={() => handleMenuItemClick('Settings')}>Settings</div>
          <div className="dropdown-item" onClick={() => handleMenuItemClick('About')}>About</div>
          {/* More dropdown items */}
        </div>
      </div>
    );
  }

  function handleMenuItemClick(itemText) {
    switch (itemText) {
      case 'Reset Chat':
        console.log('Reset Chat');
        showToastMessage('Reset Chat')
        break;
      case 'Settings':
        showToastMessage('Settings')
        break;
      case 'About':
        showToastMessage('About')
        break;
      // Add more cases as needed
      default:
        console.log('Default action');
    }

    // Close the dropdown menu if needed
    setIsDropdownVisible(false);
  }

  // for the codemirror code block
  const [codevalue, setCodeValue] = useState(exampleCode);

  const onCodeChange = React.useCallback((val, viewUpdate) => {
    console.log('val:', val);
    setCodeValue(val);
  }, []);

  const [theme, setTheme] = useState('dark-mode'); // Initial theme state

  useEffect(() => {
    document.body.className = theme; // Apply the theme class to the body
  }, [theme]); // Run effect on theme change

  const toggleTheme = () => {
    setTheme(theme === 'light-mode' ? 'dark-mode' : 'light-mode');
  };

  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return; // Prevent sending empty messages

    // Replace newlines with <br> tags for proper HTML rendering
    const formattedMessage = message.replace(/\n/g, '<br>');

    const userMessage = { type: 'user', text: formattedMessage };
    setConversation([...conversation, userMessage]); // Add user message immediately
    setMessage(''); // Clear input field

    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    const aiMessage = { type: 'bot', text: data.response };
    setConversation(convo => [...convo, aiMessage]); // Add AI response when received

  };

  // Function to show toast message
  const showToastMessage = (message) => {
    setToastMessage(message);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000); // Hide toast after 3 seconds
  };

  // Function to show toast message
  const showDefaultToastMessage = () => {
    setToastMessage("Cool Cool Cool");
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000); // Hide toast after 3 seconds
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      showToastMessage("Message copied to clipboard!");
    }).catch(err => {
      console.error('Could not copy text: ', err);
    });
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Prevent default to avoid newline on Enter
      sendMessage();
    }
  };

  function copyCodeToClipboard(headerElement, code) {
    navigator.clipboard.writeText(code).then(() => {
      // Optionally, change the headerElement text to indicate success
      headerElement.textContent = 'Copied!';
      showToastMessage("Code copied to clipboard!");
    }).catch(err => {
      console.error('Could not copy code: ', err);
    });
  }

  const handleClick = () => {
    window.open('https://examine.dev/', '_blank');
  }

  return (
    <div className={`App ${theme}`}>
      <div className="menu-bar">
        <div className="menu-title">
          <div className="title-text" onClick={handleClick}>
            examine|AI
          </div>
        </div>
        <button className="menu-button" onClick={toggleDropdown} >
            <img src={theme === 'dark-mode' ? MenuButtonIconDark : MenuButtonIconLight} alt="Toggle Theme" />
            <span className={`tooltip-text ${isDropdownVisible ? 'tooltip-disabled' : ''} menu`}>Menu</span>
            <DropdownMenu isVisible={isDropdownVisible} />
        </button>
        <button className="theme-button" onClick={toggleTheme} >
            <img src={theme === 'dark-mode' ? DarkButtonIcon : LightButtonIcon} alt="Toggle Theme" />
            <span className="tooltip-text theme">Theme</span>
        </button>
      </div>
      <div className="chat-window">
          {/* 
          <CodeMirror 
            value={codevalue} 
            extensions={[python()]} 
            theme={monokai}
            onChange={onCodeChange} 
            readOnly={true}
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
      </div>
      <textarea
        className="textarea"
        value={message}
        onChange={e => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message here..."
      ></textarea>
      {showToast && <div className="toast">{toastMessage}</div>}
    </div>
  );
}

export default App;
