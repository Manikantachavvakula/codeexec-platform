import re
import ast
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ComplexityAnalyzer:
    """Analyze code complexity for different programming languages"""
    
    @staticmethod
    def analyze_code_complexity(code: str, language: str) -> Dict[str, Any]:
        """
        Analyze time and space complexity of code based on language-specific heuristics
        """
        # Choose the appropriate analyzer based on language
        analyzer_method = getattr(
            ComplexityAnalyzer,
            f"_analyze_{language}_complexity",
            ComplexityAnalyzer._analyze_generic_complexity
        )
        
        try:
            return analyzer_method(code)
        except Exception as e:
            logger.error(f"Error analyzing complexity: {str(e)}")
            return {
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "explanation": f"Analysis failed: {str(e)}"
            }
    
    @staticmethod
    def _analyze_python_complexity(code: str) -> Dict[str, Any]:
        """
        Analyze Python code complexity using AST parsing
        """
        try:
            tree = ast.parse(code)
            
            # Count loops, function calls, etc.
            class ComplexityVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.function_names = set()
                    self.has_recursion = False
                    self.loop_count = 0
                    self.max_loop_depth = 0
                    self.current_loop_depth = 0
                    self.sort_calls = 0
                
                def visit_FunctionDef(self, node):
                    self.function_names.add(node.name)
                    self.generic_visit(node)
                    
                    # Check for recursion
                    for n in ast.walk(node):
                        if isinstance(n, ast.Call) and getattr(n.func, 'id', None) == node.name:
                            self.has_recursion = True
                
                def visit_For(self, node):
                    self.loop_count += 1
                    self.current_loop_depth += 1
                    self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
                    self.generic_visit(node)
                    self.current_loop_depth -= 1
                
                def visit_While(self, node):
                    self.loop_count += 1
                    self.current_loop_depth += 1
                    self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
                    self.generic_visit(node)
                    self.current_loop_depth -= 1
                
                def visit_Call(self, node):
                    func_name = getattr(getattr(node, 'func', None), 'id', None)
                    if func_name in ['sort', 'sorted']:
                        self.sort_calls += 1
                    self.generic_visit(node)
            
            visitor = ComplexityVisitor()
            visitor.visit(tree)
            
            # Determine complexity based on the found patterns
            time_complexity = "O(1)"  # Default - constant time
            space_complexity = "O(1)"  # Default - constant space
            explanation = "Simple operations with no loops or recursion."
            
            # Determine time complexity
            if visitor.has_recursion:
                time_complexity = "O(2^n) or O(n!)"
                explanation = "Contains recursive function calls which can lead to exponential time complexity."
            elif visitor.max_loop_depth >= 3:
                time_complexity = "O(n³)"
                explanation = "Contains triply nested loops which indicates cubic time complexity."
            elif visitor.max_loop_depth == 2:
                time_complexity = "O(n²)"
                explanation = "Contains nested loops which indicates quadratic time complexity."
            elif visitor.max_loop_depth == 1:
                if visitor.sort_calls > 0:
                    time_complexity = "O(n log n)"
                    explanation = "Contains sorting operations which typically have n log n time complexity."
                else:
                    time_complexity = "O(n)"
                    explanation = "Contains single loops which indicates linear time complexity."
            
            # Determine space complexity - simple heuristic
            if "append" in code or "extend" in code or "=" in code:
                space_complexity = "O(n)"
                if explanation != "Simple operations with no loops or recursion.":
                    explanation += " Uses data structures that grow with input size, indicating linear space complexity."
                else:
                    explanation = "Uses data structures that grow with input size, indicating linear space complexity."
            
            return {
                "time_complexity": time_complexity,
                "space_complexity": space_complexity,
                "explanation": explanation
            }
            
        except SyntaxError:
            # If AST parsing fails, fall back to regex-based analysis
            return ComplexityAnalyzer._analyze_generic_complexity(code)
    
    @staticmethod
    def _analyze_javascript_complexity(code: str) -> Dict[str, Any]:
        """
        Analyze JavaScript/TypeScript code complexity using regex patterns
        """
        # Look for nested loops
        for_loops = len(re.findall(r'for\s*\(', code))
        while_loops = len(re.findall(r'while\s*\(', code))
        forEach_loops = len(re.findall(r'\.forEach', code))
        map_calls = len(re.findall(r'\.map\s*\(', code))
        
        total_loops = for_loops + while_loops + forEach_loops + map_calls
        nested_loops = 0
        
        # Check for nested loops (simple heuristic)
        if 'for' in code and 'for' in code.split('for', 1)[1]:
            nested_loops += 1
        
        if 'while' in code and 'while' in code.split('while', 1)[1]:
            nested_loops += 1
            
        # Check for sorting or binary search operations
        has_sort = len(re.findall(r'\.sort\s*\(', code)) > 0
        
        # Determine complexity
        time_complexity = "O(1)"  # Default
        space_complexity = "O(1)"  # Default
        explanation = "Simple operations with no loops or recursion."
        
        if nested_loops > 0:
            time_complexity = "O(n²)"
            explanation = "Contains nested loops which indicates quadratic time complexity."
        elif total_loops > 0:
            if has_sort:
                time_complexity = "O(n log n)"
                explanation = "Contains sorting operations which typically have n log n time complexity."
            else:
                time_complexity = "O(n)"
                explanation = "Contains single loops which indicates linear time complexity."
        
        # Space complexity - simple heuristic
        if "push" in code or "concat" in code or "=" in code:
            space_complexity = "O(n)"
            if explanation != "Simple operations with no loops or recursion.":
                explanation += " Uses data structures that grow with input size, indicating linear space complexity."
            else:
                explanation = "Uses data structures that grow with input size, indicating linear space complexity."
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "explanation": explanation
        }
    
    @staticmethod
    def _analyze_generic_complexity(code: str) -> Dict[str, Any]:
        """
        Generic complexity analysis for languages without specific analyzers
        """
        # Simple pattern-based analysis
        nested_loops = 0
        has_loops = False
        
        # Common loop patterns in various languages
        loop_patterns = [
            r'for\s*\(', r'while\s*\(', r'foreach', r'\.forEach',
            r'\.map\s*\(', r'\.reduce\s*\(', r'\.filter\s*\(',
        ]
        
        # Check for loops
        for pattern in loop_patterns:
            if re.search(pattern, code):
                has_loops = True
                break
        
        # Simplistic check for nested loops
        if has_loops:
            for pattern in loop_patterns:
                matches = re.findall(pattern, code)
                if len(matches) > 1:
                    nested_loops = 1
                    break
        
        # Check for common sorting functions
        has_sort = any(sort_func in code for sort_func in [
            '.sort(', 'sort(', 'sorted(', 'qsort', 'mergesort'
        ])
        
        # Determine complexity
        time_complexity = "O(1)"  # Default
        space_complexity = "O(1)"  # Default
        explanation = "Based on general code patterns. Detailed analysis requires language-specific parsing."
        
        if nested_loops > 0:
            time_complexity = "O(n²)"
            explanation = "Contains what appear to be nested loops, suggesting quadratic time complexity."
        elif has_loops:
            if has_sort:
                time_complexity = "O(n log n)"
                explanation = "Contains sorting operations which typically have n log n time complexity."
            else:
                time_complexity = "O(n)"
                explanation = "Contains loops which suggests linear time complexity."
        
        # Very basic space complexity heuristic
        if any(x in code for x in [
            'new ', 'malloc', 'append', 'push', 'add', 'insert', 'emplace'
        ]):
            space_complexity = "O(n)"
            explanation += " Uses operations that may grow with input size, suggesting linear space complexity."
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "explanation": explanation
        }