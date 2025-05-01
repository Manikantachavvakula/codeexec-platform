import React from 'react';
import { Select, Group, Avatar, Text, SelectItem } from '@mantine/core';

interface LanguageSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

const languageData = [
  {
    value: 'python',
    label: 'Python',
    icon: '🐍',
    description: 'General-purpose, easy syntax'
  },
  {
    value: 'javascript',
    label: 'JavaScript',
    icon: '📜',
    description: 'Web development, frontend'
  },
  {
    value: 'typescript',
    label: 'TypeScript',
    icon: '📘',
    description: 'Typed JavaScript'
  },
  {
    value: 'java',
    label: 'Java',
    icon: '☕',
    description: 'Object-oriented programming'
  },
  {
    value: 'cpp',
    label: 'C++',
    icon: '⚙️',
    description: 'Systems programming'
  },
  {
    value: 'csharp',
    label: 'C#',
    icon: '🔷',
    description: '.NET development'
  }
];

// Custom item component for the select dropdown
interface ItemProps extends React.ComponentPropsWithoutRef<'div'> {
  image: string;
  label: string;
  description: string;
}

const SelectItem = (props: ItemProps) => {
  const { image, label, description, ...others } = props;
  return (
    <div {...others}>
      <Group noWrap>
        <Text size="sm">{image}</Text>
        <div>
          <Text size="sm">{label}</Text>
          <Text size="xs" color="dimmed">{description}</Text>
        </div>
      </Group>
    </div>
  );
};

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ value, onChange }) => {
  return (
    <Select
      label="Programming Language"
      placeholder="Choose a language"
      itemComponent={SelectItem}
      data={languageData.map((item) => ({
        value: item.value,
        label: item.label,
        image: item.icon,
        description: item.description
      }))}
      value={value}
      onChange={(val) => onChange(val || 'python')}
      maxDropdownHeight={400}
      nothingFound="No languages match the filter"
      filter={(value, item) =>
        item.label?.toLowerCase().includes(value.toLowerCase().trim()) ||
        item.description.toLowerCase().includes(value.toLowerCase().trim())
      }
    />
  );
};

export default LanguageSelector;