from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.models.analysis import CodeAnalysisRequest, CodeAnalysisResponse
from app.services.complexity_analyzer import ComplexityAnalyzer
from app.utils.language_utils import LanguageUtils

router = APIRouter(prefix="/analysis", tags=["code-analysis"])

@router.post("/complexity")
async def analyze_complexity(request: CodeAnalysisRequest) -> CodeAnalysisResponse:
    """Analyze the time and space complexity of code"""
    try:
        complexity_data = ComplexityAnalyzer.analyze_code_complexity(
            request.code, 
            request.language
        )
        
        return CodeAnalysisResponse(
            time_complexity=complexity_data["time_complexity"],
            space_complexity=complexity_data["space_complexity"],
            explanation=complexity_data["explanation"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")

@router.post("/visualize")
async def visualize_code_execution(request: CodeAnalysisRequest) -> Dict[str, Any]:
    """Generate visualization data for step-by-step code execution"""
    try:
        from app.services.visualizer import CodeVisualizerService
        
        visualization_data = CodeVisualizerService.generate_visualization_data(
            request.code,
            request.language
        )
        
        return visualization_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code visualization: {str(e)}")

@router.post("/optimize")
async def suggest_optimizations(request: CodeAnalysisRequest) -> Dict[str, Any]:
    """Analyze code for potential optimizations and suggest improvements"""
    try:
        # Analyze complexity first
        complexity_data = ComplexityAnalyzer.analyze_code_complexity(
            request.code, 
            request.language
        )
        
        # Look for optimization opportunities based on complexity
        optimization_suggestions = []
        
        # Check time complexity optimizations
        if complexity_data["time_complexity"] in ["O(n²)", "O(n³)", "O(2^n)", "O(n!)"]:
            if request.language == "python":
                if "sorted(" in request.code or ".sort()" in request.code:
                    optimization_suggestions.append({
                        "type": "time_complexity",
                        "issue": "Using sort in a nested loop creates O(n² log n) complexity",
                        "suggestion": "Consider moving the sort operation outside the loop if possible"
                    })
                
                if "for" in request.code and "for" in request.code.split("for", 1)[1]:
                    # Check for common inefficient patterns in nested loops
                    if "append" in request.code or "extend" in request.code:
                        optimization_suggestions.append({
                            "type": "time_complexity",
                            "issue": "Nested loops with list modifications can be inefficient",
                            "suggestion": "Consider using list comprehensions or NumPy for better performance"
                        })
            
            elif request.language in ["javascript", "typescript"]:
                if ".map" in request.code and ".filter" in request.code:
                    optimization_suggestions.append({
                        "type": "time_complexity",
                        "issue": "Chaining .map() and .filter() creates multiple iterations",
                        "suggestion": "Consider using .reduce() to combine these operations into a single pass"
                    })
        
        # Check space complexity optimizations
        if complexity_data["space_complexity"] in ["O(n)", "O(n²)"]:
            if request.language == "python":
                if "append" in request.code and "range" in request.code:
                    optimization_suggestions.append({
                        "type": "space_complexity",
                        "issue": "Building a list incrementally with append() uses extra memory",
                        "suggestion": "Consider using a list comprehension to initialize the list directly"
                    })
            
            elif request.language in ["javascript", "typescript"]:
                if ".push" in request.code and "for" in request.code:
                    optimization_suggestions.append({
                        "type": "space_complexity",
                        "issue": "Building an array with push() in a loop uses extra memory",
                        "suggestion": "Consider using Array.from() or .map() to create the array directly"
                    })
        
        # Add algorithm-specific suggestions
        if "bubble sort" in request.code.lower() or (("for" in request.code and "swap" in request.code.lower()) and complexity_data["time_complexity"] == "O(n²)"):
            optimization_suggestions.append({
                "type": "algorithm",
                "issue": "Bubble sort has average time complexity of O(n²)",
                "suggestion": "Consider using a more efficient sorting algorithm like Quick Sort (O(n log n))"
            })
        
        if "factorial" in request.code.lower() and "recursion" in complexity_data["explanation"].lower():
            optimization_suggestions.append({
                "type": "algorithm",
                "issue": "Recursive factorial implementation can cause stack overflow for large inputs",
                "suggestion": "Consider using an iterative approach with a loop instead of recursion"
            })
            
        # Return optimization results
        return {
            "complexity": {
                "time_complexity": complexity_data["time_complexity"],
                "space_complexity": complexity_data["space_complexity"],
            },
            "optimization_suggestions": optimization_suggestions,
            "optimizable": len(optimization_suggestions) > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code for optimizations: {str(e)}")

@router.post("/patterns")
async def detect_code_patterns(request: CodeAnalysisRequest) -> Dict[str, Any]:
    """Analyze code to detect common patterns and anti-patterns"""
    try:
        patterns_detected = []
        anti_patterns_detected = []
        
        # Detect language-specific patterns
        if request.language == "python":
            # Check for pythonic patterns
            if "list(map(" in request.code or "filter(" in request.code:
                patterns_detected.append({
                    "name": "Functional Programming",
                    "description": "Using map() and filter() for functional operations"
                })
            
            if any(x in request.code for x in ["[x for x in", "dict(", "{k: v for"]):
                patterns_detected.append({
                    "name": "Comprehensions",
                    "description": "Using list, dict, or set comprehensions for concise data transformation"
                })
                
            # Check for anti-patterns
            if "global " in request.code:
                anti_patterns_detected.append({
                    "name": "Global Variables",
                    "description": "Using global variables can lead to hard-to-debug code and side effects",
                    "suggestion": "Consider using function parameters or class attributes instead"
                })
                
            if "except:" in request.code and not "except Exception:" in request.code:
                anti_patterns_detected.append({
                    "name": "Bare Except",
                    "description": "Using bare 'except:' catches all exceptions, including KeyboardInterrupt",
                    "suggestion": "Use 'except Exception:' or catch specific exceptions"
                })
                
        elif request.language in ["javascript", "typescript"]:
            # Check for JS patterns
            if "=>" in request.code:
                patterns_detected.append({
                    "name": "Arrow Functions",
                    "description": "Using arrow functions for concise function syntax"
                })
                
            if "async" in request.code and "await" in request.code:
                patterns_detected.append({
                    "name": "Async/Await",
                    "description": "Using async/await for handling asynchronous operations"
                })
                
            # Check for anti-patterns
            if "var " in request.code:
                anti_patterns_detected.append({
                    "name": "Var Usage",
                    "description": "'var' has function scope which can lead to unexpected behavior",
                    "suggestion": "Use 'let' or 'const' which have block scope"
                })
                
            if "==" in request.code:
                anti_patterns_detected.append({
                    "name": "Loose Equality",
                    "description": "Using '==' allows type coercion and can lead to unexpected results",
                    "suggestion": "Use '===' for strict equality comparison"
                })
        
        # Check language-agnostic patterns
        function_count = 0
        if request.language == "python":
            function_count = request.code.count("def ")
        elif request.language in ["javascript", "typescript"]:
            function_count = request.code.count("function ")
            function_count += sum(1 for _ in re.finditer(r'=\s*\([^)]*\)\s*=>', request.code))
            
        if function_count > 5:
            patterns_detected.append({
                "name": "Modularity",
                "description": "Code is broken down into multiple functions for better organization"
            })
        
        if request.code.count("\n") > 50 and function_count <= 1:
            anti_patterns_detected.append({
                "name": "Long Function",
                "description": "Long functions without breakdown into smaller functions",
                "suggestion": "Break down large functions into smaller, focused functions"
            })
            
        # Return detected patterns
        return {
            "patterns": patterns_detected,
            "anti_patterns": anti_patterns_detected,
            "recommendations": _generate_pattern_recommendations(patterns_detected, anti_patterns_detected, request.language)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting code patterns: {str(e)}")

@router.post("/security")
async def security_analysis(request: CodeAnalysisRequest) -> Dict[str, Any]:
    """Analyze code for potential security vulnerabilities"""
    try:
        vulnerabilities = []
        
        # Python-specific security checks
        if request.language == "python":
            if "eval(" in request.code:
                vulnerabilities.append({
                    "severity": "high",
                    "type": "code_injection",
                    "description": "Using eval() on user input can allow arbitrary code execution",
                    "line_hint": next((i+1 for i, line in enumerate(request.code.split('\n')) if "eval(" in line), None)
                })
                
            if "subprocess" in request.code and "shell=True" in request.code:
                vulnerabilities.append({
                    "severity": "high",
                    "type": "command_injection",
                    "description": "subprocess with shell=True can lead to command injection vulnerabilities",
                    "line_hint": next((i+1 for i, line in enumerate(request.code.split('\n')) if "shell=True" in line), None)
                })
                
            if "pickle.load" in request.code:
                vulnerabilities.append({
                    "severity": "high",
                    "type": "deserialization",
                    "description": "Deserializing pickle data can lead to arbitrary code execution",
                    "line_hint": next((i+1 for i, line in enumerate(request.code.split('\n')) if "pickle.load" in line), None)
                })
                
            # SQL Injection checks
            if any(db in request.code.lower() for db in ["sqlite", "mysql", "postgresql"]) and "%" in request.code and "execute" in request.code:
                vulnerabilities.append({
                    "severity": "high",
                    "type": "sql_injection",
                    "description": "String formatting in SQL queries can lead to SQL injection",
                    "line_hint": next((i+1 for i, line in enumerate(request.code.split('\n')) if "execute" in line and "%" in line), None)
                })
                
        # JavaScript/TypeScript specific checks
        elif request.language in ["javascript", "typescript"]:
            if "eval(" in request.code or "new Function(" in request.code:
                vulnerabilities.append({
                    "severity": "high",
                    "type": "code_injection",
                    "description": "Using eval() or new Function() on user input can allow arbitrary code execution",
                    "line_hint": next((i+1 for i, line in enumerate(request.code.split('\n')) if "eval(" in line or "new Function(" in line), None)
                })
                
            if "innerHTML" in request.code:
                vulnerabilities.append({
                    "severity": "medium",
                    "type": "xss",
                    "description": "Using innerHTML with user input can lead to XSS vulnerabilities",
                    "line_hint": next((i+1 for i, line in enumerate(request.code.split('\n')) if "innerHTML" in line), None)
                })
                
            if "document.write" in request.code:
                vulnerabilities.append({
                    "severity": "medium", 
                    "type": "xss",
                    "description": "document.write can lead to XSS vulnerabilities if used with user input",
                    "line_hint": next((i+1 for i, line in enumerate(request.code.split('\n')) if "document.write" in line), None)
                })
                
        # Return security analysis results
        return {
            "vulnerabilities": vulnerabilities,
            "vulnerability_count": len(vulnerabilities),
            "has_high_severity": any(v["severity"] == "high" for v in vulnerabilities),
            "recommendation": _generate_security_recommendations(vulnerabilities, request.language)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code for security issues: {str(e)}")

@router.post("/quality")
async def code_quality_analysis(request: CodeAnalysisRequest) -> Dict[str, Any]:
    """Analyze code for quality metrics and provide a score"""
    try:
        # Initialize quality metrics
        metrics = {
            "complexity": 0,  # Lower is better
            "maintainability": 0,  # Higher is better
            "readability": 0,  # Higher is better
            "testability": 0,  # Higher is better
            "overall_score": 0  # Higher is better
        }
        
        issues = []
        
        # Get code complexity first
        complexity_data = ComplexityAnalyzer.analyze_code_complexity(
            request.code, 
            request.language
        )
        
        # Calculate complexity score (0-100, lower is better)
        if complexity_data["time_complexity"] == "O(1)":
            metrics["complexity"] = 0
        elif complexity_data["time_complexity"] == "O(log n)":
            metrics["complexity"] = 20
        elif complexity_data["time_complexity"] == "O(n)":
            metrics["complexity"] = 40
        elif complexity_data["time_complexity"] == "O(n log n)":
            metrics["complexity"] = 60
        elif complexity_data["time_complexity"] == "O(n²)":
            metrics["complexity"] = 80
        else:  # O(n³), O(2^n), etc.
            metrics["complexity"] = 100
            
        # Calculate maintainability (0-100, higher is better)
        code_lines = request.code.split('\n')
        total_lines = len(code_lines)
        
        # Count comments
        comment_count = 0
        if request.language == "python":
            comment_count = sum(1 for line in code_lines if line.strip().startswith('#'))
        elif request.language in ["javascript", "typescript", "java", "cpp", "csharp"]:
            comment_count = sum(1 for line in code_lines if line.strip().startswith('//'))
            
        comment_ratio = comment_count / max(total_lines, 1)
        
        # Count functions
        function_count = 0
        if request.language == "python":
            function_count = sum(1 for line in code_lines if line.strip().startswith('def '))
        elif request.language in ["javascript", "typescript"]:
            function_count = sum(1 for line in code_lines if 'function ' in line)
            function_count += sum(1 for line in code_lines if '=>' in line)
            
        # Average function length
        avg_function_length = total_lines / max(function_count, 1)
        
        # Calculate maintainability score
        metrics["maintainability"] = max(0, min(100, 100 - (metrics["complexity"] / 2) - (avg_function_length / 2)))
        
        # If comment ratio is good (between 0.1 and 0.3), improve maintainability
        if 0.1 <= comment_ratio <= 0.3:
            metrics["maintainability"] = min(100, metrics["maintainability"] + 10)
        
        # Calculate readability (0-100, higher is better)
        # Check line length
        long_lines = sum(1 for line in code_lines if len(line.strip()) > 80)
        long_line_ratio = long_lines / max(total_lines, 1)
        
        # Check variable naming
        if request.language == "python":
            snake_case_vars = sum(1 for line in code_lines if re.search(r'[a-z_]+\s*=', line))
            non_snake_vars = sum(1 for line in code_lines if re.search(r'[a-zA-Z]+\s*=', line)) - snake_case_vars
            good_naming = snake_case_vars > non_snake_vars
        else:
            camel_case_vars = sum(1 for line in code_lines if re.search(r'[a-z][a-zA-Z]+\s*=', line))
            non_camel_vars = sum(1 for line in code_lines if re.search(r'[a-zA-Z]+\s*=', line)) - camel_case_vars
            good_naming = camel_case_vars > non_camel_vars
            
        # Calculate readability score
        metrics["readability"] = max(0, min(100, 100 - (long_line_ratio * 50) + (20 if good_naming else 0)))
        
        # If comment ratio is too low, reduce readability
        if comment_ratio < 0.1:
            metrics["readability"] = max(0, metrics["readability"] - 20)
            issues.append({
                "type": "comment_ratio",
                "severity": "medium",
                "description": "Code has too few comments relative to code lines",
                "suggestion": "Add more comments to explain logic and complex parts"
            })
        
        # Add issues for poor readability factors
        if long_line_ratio > 0.2:
            issues.append({
                "type": "line_length",
                "severity": "medium",
                "description": f"{int(long_line_ratio * 100)}% of lines are longer than 80 characters",
                "suggestion": "Break long lines into multiple lines to improve readability"
            })
            
        if not good_naming:
            issues.append({
                "type": "naming_convention",
                "severity": "medium",
                "description": "Many variables don't follow standard naming conventions",
                "suggestion": f"Use {'snake_case' if request.language == 'python' else 'camelCase'} for variables"
            })
            
        # Calculate testability (0-100, higher is better)
        # Factors: function size, cyclomatic complexity, dependencies
        
        # Estimate cyclomatic complexity by counting branches
        if_count = sum(1 for line in code_lines if ' if ' in line)
        elif_count = sum(1 for line in code_lines if ' elif ' in line or ' else if ' in line)
        for_count = sum(1 for line in code_lines if ' for ' in line)
        while_count = sum(1 for line in code_lines if ' while ' in line)
        
        cyclomatic_complexity = 1 + if_count + elif_count + for_count + while_count
        
        # Calculate testability score
        metrics["testability"] = max(0, min(100, 100 - (metrics["complexity"] / 2) - (cyclomatic_complexity * 5 / max(function_count, 1))))
        
        # If functions are too large, reduce testability
        if avg_function_length > 25:
            metrics["testability"] = max(0, metrics["testability"] - 20)
            issues.append({
                "type": "function_size",
                "severity": "high",
                "description": f"Average function length is {int(avg_function_length)} lines",
                "suggestion": "Break large functions into smaller, more focused functions"
            })
        
        # Overall score (weighted average)
        metrics["overall_score"] = (
            (metrics["complexity"] * 0.3) +  # Complexity is reversed, so higher is worse
            (metrics["maintainability"] * 0.25) +
            (metrics["readability"] * 0.25) +
            (metrics["testability"] * 0.2)
        )
        
        # Reverse complexity for final score (make higher better)
        metrics["complexity"] = 100 - metrics["complexity"]
        
        return {
            "metrics": metrics,
            "issues": issues,
            "summary": _generate_quality_summary(metrics, issues)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code quality: {str(e)}")

# Helper functions
def _generate_pattern_recommendations(patterns, anti_patterns, language):
    """Generate recommendations based on detected patterns and anti-patterns"""
    recommendations = []
    
    if anti_patterns:
        for ap in anti_patterns:
            if "suggestion" in ap:
                recommendations.append(ap["suggestion"])
    
    if language == "python":
        if not any(p["name"] == "Comprehensions" for p in patterns):
            recommendations.append("Consider using list/dict comprehensions for more concise code")
            
    elif language in ["javascript", "typescript"]:
        if not any(p["name"] == "Arrow Functions" for p in patterns):
            recommendations.append("Consider using arrow functions for more concise code")
    
    if not recommendations:
        recommendations.append("Code follows good practices for the language")
        
    return recommendations

def _generate_security_recommendations(vulnerabilities, language):
    """Generate security recommendations based on detected vulnerabilities"""
    if not vulnerabilities:
        return "No security issues detected"
        
    recommendations = []
    
    for vuln in vulnerabilities:
        if vuln["type"] == "code_injection":
            if language == "python":
                recommendations.append("Avoid using eval() on user input. Use safer alternatives like ast.literal_eval() for parsing")
            else:
                recommendations.append("Avoid using eval() or new Function() on user input. Use JSON.parse() for parsing data")
                
        elif vuln["type"] == "command_injection":
            recommendations.append("Avoid using shell=True with subprocess. Pass arguments as a list instead")
            
        elif vuln["type"] == "deserialization":
            recommendations.append("Avoid using pickle with untrusted data. Use JSON or other safer serialization formats")
            
        elif vuln["type"] == "sql_injection":
            recommendations.append("Use parameterized queries or an ORM instead of string formatting for SQL queries")
            
        elif vuln["type"] == "xss":
            recommendations.append("Use textContent instead of innerHTML or document.write. Consider using a framework that automatically escapes output")
    
    return ". ".join(recommendations)

def _generate_quality_summary(metrics, issues):
    """Generate a summary of code quality based on metrics and issues"""
    overall_score = metrics["overall_score"]
    
    if overall_score >= 80:
        quality = "Excellent"
    elif overall_score >= 60:
        quality = "Good"
    elif overall_score >= 40:
        quality = "Moderate"
    else:
        quality = "Needs improvement"
        
    summary = f"Code quality is {quality} with an overall score of {int(metrics['overall_score'])}/100."
    
    # Add top strengths
    strengths = []
    if metrics["complexity"] >= 70:
        strengths.append("good algorithmic efficiency")
    if metrics["maintainability"] >= 70:
        strengths.append("high maintainability")
    if metrics["readability"] >= 70:
        strengths.append("good readability")
    if metrics["testability"] >= 70:
        strengths.append("high testability")
        
    if strengths:
        summary += f" Strengths include {', '.join(strengths)}."
    
    # Add top issues to address
    if issues:
        critical_issues = [i for i in issues if i["severity"] == "high"]
        if critical_issues:
            summary += f" Critical issues to address: {critical_issues[0]['description']}."
            if len(critical_issues) > 1:
                summary += f" Plus {len(critical_issues)-1} more critical issues."
    
    return summary