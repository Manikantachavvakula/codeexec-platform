import React, { useState } from 'react';
import { 
  MantineProvider, 
  ColorSchemeProvider, 
  ColorScheme,
  AppShell,
  Navbar,
  Header,
  Container,
  Group,
  ActionIcon,
  Title,
  Box,
  Tabs,
  Button,
  Text,
  Footer as MantineFooter
} from '@mantine/core';
import { 
  IconSun, 
  IconMoon, 
  IconMaximize, 
  IconMinimize, 
  IconCode, 
  IconBraces, 
  IconChartBar,
  IconSettings,
  IconQuestionMark,
  IconKeyboard
} from '@tabler/icons-react';

// Components
import CodeEditor from './components/editor/CodeEditor';
import ComplexityDisplay from './components/analysis/ComplexityDisplay';
import VisualizerDisplay from './components/analysis/VisualizerDisplay';
import OptimizationDisplay from './components/analysis/OptimizationDisplay';
import PatternAnalysisDisplay from './components/analysis/PatternAnalysisDisplay';
import Navigation from './components/common/Navigation';
import Footer from './components/common/Footer';
import Settings from './components/common/Settings';
import About from './components/common/About';
import KeyboardShortcuts from './components/common/KeyboardShortcuts';

// Hooks and Services
import { useCodeExecution } from './hooks/useCodeExecution';
import { lightTheme, darkTheme } from './theme';

function App() {
  // Theme state
  const [colorScheme, setColorScheme] = useState<ColorScheme>('dark');
  const [isFullscreen, setIsFullscreen] = useState(false);
  
  // UI state
  const [activeTab, setActiveTab] = useState('complexity');
  const [settingsOpened, setSettingsOpened] = useState(false);
  const [aboutOpened, setAboutOpened] = useState(false);
  const [shortcutsOpened, setShortcutsOpened] = useState(false);
  
  // Editor settings
  const [editorSettings, setEditorSettings] = useState({
    editorFontSize: 14,
    editorTheme: colorScheme === 'dark' ? 'vs-dark' : 'vs',
    tabSize: 2,
    wordWrap: true,
    minimap: false,
  });
  
  // Code execution logic
  const {
    output,
    error,
    isLoading,
    complexityData,
    visualizationData,
    optimizationData,
    patternData,
    executeCode
  } = useCodeExecution();

  // Theme toggle
  const toggleColorScheme = (value?: ColorScheme) => {
    const newColorScheme = value || (colorScheme === 'dark' ? 'light' : 'dark');
    setColorScheme(newColorScheme);
    setEditorSettings(prev => ({
      ...prev,
      editorTheme: newColorScheme === 'dark' ? 'vs-dark' : 'vs'
    }));
  };

  // Fullscreen toggle
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`);
      });
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
        setIsFullscreen(false);
      }
    }
  };

  // Handle code execution
  const handleExecuteCode = (language: string, code: string, input: string) => {
    executeCode(language, code, input);
  };

  return (
    <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
      <MantineProvider theme={colorScheme === 'dark' ? darkTheme : lightTheme} withGlobalStyles withNormalizeCSS>
        <AppShell
          padding="md"
          navbar={
            <Navbar width={{ base: 250 }} height="100%" p="xs">
              <Navbar.Section>
                <Title order={4} mb="md">Code Explorer</Title>
                <Text size="sm" color="dimmed" mb="xl">
                  Analyze and execute code in multiple languages
                </Text>
              </Navbar.Section>
              
              <Navbar.Section grow>
                <Box>
                  <Text weight={500} mb="xs">Features:</Text>
                  <ul style={{ paddingLeft: '20px' }}>
                    <li>Run code in multiple languages</li>
                    <li>Analyze time & space complexity</li>
                    <li>Visualize code execution</li>
                    <li>Get optimization suggestions</li>
                    <li>Detect code patterns</li>
                  </ul>
                </Box>
              </Navbar.Section>
              
              <Navbar.Section>
                <Group position="center" spacing="xs" my="md">
                  <Button 
                    variant="subtle" 
                    leftIcon={<IconSettings size={16} />} 
                    onClick={() => setSettingsOpened(true)}
                    compact
                  >
                    Settings
                  </Button>
                  <Button 
                    variant="subtle" 
                    leftIcon={<IconKeyboard size={16} />} 
                    onClick={() => setShortcutsOpened(true)}
                    compact
                  >
                    Shortcuts
                  </Button>
                </Group>
              </Navbar.Section>
            </Navbar>
          }
          header={
            <Header height={60} p="xs">
              <Container>
                <Group position="apart">
                  <Group>
                    <IconCode size={30} color={colorScheme === 'dark' ? '#6ee7b7' : '#0ea5e9'} />
                    <Title order={3}>Code Explorer</Title>
                  </Group>
                  
                  <Group>
                    <Button
                      variant="subtle"
                      leftIcon={<IconQuestionMark size={16} />}
                      onClick={() => setAboutOpened(true)}
                      compact
                    >
                      About
                    </Button>
                    <ActionIcon 
                      onClick={toggleColorScheme} 
                      variant="default" 
                      size={30}
                    >
                      {colorScheme === 'dark' ? <IconSun size={16} /> : <IconMoon size={16} />}
                    </ActionIcon>
                    <ActionIcon onClick={toggleFullscreen} variant="default" size={30}>
                      {isFullscreen ? <IconMinimize size={16} /> : <IconMaximize size={16} />}
                    </ActionIcon>
                  </Group>
                </Group>
              </Container>
            </Header>
          }
          footer={
            <MantineFooter height={40}>
              <Footer 
                onOpenAbout={() => setAboutOpened(true)} 
                onOpenKeyboardShortcuts={() => setShortcutsOpened(true)} 
              />
            </MantineFooter>
          }
          styles={(theme) => ({
            main: { 
              backgroundColor: colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
            },
          })}
        >
          <Container size="xl">
            <Group grow align="flex-start">
              <Box sx={{ flex: 2 }}>
                <CodeEditor 
                  onExecute={handleExecuteCode}
                  isLoading={isLoading}
                  output={output}
                  error={error}
                />
              </Box>
              <Box sx={{ flex: 1 }}>
                <Tabs value={activeTab} onTabChange={setActiveTab}>
                  <Tabs.List>
                    <Tabs.Tab value="complexity" icon={<IconChartBar size={14} />}>Complexity</Tabs.Tab>
                    <Tabs.Tab value="visualizer" icon={<IconCode size={14} />}>Visualizer</Tabs.Tab>
                    <Tabs.Tab value="optimization" icon={<IconBraces size={14} />}>Optimization</Tabs.Tab>
                    <Tabs.Tab value="patterns" icon={<IconBraces size={14} />}>Patterns</Tabs.Tab>
                  </Tabs.List>

                  <Tabs.Panel value="complexity" pt="xs">
                    <ComplexityDisplay
                      timeComplexity={complexityData.timeComplexity}
                      spaceComplexity={complexityData.spaceComplexity}
                      explanation={complexityData.explanation}
                      isLoading={isLoading}
                    />
                  </Tabs.Panel>

                  <Tabs.Panel value="visualizer" pt="xs">
                    <VisualizerDisplay
                      visualizationData={visualizationData}
                      isLoading={isLoading}
                    />
                  </Tabs.Panel>

                  <Tabs.Panel value="optimization" pt="xs">
                    <OptimizationDisplay
                      optimizationData={optimizationData}
                      isLoading={isLoading}
                    />
                  </Tabs.Panel>

                  <Tabs.Panel value="patterns" pt="xs">
                    <PatternAnalysisDisplay
                      patternData={patternData}
                      isLoading={isLoading}
                    />
                  </Tabs.Panel>
                </Tabs>
              </Box>
            </Group>
          </Container>
          
          {/* Modals */}
          <Settings
            opened={settingsOpened}
            onClose={() => setSettingsOpened(false)}
            settings={editorSettings}
            onSettingsChange={setEditorSettings}
          />
          
          <About
            opened={aboutOpened}
            onClose={() => setAboutOpened(false)}
          />
          
          <KeyboardShortcuts
            opened={shortcutsOpened}
            onClose={() => setShortcutsOpened(false)}
          />
        </AppShell>
      </MantineProvider>
    </ColorSchemeProvider>
  );
}

export default App;