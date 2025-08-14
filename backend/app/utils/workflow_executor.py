from ..services.llm_service import llm_service
from ..schemas.workflow_schema import WorkflowDefinition

class WorkflowExecutor:
    """
    Executes a workflow based on its definition.
    """
    def execute(self, workflow_definition: WorkflowDefinition, query: str):
        nodes = {node.id: node for node in workflow_definition.nodes}
        edges = workflow_definition.edges
        llm_engine_node = next((node for node in workflow_definition.nodes if node.type == 'llmEngine'), None)
        
        if not llm_engine_node:
            return {"error": "LLM Engine node not found in workflow."}
            
        # These would be configured in the frontend on the node's data property
        use_knowledge_base = llm_engine_node.data.get("use_knowledge_base", False)
        use_search = llm_engine_node.data.get("use_search", False)
        llm_provider = llm_engine_node.data.get("llm_provider", "openai")

        final_response = llm_service.generate_response(
            query=query,
            llm_provider=llm_provider,
            use_knowledge_base=use_knowledge_base,
            use_search=use_search
        )
        
        return {"response": final_response}

workflow_executor = WorkflowExecutor()
