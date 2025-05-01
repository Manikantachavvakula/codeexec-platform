import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX, IconInfoCircle } from '@tabler/icons-react';

export const showSuccessNotification = (message: string, title?: string) => {
  showNotification({
    title: title || 'Success',
    message,
    color: 'green',
    icon: <IconCheck />,
    autoClose: 3000,
  });
};

export const showErrorNotification = (message: string, title?: string) => {
  showNotification({
    title: title || 'Error',
    message,
    color: 'red',
    icon: <IconX />,
    autoClose: 5000,
  });
};

export const showInfoNotification = (message: string, title?: string) => {
  showNotification({
    title: title || 'Information',
    message,
    color: 'blue',
    icon: <IconInfoCircle />,
    autoClose: 3000,
  });
};