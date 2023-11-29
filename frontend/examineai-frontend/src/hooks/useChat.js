import { useState, useEffect, useCallback } from 'react';

function useChat() {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);
  const [chatId, setChatId] = useState(null);



  // Function to initialize chat and get chat_id
  useEffect(() => {
    const initializeChat = async () => {
      console.log("initializing Chat")
      try {
        const response = await fetch('http://localhost:5000/reset_chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const data = await response.json();
        if (response.ok) {
          setChatId(data.chat_id);
          console.log("Set chat_id ", data.chat_id)
          console.log(data)
        } else {
          throw new Error(data.message || 'Error initializing chat');
        }
      } catch (error) {
        console.error('Failed to initialize chat:', error);
      }
    };

    initializeChat();
  }, []);





  // We handle resetting the chat
  const resetChat = useCallback(async () => {
    console.log("resetting Chat")
    try {
      const response = await fetch('http://localhost:5000/reset_chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      if (response.ok) {
        setChatId(data.chat_id);
        setConversation([]); // Optionally reset conversation
      } else {
        throw new Error(data.message || 'Error resetting chat');
      }
    } catch (error) {
      console.error('Failed to reset chat:', error);
    }
  }, []);




  // we handle message sending
  const sendMessage = async () => {
    if (!message.trim()) return; // Prevent sending empty messages

    if (!chatId) {
      console.error('No chat ID available');
      return;
    }
    // we replace newlines with <br> tags for proper HTML rendering
    const formattedMessage = message.replace(/\n/g, '<br>');

    const userMessage = { type: 'user', text: formattedMessage };
    setConversation([...conversation, userMessage]); // Add user message immediately
    setMessage(''); // Clear input field

    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'chat_id': chatId, 'message': message }),
    });

    const data = await response.json();
    const aiMessage = { type: 'bot', text: data.response };
    setConversation(convo => [...convo, aiMessage]); // Add AI response when received
    setMessage(''); // Clear the message input after sending
  };




  // we get the safeguard evaluation from the backend
  const getEvaluation = async () => {

    const response = await fetch('http://localhost:5000/get_eval', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'chat_id': chatId, 'message': 'optional_info' }),
    });

    const data = await response.json();
    const evalMessage = { type: 'eval', text: data.evaluation };
    setConversation(convo => [...convo, evalMessage]); // Add eval to conversation
  }




  return { message, setMessage, conversation, sendMessage, resetChat, getEvaluation };
}

export default useChat;