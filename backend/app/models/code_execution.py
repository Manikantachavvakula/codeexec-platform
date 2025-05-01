from pydantic import BaseModel
from typing import List, Optional

class CodeExecutionRequest(BaseModel):
    language: str
    code: str
    stdin: Optional[str] = None
    args: Optional[List[str]] = None
    description: Optional[str] = None
    test_mode: Optional[bool] = False  # Flag to prevent DB storage during testing

class CodeExecutionResponse(BaseModel):
    output: str
    error: Optional[str] = None
    compilation_output: Optional[str] = None
    compile_error: Optional[str] = None
    execution_time: float