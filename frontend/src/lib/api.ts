const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

async function request(path: string, opts: RequestInit = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Request failed: ${res.status} ${txt}`);
  }
  return res.json();
}

export async function getWorkflows() {
  return request('/api/v1/workflow/');
}

export async function createWorkflow(payload: { name: string; definition?: any }) {
  const body = JSON.stringify({ name: payload.name, definition: payload.definition ?? { nodes: [], edges: [] } });
  return request('/api/v1/workflow/', { method: 'POST', body });
}

export async function updateWorkflow(id: number, payload: { name: string; definition: any }) {
  const body = JSON.stringify({ name: payload.name, definition: payload.definition });
  return request(`/api/v1/workflow/${id}`, { method: 'PUT', body });
}

export async function executeWorkflow(workflowId: number, query: string) {
  const body = JSON.stringify({ query });
  return request(`/api/v1/llm/workflow/${workflowId}/execute`, { method: 'POST', body });
}

export async function queryKnowledgeBase(query: string, top_k = 3) {
  const body = JSON.stringify({ query, top_k });
  return request('/api/v1/knowledge/query', { method: 'POST', body });
}

export async function getDocuments() {
  return request('/api/v1/documents/');
}

export default { getWorkflows, createWorkflow, executeWorkflow, queryKnowledgeBase, getDocuments };
