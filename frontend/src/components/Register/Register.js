import React, { useState } from 'react';
import { Container, Box, Typography, TextField, Button, Paper, Link, Chip, Alert, IconButton, InputAdornment } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Register.module.scss'; 

function Register() {
    const navigate = useNavigate();

    // stan formularza
    const [formData, setFormData] = useState({
        nick: '',
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        deansGroup: '',
        indexNumber: ''
    });

    const [error, setError] = useState('');
    
    // stany do pokazywania/ukrywania hasla
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    // sprawdzanie roli na podstawie maila
    const emailLower = formData.email.toLowerCase();
    const isStudent = emailLower.includes('@student');
    const isProfessor = emailLower.includes('@wat.edu.pl') && !isStudent;

    // biezace sprawdzanie hasla
    const isLengthValid = formData.password.length >= 8;
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(formData.password);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        
        // blokada wyslania jesli haslo jest za slabe
        if (!isLengthValid || !hasSpecialChar) {
            setError('Hasło nie spełnia wymagań bezpieczeństwa.');
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setError('Podane hasła nie są identyczne.');
            return;
        }

        setError(''); 
        
        let userRole = 'UNKNOWN';
        if (isStudent) {
            userRole = 'STUDENT';
        } else if (isProfessor) {
            userRole = 'PROFESSOR';
        }

        // Dane do wysłania (nie jest identyczne z formData!)
        const payload = {
            username: formData.nick,
            email: formData.email,
            password: formData.password,
            first_name: formData.firstName,
            last_name: formData.lastName,
            rola: userRole,
            grupa_dziekanska: formData.deansGroup,
            numer_indeksu: formData.indexNumber
        };

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/rejestracja/", payload);
            console.log(response);
        } catch (error) {
            console.error(error);
        }

        console.log('Dane rejestracji:', payload);
        navigate('/login'); 
    };

    return (
        <main className={styles.mainWrapper || ''}>
            <Box sx={{ bgcolor: '#f8f9fa', minHeight: '80vh', display: 'flex', alignItems: 'center', py: 8 }}>
                <Container maxWidth="sm">
                    <Paper elevation={2} sx={{ p: { xs: 4, md: 6 }, borderRadius: 4, textAlign: 'center', border: '1px solid #e0e0e0' }}>
                        
                        <Typography variant="h4" sx={{ fontWeight: 800, color: '#2d3436', mb: 1 }}>
                            Dołącz do nas
                        </Typography>
                        <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                            Utwórz nowe konto w systemie CodeBin
                        </Typography>

                        {error && (
                            <Alert severity="error" sx={{ mb: 3 }}>
                                {error}
                            </Alert>
                        )}

                        <Box component="form" onSubmit={handleRegister} sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
                            
                            <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1, minHeight: '32px' }}>
                                {isStudent && <Chip label="Wykryta rola: Student" color="primary" variant="outlined" />}
                                {isProfessor && <Chip label="Wykryta rola: Pracownik" color="secondary" variant="outlined" />}
                            </Box>

                            <Box sx={{ display: 'flex', gap: 2 }}>
                                <TextField name="firstName" label="Imię" value={formData.firstName} onChange={handleChange} fullWidth required />
                                <TextField name="lastName" label="Nazwisko" value={formData.lastName} onChange={handleChange} fullWidth required />
                            </Box>

                            <TextField name="nick" label="Nick" value={formData.nick} onChange={handleChange} fullWidth required />
                            
                            <TextField 
                                name="email" 
                                label="Adres E-mail (domena WAT)" 
                                type="email" 
                                value={formData.email} 
                                onChange={handleChange} 
                                fullWidth 
                                required 
                            />

                            {isStudent && (
                                <Box sx={{ display: 'flex', gap: 2, p: 2, bgcolor: '#f1f8e9', borderRadius: 2, border: '1px dashed #219653' }}>
                                    <TextField name="indexNumber" label="Numer indeksu" value={formData.indexNumber} onChange={handleChange} fullWidth required={isStudent} />
                                    <TextField name="deansGroup" label="Grupa dziekańska" value={formData.deansGroup} onChange={handleChange} fullWidth required={isStudent} />
                                </Box>
                            )}

                            
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5, textAlign: 'left' }}>
                                <TextField 
                                    name="password" 
                                    label="Hasło" 
                                    type={showPassword ? 'text' : 'password'} 
                                    value={formData.password} 
                                    onChange={handleChange} 
                                    fullWidth 
                                    required 
                                    InputProps={{
                                        endAdornment: (
                                            <InputAdornment position="end">
                                                <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                                                    {showPassword ? <VisibilityOff /> : <Visibility />}
                                                </IconButton>
                                            </InputAdornment>
                                        )
                                    }}
                                />
                                
                                {formData.password.length > 0 && (
                                    <Box sx={{ display: 'flex', flexDirection: 'column', px: 1, mt: 0.5 }}>
                                        <Typography variant="caption" sx={{ color: isLengthValid ? 'success.main' : 'error.main' }}>
                                            • Minimum 8 znaków
                                        </Typography>
                                        <Typography variant="caption" sx={{ color: hasSpecialChar ? 'success.main' : 'error.main' }}>
                                            • Przynajmniej jeden znak specjalny
                                        </Typography>
                                    </Box>
                                )}
                            </Box>

                            <TextField 
                                name="confirmPassword" 
                                label="Powtórz hasło" 
                                type={showConfirmPassword ? 'text' : 'password'} 
                                value={formData.confirmPassword} 
                                onChange={handleChange} 
                                fullWidth 
                                required 
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton onClick={() => setShowConfirmPassword(!showConfirmPassword)} edge="end">
                                                {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                                            </IconButton>
                                        </InputAdornment>
                                    )
                                }}
                            />
                            
                            <Button 
                                type="submit" 
                                variant="contained" 
                                size="large" 
                                sx={{ py: 1.5, mt: 1, bgcolor: '#219653', fontWeight: 700, borderRadius: 2, textTransform: 'none', fontSize: '1.1rem' }}
                            >
                                Załóż konto
                            </Button>
                        </Box>

                        <Typography variant="body2" sx={{ mt: 4, color: 'text.secondary' }}>
                            Masz już konto?{' '}
                            <Link component="button" variant="body2" onClick={() => navigate('/login')} sx={{ color: '#219653', fontWeight: 'bold', textDecoration: 'none' }}>
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