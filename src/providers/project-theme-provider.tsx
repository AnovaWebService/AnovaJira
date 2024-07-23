import {ConfigProvider} from 'antd';
import ruRu from 'antd/locale/ru_RU';
import {createContext, useState} from 'react';
import {ThemeProvider} from 'styled-components';

import {darkTheme, lightTheme} from '../config-provider';
import {styledDarkTheme, styledLightTheme} from '../global-styles';

type themeType = 'light' | 'dark';

type TProjectThemeProvider = {
  setTheme: (_: themeType) => void;
};

export const ThemeProviderContext = createContext<TProjectThemeProvider>({
  setTheme(_) {
    return _;
  },
});

const themes = {
  light: [lightTheme, styledLightTheme],
  dark: [darkTheme, styledDarkTheme],
};

export function ProjectThemeProvider({children}) {
  const [currentTheme, setCurrentTheme] = useState<themeType>('light');

  const handleThemeSwitch = (theme: themeType) => {
    setCurrentTheme(theme);
  };

  return (
    <ThemeProviderContext.Provider value={{setTheme: handleThemeSwitch}}>
      <ConfigProvider
        theme={{
          ...themes[currentTheme].at(0) as any,
          hashed: false,
        }}
        locale={ruRu}
      >
        <ThemeProvider theme={themes[currentTheme].at(1) as any}>
          {children}
        </ThemeProvider>
      </ConfigProvider>
    </ThemeProviderContext.Provider>
  );
}
