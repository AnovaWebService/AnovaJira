import {useContext} from 'react';

import {ThemeProviderContext} from '../providers/project-theme-provider';

export function useThemeContext() {
  const context = useContext(ThemeProviderContext);

  if (!context) {
    throw new Error('Theme Context вызван не там');
  }

  return context.setTheme;
}
