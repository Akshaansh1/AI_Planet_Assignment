import { useState } from 'react';
import type { Message } from '../types';
import { BotIcon, CloseIcon, SendIcon, UserIcon } from './icons';

interface ChatModalProps {
    isOpen: boolean;
    onClose: () => void;
    stackName?: string;
    workflowId?: number | null;
}

const ChatModal = ({ isOpen, onClose, stackName, workflowId }: ChatModalProps) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    if (!isOpen) return null;

    const handleSend = () => {
        if (!input.trim()) return;

        const userMessage: Message = { id: Date.now(), text: input, sender: 'user' };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        // If we have a workflowId, call backend execute endpoint
        (async () => {
            try {
                if (workflowId) {
                    // lazy import to avoid cycles
                    const api = await import('../lib/api');
                    const res = await api.executeWorkflow(workflowId, input);
                    const botText = res.response ?? JSON.stringify(res);
                    const botMessage: Message = { id: Date.now() + 1, text: botText, sender: 'bot' };
                    setMessages(prev => [...prev, botMessage]);
                } else {
                    // Simulate a bot response
                    const botMessage: Message = {
                        id: Date.now() + 1,
                        text: `This is a simulated response to your query: "${input}". The actual response would come from executing the '${stackName}' stack.`,
                        sender: 'bot'
                    };
                    setMessages(prev => [...prev, botMessage]);
                }
            } catch (err) {
                const botMessage: Message = { id: Date.now() + 1, text: `Error: ${err instanceof Error ? err.message : String(err)}`, sender: 'bot' };
                setMessages(prev => [...prev, botMessage]);
            } finally {
                setIsLoading(false);
            }
        })();
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl h-[80vh] flex flex-col">
                <div className="p-4 border-b flex justify-between items-center">
                    <h3 className="text-lg font-semibold text-gray-800">{stackName} Chat</h3>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-800">
                        <CloseIcon />
                    </button>
                </div>
                <div className="flex-1 p-6 overflow-y-auto space-y-6">
                    {messages.length === 0 ? (
                        <div className="text-center text-gray-500 h-full flex flex-col justify-center items-center">
                            <div className="bg-green-500 rounded-full p-3 mb-4">
                               <BotIcon />
                            </div>
                            <p className="font-semibold">GenAI Stack Chat</p>
                            <p className="text-sm">Start a conversation to test your stack.</p>
                        </div>
                    ) : (
                         messages.map(msg => (
                            <div key={msg.id} className={`flex items-start gap-3 ${msg.sender === 'user' ? 'justify-end' : ''}`}>
                                {msg.sender === 'bot' && <div className="bg-green-500 rounded-full p-2"><BotIcon /></div>}
                                <div className={`max-w-md p-3 rounded-xl ${msg.sender === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-800'}`}>
                                    <p className="text-sm">{msg.text}</p>
                                </div>
                                {msg.sender === 'user' && <UserIcon className="w-10 h-10 text-gray-600 bg-gray-200 rounded-full p-1" />}
                            </div>
                        ))
                    )}
                     {isLoading && (
                        <div className="flex items-start gap-3">
                            <div className="bg-green-500 rounded-full p-2"><BotIcon /></div>
                            <div className="max-w-md p-3 rounded-xl bg-gray-100 text-gray-800">
                                <div className="flex items-center space-x-1">
                                    <span className="text-sm">Training...</span>
                                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse delay-0"></div>
                                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse delay-200"></div>
                                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-pulse delay-400"></div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
                <div className="p-4 border-t">
                    <div className="relative">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Send a message..."
                            className="w-full border border-gray-300 rounded-lg py-3 pl-4 pr-12 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            disabled={isLoading}
                        />
                        <button onClick={handleSend} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-indigo-600 disabled:text-gray-300" disabled={isLoading}>
                            <SendIcon />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatModal;
