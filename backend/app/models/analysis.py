from pydantic import BaseModel
from typing import Optional

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    code_snippet_id: Optional[str] = None
    test_mode: Optional[bool] = False

class CodeAnalysisResponse(BaseModel):
    time_complexity: str
    space_complexity: str
    explanation: str