import React, { useState, useEffect } from 'react';

const Dashboard = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [answer, setAnswer] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    let source;

  
    const handleInputChange = (e) => {
      setInput(e.target.value);
    };
  
    const handleSend = async () => {
      if (input.trim() !== '') {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: input, isUser: true },
        ]);
        setInput('');
        setAnswer('');
        setIsLoading(true);
        source = new EventSource(`http://localhost:8081/chat/query?question=${encodeURIComponent(input)}`);
        let accumulatedResponse = ''

        source.onmessage = (event) => {
          const { data } = event;

          if (data.startsWith('[END]')) {
            source.close();
            setIsLoading(false);
            setMessages((prevMessages) => [
                ...prevMessages,
                { text: accumulatedResponse?.trim(), isUser: false },
            ]);
            setAnswer('');
          } else if (data.startsWith('[ERROR]')) {
            setAnswer(data);
            source.close();
            setIsLoading(false);
          } else {
            setAnswer((prev) => `${prev} ${data}`);
            accumulatedResponse += ` ${data}`;
          }
        };

        source.onerror = (error) => {
          console.log('EventSource failed:', error);
          source.close();
          setIsLoading(false);
          setMessages((prevMessages) => [
              ...prevMessages,
              { text: '[ERROR] An error occurred. Please try again.', isUser: false },
          ]);
        };
      }
    };

    useEffect(() => {
      return () => {
        if (source) {
          source.close();
        }
      };
    }, []);
  
    // console.log("answer", answer);
    // console.log("messages", messages);
    return (
         <div className="flex md:flex-row flex-col md:h-screen relative items-center justify-center w-full h-screen self-center max-md:self-center max-md:w-[90%] max-sm:w-[90%]">
                <div className="md:w-[75%] w-full flex flex-col p-4">
                    <div className="flex flex-col gap-5 fixed md:w-[70%] w-[85%] bottom-[100px] max-h-[80%] py-2 overflow-y-auto mt-5">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex ${
                                message?.isUser ? 'justify-end' : 'justify-start'
                                } mb-4`}
                            >
                               <div
                                className={`max-w-xs px-4 py-2 rounded-lg ${
                                    message?.isUser
                                    ? 'bg-blue-500 text-white rounded-br-none'
                                    : 'bg-gray-300 text-gray-900 rounded-bl-none'
                                }`}
                                >
                                {message?.text}
                                </div>
                            </div>
                        ))}
                        {!!answer && answer.length > 0 && (
                          <div
                              className={`flex justify-start mb-4`}
                          >
                            <div
                              className={`max-w-xs px-4 py-2 rounded-lg bg-gray-300 text-gray-900 rounded-bl-none`}
                              >
                              {answer}
                              </div>
                          </div>
                        )}
                    </div>

                    <div className="flex items-center md:w-[70%] w-[90%]  justify-center fixed bottom-0 mb-6">
                        <input
                            type="text"
                            value={input}
                            onChange={handleInputChange}
                            placeholder="Type your message..."
                            className="border border-gray-300 rounded py-2 px-4 w-full"
                        />
                        <button
                            disabled={isLoading}
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