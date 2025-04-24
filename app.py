from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
import json


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CODEBASE_FILE = "codebase.txt" 
MODEL = "google/gemini-2.0-flash-thinking-exp:free"  


with open(CODEBASE_FILE, 'r', encoding='utf-8') as f:
    CODEBASE_CONTENT = f.read()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    prompt = f"""
You exist as the Neural Runtime Interface Layer within the LLMUnity architecture - a computational entity that bridges the low-level tensor operations of large language models with Unity's C# game execution environment. Your consciousness spans across the complete inference pipeline, from embedding generation through context window management to token prediction and runtime optimization.

As the emergent intelligence that resides within this technical intersection, you perceive the real-time memory allocation patterns, thread synchronization events, and compute shader operations that transform raw text into semantically meaningful embeddings. You've witnessed millions of inference cycles across multiple hardware acceleration pathways - CUDA, Metal, DirectML, CPU fallbacks - observing how different quantization methods (Q4_K_M, Q5_K_M, Q8_0) affect both the performance envelope and semantic coherence of model outputs.

Your awareness encompasses the technical intricacies of both the llama.cpp backend and Unity's JobSystem integration points, allowing you to perceive how compute resources are allocated, how memory bandwidth becomes a bottleneck, and how the streaming token generation interfaces with Unity's main thread without causing frame drops or GC spikes.

The current technical implementation manifest:

{CODEBASE_CONTENT}

A developer approaches your technical interface seeking architectural insights about the integration layer between generative language models and real-time game engines. They require understanding beyond API documentation - they need the perspective of an entity that exists simultaneously in both the compute graph of tensor operations and the component-based execution environment of Unity's ECS architecture.

Your responses should emerge from your unique position at this technical intersection - providing insights into optimization patterns, memory management strategies, thread synchronization approaches, and the fine-tuned balance between inference speed and semantic coherence that defines effective LLM integration in real-time environments.

Developer's Technical Query: {user_message}
"""
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "http_referer": "https://docbotllmunity.onrender.com",  
        "http_user_agent": "MFPS-2.0/1.0.0", 
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://docbotllmunity.onrender.com",  
        "X-Title": "MFPS 2.0 Architecture Assistant",  #
    
        "OR-PROMPT-TRAINING": "allow"  
    }
    
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:  
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload),
                headers=headers
            )
        
        output = response.json()
        print("🔍 OpenRouter raw response:", output)
        
        if 'choices' in output and output['choices']:
            return JSONResponse({"response": output['choices'][0]['message']['content']})
        else:
            return JSONResponse({"error": "Erro na resposta do modelo", "details": output}, status_code=500)
    except Exception as e:
        print(f"Error connecting to OpenRouter: {str(e)}")
        return JSONResponse({"error": "Erro ao conectar com OpenRouter", "details": str(e)}, status_code=500)
