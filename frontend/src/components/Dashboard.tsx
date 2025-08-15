import type { Stack } from '../types';
import { EditIcon, PlusIcon } from './icons';

const StackCard = ({ stack, onEdit }: { stack: Stack; onEdit: (id: number) => void; }) => (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
    <div>
      <h3 className="font-bold text-gray-800">{stack.name}</h3>
      <p className="text-sm text-gray-500 mt-1">{stack.description}</p>
    </div>
    <button onClick={() => onEdit(stack.id)} className="text-sm text-indigo-600 font-semibold mt-4 self-start flex items-center hover:text-indigo-800">
      Edit Stack <EditIcon />
    </button>
  </div>
);

interface DashboardProps {
    stacks: Stack[];
    onNewStack: () => void;
    onEditStack: (id: number) => void;
}

const Dashboard = ({ stacks, onNewStack, onEditStack }: DashboardProps) => (
  <div className="flex-1 bg-gray-50 p-8">
    <div className="flex justify-between items-center mb-6">
      <h2 className="text-xl font-bold text-gray-800">My Stacks</h2>
      <button onClick={onNewStack} className="bg-green-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-600 transition-colors flex items-center sm:hidden">
        <PlusIcon /> New Stack
      </button>
    </div>
    {stacks.length > 0 ? (
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {stacks.map(stack => <StackCard key={stack.id} stack={stack} onEdit={onEditStack} />)}
      </div>
    ) : (
      <div className="text-center py-20 bg-white rounded-lg border border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Create New Stack</h3>
        <p className="text-sm text-gray-500 mt-2 mb-4">Start building your generative AI apps with our essential tools and frameworks</p>
        <button onClick={onNewStack} className="bg-green-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-600 transition-colors flex items-center mx-auto">
          <PlusIcon /> New Stack
        </button>
      </div>
    )}
  </div>
);

export default Dashboard;
