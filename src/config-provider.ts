import {theme, ThemeConfig} from 'antd';

export const lightTheme = {
  token: {
    colorPrimary: '#A717FF',
    colorLink: '#A717FF',
  },
};

export const darkTheme: ThemeConfig = {
  token: {
    ...lightTheme.token,
    colorBgLayout: '#333333',
  },
  components: {},
  algorithm: theme.darkAlgorithm,
};
