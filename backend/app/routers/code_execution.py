from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional, List

from app.models.code_execution import CodeExecutionRequest, CodeExecutionResponse
from app.services.code_executor import CodeExecutionService
from app.config import SUPPORTED_LANGUAGES

router = APIRouter(prefix="/execute", tags=["code-execution"])

@router.get("/languages")
async def get_supported_languages() -> Dict[str, List[str]]:
    """Return list of supported programming languages"""
    try:
        language_versions = await CodeExecutionService.get_language_versions()
        return {"languages": language_versions.keys()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching language versions: {str(e)}")

@router.post("/")
async def execute_code(request: CodeExecutionRequest) -> CodeExecutionResponse:
    """Execute code via Piston API and return results"""
    try:
        if request.language not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400, 
                detail=f"Language '{request.language}' not supported. Supported languages: {SUPPORTED_LANGUAGES}"
            )
        
        execution_result = await CodeExecutionService.execute_code(request)
        return execution_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing code: {str(e)}")