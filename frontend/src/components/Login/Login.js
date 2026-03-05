import React, { useState } from 'react';
import { Container, Box, Typography, TextField, Button, Paper, Link } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Login.module.scss'; 

function Login() {
    const navigate = useNavigate();
    
    // stan formularza
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/logowanie/", formData);
            console.log(response);
        } catch (error) {
            console.error(error);
        }

        navigate('/generator'); 
    };

    return (
        <main className={styles.mainWrapper || ''}>
            <Box sx={{ bgcolor: '#f8f9fa', minHeight: '80vh', display: 'flex', alignItems: 'center', py: 8 }}>
                <Container maxWidth="sm">
                    <Paper elevation={2} sx={{ p: { xs: 4, md: 6 }, borderRadius: 4, textAlign: 'center', border: '1px solid #e0e0e0' }}>
                        
                        <Typography variant="h4" sx={{ fontWeight: 800, color: '#2d3436', mb: 1 }}>
                            Witaj ponownie
                        </Typography>
                        <Typography variant="body1" color="text.secondary" sx={{ mb: 5 }}>
                            Zaloguj się do systemu CodeBin WAT
                        </Typography>

                        <Box component="form" onSubmit={handleLogin} sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                            <TextField 
                                name="email"
                                label="Adres E-mail" 
                                type="email" 
                                variant="outlined" 
                                fullWidth 
                                required 
                                InputProps={{ sx: { borderRadius: 2 } }}
                                onChange={handleChange}
                            />
                            <TextField 
                                name="password"
                                label="Hasło" 
                                type="password" 
                                variant="outlined" 
                                fullWidth 
                                required 
                                InputProps={{ sx: { borderRadius: 2 } }}
                                onChange={handleChange}
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
                                Zaloguj się
                            </Button>
                        </Box>

                        <Typography variant="body2" sx={{ mt: 4, color: 'text.secondary' }}>
                            Nie masz jeszcze konta?{' '}
                            <Link 
                                component="button" 
                                variant="body2" 
                                onClick={() => navigate('/register')}
                                sx={{ color: '#219653', fontWeight: 'bold', textDecoration: 'none' }}
                            >
                                Zarejestruj się
                            </Link>
                        </Typography>
                        
                    </Paper>
                </Container>
            </Box>
        </main>
    );
}

export default Login;