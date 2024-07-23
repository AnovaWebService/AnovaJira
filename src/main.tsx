import {App} from 'antd';
import React from 'react';
import {DndProvider} from 'react-dnd';
import {HTML5Backend} from 'react-dnd-html5-backend';
import ReactDOM from 'react-dom/client';

import {PoppinsFont} from './global-styles';
import {ProjectRouter} from './router';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App>
      <PoppinsFont />
      <DndProvider backend={HTML5Backend}>
        <ProjectRouter />
      </DndProvider>
    </App>
  </React.StrictMode>,
);
