import os
import sys
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool 


# Absolute anchoring to ensure deep dependencies resolve seamlessly
# even though it's running via the -m option from the command line.
# this is being done for defensive programming
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from patterns.memory_agent.tools.syllabus_rag_tool import query_syllabus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgenticLab.API")

app = FastAPI(
    title="Agentic Patterns Lab API",
    description="Asynchronous backend routing engine for educational orchestration and tool execution.",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str = Field(..., example="What do students learn in week 5?")
    engine_type: str = Field(default="gemini", example="gemini")

class QueryResponse(BaseModel):
    query: str
    engine_type: str
    response: str

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/query", response_model=QueryResponse)
async def handle_syllabus_query(payload: QueryRequest):
    logger.info(f"Received async API request: '{payload.query}' via engine: '{payload.engine_type}'")
    
    try:
        # Offload the blocking RAG operation to an external thread pool safely
        result = await run_in_threadpool(
            query_syllabus, 
            query=payload.query, 
            engine_type=payload.engine_type
        )
        
        if result.startswith("Error"):
            raise HTTPException(status_code=500, detail=result)
            
        return QueryResponse(
            query=payload.query,
            engine_type=payload.engine_type,
            response=result
        )
    except Exception as e:
        logger.exception("An unhandled exception occurred during API route execution.")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")