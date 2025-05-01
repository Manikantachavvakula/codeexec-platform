import React from 'react';
import { Group, ActionIcon, Title, Switch, Box, Text, Stack } from '@mantine/core';
import { IconSun, IconMoon, IconBrandGithub } from '@tabler/icons-react';

interface NavigationProps {
  colorScheme: 'light' | 'dark';
  toggleColorScheme: () => void;
}

const Navigation: React.FC<NavigationProps> = ({ colorScheme, toggleColorScheme }) => {
  return (
    <Box p="md">
      <Group position="apart">
        <Stack spacing={0}>
          <Title order={4}>Code Explorer</Title>
          <Text size="xs" color="dimmed">Analyze & Execute Code</Text>
        </Stack>
        
        <Group>
          <Switch
            checked={colorScheme === 'dark'}
            onChange={toggleColorScheme}
            size="md"
            onLabel={<IconMoon size={16} />}
            offLabel={<IconSun size={16} />}
          />
          
          <ActionIcon component="a" href="https://github.com/your-username/code-explorer" target="_blank" variant="subtle">
            <IconBrandGithub size={20} />
          </ActionIcon>
        </Group>
      </Group>
    </Box>
  );
};

export default Navigation;