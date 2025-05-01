from fastapi import HTTPException
from typing import Dict, Any, Optional
import traceback
import logging
import json

logger = logging.getLogger(__name__)

class CodeExplorerError(Exception):
    """Base exception class for Code Explorer errors"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

def handle_exception(e: Exception) -> HTTPException:
    """Convert exceptions to appropriate HTTP responses"""
    if isinstance(e, CodeExplorerError):
        logger.error(f"Application error: {e.message}", exc_info=True)
        return HTTPException(
            status_code=e.status_code,
            detail={
                "message": e.message,
                "details": e.details
            }
        )
    
    # For other exceptions, return a 500 error
    error_id = logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    
    return HTTPException(
        status_code=500,
        detail={
            "message": "An unexpected error occurred",
            "error_id": str(error_id)
        }
    )

class ValidationError(CodeExplorerError):
    """Error for invalid input data"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)

class ExternalAPIError(CodeExplorerError):
    """Error when external APIs fail"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=502, details=details)

class ResourceNotFoundError(CodeExplorerError):
    """Error when a requested resource is not found"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)