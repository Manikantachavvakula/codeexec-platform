from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.models.code_execution import CodeExecutionRequest
from app.services.visualizer import CodeVisualizerService
from app.utils.language_utils import LanguageUtils

router = APIRouter(prefix="/visualize", tags=["code-visualization"])

@router.post("/generate")
async def generate_visualization(
    request: CodeExecutionRequest
) -> Dict[str, Any]:
    """Generate visualization data for step-by-step code execution"""
    try:
        visualization_data = CodeVisualizerService.generate_visualization_data(
            request.code, 
            request.language
        )
        
        return visualization_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating visualization: {str(e)}")

@router.get("/templates/{language}")
async def get_visualization_template(
    language: str
) -> Dict[str, Any]:
    """Get code templates optimized for visualization"""
    try:
        # Return appropriate template for visualization
        boilerplate = LanguageUtils.get_boilerplate(language)
        
        # Add visualization-friendly examples
        if language == "python":
            examples = [
                {
                    "name": "Simple Loop",
                    "code": "# Simple loop example\nn = 5\nsum = 0\nfor i in range(n):\n    sum += i\n    print(f\"Current sum: {sum}\")\nprint(f\"Final sum: {sum}\")"
                },
                {
                    "name": "Recursive Factorial",
                    "code": "# Recursive factorial\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n\nresult = factorial(5)\nprint(f\"Factorial of 5 is {result}\")"
                }
            ]
        elif language in ["javascript", "typescript"]:
            examples = [
                {
                    "name": "Array Operations",
                    "code": "// Array operations example\nconst numbers = [1, 2, 3, 4, 5];\nlet sum = 0;\n\nfor (let i = 0; i < numbers.length; i++) {\n    sum += numbers[i];\n    console.log(`Current sum: ${sum}`);\n}\n\nconsole.log(`Final sum: ${sum}`);"
                },
                {
                    "name": "Bubble Sort",
                    "code": "// Bubble sort implementation\nfunction bubbleSort(arr) {\n    const n = arr.length;\n    for (let i = 0; i < n; i++) {\n        for (let j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                // Swap elements\n                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];\n            }\n        }\n    }\n    return arr;\n}\n\nconst unsorted = [64, 34, 25, 12, 22];\nconsole.log(`Original array: ${unsorted}`);\nconst sorted = bubbleSort([...unsorted]);\nconsole.log(`Sorted array: ${sorted}`);"
                }
            ]
        else:
            examples = []
        
        return {
            "language": language,
            "boilerplate": boilerplate,
            "examples": examples
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting visualization template: {str(e)}")