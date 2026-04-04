import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './style/index.css'
import Home from './Home'
import { initTheme } from './lib/theme.ts';
import { Toaster } from "@/components/ui/sonner" 

initTheme();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Home />
    <Toaster />
  </StrictMode>
)
