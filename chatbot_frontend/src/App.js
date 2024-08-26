import React, { useState, useEffect } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const sendMessage = async (event) => {
    event.preventDefault();
    if (userInput.trim() === '') return;

    setMessages([...messages, { type: 'user', content: userInput }]);

    const response = await fetch('http://localhost:8000//api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();
    setMessages([...messages, { type: 'bot', content: data.bot_response }]);

    setUserInput('');
  };

  return (
    <main>
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`${message.type}-message`}>
            {message.content}
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage}>
        <input
          value={userInput}
          onChange={(event) => setUserInput(event.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </main>
  );
}

export default App;