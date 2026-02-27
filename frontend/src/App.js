import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box, CssBaseline } from '@mui/material';

import NavBar from './components/NavBar/NavBar';
import Footer from './components/Footer/Footer';
import Home from './components/Home/Home';
import Generator from './components/Generator/Generator';
import Login from './components/Login/Login';
import Register from './components/Register/Register';

const watTheme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#219653' },
    secondary: { main: '#d32f2f' },
    background: { default: '#f8f9fa', paper: '#ffffff' },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const isLoggedIn = false;

  return (
    <ThemeProvider theme={watTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        
        <NavBar isAuthenticated={isLoggedIn} />
        
        <Box component="main" sx={{ flexGrow: 1 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/generator" element={<Generator />} />
          </Routes>
        </Box>
        
        <Footer />
      </Box>
    </ThemeProvider>
  );
}

export default App;