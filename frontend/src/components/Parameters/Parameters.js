import { TextField, Typography, Slider, Box, Stack, Button } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { useDispatch } from 'react-redux';
import { updateDescription, updateDifficulty, updateTitle } from '../../redux/parametersRedux';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { getParameters } from '../../redux/parametersRedux';

function Parameters() {
    const dispatch = useDispatch();
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
        // Stack to idealny komponent do pionowego układania elementów w równych odstępach
        <Stack spacing={4} sx={{ flexGrow: 1 }}>
            
            <TextField 
                name='title'
                fullWidth 
                label="Nazwa zadania" 
                variant="outlined" 
                placeholder="np. Algorytm Dijkstry w C++"
                InputProps={{ sx: { borderRadius: 2 } }}
                onChange={e => dispatch(updateTitle(e.target.value))} // <- aktualizacja tytułu w magazynu (Redux)
            />
            
            <Box sx={{ px: 1 }}>
                <Typography variant="subtitle2" gutterBottom color="text.secondary" sx={{ fontWeight: 600 }}>
                    Poziom trudności zadania:
                </Typography>
                <Slider
                    name='difficulty'
                    defaultValue={1}
                    step={1}
                    marks={[
                        { value: 1, label: 'Łatwy' },
                        { value: 2, label: 'Średni' },
                        { value: 3, label: 'Trudny' },
                    ]}
                    min={1}
                    max={3}
                    sx={{ color: '#219653' }}
                    onChange={e => dispatch(updateDifficulty(e.target.value))} // <- aktualizacja stopnia trudności w magazynu (Redux)
                />
            </Box>

            {/* Zwiększona liczba wierszy (rows={14}), by pole zajęło odpowiednio dużo miejsca */}
            <TextField 
                name='description'
                fullWidth 
                label="Pełna treść wyzwania" 
                multiline 
                rows={14} 
                variant="outlined"
                placeholder="Tutaj wpisz treść zadania, którą zobaczy student..."
                InputProps={{ sx: { borderRadius: 2 } }}
                onChange={e => dispatch(updateDescription(e.target.value))} // <- aktualizacja opisu w magazynu (Redux)
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

export default Parameters;