import { useState, useCallback } from 'react';
import apiService from '../services/api';
import { ComplexityData, VisualizationData, OptimizationData, PatternData } from '../types';

export const useCodeExecution = () => {
  // State for execution results
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [executionTime, setExecutionTime] = useState(0);
  
  // State for analysis results
  const [complexityData, setComplexityData] = useState<ComplexityData>({
    timeComplexity: '',
    spaceComplexity: '',
    explanation: ''
  });
  
  const [visualizationData, setVisualizationData] = useState<VisualizationData>({
    steps: [],
  });
  
  const [optimizationData, setOptimizationData] = useState<OptimizationData>({
    optimization_suggestions: [],
    optimizable: false
  });
  
  const [patternData, setPatternData] = useState<PatternData>({
    patterns: [],
    anti_patterns: [],
    recommendations: []
  });

  // Function to execute code and get all analysis data
  const executeCode = useCallback(async (language: string, code: string, input: string) => {
    setIsLoading(true);
    setOutput('');
    setError('');
    
    try {
      // Execute code
      const executionResult = await apiService.executeCode({
        language,
        code,
        stdin: input
      });
      
      setOutput(executionResult.output || '');
      if (executionResult.error) {
        setError(executionResult.error);
      }
      setExecutionTime(executionResult.execution_time || 0);
      
      // If execution successful, analyze code
      if (!executionResult.error) {
        try {
          // Run analysis in parallel
          const [complexityResult, visualizationResult, optimizationResult, patternResult] = await Promise.all([
            apiService.analyzeComplexity(language, code),
            apiService.visualizeCode(language, code),
            apiService.optimizeCode(language, code),
            apiService.analyzePatterns(language, code)
          ]);
          
          setComplexityData(complexityResult);
          setVisualizationData(visualizationResult);
          setOptimizationData(optimizationResult);
          setPatternData(patternResult);
        } catch (analysisError: any) {
          console.error('Error performing code analysis:', analysisError);
          // Don't show analysis errors to the user, just log them
        }
      }
    } catch (err: any) {
      // Handle API errors
      console.error('Error executing code:', err);
      if (err.response?.data?.detail) {
        setError(`Error: ${err.response.data.detail}`);
      } else {
        setError('Failed to execute code. Please check your connection and try again.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Function to just update the code analysis without execution
  const analyzeCodeOnly = useCallback(async (language: string, code: string) => {
    try {
      const [complexityResult, optimizationResult, patternResult] = await Promise.all([
        apiService.analyzeComplexity(language, code),
        apiService.optimizeCode(language, code),
        apiService.analyzePatterns(language, code)
      ]);
      
      setComplexityData(complexityResult);
      setOptimizationData(optimizationResult);
      setPatternData(patternResult);
      
      return true;
    } catch (err) {
      console.error('Error analyzing code:', err);
      return false;
    }
  }, []);

  return {
    // Execution state
    output,
    error,
    isLoading,
    executionTime,
    
    // Analysis state
    complexityData,
    visualizationData,
    optimizationData,
    patternData,
    
    // Actions
    executeCode,
    analyzeCodeOnly
  };
};

export default useCodeExecution;