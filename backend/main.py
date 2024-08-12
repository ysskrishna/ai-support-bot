from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from dotenv import load_dotenv
load_dotenv()
from src.routers.chat import router as chat_router

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

app.include_router(chat_router, prefix="/chat", tags=["chat"])



@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return """
    <html>
    <head>
        <title>AI Support Bot</title>
    </head>
    <body>
        <h1>AI Support Bot</h1>
    </body>
    </html>
    """

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8081)