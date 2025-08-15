import { useState } from 'react';
import type { Stack } from '../types';
import { CloseIcon } from './icons';

interface CreateStackModalProps {
    isOpen: boolean;
    onClose: () => void;
    onCreate: (stack: Omit<Stack, 'id'>) => void;
}

const CreateStackModal = ({ isOpen, onClose, onCreate }: CreateStackModalProps) => {
  if (!isOpen) return null;
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const handleCreate = () => {
      if(name && description) {
          onCreate({ name, description });
          setName('');
          setDescription('');
      }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium text-gray-900">Create New Stack</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <CloseIcon />
          </button>
        </div>
        <div className="space-y-4">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="e.g., Chat With PDF"
            />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="e.g., A stack to chat with your PDF documents"
            />
          </div>
        </div>
        <div className="mt-6 flex justify-end space-x-3">
          <button onClick={onClose} className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none">
            Cancel
          </button>
          <button onClick={handleCreate} className="bg-green-600 text-white py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium hover:bg-green-700 focus:outline-none">
            Create
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateStackModal;
