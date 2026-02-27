import { Container, Typography, Box, Paper } from '@mui/material';
import Parameters from '../Parameters/Parameters';
import Results from '../Results/Results';

function Generator() {
    return (
        <Box component="main" sx={{ bgcolor: '#f8f9fa', minHeight: '100vh', py: 6 }}>
            {/* maxWidth={false} zdejmuje KAŻDY limit szerokości. Kontener zajmie 100% monitora */}
            <Container maxWidth={false} sx={{ px: { xs: 2, md: 6, xl: 10 } }}>
                
                <Box sx={{ mb: 5, borderLeft: '6px solid #219653', pl: 3 }}>
                    <Typography variant="h3" sx={{ fontWeight: 800, color: '#2d3436' }}>
                        Kreator Zadania
                    </Typography>
                    <Typography variant="body1" color="text.secondary" sx={{ fontSize: '1.1rem', mt: 1 }}>
                        Zdefiniuj parametry po lewej i oczekiwane wyniki po prawej stronie.
                    </Typography>
                </Box>

                {/* Niezawodny Flexbox - wymusza zajęcie 100% dostępnej szerokości ekranu */}
                <Box sx={{ 
                    display: 'flex', 
                    flexDirection: { xs: 'column', lg: 'row' }, 
                    gap: 5, // Odstęp między kafelkami
                    width: '100%' 
                }}>
                    
                    {/* LEWY KAFELEK - Parametry */}
                    <Paper elevation={0} sx={{ 
                        flex: 1, // Magiczna właściwość - wymusza równe 50% szerokości
                        p: { xs: 3, md: 5 }, 
                        borderRadius: 4, 
                        border: '1px solid #e0e0e0', // Dokładnie taki sam styl jak na stronie głównej
                        background: '#fff', 
                        display: 'flex',
                        flexDirection: 'column'
                    }}>
                        <Typography variant="h5" sx={{ mb: 4, fontWeight: 700, color: '#219653' }}>
                            1. Podstawowe Informacje
                        </Typography>
                        <Parameters />
                    </Paper>

                    {/* PRAWY KAFELEK - Wyniki */}
                    <Paper elevation={0} sx={{ 
                        flex: 1, // Wymusza równe 50% szerokości
                        p: { xs: 3, md: 5 }, 
                        borderRadius: 4, 
                        border: '1px solid #e0e0e0', // Dokładnie taki sam styl jak na stronie głównej
                        background: '#fff', 
                        display: 'flex',
                        flexDirection: 'column'
                    }}>
                        <Typography variant="h5" sx={{ mb: 4, fontWeight: 700, color: '#d32f2f' }}>
                            2. Kryteria Oceny i Testy
                        </Typography>
                        <Results />
                    </Paper>

                </Box>
            </Container>
        </Box>
    );
}

export default Generator;