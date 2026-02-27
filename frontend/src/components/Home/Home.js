import React from 'react';
import { Container, Typography, Grid, Card, CardContent, CardActionArea, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import CodeIcon from '@mui/icons-material/Code';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import AssessmentIcon from '@mui/icons-material/Assessment';

function Home() {
    const navigate = useNavigate();

    const sections = [
        {
            title: 'Rozwiąż Zadanie',
            desc: 'Przejdź do listy dostępnych wyzwań i prześlij swój kod do sprawdzenia.',
            path: '/zadania',
            icon: <CodeIcon sx={{ fontSize: 50, color: '#219653' }} />
        },
        {
            title: 'Moje Wyniki',
            desc: 'Sprawdź historię swoich zgłoszeń oraz oceny wystawione przez AI.',
            path: '/wyniki',
            icon: <AssessmentIcon sx={{ fontSize: 50, color: '#219653' }} />
        },
        {
            title: 'Panel Administratora',
            desc: 'Generowanie nowych zadań dla grup studenckich i zarządzanie parametrami.',
            path: '/generator', // Twój obecny Generator
            icon: <AdminPanelSettingsIcon sx={{ fontSize: 50, color: '#d32f2f' }} /> // Akcent czerwony dla admina
        }
    ];

    return (
        <Container maxWidth="lg" sx={{ mt: 8 }}>
            <Box sx={{ textAlign: 'center', mb: 10 }}>
                <Typography variant="h2" sx={{ fontWeight: 900, color: '#219653', letterSpacing: -1 }}>
                    CODEBIN WAT
                </Typography>
                <Typography variant="h6" sx={{ color: '#555', mt: 2, fontWeight: 300 }}>
                    Wojskowa Akademia Techniczna - System Automatycznej Oceny Kodu
                </Typography>
                <Box sx={{ width: '60px', height: '4px', bgcolor: '#d32f2f', mx: 'auto', mt: 3 }} />
            </Box>

            <Grid container spacing={4} justifyContent="center">
                {sections.map((item, index) => (
                    <Grid item xs={12} md={4} key={index}>
                        <Card elevation={0} sx={{ 
                            height: '100%', 
                            border: '1px solid #e0e0e0',
                            borderRadius: 4,
                            transition: 'all 0.3s ease',
                            '&:hover': { 
                                borderColor: '#219653',
                                boxShadow: '0 10px 30px rgba(33, 150, 83, 0.1)',
                                transform: 'translateY(-5px)'
                            }
                        }}>
                            <CardActionArea onClick={() => navigate(item.path)} sx={{ height: '100%', p: 3 }}>
                                <CardContent sx={{ textAlign: 'center' }}>
                                    <Box sx={{ mb: 3 }}>{item.icon}</Box>
                                    <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 2 }}>
                                        {item.title}
                                    </Typography>
                                    <Typography variant="body2" sx={{ color: '#777', lineHeight: 1.6 }}>
                                        {item.desc}
                                    </Typography>
                                </CardContent>
                            </CardActionArea>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Container>
    );
}

export default Home;