import React from 'react';
import { Modal, Group, Text, Kbd, Stack, Table } from '@mantine/core';

interface KeyboardShortcutsProps {
  opened: boolean;
  onClose: () => void;
}

const KeyboardShortcuts: React.FC<KeyboardShortcutsProps> = ({ opened, onClose }) => {
  const shortcuts = [
    { keys: ['Ctrl', 'Enter'], description: 'Run code' },
    { keys: ['Ctrl', 'S'], description: 'Save current code' },
    { keys: ['Ctrl', '/'], description: 'Toggle comment' },
    { keys: ['Ctrl', 'Space'], description: 'Trigger autocomplete' },
    { keys: ['Ctrl', 'F'], description: 'Find in code' },
    { keys: ['Ctrl', 'G'], description: 'Go to line' },
    { keys: ['F11'], description: 'Toggle fullscreen' },
  ];
  
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Keyboard Shortcuts"
      centered
    >
      <Table>
        <thead>
          <tr>
            <th>Shortcut</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {shortcuts.map((shortcut, index) => (
            <tr key={index}>
              <td>
                <Group spacing={5}>
                  {shortcut.keys.map((key, keyIndex) => (
                    <React.Fragment key={keyIndex}>
                      <Kbd>{key}</Kbd>
                      {keyIndex < shortcut.keys.length - 1 && ' + '}
                    </React.Fragment>
                  ))}
                </Group>
              </td>
              <td>
                <Text size="sm">{shortcut.description}</Text>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Modal>
  );
};

export default KeyboardShortcuts;