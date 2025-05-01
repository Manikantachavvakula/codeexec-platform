from typing import Dict
import re
import logging

logger = logging.getLogger(__name__)

class LanguageUtils:
    """Utilities for language-specific operations"""
    
    # Default boilerplate code templates by language
    BOILERPLATE_CODE = {
        "python": "# Python code\n\ndef main():\n    print(\"Hello, World!\")\n\nif __name__ == \"__main__\":\n    main()",
        "javascript": "// JavaScript code\n\nfunction main() {\n    console.log(\"Hello, World!\");\n}\n\nmain();",
        "typescript": "// TypeScript code\n\nfunction main(): void {\n    console.log(\"Hello, World!\");\n}\n\nmain();",
        "java": "// Java code\n\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
        "cpp": "// C++ code\n#include <iostream>\n\nint main() {\n    std::cout << \"Hello, World!\" << std::endl;\n    return 0;\n}",
        "csharp": "// C# code\nusing System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"Hello, World!\");\n    }\n}"
    }
    
    # File extensions by language
    FILE_EXTENSIONS = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "cpp": ".cpp",
        "csharp": ".cs"
    }
    
    @staticmethod
    def get_boilerplate(language: str) -> str:
        """Get boilerplate code for a specific language"""
        return LanguageUtils.BOILERPLATE_CODE.get(language, "// Code goes here")
    
    @staticmethod
    def get_file_extension(language: str) -> str:
        """Get file extension for a specific language"""
        return LanguageUtils.FILE_EXTENSIONS.get(language, ".txt")
    
    @staticmethod
    def detect_language(code: str) -> str:
        """Try to detect programming language from code"""
        # Simple heuristics for language detection
        if re.search(r'import\s+[a-zA-Z0-9_]+|def\s+[a-zA-Z0-9_]+\s*\(|print\s*\(', code):
            return "python"
        elif re.search(r'#include\s*<[a-zA-Z0-9_\.]+>|std::', code):
            return "cpp"
        elif re.search(r'public\s+class|public\s+static\s+void\s+main|System\.out\.println', code):
            return "java"
        elif re.search(r'using\s+System|Console\.WriteLine', code):
            return "csharp"
        elif re.search(r'function\s+[a-zA-Z0-9_]+\s*\(.*\)\s*:\s*[a-zA-Z0-9_]+', code):
            return "typescript"
        elif re.search(r'function\s+[a-zA-Z0-9_]+|console\.log|var\s+|let\s+|const\s+', code):
            return "javascript"
        else:
            return "unknown"
    
    @staticmethod
    def format_output(output: str, language: str) -> str:
        """Format output for display based on language"""
        if not output:
            return ""
            
        if language == "java" and "Error:" in output:
            # Highlight Java errors
            formatted = []
            for line in output.split('\n'):
                if "Error:" in line:
                    formatted.append(f"❌ {line}")
                else:
                    formatted.append(line)
            return '\n'.join(formatted)
        
        return output