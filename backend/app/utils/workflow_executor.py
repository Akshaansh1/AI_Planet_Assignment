from ..services.llm_service import llm_service


class WorkflowExecutor:
    """
    Executes a workflow based on its definition.
    Accepts either a pydantic WorkflowDefinition (with .nodes/.edges) or a plain dict
    coming from the JSONB column stored in the database.
    """

    def _get_attr(self, node, key, default=None):
        if isinstance(node, dict):
            return node.get(key, default)
        return getattr(node, key, default)

    def _get_data_dict(self, node):
        data = self._get_attr(node, "data", {})
        if data is None:
            return {}
        if isinstance(data, dict):
            return data
        # pydantic BaseModel or object -> try to convert to dict-like
        try:
            return data.dict()
        except Exception:
            try:
                return data.__dict__
            except Exception:
                return {}

    def execute(self, workflow_definition, query: str):
        # Support both pydantic objects and plain dicts
        if hasattr(workflow_definition, "nodes"):
            nodes_list = list(getattr(workflow_definition, "nodes") or [])
            edges = getattr(workflow_definition, "edges", []) or []
        elif isinstance(workflow_definition, dict):
            nodes_list = workflow_definition.get("nodes", []) or []
            edges = workflow_definition.get("edges", []) or []
        else:
            return {"error": "Unsupported workflow definition format"}

        # Build quick lookup (id -> node)
        nodes = {}
        for n in nodes_list:
            node_id = self._get_attr(n, "id")
            if node_id is not None:
                nodes[node_id] = n

        # Find LLM engine node (type may be 'llmEngine' or 'llm')
        llm_engine_node = None
        for n in nodes_list:
            ntype = self._get_attr(n, "type")
            if ntype in ("llmEngine", "llm"):
                llm_engine_node = n
                break

        if not llm_engine_node:
            return {"error": "LLM Engine node not found in workflow."}

        data = self._get_data_dict(llm_engine_node)
        use_knowledge_base = data.get("use_knowledge_base", False)
        use_search = data.get("use_search", False)
        llm_provider = data.get("llm_provider", "openai")

        final_response = llm_service.generate_response(
            query=query,
            llm_provider=llm_provider,
            use_knowledge_base=use_knowledge_base,
            use_search=use_search,
        )

        return {"response": final_response}


workflow_executor = WorkflowExecutor()
