import { useState } from 'react';

function useChat() {
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
    setMessage(''); // Clear the message input after sending
  };

  return { message, setMessage, conversation, sendMessage };
}

export default useChat;