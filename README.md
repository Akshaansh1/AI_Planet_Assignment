# 🌍 AIPlanet

AIPlanet is a powerful no-code/low-code workflow platform that combines AI capabilities with visual workflow design. Build intelligent automation workflows using a drag-and-drop interface, powered by multiple LLM providers and knowledge base integration.

## ✨ Features

- **🎯 Visual Workflow Designer**: Drag-and-drop interface for creating complex workflows
- **🤖 Multi-LLM Support**: Integration with OpenAI, Google Gemini, and Mistral AI
- **📚 Knowledge Base Management**: Upload and manage documents for context-aware AI responses
- **🔍 Smart Search**: Web search integration for real-time information
- **💬 Chat Interface**: Interactive chat with AI workflows
- **📊 Document Processing**: PDF parsing and text extraction
- **🔄 Workflow Execution**: Run and monitor workflow performance
- **🌐 Modern Web UI**: Built with React, TypeScript, and Tailwind CSS

## 🏗️ Architecture

AIPlanet consists of two main components:

- **Backend**: FastAPI-based REST API with PostgreSQL database and ChromaDB for vector storage
- **Frontend**: React-based web application with ReactFlow for workflow visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL database
- API keys for LLM providers (OpenAI, Google Gemini, Mistral)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/aiplanet
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   SERPAPI_API_KEY=your_serpapi_key
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`.

## 📖 Usage

### Creating Workflows

1. **Dashboard**: Start from the main dashboard to see existing workflows
2. **New Workflow**: Click "Create New Stack" to start a new workflow
3. **Design**: Use the drag-and-drop interface to add nodes and connect them
4. **Configure**: Set parameters for each node (LLM provider, prompts, etc.)
5. **Save**: Save your workflow for future use

### Node Types

- **LLM Node**: Connect to various AI providers (OpenAI, Gemini, Mistral)
- **Document Node**: Process and analyze uploaded documents
- **Search Node**: Perform web searches for real-time information
- **Custom Nodes**: Extend functionality with custom node types

### Knowledge Base

- Upload PDFs and other documents
- Documents are automatically processed and indexed
- Use in workflows for context-aware AI responses
- Vector search capabilities for relevant information retrieval

## 🔧 API Endpoints

### Core Endpoints

- `GET /` - API information and status
- `GET /health` - Health check endpoint

### Document Management

- `POST /api/v1/documents/upload` - Upload documents
- `GET /api/v1/documents/` - List all documents
- `GET /api/v1/documents/{id}` - Get document details

### Workflow Management

- `POST /api/v1/workflow/` - Create new workflow
- `GET /api/v1/workflow/` - List all workflows
- `GET /api/v1/workflow/{id}` - Get workflow details
- `PUT /api/v1/workflow/{id}` - Update workflow
- `DELETE /api/v1/workflow/{id}` - Delete workflow

### Chat & LLM

- `POST /api/v1/chat/` - Send chat message
- `POST /api/v1/llm/generate` - Generate AI response
- `GET /api/v1/llm/providers` - List available LLM providers

### Knowledge Base

- `POST /api/v1/knowledge/query` - Query knowledge base
- `GET /api/v1/knowledge/documents` - List knowledge base documents

## 🛠️ Development

### Backend Development

The backend is built with:
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **ChromaDB**: Vector database for embeddings
- **Pydantic**: Data validation using Python type annotations

### Frontend Development

The frontend is built with:
- **React 19**: Latest React with modern features
- **TypeScript**: Type-safe JavaScript development
- **ReactFlow**: Workflow visualization library
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server

### Project Structure

```
AIPlanet/
├── backend/                 # FastAPI backend
│   ├── app/                # Main application code
│   │   ├── api/           # API route definitions
│   │   ├── core/          # Core functionality
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utility functions
│   ├── alembic/           # Database migrations
│   └── requirements.txt   # Python dependencies
├── frontend/               # React frontend
│   ├── src/               # Source code
│   │   ├── components/    # React components
│   │   ├── nodes/         # Workflow node definitions
│   │   └── lib/           # Utility libraries
│   └── package.json       # Node.js dependencies
└── README.md              # This file
```

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key | No (if using OpenAI) |
| `GOOGLE_API_KEY` | Google API key | No (if using Gemini) |
| `MISTRAL_API_KEY` | Mistral AI API key | No (if using Mistral) |
| `SERPAPI_API_KEY` | SerpAPI key for web search | No (if using search) |

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify database exists

2. **LLM API Errors**
   - Verify API keys are correct
   - Check API quota and billing
   - Ensure internet connectivity

3. **Frontend Build Issues**
   - Clear `node_modules` and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

### Logs

- Backend logs are displayed in the console when running with `--reload`
- Frontend errors appear in the browser console
- Database connection issues are logged at startup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs` when the backend is running
- Review the troubleshooting section above

## 🔮 Roadmap

- [ ] Enhanced workflow templates
- [ ] Real-time collaboration
- [ ] Advanced analytics and monitoring
- [ ] Mobile application
- [ ] Plugin system for custom nodes
- [ ] Multi-tenant support
- [ ] Advanced security features

---

**AIPlanet** - Empowering AI workflows through visual design 🚀
