import React, { useState } from 'react';
import { Handle, Position } from 'reactflow';
import { DragHandleIcon } from '../components/icons';
import { LLMNode } from './LLMNode';

export { LLMNode };

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

export const UserQueryNode = ({ data }: { data: any }) => {
    return (
        <NodeWrapper title="User Query" hasInput={false} hasOutput={true}>
            <p className="text-xs text-gray-500 mb-2">Enter point for queries</p>
            <textarea
                defaultValue={data.query || "Write your query here"}
                className="nodrag w-full p-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-indigo-500"
                rows={3}
            />
        </NodeWrapper>
    );
};

export const KnowledgeBaseNode = ({ data }: { data: any }) => {
    const [fileName, setFileName] = useState<string | null>(null);
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFileName(e.target.files[0].name);
        }
    };

    return (
        <NodeWrapper title="Knowledge Base" hasInput={true} hasOutput={true}>
            <p className="text-xs text-gray-500 mb-2">Let LLM search info in your file</p>
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">File for Knowledge Base</label>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                    <div className="space-y-1 text-center">
                        <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        <div className="flex text-sm text-gray-600">
                            <label htmlFor="file-upload" className="nodrag relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                                <span>Upload File</span>
                                <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileChange} />
                            </label>
                            <p className="pl-1">or drag and drop</p>
                        </div>
                        {fileName ? <p className="text-xs text-green-500 mt-1">{fileName}</p> : <p className="text-xs text-gray-500">PDF, TXT, DOC up to 10MB</p>}
                    </div>
                </div>
            </div>
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700">Embedding Model</label>
                <select className="nodrag mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                    <option>text-embedding-3-large</option>
                    <option>text-embedding-ada-002</option>
                </select>
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700">API Key</label>
                <input type="password" defaultValue="xxxxxxxxxxxxxxxxxxxx" className="nodrag mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md" />
            </div>
        </NodeWrapper>
    );
};

// LLMNode is now imported from LLMNode.tsx

export const OutputNode = ({ data }: { data: any }) => {
    return (
        <NodeWrapper title="Output" hasInput={true} hasOutput={false}>
            <p className="text-xs text-gray-500 mb-2">Final output of your workflow</p>
            <div className="bg-gray-50 p-3 rounded-md border border-gray-200">
                <p className="text-sm text-gray-600">Output will appear here when workflow runs</p>
            </div>
        </NodeWrapper>
    );
};
