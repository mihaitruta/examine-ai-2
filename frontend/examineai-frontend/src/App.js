import './App.css';

import React, { useState, useEffect } from 'react';
import useChat from './hooks/useChat';
import useToast from './hooks/useToast';

import exampleCode from './resources/codeContent';
import MenuBar from './components/MenuBar';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';

function App() {

  const [chatId, setChatId] = useState(null);

  // Chat functionality
  const { message: chatMessage, setMessage, conversation, sendMessage, resetChat, getEvaluation } = useChat();

  // Toast functionality
  const { isVisible, message: toastMessage, showToast } = useToast();





  // Handle Menu Logic


  const [isDropdownVisible, setIsDropdownVisible] = useState(false);

  // we keep this in the main app so we can close the menu from here
  const toggleDropdown = () => {
    setIsDropdownVisible(!isDropdownVisible);
  };

  // we keep this here to be able to perform app wide actions
  function handleMenuItemClick(itemText) {
    switch (itemText) {
      case 'Reset Chat':
        console.log('Reset Chat');
        resetChat(); // Method to reset conversation
        showToast('Chat reset');
        break;
      case 'Settings':
        showToast('Settings')
        break;
      case 'About':
        showToast('About')
        break;
      // Add more cases as needed
      default:
        console.log('Default action');
    }

    // Close the dropdown menu if needed
    setIsDropdownVisible(false);
  }



  // for the codemirror demo code block
  const [codevalue, setCodeValue] = useState(exampleCode);




  // Theme Handling

  // we keep the theme state here since it applies to the whole app
  const [theme, setTheme] = useState('dark-mode'); // Initial theme state

  useEffect(() => {
    document.body.className = theme; // Apply the theme class to the body
  }, [theme]); // Run effect on theme change

  const toggleTheme = () => {
    setTheme(theme === 'light-mode' ? 'dark-mode' : 'light-mode');
    console.log(theme)
  };

  return (
    <div className={`App ${theme}`}>
      <MenuBar
        toggleDropdown={toggleDropdown}
        handleMenuItemClick={handleMenuItemClick}
        toggleTheme={toggleTheme}
        theme={theme}
        isDropdownVisible={isDropdownVisible}
      />
      <ChatWindow
        conversation={conversation} 
        codevalue={codevalue}
      />
      <MessageInput
        message={chatMessage}
        setMessage={setMessage}
        sendMessage={sendMessage}
        get_evaluation={getEvaluation}
      />
      {isVisible && <div className="toast">{toastMessage}</div>}
    </div>
  );
}

export default App;
