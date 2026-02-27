import { Box, Button, Stack } from '@mui/material';
import Logo from '../Logo/Logo';
import { useNavigate } from 'react-router-dom';

function NavBar() {
    const navigate = useNavigate();

    return (
        <nav style={{ borderBottom: '1px solid #eee', backgroundColor: '#fff' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', px: { xs: 2, md: 5 }, py: 1.5 }}>
                <Logo onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>CodeBin</Logo>
                
                <Stack direction="row" spacing={2}>
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
                            whiteSpace: 'nowrap' // Zapobiega łamaniu tekstu
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
                            whiteSpace: 'nowrap', // Zapobiega łamaniu tekstu
                            boxShadow: 'none',
                            '&:hover': { boxShadow: 'none' }
                        }}
                    >
                        Zarejestruj się
                    </Button>
                </Stack>
            </Box>
        </nav>
    );
}

export default NavBar;