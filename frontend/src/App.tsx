"use client";

import { useState, useEffect } from 'react';
import { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';

import type { Stack } from './types';
import api from './lib/api';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import CreateStackModal from './components/CreateStackModal';
import Workflow from './components/Workflow';

export default function App() {
  const [view, setView] = useState<'dashboard' | 'editor'>('dashboard');
  const [stacks, setStacks] = useState<Stack[]>([]);
  const [activeStack, setActiveStack] = useState<Stack | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleNewStack = () => {
    setIsModalOpen(true);
  };

  const handleCreateStack = (newStackData: Omit<Stack, 'id'>) => {
    // Create stack locally and attempt to persist to backend
    (async () => {
      try {
        // Provide a minimal workflow definition with an LLM node so backend executor can run it
        const minimalDefinition = {
          nodes: [
            {
              id: 'node-llm-1',
              type: 'llm',
              position: { x: 0, y: 0 },
              data: { label: 'LLM Engine', llm_provider: 'mistral', use_knowledge_base: false, use_search: false }
            }
          ],
          edges: []
        };
        const created = await api.createWorkflow({ name: newStackData.name, definition: minimalDefinition });
        const newStack: Stack = { id: created.id, name: created.name, description: newStackData.description };
        setStacks(prev => [...prev, newStack]);
        setIsModalOpen(false);
        setActiveStack(newStack);
        setView('editor');
      } catch (err) {
        // Fallback to local-only if backend not available
        const newStack: Stack = { id: Date.now(), ...newStackData };
        setStacks(prev => [...prev, newStack]);
        setIsModalOpen(false);
        setActiveStack(newStack);
        setView('editor');
      }
    })();
  };

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const ws = await api.getWorkflows();
        if (mounted && Array.isArray(ws)) {
          // Map backend workflow shape to Stack
          setStacks(ws.map((w: any) => ({ id: w.id, name: w.name, description: w.definition?.nodes?.length ? 'Saved workflow' : 'Saved workflow' })));
        }
      } catch (e) {
        // ignore — backend may be down
      }
    })();
    return () => { mounted = false; };
  }, []);

  const handleEditStack = (id: number) => {
    const stackToEdit = stacks.find(s => s.id === id);
    if (stackToEdit) {
      setActiveStack(stackToEdit);
      setView('editor');
    }
  };

  const handleBackToDashboard = () => {
    setActiveStack(null);
    setView('dashboard');
  }

  return (
    <div className="h-screen w-screen bg-gray-100 flex flex-col font-sans">
      {view === 'dashboard' ? (
        <>
          <Header onNewStack={handleNewStack} />
          <Dashboard stacks={stacks} onNewStack={handleNewStack} onEditStack={handleEditStack} />
        </>
      ) : activeStack ? (
        <ReactFlowProvider>
          <Workflow stack={activeStack} onBack={handleBackToDashboard} />
        </ReactFlowProvider>
      ) : null}

      <CreateStackModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreate={handleCreateStack}
      />
    </div>
  );
}
