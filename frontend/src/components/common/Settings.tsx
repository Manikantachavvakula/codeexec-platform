import React from 'react';
import { Modal, Group, Text, Switch, Stack, Select, NumberInput, Button } from '@mantine/core';

interface SettingsProps {
  opened: boolean;
  onClose: () => void;
  settings: {
    editorFontSize: number;
    editorTheme: string;
    tabSize: number;
    wordWrap: boolean;
    minimap: boolean;
  };
  onSettingsChange: (settings: any) => void;
}

const editorThemes = [
  { value: 'vs', label: 'Light' },
  { value: 'vs-dark', label: 'Dark' },
  { value: 'hc-black', label: 'High Contrast' },
];

const Settings: React.FC<SettingsProps> = ({ 
  opened, 
  onClose, 
  settings, 
  onSettingsChange 
}) => {
  const [localSettings, setLocalSettings] = React.useState(settings);
  
  const handleChange = (key: string, value: any) => {
    setLocalSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };
  
  const handleSave = () => {
    onSettingsChange(localSettings);
    onClose();
  };
  
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Editor Settings"
      centered
    >
      <Stack spacing="md">
        <NumberInput
          label="Font Size"
          value={localSettings.editorFontSize}
          onChange={(val) => handleChange('editorFontSize', val)}
          min={10}
          max={24}
          step={1}
        />
        
        <Select
          label="Editor Theme"
          data={editorThemes}
          value={localSettings.editorTheme}
          onChange={(val) => handleChange('editorTheme', val)}
        />
        
        <NumberInput
          label="Tab Size"
          value={localSettings.tabSize}
          onChange={(val) => handleChange('tabSize', val)}
          min={2}
          max={8}
          step={1}
        />
        
        <Switch
          label="Word Wrap"
          checked={localSettings.wordWrap}
          onChange={(e) => handleChange('wordWrap', e.currentTarget.checked)}
        />
        
        <Switch
          label="Show Minimap"
          checked={localSettings.minimap}
          onChange={(e) => handleChange('minimap', e.currentTarget.checked)}
        />
        
        <Group position="right" mt="md">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleSave}>Save Changes</Button>
        </Group>
      </Stack>
    </Modal>
  );
};

export default Settings;