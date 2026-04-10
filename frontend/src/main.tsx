import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './style/index.css'
import Home from './pages/Home'
import { initTheme } from './lib/theme.ts';
import { Toaster } from "@/components/ui/sonner" 
import { BrowserRouter } from 'react-router-dom';
import { Routes, Route } from 'react-router-dom';
import IngestVectors from './pages/IngestVectors';
import { AppContextProvider } from './contexts/AppContext'
import { HOME_ROUTE, INGEST_VECTOR_ROUTE, SEARCH_VECTOR_ROUTE } from './config/routes.ts';
import SearchVectors from './pages/SearchVectors.tsx';

initTheme();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppContextProvider>
      <BrowserRouter>
        <Routes>
          <Route path={HOME_ROUTE} element={<Home />} />
          <Route path={INGEST_VECTOR_ROUTE} element={<IngestVectors />} />
          <Route path={SEARCH_VECTOR_ROUTE} element={<SearchVectors />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </AppContextProvider>
  </StrictMode>
)
