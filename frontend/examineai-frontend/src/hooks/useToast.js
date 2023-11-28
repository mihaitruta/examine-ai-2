import { useState, useEffect } from 'react';

function useToast(initialVisibility = false, timeout = 3000) {
  const [isVisible, setIsVisible] = useState(initialVisibility);
  const [message, setMessage] = useState('');

  useEffect(() => {
    let timer;
    if (isVisible && timeout) {
      timer = setTimeout(() => {
        setIsVisible(false);
      }, timeout);
    }
    return () => clearTimeout(timer);
  }, [isVisible, timeout]);

  const showToast = (msg) => {
    setMessage(msg);
    setIsVisible(true);
  };

  return { isVisible, message, showToast };
}

export default useToast;
