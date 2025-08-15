import React from 'react';
import { BotIcon, FileIcon, BrainIcon, OutputIcon } from './icons';

const Sidebar = () => {
    const onDragStart = (event: React.DragEvent, nodeType: string, label: string) => {
        event.dataTransfer.setData('application/reactflow', JSON.stringify({ nodeType, label }));
        event.dataTransfer.effectAllowed = 'move';
    };

    return (
        <div className="w-64 bg-white border-r border-gray-200 p-4 overflow-y-auto">
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Workflow Nodes</h3>
                <p className="text-sm text-gray-600">Drag and drop nodes to build your workflow</p>
            </div>

            <div className="space-y-4">
                <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-500 mb-2">Input</h4>
                    <div
                        className="bg-blue-50 border border-blue-200 rounded-lg p-3 cursor-move hover:bg-blue-100 transition-colors"
                        draggable
                        onDragStart={(event) => onDragStart(event, 'userQuery', 'User Query')}
                    >
                        <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                                <BotIcon />
                            </div>
                            <div>
                                <h4 className="font-medium text-blue-900">User Query</h4>
                                <p className="text-xs text-blue-700">Start your workflow</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-500 mb-2">Processing</h4>
                    <div className="space-y-3">
                        <div
                            className="bg-green-50 border border-green-200 rounded-lg p-3 cursor-move hover:bg-green-100 transition-colors"
                            draggable
                            onDragStart={(event) => onDragStart(event, 'knowledgeBase', 'Knowledge Base')}
                        >
                            <div className="flex items-center space-x-3">
                                <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                                    <FileIcon />
                                </div>
                                <div>
                                    <h4 className="font-medium text-green-900">Knowledge Base</h4>
                                    <p className="text-xs text-green-700">Load your documents</p>
                                </div>
                            </div>
                        </div>

                        <div
                            className="bg-purple-50 border border-purple-200 rounded-lg p-3 cursor-move hover:bg-purple-100 transition-colors"
                            draggable
                            onDragStart={(event) => onDragStart(event, 'llm', 'LLM')}
                        >
                            <div className="flex items-center space-x-3">
                                <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
                                    <BrainIcon />
                                </div>
                                <div>
                                    <h4 className="font-medium text-purple-900">Language Model</h4>
                                    <p className="text-xs text-purple-700">Process with AI</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-500 mb-2">Output</h4>
                    <div
                        className="bg-orange-50 border border-orange-200 rounded-lg p-3 cursor-move hover:bg-orange-100 transition-colors"
                        draggable
                        onDragStart={(event) => onDragStart(event, 'output', 'Output')}
                    >
                        <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
                                <OutputIcon />
                            </div>
                            <div>
                                <h4 className="font-medium text-orange-900">Output</h4>
                                <p className="text-xs text-orange-700">Display results</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                    <h4 className="font-medium text-gray-800 mb-2">How to use:</h4>
                    <ol className="text-xs text-gray-600 space-y-1">
                        <li>1. Drag nodes from the sidebar</li>
                        <li>2. Connect them by dragging from output to input</li>
                        <li>3. Configure each node's settings</li>
                        <li>4. Run your workflow</li>
                    </ol>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
