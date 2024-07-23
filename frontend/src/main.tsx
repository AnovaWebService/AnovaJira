import {App, ConfigProvider} from 'antd';
import dayjs from 'dayjs';
import 'dayjs/locale/ru';
import relativeTime from 'dayjs/plugin/relativeTime';
import updateLocale from 'dayjs/plugin/updateLocale';
import React from 'react';
import {DndProvider} from 'react-dnd';
import {HTML5Backend} from 'react-dnd-html5-backend';
import ReactDOM from 'react-dom/client';

import {darkTheme, lightTheme} from './config-provider';
import {PoppinsFont, styledDarkTheme} from './global-styles';
import {ProjectRouter} from './router';
import { ThemeProvider } from 'styled-components';
import { ProjectThemeProvider } from './providers/project-theme-provider';

dayjs.extend(relativeTime);
dayjs.extend(updateLocale);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ProjectThemeProvider>
      <App>
        <PoppinsFont />
        <DndProvider backend={HTML5Backend}>
          <ProjectRouter />
        </DndProvider>
      </App>
    </ProjectThemeProvider>
  </React.StrictMode>,
);
