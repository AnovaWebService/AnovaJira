import {BrowserRouter, Route, Routes} from 'react-router-dom';

import {MainPage} from './pages/MainPage/main';

export function ProjectRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" Component={MainPage} />
      </Routes>
    </BrowserRouter>
  );
}
