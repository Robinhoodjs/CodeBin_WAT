import { TextField, Typography, Slider, Box, Stack, Button, List, ListItem, ListItemText, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';
import { useState, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updateDescription, updateDifficulty, updateTitle } from '../../redux/parametersRedux';
import axios from 'axios';
import { getParameters } from '../../redux/parametersRedux';
import { updateResults } from '../../redux/resultsRedux';

function Parameters() {
    const dispatch = useDispatch();
    const parameters = useSelector(state => getParameters(state));

    const [files, setFiles] = useState([]);
    const attachedFileNames = files.map(file => file.name);
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        const selectedFiles = Array.from(e.target.files);
        setFiles(prev => [...prev, ...selectedFiles]);
    };

    const handleRemoveFile = (index) => {
        setFiles(prev => prev.filter((_, i) => i !== index));
    };

    const handleButtonClick = () => {
        if (fileInputRef.current) fileInputRef.current.click();
    };

    // Funkcja obsługująca wysyłanie danych do backendu - tworzy formData, dodaje parametry i pliki, a następnie wysyła POST request.
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const formData = new FormData();
            formData.append('title', parameters.title || '');
            formData.append('difficulty', parameters.difficulty || '1');
            formData.append('description', parameters.description || '');

            files.forEach((file) => {
                formData.append('files', file);
            });

            console.log('Wysyłane dane:', {
                title: parameters.title,
                difficulty: parameters.difficulty,
                description: parameters.description,
                files: attachedFileNames
            });

            let response = await axios.post("http://127.0.0.1:8000/api/kody/", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(response);
            dispatch(updateResults(response.data));
        } catch (error) {
            console.error(error);
        }
    };

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

            <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom color="text.secondary" sx={{ fontWeight: 600 }}>
                    Załącz pliki (np. testy, szablony kodu):
                </Typography>
                <Button variant="contained" onClick={handleButtonClick} sx={{ mb: 1 }}>
                    Wybierz pliki
                </Button>
                <input
                    type="file"
                    multiple
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    accept="*"
                    style={{ display: 'none' }}
                />
                <List>
                    {attachedFileNames.map((name, index) => (
                        <ListItem key={index} secondaryAction={
                            <IconButton edge="end" onClick={() => handleRemoveFile(index)}>
                                <DeleteIcon />
                            </IconButton>
                        }>
                            <ListItemText primary={name} />
                        </ListItem>
                    ))}
                </List>
            </Box>
            
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