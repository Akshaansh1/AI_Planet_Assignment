
import { BotIcon, PlusIcon, UserIcon } from './icons';

interface HeaderProps {
    onNewStack?: () => void;
    onSave?: () => void;
    pageTitle?: string;
}

const Header = ({ onNewStack, onSave, pageTitle }: HeaderProps) => (
  <header className="bg-white border-b border-gray-200 px-6 py-3 flex justify-between items-center">
    <div className="flex items-center">
      <div className="bg-green-500 p-2 rounded-md mr-3">
        <BotIcon />
      </div>
      <h1 className="text-lg font-bold text-gray-800">GenAI Stack</h1>
      {pageTitle && <span className="text-lg text-gray-500 mx-2">/</span>}
      {pageTitle && <h2 className="text-lg text-gray-600">{pageTitle}</h2>}
    </div>
    <div className="flex items-center">
      {onSave && (
        <button onClick={onSave} className="bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors mr-4">
          Save
        </button>
      )}
      {onNewStack && (
        <button onClick={onNewStack} className="bg-green-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-600 transition-colors flex items-center">
          <PlusIcon /> New Stack
        </button>
      )}
       <div className="ml-4">
            <UserIcon className="w-8 h-8 text-white bg-purple-500 rounded-full p-1" />
        </div>
    </div>
  </header>
);

export default Header;
