import {BrowserRouter, Route, Routes} from 'react-router-dom';

import {AuthPage} from './pages/AuthPage/auth-page';

export function ProjectRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" Component={AuthPage} />
      </Routes>
    </BrowserRouter>
  );
}
