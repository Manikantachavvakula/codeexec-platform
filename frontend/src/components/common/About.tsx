import React from 'react';
import { Modal, Group, Text, Stack, Title, Divider, Anchor, Badge, Paper } from '@mantine/core';
import { IconCode, IconBook, IconBrandGithub } from '@tabler/icons-react';

interface AboutProps {
  opened: boolean;
  onClose: () => void;
}

const About: React.FC<AboutProps> = ({ opened, onClose }) => {
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="About Code Explorer"
      size="lg"
      centered
    >
      <Stack spacing="md">
        <Group>
          <IconCode size={24} />
          <Title order={3}>Code Explorer</Title>
          <Badge color="blue" variant="filled">Beta</Badge>
        </Group>
        
        <Text>
          Code Explorer is an interactive platform for coding, analysis, and visualization.
          Execute code in multiple languages, analyze complexity, and get optimization suggestions.
        </Text>
        
        <Divider label="Features" labelPosition="center" />
        
        <Stack spacing="xs">
          <Paper withBorder p="xs">
            <Text weight={500}>🚀 Multiple Language Support</Text>
            <Text size="sm">Write and execute code in Python, JavaScript, TypeScript, Java, C++, and C#</Text>
          </Paper>
          
          <Paper withBorder p="xs">
            <Text weight={500}>📊 Complexity Analysis</Text>
            <Text size="sm">Get time and space complexity analysis with detailed explanations</Text>
          </Paper>
          
          <Paper withBorder p="xs">
            <Text weight={500}>🔍 Code Visualization</Text>
            <Text size="sm">Step through your code execution and see variable changes</Text>
          </Paper>
          
          <Paper withBorder p="xs">
            <Text weight={500}>💡 Optimization Suggestions</Text>
            <Text size="sm">Receive suggestions to improve your code efficiency</Text>
          </Paper>
          
          <Paper withBorder p="xs">
            <Text weight={500}>🔎 Pattern Analysis</Text>
            <Text size="sm">Detect common patterns and anti-patterns in your code</Text>
          </Paper>
        </Stack>
        
        <Divider label="Technical Stack" labelPosition="center" />
        
        <Text size="sm">
          Built with <b>FastAPI</b> (backend) and <b>React/TypeScript</b> (frontend).
          Code execution is powered by the Piston API. Complex analysis algorithms
          written in Python. UI components from Mantine UI library.
        </Text>
        
        <Group position="center" mt="md">
          <Anchor href="https://github.com/your-username/code-explorer" target="_blank">
            <Group spacing="xs">
              <IconBrandGithub size={16} />
              <Text>GitHub Repository</Text>
            </Group>
          </Anchor>
          
          <Anchor href="https://docs-link-placeholder.com" target="_blank">
            <Group spacing="xs">
              <IconBook size={16} />
              <Text>Documentation</Text>
            </Group>
          </Anchor>
        </Group>
      </Stack>
    </Modal>
  );
};

export default About;