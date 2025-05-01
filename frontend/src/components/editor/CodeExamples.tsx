import React from 'react';
import { Menu, Button, Text, ScrollArea, Code } from '@mantine/core';
import { IconCode, IconChevronDown } from '@tabler/icons-react';

interface CodeExample {
  name: string;
  code: string;
  description: string;
}

interface CodeExamplesProps {
  language: string;
  onSelectExample: (code: string) => void;
}

// Example snippets by language
const EXAMPLES: Record<string, CodeExample[]> = {
  python: [
    {
      name: "Bubble Sort",
      description: "Implementation of the bubble sort algorithm",
      code: `def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Test the function
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers.copy())
print(f"Original array: {numbers}")
print(f"Sorted array: {sorted_numbers}")`
    },
    {
      name: "Fibonacci Sequence",
      description: "Recursive and iterative implementations",
      code: `# Recursive implementation (O(2^n) time complexity)
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# Iterative implementation (O(n) time complexity)
def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Test and compare both implementations
n = 10
print(f"Recursive Fibonacci of {n}: {fibonacci_recursive(n)}")
print(f"Iterative Fibonacci of {n}: {fibonacci_iterative(n)}")`
    }
  ],
  javascript: [
    {
      name: "Array Operations",
      description: "Common array methods and operations",
      code: `// Sample array
const numbers = [1, 2, 3, 4, 5];

// Map, filter, reduce examples
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((total, n) => total + n, 0);

// Output results
console.log("Original array:", numbers);
console.log("Doubled:", doubled);
console.log("Even numbers:", evens);
console.log("Sum of all numbers:", sum);`
    },
    {
      name: "Async/Await Example",
      description: "Using async/await for asynchronous operations",
      code: `// Simulated API call
function fetchData() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id: 1, name: "Sample Data" });
    }, 1000);
  });
}

// Using async/await
async function getData() {
  console.log("Fetching data...");
  try {
    const data = await fetchData();
    console.log("Data received:", data);
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Execute the async function
getData().then(() => {
  console.log("Process completed");
});`
    }
  ],
  // Add more examples for other languages
};

const CodeExamples: React.FC<CodeExamplesProps> = ({ language, onSelectExample }) => {
  const examples = EXAMPLES[language] || [];
  
  if (examples.length === 0) {
    return null;
  }
  
  return (
    <Menu width={300} position="bottom-start">
      <Menu.Target>
        <Button variant="subtle" rightIcon={<IconChevronDown size={16} />} leftIcon={<IconCode size={16} />}>
          Examples
        </Button>
      </Menu.Target>
      
      <Menu.Dropdown>
        <Menu.Label>Example Code Snippets</Menu.Label>
        
        {examples.map((example, index) => (
          <Menu.Item 
            key={index} 
            onClick={() => onSelectExample(example.code)}
          >
            <Text weight={500}>{example.name}</Text>
            <Text size="xs" color="dimmed">{example.description}</Text>
          </Menu.Item>
        ))}
      </Menu.Dropdown>
    </Menu>
  );
};

export default CodeExamples;