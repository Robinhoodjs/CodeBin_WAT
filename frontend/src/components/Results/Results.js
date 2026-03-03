import { TextField, Box, Button, Divider, Stack } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { getParameters } from '../../redux/parametersRedux';
import { useState } from 'react';

function Results() {
    const parameters = useSelector(state => getParameters(state));

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/kody/", parameters);
            console.log(response);
        } catch (error) {
            console.error(error);
        }
    }

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
                    onClick={handleSubmit}
                >
                    Generuj i publikuj zadanie
                </Button>
            </Box>

        </Stack>
    );
}

export default Results;