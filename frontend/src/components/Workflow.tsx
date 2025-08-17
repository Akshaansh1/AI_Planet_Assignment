import React, { useState, useCallback, useMemo, DragEvent } from 'react';
import ReactFlow, {
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
  Node,
  Edge,
  Connection,
  NodeTypes,
} from 'reactflow';
import { Stack } from '../../types';
import Header from '../Header';
import Sidebar from './Sidebar';
import ChatModal from '../modals/ChatModal';
import { UserQueryNode, KnowledgeBaseNode, LLMNode, OutputNode } from '../../nodes/CustomNodes';
import { PlayIcon } from '../icons';

const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

let id = 0;
const getId = () => `dndnode_${id++}`;

interface WorkflowEditorProps {
    stack: Stack;
    onBack: () => void;
}

const WorkflowEditor = ({ stack, onBack }: WorkflowEditorProps) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const onConnect = useCallback((params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const onDragOver = useCallback((event: DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: DragEvent) => {
      event.preventDefault();

      if (reactFlowInstance) {
        const { nodeType, label } = JSON.parse(event.dataTransfer.getData('application/reactflow'));
        const position = reactFlowInstance.screenToFlowPosition({
          x: event.clientX,
          y: event.clientY,
        });
        const newNode: Node = {
          id: getId(),
          type: nodeType,
          position,
          data: { label },
        };

        setNodes((nds) => nds.concat(newNode));
      }
    },
    [reactFlowInstance, setNodes]
  );
  
  const nodeTypes: NodeTypes = useMemo(() => ({
      userQuery: UserQueryNode,
      knowledgeBase: KnowledgeBaseNode,
      llm: LLMNode,
      output: OutputNode,
  }), []);

  return (
    <div className="flex-1 flex flex-col h-full">
        <Header onSave={() => console.log("Saving workflow...")} pageTitle={stack.name} />
        <div className="flex-1 flex">
            <Sidebar />
            <main className="flex-1 h-full relative" style={{ height: 'calc(100vh - 65px)' }}>
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onInit={setReactFlowInstance}
                    onDrop={onDrop}
                    onDragOver={onDragOver}
                    nodeTypes={nodeTypes}
                    fitView
                >
                    <Controls />
                    <Background />
                    <MiniMap />
                </ReactFlow>
                {nodes.length === 0 && (
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center text-gray-400 pointer-events-none">
                        <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M7 11.5V14m0-2.5v-6a1.5 1.5 0 113 0m-3 6a1.5 1.5 0 00-3 0v2a7.5 7.5 0 0015 0v-5a1.5 1.5 0 00-3 0m-6-3V11" /></svg>
                        <p>Drag & drop to get started</p>
                    </div>
                )}
                <button 
                    onClick={() => setIsChatOpen(true)}
                    className="absolute bottom-8 right-8 bg-green-500 p-4 rounded-full shadow-lg hover:bg-green-600 transition-all transform hover:scale-110"
                >
                    <PlayIcon />
                </button>
                <span className="absolute bottom-10 right-24 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">
                    Chat with Stack
                </span>
            </main>
        </div>
        <ChatModal isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} stackName={stack.name} />
    </div>
  );
};

export default WorkflowEditor;
