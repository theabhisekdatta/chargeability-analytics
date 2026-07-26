from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent.graph_builder import build_graph


app = FastAPI(
    title="Chargeability Analytics Agent",
    description="Agentic Chargeability Analytics using LangGraph and MCP",
    version="1.0.0",
)


# Build the graph once when the application starts
graph = build_graph()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def root():

    return {
        "message": "Chargeability Analytics Agent is running",
        "status": "healthy",
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

    try:

        result = graph.invoke(
            {
                "question": request.question,
                "attempts": 0,
            },
            config={
                "recursion_limit": 20
            },
        )

        return QueryResponse(
            question=request.question,
            answer=result.get(
                "final_answer",
                "No answer generated."
            ),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "fastapi_main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )