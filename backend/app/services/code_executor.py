import requests
import logging
from typing import Dict, Any, Optional, List

from app.config import PISTON_API_URL, SUPPORTED_LANGUAGES
from app.models.code_execution import CodeExecutionRequest, CodeExecutionResponse

logger = logging.getLogger(__name__)

class CodeExecutionService:
    """Service to handle code execution via Piston API"""
    
    @staticmethod
    async def execute_code(request: CodeExecutionRequest) -> CodeExecutionResponse:
        """Execute code via Piston API and return results"""
        if request.language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language '{request.language}' not supported")
        
        # Prepare payload for Piston API
        payload = {
            "language": request.language,
            "version": "latest",
            "files": [{"content": request.code}],
            "stdin": request.stdin or "",
            "args": request.args or [],
            "compile_timeout": 10000,
            "run_timeout": 5000,
        }
        
        try:
            # Execute code via Piston API
            response = requests.post(f"{PISTON_API_URL}/execute", json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Log execution details
            logger.info(f"Code execution completed for {request.language}")
            if data.get("run", {}).get("stderr"):
                logger.warning(f"Execution produced stderr: {data.get('run', {}).get('stderr')}")
                
            return CodeExecutionResponse(
                output=data.get("run", {}).get("output", ""),
                error=data.get("run", {}).get("stderr", ""),
                compilation_output=data.get("compile", {}).get("output", ""),
                compile_error=data.get("compile", {}).get("stderr", ""),
                execution_time=data.get("run", {}).get("time", 0),
            )
        except requests.RequestException as e:
            logger.error(f"Error executing code: {str(e)}")
            raise ValueError(f"Error executing code: {str(e)}")
    
    @staticmethod
    async def get_language_versions() -> Dict[str, List[str]]:
        """Get available language versions from Piston API"""
        try:
            response = requests.get(f"{PISTON_API_URL}/runtimes")
            response.raise_for_status()
            data = response.json()
            
            # Process and organize language versions
            language_versions = {}
            for runtime in data:
                language = runtime.get("language")
                version = runtime.get("version")
                if language:
                    if language not in language_versions:
                        language_versions[language] = []
                    language_versions[language].append(version)
            
            return language_versions
        except requests.RequestException as e:
            logger.error(f"Error fetching language versions: {str(e)}")
            return {}