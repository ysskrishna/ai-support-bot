import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';





const Dashboard = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [response, setResponse] = useState(null);
    const [eventSource, setEventSource] = useState(null);


    const messageEndRef = useRef(null);

    useEffect(() => {
      messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Cleanup on component unmount
    useEffect(() => {
      return () => {
        if (eventSource) {
          eventSource.close();
        }
      };
    }, [eventSource]);
  
    const handleInputChange = (e) => {
      setInput(e.target.value);
    };
  
    const handleSend = () => {
      if (input.trim() !== '') {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: input, isUser: true },
        ]);

        // Clean up any existing EventSource connection
        if (eventSource) {
          eventSource.close();
        }

        let source = new EventSource(`http://localhost:8081/chat/query?question=${encodeURIComponent(input)}`);
        
        setResponse({
          isUser: false,
          text:""
        })
        source.onmessage = (event) => {
          console.log("source event - ", event);
          setResponse(prevResponse => ({
            ...prevResponse,
            text: prevResponse.text + event.data + '\n',
          }));
        };

        source.onerror = (error) => {
          console.error('EventSource failed:', error);
          source.close();
        };

        setEventSource(source);
        setMessages((prevMessages) => [
          ...prevMessages,
          response,
        ]);
        setResponse(null);
      }
    };
  
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
          handleSend();
        }
    };
    console.log("response", response);
    console.log("messages", messages);
    return (
         <div className="flex md:flex-row flex-col md:h-screen relative items-center justify-center w-full h-screen self-center max-md:self-center max-md:w-[90%] max-sm:w-[90%]">
                <div className="md:w-[75%] w-full flex flex-col p-4">
                    <div className="flex flex-col gap-5 fixed md:w-[70%] w-[85%] bottom-[100px] max-h-[80%] py-2 overflow-y-auto mt-5">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex ${
                                message.isUser ? 'justify-end' : 'justify-start'
                                } mb-4`}
                            >
                               <div
                                className={`max-w-xs px-4 py-2 rounded-lg ${
                                    message.isUser
                                    ? 'bg-blue-500 text-white rounded-br-none'
                                    : 'bg-gray-300 text-gray-900 rounded-bl-none'
                                }`}
                                >
                                {message.text}
                                </div>
                            </div>
                        ))}
                        {!!response && !!response?.text && (
                          <div
                              key={index}
                              className={`flex ${
                              response?.isUser ? 'justify-end' : 'justify-start'
                              } mb-4`}
                          >
                            <div
                              className={`max-w-xs px-4 py-2 rounded-lg ${
                                  response?.isUser
                                  ? 'bg-blue-500 text-white rounded-br-none'
                                  : 'bg-gray-300 text-gray-900 rounded-bl-none'
                              }`}
                              >
                              {response?.text}
                              </div>
                          </div>
                        )}
                        <div ref={messageEndRef} />
                    </div>

                    <div className="flex items-center md:w-[70%] w-[90%]  justify-center fixed bottom-0 mb-6">
                        <input
                            type="text"
                            value={input}
                            onChange={handleInputChange}
                            onKeyPress={handleKeyPress}
                            placeholder="Type your message..."
                            className="border border-gray-300 rounded py-2 px-4 w-full"
                        />
                        <button
                            onClick={handleSend}
                            className="bg-[#ececec] hover:bg-gray-200 font-bold py-2 px-4 ml-2 rounded"
                        >
                        Send
                        </button>                         
                    </div>
                </div>
         </div>
    );
};

export default Dashboard;