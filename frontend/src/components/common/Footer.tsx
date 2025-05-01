import React from 'react';
import { Group, Text, Anchor, Box } from '@mantine/core';
import { IconBrandGithub, IconBrandTwitter, IconQuestionMark } from '@tabler/icons-react';

interface FooterProps {
  onOpenAbout: () => void;
  onOpenKeyboardShortcuts: () => void;
}

const Footer: React.FC<FooterProps> = ({ onOpenAbout, onOpenKeyboardShortcuts }) => {
  return (
    <Box
      component="footer"
      py="xs"
      px="md"
      sx={(theme) => ({
        borderTop: `1px solid ${
          theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
        }`,
      })}
    >
      <Group position="apart">
        <Text color="dimmed" size="xs">
          © {new Date().getFullYear()} Code Explorer. MIT License
        </Text>
        
        <Group spacing="xs">
          <Anchor size="xs" onClick={onOpenAbout} sx={{ cursor: 'pointer' }}>
            <Group spacing={4}>
              <IconQuestionMark size={14} />
              <Text size="xs">About</Text>
            </Group>
          </Anchor>
          
          <Anchor size="xs" onClick={onOpenKeyboardShortcuts} sx={{ cursor: 'pointer' }}>
            <Text size="xs">Shortcuts</Text>
          </Anchor>
          
          <Anchor
            href="https://github.com/your-username/code-explorer"
            target="_blank"
            rel="noopener noreferrer"
            size="xs"
          >
            <Group spacing={4}>
              <IconBrandGithub size={14} />
              <Text size="xs">GitHub</Text>
            </Group>
          </Anchor>
        </Group>
      </Group>
    </Box>
  );
};

export default Footer;