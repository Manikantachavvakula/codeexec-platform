import axios from 'axios';
import { 
  CodeExecutionRequest, 
  CodeExecutionResponse,
  ComplexityData,
  VisualizationData,
  OptimizationData,
  PatternData
} from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create a configured axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const executeCode = async (request: CodeExecutionRequest): Promise<CodeExecutionResponse> => {
  const response = await apiClient.post('/execute', request);
  return response.data;
};

export const analyzeComplexity = async (language: string, code: string): Promise<ComplexityData> => {
  const response = await apiClient.post('/analysis/complexity', { language, code });
  return {
    timeComplexity: response.data.time_complexity,
    spaceComplexity: response.data.space_complexity,
    explanation: response.data.explanation
  };
};

export const visualizeCode = async (language: string, code: string): Promise<VisualizationData> => {
  const response = await apiClient.post('/analysis/visualize', { language, code });
  return response.data;
};

export const optimizeCode = async (language: string, code: string): Promise<OptimizationData> => {
  const response = await apiClient.post('/analysis/optimize', { language, code });
  return response.data;
};

export const analyzePatterns = async (language: string, code: string): Promise<PatternData> => {
  const response = await apiClient.post('/analysis/patterns', { language, code });
  return response.data;
};

export const getLanguages = async (): Promise<string[]> => {
  const response = await apiClient.get('/execute/languages');
  return response.data.languages;
};

const apiService = {
  executeCode,
  analyzeComplexity,
  visualizeCode,
  optimizeCode,
  analyzePatterns,
  getLanguages
};

export default apiService;