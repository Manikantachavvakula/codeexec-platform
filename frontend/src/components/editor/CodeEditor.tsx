import React, { useState, useRef, useEffect } from 'react';
import { Paper, Text, Button, Group, Textarea, Select, Box, Tabs, Loader } from '@mantine/core';
import { IconPlay, IconCode } from '@tabler/icons-react';
import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  onExecute: (language: string, code: string, input: string) => void;
  isLoading: boolean;
  output: string;
  error: string;
}

const LANGUAGE_OPTIONS = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
  { value: 'csharp', label: 'C#' }
];

const BOILERPLATE_CODE = {
  python: "# Python code\n\ndef main():\n    print(\"Hello, World!\")\n\nif __name__ == \"__main__\":\n    main()",
  javascript: "// JavaScript code\n\nfunction main() {\n    console.log(\"Hello, World!\");\n}\n\nmain();",
  typescript: "// TypeScript code\n\nfunction main(): void {\n    console.log(\"Hello, World!\");\n}\n\nmain();",
  java: "// Java code\n\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
  cpp: "// C++ code\n#include <iostream>\n\nint main() {\n    std::cout << \"Hello, World!\" << std::endl;\n    return 0;\n}",
  csharp: "// C# code\nusing System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine(\"Hello, World!\");\n    }\n}"
};

const CodeEditor: React.FC<CodeEditorProps> = ({
  onExecute,
  isLoading,
  output,
  error
}) => {
  const [language, setLanguage] = useState<string>('python');
  const [code, setCode] = useState<string>(BOILERPLATE_CODE.python);
  const [input, setInput] = useState<string>('');
  const [activeTab, setActiveTab] = useState<string>('output');
  
  const editorRef = useRef<any>(null);
  
  // Update boilerplate code when language changes
  useEffect(() => {
    setCode(BOILERPLATE_CODE[language as keyof typeof BOILERPLATE_CODE] || '');
  }, [language]);
  
  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor;
  };
  
  const handleExecute = () => {
    const currentCode = editorRef.current ? editorRef.current.getValue() : code;
    onExecute(language, currentCode, input);
    setActiveTab('output');
  };
  
  return (
    <Paper withBorder p="md">
      <Group position="apart" mb="md">
        <Group>
          <IconCode size={20} />
          <Text weight={500}>Code Editor</Text>
        </Group>
        
        <Select
          value={language}
          onChange={(value) => setLanguage(value || 'python')}
          data={LANGUAGE_OPTIONS}
          style={{ width: '150px' }}
        />
      </Group>
      
      <Box mb="md" style={{ border: '1px solid #ccc', borderRadius: '4px' }}>
        <Editor
          height="400px"
          language={language}
          value={code}
          onChange={(value) => value && setCode(value)}
          theme="vs-dark"
          onMount={handleEditorDidMount}
          options={{
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            fontSize: 14,
            tabSize: 2,
          }}
        />
      </Box>
      
      <Tabs value={activeTab} onTabChange={setActiveTab}>
        <Tabs.List>
          <Tabs.Tab value="input">Input</Tabs.Tab>
          <Tabs.Tab value="output">Output</Tabs.Tab>
        </Tabs.List>
        
        <Tabs.Panel value="input" pt="xs">
          <Textarea
            placeholder="Enter input here (if required)"
            minRows={5}
            value={input}
            onChange={(e) => setInput(e.currentTarget.value)}
          />
        </Tabs.Panel>
        
        <Tabs.Panel value="output" pt="xs">
          {isLoading ? (
            <Group position="center" py="lg">
              <Loader size="sm" />
              <Text>Executing code...</Text>
            </Group>
          ) : (
            <Box>
              {output && (
                <Box mb="md">
                  <Text weight={500} size="sm">Output:</Text>
                  <Paper withBorder p="xs" style={{ 
                    whiteSpace: 'pre-wrap', 
                    fontFamily: 'monospace',
                    maxHeight: '200px',
                    overflowY: 'auto',
                    backgroundColor: '#f0f0f0',
                    color: '#333'
                  }}>
                    {output}
                  </Paper>
                </Box>
              )}
              
              {error && (
                <Box>
                  <Text weight={500} size="sm" color="red">Errors:</Text>
                  <Paper withBorder p="xs" style={{ 
                    whiteSpace: 'pre-wrap', 
                    fontFamily: 'monospace',
                    maxHeight: '200px',
                    overflowY: 'auto',
                    backgroundColor: '#ffe0e0',
                    color: '#b00020'
                  }}>
                    {error}
                  </Paper>
                </Box>
              )}
              
              {!output && !error && (
                <Text color="dimmed" align="center" py="lg">
                  Execute your code to see the output here
                </Text>
              )}
            </Box>
          )}
        </Tabs.Panel>
      </Tabs>
      
      <Group position="right" mt="md">
        <Button
          leftIcon={<IconPlay size={16} />}
          onClick={handleExecute}
          loading={isLoading}
          disabled={!code.trim()}
        >
          Run Code
        </Button>
      </Group>
    </Paper>
  );
};

export default CodeEditor;