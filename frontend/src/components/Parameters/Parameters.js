import { TextField, Typography, Slider, Box, Stack } from '@mui/material';
import { useDispatch } from 'react-redux';
import { updateDescription, updateDifficulty, updateTitle } from '../../redux/parametersRedux';

function Parameters() {
    const dispatch = useDispatch();

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
            
        </Stack>
    );
}

export default Parameters;