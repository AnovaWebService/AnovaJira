import {BrowserRouter, Route, Routes} from 'react-router-dom';

import {AuthPage} from './pages/AuthPage/auth-page';
import {MainPage} from './pages/MainPage/main';

export function ProjectRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" Component={MainPage} />
        <Route path="/auth" Component={AuthPage} />
      </Routes>
    </BrowserRouter>
  );
}
