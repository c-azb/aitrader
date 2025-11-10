
# from dotenv import load_dotenv

# load_dotenv('C:/env/.env')

from src.API import graph_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(graph_router.graph_router)

@app.get('/')
def welcome():
    return {'msg':'Welcome to AI agent trader!'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#"http://localhost:5173","http://127.0.0.1:5173","http://localhost:61936"
    # allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)