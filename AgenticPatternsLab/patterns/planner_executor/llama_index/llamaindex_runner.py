import os
import logging
from index_manager import LocalIndexManager
# 1. Using the modern Scenario A imports
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

# Initialize clean logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AgenticLab.Runner")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(base_dir, "knowledge_base")
    storage_directory = os.path.join(base_dir, "local_vector_storage")

    logger.info("--- Starting Cloud LlamaIndex RAG Test (Gemini) ---")

    # 2. Point Settings to Google GenAI with the recommended 2.5-flash model
    logger.info("Configuring cloud generation engine via Gemini (gemini-2.5-flash)...")
    Settings.llm = GoogleGenAI(
        model="gemini-2.5-flash",
        temperature=0.1
    )

    # 3. Instantiate the local manager (handles our cached embeddings)
    manager = LocalIndexManager(storage_dir=storage_directory)

    try:
        # Load the vector index completely locally (reusing your bge-small embeddings)
        index = manager.build_or_load_index(data_dir=data_directory)
        logger.info("✅ Vector Index successfully established.")
        
        # Combine the local retriever chunking with our cloud generator
        query_engine = index.as_query_engine(similarity_top_k=1)
        
        test_query = "What do students learn in week 5?"
        logger.info(f"Dispatching RAG query to cloud model: '{test_query}'")
        
        # Execute the query out to the cloud
        response = query_engine.query(test_query)
        
        print("\n" + "="*50)
        print("SYNTHESIZED CLOUD GEMINI ANSWER:")
        print("="*50)
        print(response)
        print("="*50 + "\n")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()