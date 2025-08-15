import React, { useState, useEffect } from 'react';
import { Handle, Position } from 'reactflow';
import { DragHandleIcon } from '../components/icons';

const NodeWrapper = ({ children, title, hasInput = true, hasOutput = true }: {
    children: React.ReactNode,
    title: string,
    hasInput?: boolean,
    hasOutput?: boolean
}) => (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 w-80 react-flow__node-default">
        {hasInput && (
            <Handle
                type="target"
                position={Position.Left}
                className="w-3 h-3 bg-blue-500 border-2 border-white"
            />
        )}
        <div className="bg-gray-50 p-3 border-b border-gray-200 rounded-t-lg flex justify-between items-center cursor-move">
            <span className="text-sm font-semibold text-gray-700">{title}</span>
            <DragHandleIcon />
        </div>
        <div className="p-4">
            {children}
        </div>
        {hasOutput && (
            <Handle
                type="source"
                position={Position.Right}
                className="w-3 h-3 bg-green-500 border-2 border-white"
            />
        )}
    </div>
);

export const LLMNode = ({ data, selected }: { data: any, selected?: boolean }) => {
    // Initialize state from node data or defaults
    const [provider, setProvider] = useState(data?.llm_provider || 'mistral');
    const [useKnowledgeBase, setUseKnowledgeBase] = useState(data?.use_knowledge_base || false);
    const [useSearch, setUseSearch] = useState(data?.use_search || false);
    const [temperature, setTemperature] = useState(data?.temperature || 0.7);
    const [apiKeyStatus, setApiKeyStatus] = useState<Record<string, boolean>>({ mistral: false });
    const [testingApi, setTestingApi] = useState(false);
    const [testResult, setTestResult] = useState<string | null>(null);

    // Fetch API key status on mount and when provider changes
    useEffect(() => {
        const fetchApiKeyStatus = async () => {
            try {
                // Using the correct backend URL with v1 prefix
                const response = await fetch('http://localhost:8000/api/v1/llm/api-key-status');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const status = await response.json();
                console.log('API key status response:', status); // Debug log
                setApiKeyStatus(status);
            } catch (error) {
                console.error('Failed to fetch API key status:', error);
                // Set mistral key as false if there's an error
                setApiKeyStatus({ mistral: false });
            }
        };
        fetchApiKeyStatus();
    }, []);

    // Test the API key
    const testApiKey = async () => {
        setTestingApi(true);
        setTestResult(null);
        try {
            const backendProvider = provider;
            const response = await fetch(`http://localhost:8000/api/v1/llm/test-api-key/${backendProvider}`, {
                method: 'POST'
            });
            const data = await response.json();
            console.log('API test response:', data); // Debug log
            
            if (response.ok) {
                setTestResult('success');
            } else {
                setTestResult(`error: ${data.detail || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('API test error:', error); // Debug log
            const err = error as Error;
            setTestResult(`error: ${err.message || 'Failed to test API key'}`);
        } finally {
            setTestingApi(false);
        }
    };

    // Sync state changes back to node data
    useEffect(() => {
        if (data && typeof data === 'object') {
            data.llm_provider = provider;
            data.use_knowledge_base = useKnowledgeBase;
            data.use_search = useSearch;
            data.temperature = temperature;
        }
    }, [provider, useKnowledgeBase, useSearch, temperature, data]);

    const handleProviderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const newProvider = e.target.value;
        setProvider(newProvider);
        // Reset model when changing provider
        if (data) {
            if (newProvider === 'mistral') data.model = 'mistral-small';
            else if (newProvider === 'openai') data.model = 'gpt-3.5-turbo';
            else data.model = 'gemini-pro';
        }
    };

    return (
        <NodeWrapper title="Language Model" hasInput={true} hasOutput={true}>
            <p className="text-xs text-gray-500 mb-4">Run queries with AI language models</p>
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Provider</label>
                <select 
                    className="nodrag mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={provider}
                    onChange={handleProviderChange}
                >
                    <option value="mistral">Mistral</option>
                    <option value="openai">OpenAI (legacy)</option>
                    <option value="gemini">Google (Gemini) (legacy)</option>
                </select>
            </div>
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Model</label>
                <select 
                    className="nodrag mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={data?.model || (provider === 'mistral' ? 'mistral-small' : provider === 'openai' ? 'gpt-3.5-turbo' : 'gemini-pro')}
                    onChange={(e) => { if (data) data.model = e.target.value; }}
                >
                    {provider === 'mistral' ? (
                        <>
                            <option value="mistral-small">Mistral Small</option>
                            <option value="mistral-large">Mistral Large</option>
                        </>
                    ) : provider === 'openai' ? (
                        <>
                            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                            <option value="gpt-4">GPT-4</option>
                        </>
                    ) : (
                        <option value="gemini-pro">Gemini Pro</option>
                    )}
                </select>
            </div>
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Temperature</label>
                <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    value={temperature}
                    onChange={(e) => setTemperature(parseFloat(e.target.value))}
                    className="nodrag w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" 
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Precise</span>
                    <span>Creative</span>
                </div>
            </div>
            <div className="space-y-2">
                <div className="flex items-center">
                    <input
                        type="checkbox"
                        id="use-knowledge"
                        checked={useKnowledgeBase}
                        onChange={(e) => setUseKnowledgeBase(e.target.checked)}
                        className="nodrag h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <label htmlFor="use-knowledge" className="nodrag ml-2 block text-sm text-gray-700">
                        Use knowledge base for context
                    </label>
                </div>
                <div className="flex items-center">
                    <input
                        type="checkbox"
                        id="use-search"
                        checked={useSearch}
                        onChange={(e) => setUseSearch(e.target.checked)}
                        className="nodrag h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <label htmlFor="use-search" className="nodrag ml-2 block text-sm text-gray-700">
                        Use web search for additional context
                    </label>
                </div>
            </div>
            {/* API Key Status and Test */}
            <div className="mt-4 space-y-2">
                <div className={`p-2 rounded text-xs ${
                    apiKeyStatus[provider] 
                        ? 'bg-green-50 text-green-700'
                        : 'bg-red-50 text-red-700'
                }`}>
                    {apiKeyStatus[provider]
                        ? `${provider === 'mistral' ? 'Mistral' : provider} API key is configured`
                        : `${provider === 'mistral' ? 'Mistral' : provider} API key is not configured`
                    }
                </div>
                {testResult?.startsWith('error') && testResult.includes('insufficient_quota') && (
                    <div className="mt-2 p-2 bg-yellow-50 rounded text-xs text-yellow-800">
                        Your OpenAI API key has insufficient quota. Please:
                        <ul className="list-disc ml-4 mt-1">
                            <li>Add billing information to your OpenAI account</li>
                            <li>Use a different API key with available credits</li>
                            <li>Or switch to using Gemini</li>
                        </ul>
                    </div>
                )}
                <button
                    onClick={testApiKey}
                    disabled={!apiKeyStatus[provider] || testingApi}
                    className={`w-full py-1 px-2 rounded text-sm ${
                        !apiKeyStatus[provider] || testingApi
                            ? 'bg-gray-100 text-gray-400'
                            : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
                    }`}
                >
                    {testingApi ? 'Testing API Key...' : 'Test API Key'}
                </button>
                {testResult && (
                    <div className={`p-2 rounded text-xs ${
                        testResult.startsWith('error')
                            ? 'bg-red-50 text-red-700'
                            : 'bg-green-50 text-green-700'
                    }`}>
                        {testResult.startsWith('error')
                            ? testResult.substring(7)
                            : 'API key is working correctly'
                        }
                    </div>
                )}
                <div className="text-xs text-gray-500 mt-1">
                    API keys are securely managed in the backend .env file
                </div>
            </div>
        </NodeWrapper>
    );
};
