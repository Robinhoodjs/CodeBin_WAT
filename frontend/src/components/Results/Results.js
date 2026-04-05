import { TextField, Stack, Button, List, ListItem, ListItemText, Link, Typography, Box } from '@mui/material';
import { useSelector } from 'react-redux';
import { getResults } from '../../redux/resultsRedux';

function Results() {
    const results = useSelector(getResults);

    const handleDownload = (file) => {
        const getUrl = () => {
            if (typeof file.content !== 'string') return null;
            if (file.content.startsWith('data:')) {
                return file.content;
            }
            // Block w postaci tekstu - konwertujemy na Blob
            const blob = new Blob([file.content], { type: 'text/plain;charset=utf-8' });
            return URL.createObjectURL(blob);
        };

        const url = getUrl();
        if (!url) {
            console.error('Nieprawidłowa zawartość pliku do pobrania:', file);
            return;
        }

        const link = document.createElement('a');
        link.href = url;
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        if (!file.content.startsWith('data:')) {
            URL.revokeObjectURL(url);
        }
    };

    return (
        <Stack spacing={4} sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>

            <TextField
                name='title'
                fullWidth
                label="Tytuł"
                variant="outlined"
                value={results.title || ''}
                InputProps={{ sx: { borderRadius: 2 } }}
            />

            <TextField
                name='task'
                fullWidth
                label="Polecenie"
                multiline
                rows={12}
                variant="outlined"
                value={results.task || ''}
                InputProps={{ sx: { borderRadius: 2 } }}
            />

            <Box>
                <Typography variant="subtitle2" gutterBottom color="text.secondary" sx={{ fontWeight: 600 }}>
                    Pliki do pobrania:
                </Typography>

                <List>
                    {(results.files || []).map((file) => (
                        <ListItem key={file.content} disablePadding>
                            <ListItemText
                                primary={
                                    <Link
                                        component="button"
                                        variant="body2"
                                        onClick={() => handleDownload(file)}
                                        sx={{ textDecoration: 'underline', color: 'primary.main' }}
                                    >
                                        {file.name}
                                    </Link>
                                }
                            />
                        </ListItem>
                    ))}
                </List>
            </Box>

        </Stack>
    );
}

export default Results;