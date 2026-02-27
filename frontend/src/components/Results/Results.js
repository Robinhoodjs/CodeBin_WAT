import { TextField, Box, Button, Divider, Stack } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

function Results() {
    return (
        <Stack spacing={4} sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            
            <TextField
                fullWidth
                multiline
                rows={6}
                label="Testy jednostkowe / Przypadki testowe"
                variant="outlined"
                placeholder="Wprowadź dane wejściowe i oczekiwane wyjście..."
                InputProps={{ sx: { borderRadius: 2 } }}
            />

            <Divider sx={{ color: 'text.secondary', fontWeight: 600, fontSize: '0.9rem' }}>
                LUB
            </Divider>

            <TextField
                fullWidth
                multiline
                rows={6}
                label="Wzorcowe rozwiązanie"
                variant="outlined"
                placeholder="Wklej kod źródłowy, do którego AI ma porównać rozwiązanie..."
                InputProps={{ sx: { borderRadius: 2 } }}
            />
            
            {/* mt: 'auto' automatycznie zepchnie przycisk na sam dół karty, jeśli jest wolne miejsce */}
            <Box sx={{ mt: 'auto', pt: 4, display: 'flex', justifyContent: 'flex-end' }}>
                <Button 
                    variant="contained" 
                    size="large"
                    startIcon={<SendIcon />}
                    sx={{ 
                        px: 4, 
                        py: 1.5, 
                        fontWeight: 700, 
                        textTransform: 'none',
                        fontSize: '1.1rem',
                        borderRadius: 2,
                        bgcolor: '#219653',
                        '&:hover': { bgcolor: '#1b7a43' },
                        boxShadow: 'none'
                    }}
                >
                    Generuj i publikuj zadanie
                </Button>
            </Box>

        </Stack>
    );
}

export default Results;