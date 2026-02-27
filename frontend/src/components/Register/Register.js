import React from 'react';
import { Container, Box, Typography, TextField, Button, Paper, Link } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import styles from './Register.module.scss'; 

function Register() {
    const navigate = useNavigate();

    const handleRegister = (e) => {
        e.preventDefault();
        // TODO: Walidacja danych i wysłanie do backendu
        navigate('/login'); 
    };

    return (
        <main className={styles.mainWrapper}>
            <Box sx={{ bgcolor: '#f8f9fa', minHeight: '80vh', display: 'flex', alignItems: 'center', py: 8 }}>
                <Container maxWidth="sm">
                    <Paper elevation={2} sx={{ p: { xs: 4, md: 6 }, borderRadius: 4, textAlign: 'center', border: '1px solid #e0e0e0' }}>
                        
                        <Typography variant="h4" sx={{ fontWeight: 800, color: '#2d3436', mb: 1 }}>
                            Dołącz do nas
                        </Typography>
                        <Typography variant="body1" color="text.secondary" sx={{ mb: 5 }}>
                            Utwórz nowe konto studenta lub prowadzącego
                        </Typography>

                        <Box component="form" onSubmit={handleRegister} sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                            <TextField 
                                label="Imię i nazwisko" 
                                type="text" 
                                variant="outlined" 
                                fullWidth 
                                required 
                                InputProps={{ sx: { borderRadius: 2 } }}
                            />
                            <TextField 
                                label="Adres E-mail (domena WAT)" 
                                type="email" 
                                variant="outlined" 
                                fullWidth 
                                required 
                                InputProps={{ sx: { borderRadius: 2 } }}
                            />
                            <TextField 
                                label="Hasło" 
                                type="password" 
                                variant="outlined" 
                                fullWidth 
                                required 
                                InputProps={{ sx: { borderRadius: 2 } }}
                            />
                            <TextField 
                                label="Powtórz hasło" 
                                type="password" 
                                variant="outlined" 
                                fullWidth 
                                required 
                                InputProps={{ sx: { borderRadius: 2 } }}
                            />
                            
                            <Button 
                                type="submit" 
                                variant="contained" 
                                size="large" 
                                sx={{ 
                                    py: 1.5, 
                                    mt: 2, 
                                    bgcolor: '#219653', 
                                    fontWeight: 700,
                                    borderRadius: 2,
                                    textTransform: 'none',
                                    fontSize: '1.1rem',
                                    boxShadow: 'none',
                                    '&:hover': { bgcolor: '#1b7a43', boxShadow: 'none' }
                                }}
                            >
                                Załóż konto
                            </Button>
                        </Box>

                        <Typography variant="body2" sx={{ mt: 4, color: 'text.secondary' }}>
                            Masz już konto?{' '}
                            <Link 
                                component="button" 
                                variant="body2" 
                                onClick={() => navigate('/login')}
                                sx={{ color: '#219653', fontWeight: 'bold', textDecoration: 'none' }}
                            >
                                Zaloguj się
                            </Link>
                        </Typography>
                        
                    </Paper>
                </Container>
            </Box>
        </main>
    );
}

export default Register;