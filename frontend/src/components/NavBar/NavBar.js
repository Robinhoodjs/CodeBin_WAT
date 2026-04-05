import { Box, Button, Stack } from '@mui/material';
import Logo from '../Logo/Logo';
import { useNavigate } from 'react-router-dom';

function NavBar({ isAuthenticated, onLogout }) {
    const navigate = useNavigate();

    return (
        <nav style={{ borderBottom: '1px solid #eee', backgroundColor: '#fff' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', px: { xs: 2, md: 5 }, py: 1.5 }}>
                {/* Logo po lewej - zawsze wraca do głównej */}
                <Logo onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>CodeBin</Logo>
                
                <Stack direction="row" spacing={2}>
                    {isAuthenticated ? (
                        // Widok po zalogowaniu
                        <>
                            <Button 
                                variant="outlined" 
                                color="primary"
                                onClick={() => navigate('/profile')}
                                sx={{ 
                                    borderRadius: '8px', 
                                    textTransform: 'none', 
                                    fontWeight: 600,
                                    px: 2,
                                    fontSize: '0.9rem',
                                    whiteSpace: 'nowrap'
                                }}
                            >
                                Moje konto
                            </Button>
                            <Button 
                                variant="contained" 
                                color="secondary"
                                onClick={onLogout}
                                sx={{ 
                                    borderRadius: '8px', 
                                    textTransform: 'none', 
                                    fontWeight: 600, 
                                    px: 2,
                                    fontSize: '0.9rem',
                                    whiteSpace: 'nowrap',
                                    boxShadow: 'none',
                                    '&:hover': { boxShadow: 'none' }
                                }}
                            >
                                Wyloguj się
                            </Button>
                        </>
                    ) : (
                        // Widok dla gościa
                        <>
                            <Button 
                                variant="outlined" 
                                color="primary"
                                onClick={() => navigate('/login')}
                                sx={{ 
                                    borderRadius: '8px', 
                                    textTransform: 'none', 
                                    fontWeight: 600,
                                    px: 2,
                                    fontSize: '0.9rem',
                                    whiteSpace: 'nowrap'
                                }}
                            >
                                Zaloguj się
                            </Button>
                            <Button 
                                variant="contained" 
                                color="primary"
                                onClick={() => navigate('/register')}
                                sx={{ 
                                    borderRadius: '8px', 
                                    textTransform: 'none', 
                                    fontWeight: 600, 
                                    px: 2,
                                    fontSize: '0.9rem',
                                    whiteSpace: 'nowrap',
                                    boxShadow: 'none',
                                    '&:hover': { boxShadow: 'none' }
                                }}
                            >
                                Zarejestruj się
                            </Button>
                        </>
                    )}
                </Stack>
            </Box>
        </nav>
    );
}

export default NavBar;