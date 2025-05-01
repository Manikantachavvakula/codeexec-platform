from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import API_PREFIX, PROJECT_NAME
from app.routers import code_execution, analysis, visualization

app = FastAPI(title=PROJECT_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(code_execution.router, prefix=API_PREFIX)
app.include_router(analysis.router, prefix=API_PREFIX)
app.include_router(visualization.router, prefix=API_PREFIX)

@app.get("/")
def health_check():
    return {"status": "healthy", "service": PROJECT_NAME}

@app.get("/api/info")
def api_info():
    return {
        "name": PROJECT_NAME,
        "routes": [
            {"path": "/api/execute", "methods": ["POST"], "description": "Execute code"},
            {"path": "/api/execute/languages", "methods": ["GET"], "description": "Get supported languages"},
            {"path": "/api/execute/history", "methods": ["GET"], "description": "Get execution history"},
            {"path": "/api/analysis/complexity", "methods": ["POST"], "description": "Analyze code complexity"},
            {"path": "/api/analysis/visualize", "methods": ["POST"], "description": "Generate code visualization"},
            {"path": "/api/visualize/generate", "methods": ["POST"], "description": "Generate visualization data"},
        ]
    }