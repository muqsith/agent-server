from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from homework import handle_homework_query

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint: Hello
@app.get("/api/ping")
def hello():
    return JSONResponse({"message": "Hello from API"})

# API Endpoint: Chat
@app.post("/api/chat/homework")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    airesponse = await handle_homework_query(message)
    return JSONResponse({"message": airesponse})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8502, reload=True)
