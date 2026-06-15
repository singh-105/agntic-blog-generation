import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

print(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic = data.get("topic", "")

    if not topic:
        return {"error": "topic is required"}

    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    graph_builder = GraphBuilder(llm)
    graph = graph_builder.setup_graph(usecase="topic")
    state = graph.invoke({"topic": topic})

    return {"data": state}

@app.post("/blogs/yt")
async def create_blog_from_yt(request: Request):
    data = await request.json()
    yt_url = data.get("yt_url", "")

    if not yt_url:
        return {"error": "yt_url is required"}

    groqllm = GroqLLM()
    llm = groqllm.get_llm()

    graph_builder = GraphBuilder(llm)
    graph = graph_builder.setup_graph(usecase="youtube")
    state = graph.invoke({"yt_url": yt_url})

    return {"data": state}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)