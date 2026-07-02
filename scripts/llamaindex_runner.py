import logging
from utils.logging import create_logger  # Changed to match your exact utility function
from patterns.memory_agent.tools.syllabus_rag_tool import query_syllabus

def main():
    # Initialize basic python logging configurations
    logging.basicConfig(level=logging.INFO)
    
    # Trigger your custom log directory creation utility
    create_logger(prefix="llamaindex_tool")
    
    logger = logging.getLogger("AgenticLab.Runner")
    logger.info("--- Starting Tool Verification Runner ---")

    test_query = "What do students learn in week 5?"
    logger.info(f"Testing local tool execution with query: '{test_query}'")
    
    # Execute tool wrapper
    answer = query_syllabus(test_query, engine_type="gemini")
    
    print("\n" + "="*50)
    print("TOOL WRAPPER OUTPUT GENERATION:")
    print("="*50)
    print(answer)
    print("="*50 + "\n")

if __name__ == "__main__":
    main()