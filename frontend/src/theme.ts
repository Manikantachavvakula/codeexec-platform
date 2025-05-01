import { MantineThemeOverride } from '@mantine/core';

export const lightTheme: MantineThemeOverride = {
  colorScheme: 'light',
  primaryColor: 'cyan',
  colors: {
    // Custom color palette
    brand: [
      '#E3F8FF', '#B3ECFF', '#81DEFD', '#4ED1FA', '#1AC0F5',
      '#0CAFDD', '#099DC8', '#0789B1', '#037099', '#015B7D',
    ]
  },
  fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
  fontFamilyMonospace: 'Monaco, Courier, monospace',
  headings: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
  }
};

export const darkTheme: MantineThemeOverride = {
  colorScheme: 'dark',
  primaryColor: 'cyan',
  colors: {
    // Custom color palette
    brand: [
      '#E3F8FF', '#B3ECFF', '#81DEFD', '#4ED1FA', '#1AC0F5',
      '#0CAFDD', '#099DC8', '#0789B1', '#037099', '#015B7D',
    ],
    dark: [
      '#C1C2C5', '#A6A7AB', '#909296', '#5c5f66', '#373A40',
      '#2C2E33', '#25262b', '#1A1B1E', '#141517', '#101113',
    ],
  },
  fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
  fontFamilyMonospace: 'Monaco, Courier, monospace',
  headings: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
  }
};