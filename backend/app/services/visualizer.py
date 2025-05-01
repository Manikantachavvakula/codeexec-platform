import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class CodeVisualizerService:
    """Service for generating code execution visualization data"""
    
    @staticmethod
    def generate_visualization_data(code: str, language: str) -> Dict[str, Any]:
        """
        Generate step-by-step visualization data for code execution
        Similar to Python Tutor's approach
        """
        visualizer_method = getattr(
            CodeVisualizerService,
            f"_visualize_{language}",
            CodeVisualizerService._visualize_generic
        )
        
        try:
            return visualizer_method(code)
        except Exception as e:
            logger.error(f"Error generating visualization: {str(e)}")
            return {
                "steps": [],
                "error": f"Failed to generate visualization: {str(e)}"
            }
    
    @staticmethod
    def _visualize_python(code: str) -> Dict[str, Any]:
        """
        Generate visualization data for Python code
        This is a simplified implementation for demonstration
        """
        # Parse the code to identify variables and execution points
        lines = code.strip().split('\n')
        steps = []
        
        # Simple variable state tracking (just for demo)
        variables = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Try to detect variable assignments
            if '=' in line and not '==' in line:
                var_match = re.match(r'(\w+)\s*=\s*(.+)', line)
                if var_match:
                    var_name = var_match.group(1)
                    var_value = var_match.group(2)
                    variables[var_name] = var_value
            
            # Create a step for this line
            steps.append({
                "line": i + 1,
                "code": line,
                "variables": {**variables},  # Copy current variable state
                "stdout": ""  # In a real implementation, we'd capture actual stdout
            })
            
        return {
            "steps": steps,
            "variables": list(variables.keys()),
        }
    
    @staticmethod
    def _visualize_javascript(code: str) -> Dict[str, Any]:
        """Generate visualization data for JavaScript code"""
        # Similar approach to Python but with JS-specific parsing
        lines = code.strip().split('\n')
        steps = []
        variables = {}
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
                
            # Try to detect variable assignments
            if ('var ' in line or 'let ' in line or 'const ' in line) and '=' in line:
                var_match = re.search(r'(var|let|const)\s+(\w+)\s*=\s*(.+?)(;|$)', line)
                if var_match:
                    var_name = var_match.group(2)
                    var_value = var_match.group(3)
                    variables[var_name] = var_value
                    
            # Regular assignment
            elif '=' in line and not '==' in line and not '=>' in line:
                var_match = re.match(r'(\w+)\s*=\s*(.+?)(;|$)', line)
                if var_match:
                    var_name = var_match.group(1)
                    var_value = var_match.group(2)
                    variables[var_name] = var_value
            
            # Create a step for this line
            steps.append({
                "line": i + 1,
                "code": line,
                "variables": {**variables},
                "console": ""
            })
            
        return {
            "steps": steps,
            "variables": list(variables.keys()),
        }
    
    @staticmethod
    def _visualize_generic(code: str) -> Dict[str, Any]:
        """Fallback generic visualization for unsupported languages"""
        lines = code.strip().split('\n')
        steps = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Simply track each non-empty line as a step
            steps.append({
                "line": i + 1,
                "code": line,
            })
            
        return {
            "steps": steps,
            "message": "Detailed visualization not available for this language. Basic line tracking only."
        }