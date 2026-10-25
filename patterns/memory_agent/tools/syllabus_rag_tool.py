import os
import logging
from typing import Optional
from llama_index.core.tools import FunctionTool
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

# Relative import targeting your existing IndexManager
from patterns.planner_executor.llama_index.index_manager import LocalIndexManager

logger = logging.getLogger("AgenticLab.SyllabusTool")

def query_syllabus(query: str, engine_type: str = "gemini") -> str:
    """
    Queries the official computational thinking course syllabus and curriculum guidelines.
    
    Use this tool whenever a student asks questions about:
      - Weekly course schedules and layout (e.g., what is taught in Week 5)
      - Specific loop architectures, conditionals, or coding concepts covered in class
      - Lab objectives, grading scope, or curriculum benchmarks
    
    Args:
        query (str): The specific question or search topic related to the syllabus.
        engine_type (str): The generative engine to use ('gemini' or 'ollama'). Defaults to 'gemini'.
        
    Returns:
        str: A comprehensive, synthesized response containing the exact facts from the curriculum docs.
    """
    logger.info(f"Syllabus Tool invoked with query: '{query}' using engine: {engine_type}")
    
    # 1. Dynamically configure the generation engine based on request
    if engine_type.lower() == "gemini":
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY environment variable is completely missing.")
            return "Error: Generation failed because the cloud API authentication key is missing."
        
        Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=api_key)
    else:
        # Fallback to Ollama if explicitly requested or if cloud keys are omitted
        from llama_index.llms.ollama import Ollama
        Settings.llm = Ollama(model="llama3", request_timeout=60.0)

    # 2. Resolve paths dynamically relative to the runtime environment
    # Since this file sits in patterns/memory_agent/tools/, we navigate up and over
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "planner_executor", "llama_index"))
    storage_dir = os.path.join(base_dir, "local_vector_storage")
    data_dir = os.path.join(base_dir, "knowledge_base")

    try:
        # 3. Load the index using your existing asset
        manager = LocalIndexManager(storage_dir=storage_dir)
        index = manager.build_or_load_index(data_dir=data_dir)
        
        # 4. Generate the response
        query_engine = index.as_query_engine(similarity_top_k=1)
        response = query_engine.query(query)
        return str(response)
        
    except Exception as e:
        logger.exception("An exception occurred while querying the vector database.")
        return f"Error executing RAG search: {str(e)}"

# 5. Export the function wrapped into LlamaIndex's official Tool schema
syllabus_rag_tool = FunctionTool.from_defaults(
    fn=query_syllabus,
    name="query_syllabus",
    description="Search and retrieve verified information from the course syllabus and week-by-week lesson goals."
)